""" pydantic2 재사용가능한 field_validator 모음 / validate_field로 사용 """
from pydantic import field_validator


def validate_field(field_name: str, fn: callable, conditionValue=None):
    return field_validator(field_name)(lambda v: fn(field_name, v, conditionValue))


def check_equal(field_name, value, conditionValue):
    if value != conditionValue:
        raise ValueError(f"{field_name} must be equal {conditionValue}")
    return value


def check_length(field_name, value, length: int):
    if value and len(value) != length:
        raise ValueError(f"{field_name} must be equal length {length}")
    return value


def check_max(field_name, value, max_value: int):
    if value and value > max_value:
        raise ValueError(f"{field_name} must be less than {max_value}")
    return value


def check_min(field_name, value, min_value: int):
    if value and value < min_value:
        raise ValueError(f"{field_name} must be more than {min_value}")
    return value


def check_max_length(field_name, value, max_length: int):
    if value and len(value) > max_length:
        raise ValueError(f"{field_name} must be less than {max_length} length")
    return value


def check_min_length(field_name, value, min_length: int):
    if value and len(value) < min_length:
        raise ValueError(f"{field_name} must be more than {min_length} length")
    return value
