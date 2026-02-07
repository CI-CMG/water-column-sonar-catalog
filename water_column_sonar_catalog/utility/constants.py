from enum import Enum, unique


@unique
class Instruments(Enum):
    EK60 = "EK60"
    EK80 = "EK80"


@unique
class Levels(Enum):
    LEVEL_0 = "raw"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2a"
    LEVEL_3 = "level_3"
