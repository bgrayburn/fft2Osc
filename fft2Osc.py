#!/usr/bin/env python

import argparse
import random
import time
import pyaudio
import numpy as np

from pythonosc import osc_message_builder
from pythonosc import udp_client

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=12345,
    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
              channels=CHANNELS,
              rate=RATE,
              input=True,
              input_device_index=1,
              frames_per_buffer=CHUNK)

while (True):
  data = stream.read(CHUNK) 
  fft = np.fft.fft(data)
  client.send_message("/fft", fft)
  time.sleep(1)

