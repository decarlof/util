import matplotlib.pyplot as plt
import matplotlib.animation as manim
import numpy as np
import zmq
import math
import argparse
import sys

from local import flatbuffers
import TraceSerializer

builder = flatbuffers.Builder(0)
serializer = TraceSerializer.ImageSerializer(builder)


input_address = "tcp://164.54.113.96:5560"
recon_address = "tcp://*:9999"

plt.ion = True

ctx = zmq.Context()

sock = ctx.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, b"")
sock.connect(input_address)

recon_sock = ctx.socket(zmq.SUB)
recon_sock.setsockopt(zmq.SUBSCRIBE, b"")
recon_sock.bind(recon_address)

poller = zmq.Poller()
poller.register(sock, zmq.POLLIN)
poller.register(recon_sock, zmq.POLLIN)

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_title('Simple View')
plt.pause(.01)

im1 = im2 = None
cnt = 0
while True:
  socks = dict(poller.poll(timeout=50))
  if sock in socks and socks[sock] == zmq.POLLIN:
    print("got projection data")
    data = sock.recv()
    cnt += 1
    if cnt % 5 == 0:
      read_image = serializer.deserialize(serialized_image=data)
      my_image = read_image.TdataAsNumpy()
  
      my_image.dtype = np.uint16
      my_image = my_image.reshape((read_image.Dims().Y(), read_image.Dims().X()))
      if im1 is None:
          im1 = ax1.imshow(my_image, cmap='gray', vmin=2300, vmax=3800)
      else:
          im1.set_data(my_image)
      fig.canvas.draw_idle()
      plt.pause(0.01)
  if recon_sock in socks and socks[recon_sock] == zmq.POLLIN:
    print ("got recon data")
    image = recon_sock.recv_pyobj()
    print(image.shape)

    if im2 is None:
        im2 = ax2.imshow(image[0], cmap='gray')
    else:
        im2.set_data(image[0])
        #im2.set_clim(np.min(image[0]), np.max(image[0])*0.7)
        im2.set_clim(1e-4, 5e-4)#np.max(image[0])*0.7)
    fig.canvas.draw_idle()
    plt.pause(0.01)
  if not socks:
    plt.pause(.1)

