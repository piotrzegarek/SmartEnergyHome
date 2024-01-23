from enum import Enum


class PlanPeriod(Enum):
    """
    Enum to represent type of energy device.
    """

    WEEK = "Week"
    MONTH = "Month"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
