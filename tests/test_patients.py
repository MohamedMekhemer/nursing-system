import pytest

from patients import (
    add_patient,
    display_patient,
    display_patients,
    search_patient,
    serve_next_patient,
    update_patient,
)


def test_add_patient_creates_and_stores_patient(monkeypatch):
    monkeypatch.setattr("patients.random.randint", lambda start, end: 4821)
    patients = []

    patient = add_patient(patients, " Ahmed ", "25", "01012345678", "12")

    assert patient == {
        "id": 4821,
        "name": "Ahmed",
        "age": 25,
        "phone": "01012345678",
        "room": "12",
    }
    assert patients == [patient]


def test_invalid_patient_is_not_added():
    patients = []

    with pytest.raises(ValueError):
        add_patient(patients, "Ahmed", "150", "01012345678", "12")

    assert patients == []


def test_display_patients(capsys):
    patients = [{"id": 4821, "name": "Ahmed", "age": 25, "room": "12"}]

    display_patients(patients)

    assert capsys.readouterr().out == "ID: 4821 | Ahmed | Age: 25 | Room: 12\n"


def test_search_patient_by_name_or_id():
    patient = {"id": 4821, "name": "Ahmed", "age": 25, "phone": "0101", "room": "12"}
    patients = [patient]

    assert search_patient(patients, "ahmed") is patient
    assert search_patient(patients, "4821") is patient
    assert search_patient(patients, "Ali") is None


def test_serve_next_patient_removes_first_patient():
    patients = [
        {"id": 1, "name": "Ahmed"},
        {"id": 2, "name": "Ali"},
    ]

    assert serve_next_patient(patients) == {"id": 1, "name": "Ahmed"}
    assert patients == [{"id": 2, "name": "Ali"}]
    assert serve_next_patient([]) is None


def test_update_patient_validates_and_saves_field():
    patient = {"id": 4821, "name": "Ahmed", "age": 25, "phone": "0101", "room": "12"}
    patients = [patient]

    assert update_patient(patients, "4821", "age", "30") is patient
    assert patient["age"] == 30

    with pytest.raises(ValueError):
        update_patient(patients, 4821, "age", "150")

    assert patient["age"] == 30


def test_display_patient(capsys):
    display_patient(
        {"id": 4821, "name": "Ahmed", "age": 25, "phone": "0101", "room": "12"}
    )

    assert capsys.readouterr().out == (
        "Patient found:\nID: 4821\nName: Ahmed\nAge: 25\n"
        "Phone: 0101\nRoom: 12\n"
    )