"""Common utils for sensor devices."""


def validate_sensor_power(val):
    if not isinstance(val, bool):
        raise ValueError("Invalid sensor power value!")
