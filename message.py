from dataclasses import dataclass

@dataclass
class Message:
    source: str
    payload: dict
