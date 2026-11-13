# Authors: Jarrett Clark & Katherine Pavlak
# Class: CS 361: Software Engineering 1
# Fle: Unit Conversion Microservice
# Date Created: 7 Nov 2026
# Date Last Modified: 12 Nov 2026

import zmq
import json

# Receive and send a JSON message with ZeroMQ. Assumes message received is valid JSON.
def start_unit_conversion_service():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5000")

    while True:
        json_received = socket.recv_string()
        data = json.loads(json_received)
        new_unit, new_value = convert_units(data["unit"], data["value"])
        new_json = {
            "unit": new_unit,
            "value": new_value
        }
        json_send = json.dumps(new_json)
        socket.send_string(json_send)

# Geturns the type of a unit when given a unit name. The unit name may be the full name or abbreviation.
def get_unit_type(unit: str) -> str:
    unit_types = {
        "temperature": ["celsius", "c", "fahrenheit", "f"],
        "distance": ["inch", "in", "foot", "ft", "yard", "yd", "mile", "mi",
                     "centimeter", "cm", "meter", "m", "kilometer", "km"],
        "weight": ["ounce", "oz", "pound", "lb", "gram", "g", "kilogram", "kg"],
        "speed": ["miles per hour", "mph", "kilometers per hour", "kph"]
    }

    for unit_type, unit_names in unit_types.items():
        for unit_name in unit_names:
            if unit_name == unit.lower():
                return unit_type

    return None

# Converts a value to a new unit. The new unit is automatically inferred by the source unit.
def convert_units(source_unit: str, source_value: float) -> tuple:
    unit_type = get_unit_type(source_unit)
    match unit_type:
        case "temperature":
            return convert_temperature(source_unit, source_value)
        case "distance":
            return convert_distance(source_unit, source_value)
        case "weight":
            return convert_weight(source_unit, source_value)
        case "speed":
            return convert_speed(source_unit, source_value)
        case _:
            return None, None


# Convert between C and F and vice versa.
def convert_temperature(source_unit: str, source_value: float) -> tuple:
    match source_unit.lower():
        case "f":
            new_unit = "c"
        case "fahrenheit":
            new_unit = "celsius"
        case "c":
            new_unit = "f"
        case "celsius":
            new_unit = "fahrenheit"
        case _:
            new_unit = None

    if new_unit in ("c", "celsius"):
        new_value = (source_value - 32) * (5/9)
    elif new_unit in ("f", "fahrenheit"):
        new_value = (source_value * (9/5)) + 32
    else:
        new_value = None

    return new_unit, new_value

# Convert between miles, meters, and kilometers.
def convert_distance(source_unit: str, source_value: float) -> tuple:
    return

# Convert between ounces, pounds, grams, and kilograms.
def convert_weight(source_unit: str, source_value: float) -> tuple:
    return

# Convert between miles per hour and kilometers per hours, and vice versa.
def convert_speed(source_unit: str, source_value: float) -> tuple:
    match source_unit.lower():
        case "miles per hour":
            new_unit = "kilometers per hour"
        case "mph":
            new_unit = "kph"
        case "kilometers per hour":
            new_unit = "miles per hour"
        case "kph":
            new_unit = "mph"
        case _:
            new_unit = None

    if new_unit in ("kilometers per hour", "kph"):
        new_value = source_value / 1.609
    elif new_unit in ("miles per hour", "mph"):
        new_value = source_value * 1.609
    else:
        new_value = None

    return new_unit, new_value

if __name__ == "__main__":
    start_unit_conversion_service()