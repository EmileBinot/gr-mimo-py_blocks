import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.dpi'] = 120
import math


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))



# tx = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/dumpIN"), dtype=np.complex64)
# rx = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/dumpOUT"), dtype=np.complex64)

# fig, axs = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')
# axs[0].plot(np.arange(0, len(tx)), tx)
# axs[1].plot(np.arange(0, len(rx)), rx)

# plt.show()


## ANGLE

data = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/DBS_USRP/beam_trace"), dtype=np.float32)
angles = data[1::2]
pwr = data[::2]

threshold_idx = np.where(angles > -180)[0][0]
print(threshold_idx)

angles = angles[threshold_idx:]
pwr = pwr[threshold_idx:]
scaled_pwr = NormalizeData(pwr)


fig, axs = plt.subplots()
fig.suptitle('Vertically stacked subplots')
# axs[0].plot(np.arange(0, len(angles)), angles)
axs.plot(angles[:-500], scaled_pwr[:-500])
plt.show()


angles = np.linspace(-180,180,len(scaled_pwr))
angles_rad = angles * math.pi / 180

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
ax.plot(angles_rad, scaled_pwr)
ax.set_rticks([0, 0.25, 0.5, 0.75])
ax.set_rlabel_position(45)
plt.show()


# angles_rad = angles * math.pi / 180
# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
# ax.plot(angles_rad, scaled_pwr)
# ax.set_rticks([0.25, 0.5, 0.75])  # Less radial ticks
# # ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
# ax.grid(True)
# ax.set_title("A line plot on a polar axis", va='bottom')
# plt.show()

