import numpy as np
from matplotlib import pyplot as plt
import math

plt.rcParams['figure.dpi'] = 120

x = [[1]*50]  # data vector
M = 2           # Tx antennas

H = [[1+2j ,3+0.5j]]
F_zf = np.linalg.pinv(H)
x_zf = np.matmul(F_zf,x)
y_zf = np.matmul(H,x_zf)


angle_deg = 0
A = [np.exp(-1j*math.pi*math.sin(angle_deg*math.pi/180)*np.arange(1,M+1))]
F_dbs =  np.transpose(A) * 1/math.sqrt(M)

# print(F_dbs)
# plt.plot(F_dbs)

x_dbs = np.matmul(F_dbs,x)
y_dbs = np.matmul(H,x_dbs)


# fig, axs = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')
# axs[0].plot(np.arange(0, np.shape(x)[1]), np.transpose(x))
# axs[1].plot(np.arange(0, np.shape(y_zf)[1]), np.transpose(y_zf))
# axs[1].plot(np.arange(0, np.shape(y_dbs)[1]), np.transpose(y_dbs))
# plt.show()


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

# Wavelength, antenna spacing, feed coefficients.
lam = 1
d = lam / 2
w = np.array([1, 1])  # pointing to 0
w_dbs = np.exp(-1j*math.pi*math.cos(0*math.pi/180)*np.arange(1,3))
print(w_dbs)
print(w)

# Calculate gain and directive gain; plot on a polar chart.
# phi, g = gain(d, w)
# DdBi = get_directive_gain(g)

phi, g = gain(d, w_dbs)
DdBi_dbs = get_directive_gain(g)

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
# ax.plot(phi, DdBi)
ax.plot(phi, DdBi_dbs)
ax.set_rticks([-20, -15, -10, -5])
ax.set_rlabel_position(45)
plt.show()

