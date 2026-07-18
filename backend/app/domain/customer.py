from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Customer:
    """Represents the customer associated with an investigation case."""

    name: str
    phone_number: str
