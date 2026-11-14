This Python microservice converts length, distance, weight, and temperatures between different units. It expects a JSON string to be sent via ZeroMQ. The JSON string should contain two keys: unit and value. The unit should be a string and value should be a number. For example:

{
  "unit": "lb",
  "value": 150
}

The microservice will then return a message via ZeroMQ with a JSON string containing a converted unit. The unit of conversion is assumed by the input unit. In the example above, "lb" would be converted to "kg", and the following will be sent back:

{
  "unit": "kg",
  "value": 68.02721088435374
}

The following units are supported:

* Celsius or C
* Fahrenheit or F
* Inch or In
* Foot or Ft
* Yard or Yd
* Mile or Mi
* Centimeter or Cm
* Meter or M
* Kilometer or Km
* Ounce or Oz
* Pound or Lb
* Gram or G
* Kilogram or Kg
* Miles per hour or Mph
* Kilometers per hour or Kph

## How to request data
Start the microservice with `python3 unit-conversion.py` (you need `pip install pyzmq` first). It listens on port 5000. Connect a ZeroMQ REQ socket to `tcp://localhost:5000` and send the JSON as a string.

Example call:
```python
import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5000")

request = {"unit": "lb", "value": 150}
socket.send_string(json.dumps(request))
```

## How to receive data
Call `recv()` on the same socket. The reply is a JSON string with the new unit and the converted value.

Example call:
```python
reply = json.loads(socket.recv().decode())
print(reply["unit"])   # kg
print(reply["value"])  # 68.02721088435374
```