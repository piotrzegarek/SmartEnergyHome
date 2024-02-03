from enum import Enum


class PlanPeriod(Enum):
    """Enum to represent planing period for device."""

    WEEK = "Week"
    MONTH = "Month"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


class DeviceType(Enum):
    """Enum to represent type of energy device."""

    CONSUME = "consume"
    STORE = "store"
    PRODUCE = "produce"


class EnergyUnit(Enum):
    """Enum to represent units of energy consumption."""

    W = "W"
    KWH = "kWh"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
