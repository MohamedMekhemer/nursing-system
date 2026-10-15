import re


PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9 ()-]{6,19}$")


def validate_name(name):
    if not isinstance(name, str):
        raise ValueError("Name must be text.")
    name = " ".join(name.split())
    if not name:
        raise ValueError("Name cannot be empty.")
    return name


def validate_age(age):
    try:
        if isinstance(age, bool):
            raise ValueError
        if isinstance(age, str) and not age.strip().isdigit():
            raise ValueError
        age = int(age)
    except (TypeError, ValueError) as error:
        raise ValueError("Age must be a whole number.") from error

    if not 1 <= age <= 120:
        raise ValueError("Age must be between 1 and 120.")
    return age


def validate_phone(phone):
    if not isinstance(phone, str):
        raise ValueError("Phone must be text.")
    phone = phone.strip()
    if not phone:
        raise ValueError("Phone cannot be empty.")
    if not PHONE_PATTERN.fullmatch(phone):
        raise ValueError("Phone must contain 7 to 20 digits and simple phone symbols.")
    return phone


def validate_room(room):
    if not isinstance(room, str):
        raise ValueError("Room must be text.")
    room = room.strip()
    if not room:
        raise ValueError("Room cannot be empty.")
    return room
