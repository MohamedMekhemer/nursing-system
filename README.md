# Clinic Operations Data Processor

A small, dependency-free Python data pipeline that validates clinic CSV records, cleans accepted rows, and exports JSON results with a processing report.

> **Portfolio project:** Built to demonstrate Python file I/O, CSV/JSON processing, regular expressions, data validation, object-oriented programming, command-line arguments, and automated testing. All included patient records are fictional.

## Features

- Reads UTF-8 CSV files and checks required columns.
- Cleans whitespace and validates each row independently.
- Uses a `Patient` data class to represent validated records.
- Validates phone numbers using a regular expression.
- Records rejected rows with their line numbers and validation reasons.
- Exports accepted records, rejected records, and summary counts as JSON.
- Supports custom input files and output directories.
- Uses only the Python standard library at runtime.

## Quick Start

Requires Python 3.10 or newer.

Clone the repository and enter its directory:

```bash
git clone https://github.com/MohamedMekhemer/nursing-system.git
cd nursing-system
```

Run the processor:

```bash
python processor.py
```

The default input file is `patients.csv`. Results are written beside the script:

- `patients_cleaned.json`
- `patients_rejected.json`
- `report.json`

Use a different CSV file and output directory:

```bash
python processor.py path/to/clinic.csv --output-dir output
```

View all command-line options:

```bash
python processor.py --help
```

## Input Format

The CSV header must include `name`, `age`, `phone`, and `room`. Header matching ignores capitalization and surrounding whitespace.

| Field | Rule |
|---|---|
| `name` | Required; repeated whitespace is collapsed |
| `age` | Whole number from 1 to 120 |
| `phone` | 7–20 digits; may include `+`, spaces, parentheses, or hyphens |
| `room` | Required; surrounding whitespace is removed |

Rows that fail validation are recorded in `patients_rejected.json`. Processing continues with the next row.

## Where OOP Is Used

`patient.py` defines the `Patient` data class. `processor.py` creates a validated object for each CSV row using `Patient.from_row(...)`. It then calls `patient.to_dict()` to prepare accepted records for JSON serialization.

Reusable validation rules are defined in `validation.py`.

## Run Tests

Install pytest as a development dependency:

```bash
python -m pip install pytest
```

Run the tests from the repository directory:

```bash
python -m pytest
```

The application itself has no third-party runtime dependencies.

## Project Structure

```text
nursing-system/
├── patient.py
├── processor.py
├── validation.py
├── patients.csv
└── tests/
```

These are the main files involved in the data-processing pipeline.

## Privacy

This is an educational data-processing project, not a clinical system. Use fictional data only. Do not commit real patient information to a public repository.

## License

MIT. See [LICENSE](LICENSE).