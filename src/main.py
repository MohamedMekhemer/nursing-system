import csv
import sys

from patients import add_patient, display_patients
from patients import display_patient, search_patient, serve_next_patient, update_patient
from patient_statistics import calculate_statistics
from storage import (
    CSV_FILE,
    EXPORT_FILE,
    export_patients_to_csv,
    import_patients_from_csv,
    load_patients,
    save_patients,
)


def show_menu():
    print("=================================")
    print("   NURSING PATIENT SYSTEM")
    print("=================================")
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Search Patient")
    print("4. Serve Next Patient")
    print("5. Update Patient")
    print("6. Import Patients from CSV")
    print("7. Export Patients to CSV")
    print("8. Show Statistics")
    print("9. Exit")


def show_update_menu():
    print("1. Update name")
    print("2. Update age")
    print("3. Update phone")
    print("4. Update room")
    print("5. Back")


def handle_csv_import(patients, file_path):
    try:
        accepted, rejected = import_patients_from_csv(patients, file_path)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Could not import CSV: {error}")
        return

    for patient in accepted:
        print(f"Accepted: {patient['name']}")
    for patient in rejected:
        print(f"Rejected: {patient['name']}")
        print(f"Reason: {patient['reason']}")

    if accepted:
        save_patients(patients)


def handle_csv_export(patients, file_path):
    try:
        exported_count = export_patients_to_csv(patients, file_path)
    except OSError as error:
        print(f"Could not export CSV: {error}")
        return

    print(f"Exported {exported_count} patient(s) to {file_path}.")


def show_statistics(patients):
    stats = calculate_statistics(patients)
    print("========== STATISTICS ==========")
    print(f"Total patients: {stats['total_patients']}")
    print(f"Average age: {stats['average_age']}")
    print(f"Patients under 18: {stats['under_18']}")
    print(f"Patients 60+: {stats['age_60_plus']}")
    print(f"Waiting patients: {stats['waiting_patients']}")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    try:
        patients = load_patients()
    except (OSError, ValueError) as error:
        print(f"Could not load patient data: {error}")
        return

    if argv:
        if len(argv) == 2 and argv[0] == "import":
            handle_csv_import(patients, argv[1])
        else:
            print("Usage: python main.py [import <csv_file>]")
        return

    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            try:
                patient = add_patient(
                    patients,
                    input("Patient name: "),
                    input("Age: "),
                    input("Phone: "),
                    input("Room: "),
                )
            except ValueError as error:
                print(f"Invalid patient: {error}")
            else:
                save_patients(patients)
                print(f"Patient added. ID: {patient['id']}")
        elif choice == "2":
            display_patients(patients)
        elif choice == "3":
            patient = search_patient(patients, input("Search patient: "))
            if patient is None:
                print("Patient not found.")
            else:
                display_patient(patient)
        elif choice == "4":
            patient = serve_next_patient(patients)
            if patient is None:
                print("No patients waiting.")
            else:
                save_patients(patients)
                print(f"Now serving: {patient['name']}")
        elif choice == "5":
            patient_id = input("Enter patient ID: ").strip()
            if search_patient(patients, patient_id) is None:
                print("Patient not found.")
                continue

            while True:
                show_update_menu()
                update_choice = input("Choose: ").strip()
                fields = {"1": "name", "2": "age", "3": "phone", "4": "room"}
                if update_choice == "5":
                    break
                field = fields.get(update_choice)
                if field is None:
                    print("Invalid choice. Please choose 1 to 5.")
                    continue

                new_value = input(f"New {field}: ")
                try:
                    patient = update_patient(patients, patient_id, field, new_value)
                except ValueError as error:
                    print(f"Invalid {field}: {error}")
                else:
                    save_patients(patients)
                    print("Patient updated.")
        elif choice == "6":
            file_path = input(f"CSV file path (Enter for {CSV_FILE.name}): ").strip()
            handle_csv_import(patients, file_path or CSV_FILE)
        elif choice == "7":
            file_path = input(
                f"Export file path (Enter for {EXPORT_FILE.name}): "
            ).strip()
            handle_csv_export(patients, file_path or EXPORT_FILE)
        elif choice == "8":
            show_statistics(patients)
        elif choice == "9":
            print("Saving data...")
            save_patients(patients)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 9.")


if __name__ == "__main__":
    main()