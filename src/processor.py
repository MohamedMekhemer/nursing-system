"""Read, validate, clean, and report on clinic records from a CSV file."""

import argparse
import csv
import json
from pathlib import Path

from patient import Patient

REQUIRED_FIELDS = {"name", "age", "phone", "room"}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DATA_DIR = PROJECT_ROOT / "sample_data"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"


def write_json(file_path, data):
    """Save Python data as readable UTF-8 JSON."""
    with Path(file_path).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def process_csv(input_path, output_path, rejected_path, report_path):
    """Write cleaned and rejected JSON files plus a small processing report."""
    accepted = []
    rejected = []

    with Path(input_path).open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fields = {field.strip().lower() for field in (reader.fieldnames or [])}
        if not REQUIRED_FIELDS.issubset(fields):
            missing = ", ".join(sorted(REQUIRED_FIELDS - fields))
            raise ValueError(f"CSV is missing required columns: {missing}")

        for line_number, row in enumerate(reader, start=2):
            normalized_row = {
                (key or "").strip().lower(): value for key, value in row.items()
            }
            try:
                # Create one Patient object from this CSV row. The class applies
                # the validation rules before the record is accepted.
                patient = Patient.from_row(normalized_row)
            except ValueError as error:
                rejected.append(
                    {"line": line_number, "row": normalized_row, "reason": str(error)}
                )
            else:
                # Convert the object to a plain dictionary for JSON output.
                accepted.append(patient.to_dict())

    report = {
        "input_file": Path(input_path).name,
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "total_rows": len(accepted) + len(rejected),
    }
    write_json(output_path, accepted)
    write_json(rejected_path, rejected)
    write_json(report_path, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate clinic rows from CSV and save cleaned JSON outputs."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=SAMPLE_DATA_DIR / "patients.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
    )

    args = parser.parse_args(argv)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        report = process_csv(
            args.input,
            args.output_dir / "patients_cleaned.json",
            args.output_dir / "patients_rejected.json",
            args.output_dir / "report.json",
        )
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"Could not process CSV: {error}")
        return 1

    print("Clinic CSV processing complete")
    print(f"Rows processed: {report['total_rows']}")
    print(f"Accepted: {report['accepted_count']}")
    print(f"Rejected: {report['rejected_count']}")
    print(f"Output folder: {args.output_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
