# Test program for the Unit Conversion microservice
#
# Sends one request through ZeroMQ and prints the reply.
#
# Start the microservice first, then run this
# in a 2nd terminal with: python3 test_program.py

import json
import zmq

context = zmq.Context()

# REQ socket: sends a request, then waits for the reply
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5000")

# ask the microservice to convert 150 pounds
request = {"unit": "lb", "value": 150}

request_text = json.dumps(request)
socket.send_string(request_text)
print(f"Sent request: {request_text}")

# wait for the reply and turn the JSON text back into a dictionary
reply = json.loads(socket.recv().decode())
print(f"Received reply: {reply}")

# close ZeroMQ before the program ends
context.destroy()