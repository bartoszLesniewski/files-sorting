from enum import Enum


class MainMenuOptions(Enum):
    """Represents the user's possible choices in the menu."""
    RANDOM_RECORDS = 1
    KEYBOARD = 2
    FILE = 3
    EXIT = 4


class Mode(Enum):
    """Represents the available message display modes."""
    VERBOSE_RECORDS = 1
    VERBOSE_SUM = 2
    NON_VERBOSE = 3


class PrintStage(Enum):
    """Represents the available stages after which a message may be displayed."""
    BEFORE_SORTING = "before sorting"
    AFTER_SORTING = "after sorting"
    AFTER_PHASE = "after phase"
