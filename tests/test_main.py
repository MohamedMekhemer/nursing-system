import main


def test_main_import_argument_imports_csv_and_saves_patients(
    tmp_path, monkeypatch, capsys
):
    csv_file = tmp_path / "patients.csv"
    csv_file.write_text(
        "name,age,phone,room\n"
        "Ahmed,25,01011111111,12\n"
        "Sara,150,01044444444,20\n",
        encoding="utf-8",
    )
    saved_patients = []
    monkeypatch.setattr(main, "load_patients", lambda: [])
    monkeypatch.setattr(
        main,
        "save_patients",
        lambda patients: saved_patients.extend(patient.copy() for patient in patients),
    )
    monkeypatch.setattr("patients.random.randint", lambda start, end: 4821)

    main.main(["import", str(csv_file)])

    output = capsys.readouterr().out
    assert "Accepted: Ahmed" in output
    assert "Rejected: Sara" in output
    assert "Reason: Age must be between 1 and 120." in output
    assert [patient["name"] for patient in saved_patients] == ["Ahmed"]


def test_main_searches_serves_and_saves_on_exit(monkeypatch, capsys):
    patients = [
        {"id": 4821, "name": "Ahmed", "age": 25, "phone": "0101", "room": "12"},
        {"id": 7312, "name": "Ali", "age": 40, "phone": "0102", "room": "8"},
    ]
    saved_snapshots = []
    inputs = iter(["3", "Ahmed", "4", "9"])
    monkeypatch.setattr(main, "load_patients", lambda: patients)
    monkeypatch.setattr(
        main,
        "save_patients",
        lambda current: saved_snapshots.append([patient.copy() for patient in current]),
    )
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    main.main([])

    output = capsys.readouterr().out
    assert "Patient found:" in output
    assert "Now serving: Ahmed" in output
    assert [patient["name"] for patient in patients] == ["Ali"]
    assert saved_snapshots[-1] == patients


def test_show_menu_lists_all_nine_options(capsys):
    main.show_menu()

    output = capsys.readouterr().out
    for option in range(1, 10):
        assert f"{option}. " in output