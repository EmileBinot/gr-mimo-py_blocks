import numpy as np
from matplotlib import pyplot as plt
import os

dirname = os.path.dirname(__file__)

import math

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def gain(d, w):
    """Return the power as a function of azimuthal angle, phi."""
    phi = np.linspace(0, 2*np.pi, 1000)
    psi = 2*np.pi * d / lam * np.cos(phi)
    j = np.arange(len(w))
    A = np.sum(w[j] * np.exp(j * 1j * psi[:, None]), axis=1)
    g = np.abs(A)**2
    return phi, g

def get_directive_gain(g, minDdBi=-20):
    """Return the "directive gain" of the antenna array producing gain g."""
    DdBi = 10 * np.log10(g / np.max(g))
    return np.clip(DdBi, minDdBi, None)


data = np.fromfile(open((os.path.join(dirname,"data/data_26_07_2022/max_17"))), dtype=np.float32)[:]
angles = data[1::2]
pwr = data[::2]

scaled_pwr = pwr


fig, axs = plt.subplots(3)
# fig.suptitle('Vertically stacked subplots')
axs[0].plot(scaled_pwr)
axs[0].set_title("power(t)")
axs[1].plot(np.arange(0, len(angles)), angles)
axs[1].set_title("angles(t)")
axs[2].plot(angles,scaled_pwr)
axs[2].set_title("power(angles)")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
# angles = np.linspace(-180,180,len(scaled_pwr))
angles_rad = angles * math.pi / 180
# plt.title("MiSo 2x1, DBS precoder")
# ax = fig.add_subplot(projection='polar')
ax.plot(angles_rad, scaled_pwr)
# ax.set_rticks([0, 0.25, 0.5, 0.75])
# ax.set_rlabel_position(45)

# ax.legend(['Steering vector pointing to $\Theta$ = 0°', 'Measurements'])
plt.show()