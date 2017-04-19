import logging
import zmq
import sys

context = zmq.Context()
client = context.socket(zmq.REQ)
client.bind("tcp://0.0.0.0:5555")


message = ' '.join(sys.argv[1:])
client.send_string(message)
reply = client.recv_string()
logging.warning(reply)
sys.exit(0)
