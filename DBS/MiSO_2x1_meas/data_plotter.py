import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.dpi'] = 120
# plt.rcParams['text.usetex'] = True
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

lam = 1
d = lam / 2
w = np.array([1, 1])  # pointing to 0
w_dbs = np.exp(-1j*math.pi*math.cos(0*math.pi/180)*np.arange(1,3))
phi, g = gain(d, w_dbs)
DdBi_dbs = NormalizeData(g)
fig = plt.figure()
ax = fig.add_subplot(projection='polar')
# ax.plot(phi, DdBi)
ax.plot(phi, DdBi_dbs)
ax.set_rticks([-20, -15, -10, -5])
ax.set_rlabel_position(45)

data = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/DBS/MiSO_2x1_meas/tx/beam_trace_2806"), dtype=np.float32)[800:]
angles = data[1::2]
pwr = data[::2]

threshold_idx = np.where(angles > -180)[0][0]
print(threshold_idx)

angles = angles[threshold_idx:]
pwr = pwr[threshold_idx:]
scaled_pwr = NormalizeData(pwr)


# fig, axs = plt.subplots()
# fig.suptitle('Vertically stacked subplots')
# # axs[0].plot(np.arange(0, len(angles)), angles)
# axs.plot(angles[:-500], scaled_pwr[:-500])
# plt.show()


# angles = np.linspace(-180,180,len(scaled_pwr))
angles_rad = angles * math.pi / 180
plt.title("MiSo 2x1, DBS precoder")
ax = fig.add_subplot(projection='polar')
ax.plot(angles_rad, scaled_pwr)
ax.set_rticks([0, 0.25, 0.5, 0.75])
ax.set_rlabel_position(45)

ax.legend(['Steering vector pointing to $\Theta$ = 0°', 'Measurements'])
plt.show()