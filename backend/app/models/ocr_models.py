from enum import Enum


class OCRProfile(str, Enum):

    LIGHT = "light"

    STANDARD = "standard"

    AGGRESSIVE = "aggressive"