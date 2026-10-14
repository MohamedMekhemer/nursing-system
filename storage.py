import csv
import json
from pathlib import Path

from patients import add_patient

DATA_FILE = Path(__file__).with_name("patients.json")
CSV_FILE = Path(__file__).with_name("patients.csv")
EXPORT_FILE = Path(__file__).with_name("patients_export.csv")
CSV_FIELDS = ["name", "age", "phone", "room"]


def load_patients(file_path=DATA_FILE):
    file_path = Path(file_path)
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            patients = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Patient data file contains invalid JSON: {file_path}") from error

    if not isinstance(patients, list):
        raise ValueError("Patient data file must contain a JSON list.")
    return patients


def save_patients(patients, file_path=DATA_FILE):
    file_path = Path(file_path)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(patients, file, indent=2)


def import_patients_from_csv(patients, file_path=CSV_FILE):
    accepted = []
    rejected = []

    with Path(file_path).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing_fields = set(CSV_FIELDS) - set(reader.fieldnames or [])
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row in reader:
            name = (row.get("name") or "").strip()
            try:
                patient = add_patient(
                    patients,
                    name,
                    row.get("age") or "",
                    row.get("phone") or "",
                    row.get("room") or "",
                )
            except ValueError as error:
                rejected.append({"name": name or "Unknown", "reason": str(error)})
                continue

            accepted.append(patient)

    return accepted, rejected


def export_patients_to_csv(patients, file_path=EXPORT_FILE):
    with Path(file_path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(
            {
                "name": patient["name"],
                "age": patient["age"],
                "phone": patient["phone"],
                "room": patient["room"],
            }
            for patient in patients
        )

    return len(patients)