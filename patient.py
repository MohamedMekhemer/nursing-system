"""Patient data model used by the clinic CSV processor."""

from dataclasses import asdict, dataclass

from validation import validate_age, validate_name, validate_phone, validate_room


@dataclass
class Patient:
    name: str
    age: int
    phone: str
    room: str

    def __post_init__(self):
        """Keep every Patient valid, including instances created directly."""
        self.name = validate_name(self.name)
        self.age = validate_age(self.age)
        self.phone = validate_phone(self.phone)
        self.room = validate_room(self.room)

    @classmethod
    def from_row(cls, row):
        """Build a validated Patient from a CSV-like dictionary."""
        return cls(row.get("name") or "", row.get("age") or "", row.get("phone") or "", row.get("room") or "")

    def to_dict(self):
        """Return a JSON-ready dictionary."""
        return asdict(self)
