from enum import Enum


class PlanPeriod(Enum):
    """
    Enum to represent planing period for device.
    """

    WEEK = "Week"
    MONTH = "Month"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DeviceType(Enum):
    """
    Enum to represent type of energy device.
    """

    CONSUME = "consume"
    STORE = "store"
    PRODUCE = "produce"
