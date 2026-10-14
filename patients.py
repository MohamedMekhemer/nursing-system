import random

from validation import validate_age, validate_name, validate_phone, validate_room

FIELD_VALIDATORS = {
    "name": validate_name,
    "age": validate_age,
    "phone": validate_phone,
    "room": validate_room,
}


def add_patient(patients, name, age, phone, room):
    name = validate_name(name)
    age = validate_age(age)
    phone = validate_phone(phone)
    room = validate_room(room)

    existing_ids = {patient["id"] for patient in patients}
    patient_id = random.randint(1000, 9999)
    while patient_id in existing_ids:
        patient_id = random.randint(1000, 9999)

    patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "phone": phone,
        "room": room,
    }
    patients.append(patient)
    return patient


def display_patients(patients):
    if not patients:
        print("No patients found.")
        return

    for patient in patients:
        print(
            f"ID: {patient['id']} | {patient['name']} | "
            f"Age: {patient['age']} | Room: {patient['room']}"
        )


def search_patient(patients, query):
    query = str(query).strip()
    if not query:
        return None

    if query.isdigit():
        patient_id = int(query)
        return next(
            (patient for patient in patients if patient["id"] == patient_id),
            None,
        )

    normalized_name = query.casefold()
    return next(
        (patient for patient in patients if patient["name"].casefold() == normalized_name),
        None,
    )


def serve_next_patient(patients):
    if not patients:
        return None
    return patients.pop(0)


def update_patient(patients, patient_id, field, value):
    try:
        patient_id = int(patient_id)
    except (TypeError, ValueError):
        return None

    patient = next(
        (item for item in patients if item["id"] == patient_id),
        None,
    )
    if patient is None:
        return None

    validator = FIELD_VALIDATORS.get(field)
    if validator is None:
        raise ValueError("Unsupported patient field.")

    patient[field] = validator(value)
    return patient


def display_patient(patient):
    print("Patient found:")
    print(f"ID: {patient['id']}")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Phone: {patient['phone']}")
    print(f"Room: {patient['room']}")