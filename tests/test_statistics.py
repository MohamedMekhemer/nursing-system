from patient_statistics import calculate_statistics


def test_calculate_statistics():
    patients = [
        {"id": 1, "name": "Ahmed", "age": 25},
        {"id": 2, "name": "Ali", "age": 70},
        {"id": 3, "name": "Omar", "age": 15},
    ]

    assert calculate_statistics(patients) == {
        "total_patients": 3,
        "average_age": 36.7,
        "under_18": 1,
        "age_60_plus": 1,
        "waiting_patients": 3,
    }


def test_empty_patient_statistics():
    assert calculate_statistics([]) == {
        "total_patients": 0,
        "average_age": 0,
        "under_18": 0,
        "age_60_plus": 0,
        "waiting_patients": 0,
    }