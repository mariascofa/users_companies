from enum import Enum


class Condition(str, Enum):
    LESS_THAN = "Less than"
    GREATER_THAN = "Greater than"
    LESS_OR_EQUAL = "Less than or equal to"
    GREATER_OR_EQUAL = "Greater than or equal to"
    EQUAL = "Is equal to"
    NOT_EQUAL = "Is not equal to"
