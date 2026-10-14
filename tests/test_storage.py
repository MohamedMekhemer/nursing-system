import csv

import pytest

from storage import (
    export_patients_to_csv,
    import_patients_from_csv,
    load_patients,
    save_patients,
)


def test_save_and_load_patients(tmp_path):
    file_path = tmp_path / "patients.json"
    patients = [{"id": 4821, "name": "Ahmed", "age": 25}]

    save_patients(patients, file_path)

    assert load_patients(file_path) == patients


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_patients(tmp_path / "missing.json") == []


def test_load_invalid_json_raises_value_error(tmp_path):
    file_path = tmp_path / "patients.json"
    file_path.write_text("not json", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON"):
        load_patients(file_path)


def test_import_csv_accepts_valid_patients_and_rejects_invalid_ages(
    tmp_path, monkeypatch
):
    file_path = tmp_path / "patients.csv"
    file_path.write_text(
        "name,age,phone,room\n"
        "Ahmed,25,01011111111,12\n"
        "Sara,150,01044444444,20\n"
        "Ali,abc,01022222222,8\n",
        encoding="utf-8",
    )
    ids = iter([1001])
    monkeypatch.setattr("patients.random.randint", lambda start, end: next(ids))
    patients = []

    accepted, rejected = import_patients_from_csv(patients, file_path)

    assert [patient["name"] for patient in accepted] == ["Ahmed"]
    assert [item["name"] for item in rejected] == ["Sara", "Ali"]
    assert patients == accepted


def test_import_csv_requires_all_columns(tmp_path):
    file_path = tmp_path / "patients.csv"
    file_path.write_text("name,age\nAhmed,25\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required columns"):
        import_patients_from_csv([], file_path)


def test_export_csv_writes_header_and_patient_rows(tmp_path):
    file_path = tmp_path / "patients_export.csv"
    patients = [
        {
            "id": 1001,
            "name": "Ahmed",
            "age": 25,
            "phone": "01011111111",
            "room": "12",
        }
    ]

    assert export_patients_to_csv(patients, file_path) == 1

    with file_path.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows == [
        {
            "name": "Ahmed",
            "age": "25",
            "phone": "01011111111",
            "room": "12",
        }
    ]