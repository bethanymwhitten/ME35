sensor = {
    "type": "temperature",
    "value": 24.5
}

if "value" in sensor:
    print(sensor["value"])

if "unit" in sensor:
    print(sensor["unit"])
else:
    print("No unit was provided")