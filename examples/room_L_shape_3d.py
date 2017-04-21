'''
In this example, we construct an L-shape 3D room. We use the same floor as in
the 2D example and extrude a 3D room from the floor with a given height.  This
is a simple way to create 3D rooms that fits most situations.  Then, we place
one source and two microphones in the room and compute the room impulse
responses.

In this example, we also compare the speed of the C extension module to
that of the pure python code.
'''
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import time
import pyroomacoustics as pra

# Create the 2D L-shaped room from the floor polygon
pol = 4 * np.array([[0,0], [0,1], [2,1], [2,0.5], [1,0.5], [1,0]]).T
room = pra.Room.from_corners(pol, fs=16000, max_order=6, absorption=0.85)

# Create the 3D room by extruding the 2D by 3 meters
room.extrude(3.)

# Add a source somewhere in the room
room.add_source([1.5, 1.2, 0.5])

# Create a linear array beamformer with 4 microphones
# Place an array of two microphones
R = np.array([[3.,   2.2], 
              [2.25, 2.1], 
              [0.6,  0.55]])
room.add_microphone_array(pra.MicrophoneArray(R, room.fs))

then = time.time()
# a parameter controls the use of the c-extension
# for the computation of image sources
room.image_source_model(use_libroom=False)
t_pure_python = time.time() - then

room.plot_rir()
plt.title('Pure python')

then = time.time()
room.image_source_model(use_libroom=True)
t_c = time.time() - then

room.compute_rir()

room.plot_rir()
plt.title('libroom')

#show the room and the image sources
room.plot()

print("Time to compute in Python:", t_pure_python)
print("Time to compute in C:", t_c)
print("Speed-up:", t_pure_python/t_c, "x")

plt.show()