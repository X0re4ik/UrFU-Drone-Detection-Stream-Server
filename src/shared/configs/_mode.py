from typing import Literal


def mode(status: bool) -> Literal["On", "Off"]:
    return "On" if status else "Off"
