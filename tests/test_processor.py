import json

import pytest

from patient import Patient
from processor import process_csv


def test_patient_cleans_fields_and_serializes():
    patient = Patient.from_row(
        {"name": "  Lina   Hassan ", "age": "22", "phone": "+201234567890", "room": " A 1 "}
    )

    assert patient.to_dict() == {
        "name": "Lina Hassan",
        "age": 22,
        "phone": "+201234567890",
        "room": "A 1",
    }


def test_direct_patient_construction_also_validates():
    with pytest.raises(ValueError, match="Age must be between"):
        Patient("Lina", 150, "01012345678", "A1")


def test_processor_writes_accepted_rejected_and_report(tmp_path):
    source = tmp_path / "clinic.csv"
    source.write_text(
        "name,age,phone,room\nLina,22,01012345678,A1\nBad,abc,123,A2\n",
        encoding="utf-8",
    )
    accepted_path = tmp_path / "accepted.json"
    rejected_path = tmp_path / "rejected.json"
    report_path = tmp_path / "report.json"

    report = process_csv(source, accepted_path, rejected_path, report_path)

    assert report == {
        "input_file": "clinic.csv",
        "accepted_count": 1,
        "rejected_count": 1,
        "total_rows": 2,
    }
    assert json.loads(accepted_path.read_text(encoding="utf-8")) == [
        {"name": "Lina", "age": 22, "phone": "01012345678", "room": "A1"}
    ]
    rejected = json.loads(rejected_path.read_text(encoding="utf-8"))
    assert rejected[0]["line"] == 3
    assert rejected[0]["reason"] == "Age must be a whole number."
    assert json.loads(report_path.read_text(encoding="utf-8")) == report


def test_processor_rejects_missing_columns(tmp_path):
    source = tmp_path / "wrong.csv"
    source.write_text("name,age\nLina,22\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        process_csv(source, tmp_path / "ok.json", tmp_path / "bad.json", tmp_path / "report.json")
