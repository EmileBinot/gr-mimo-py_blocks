import numpy as np
from matplotlib import pyplot as plt
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
from math import *
import scipy.signal

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

ant0 =np.real(np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/DoA/rx0"), dtype=np.complex64))[-1000:]
ant1 =np.real(np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/DoA/rx1"), dtype=np.complex64))[-1000:]

d = 0.5 # Inter element spacing [lambda]
M = 2  # number of antenna elements in the antenna system (ULA)  

soi_matrix  = [ant0 ,ant1]
x = soi_matrix

Rxx = x * np.matrix.getH(np.asmatrix(x))/len(x)

angles = np.linspace(-pi,pi,100)

# EASY technique
Peasy = []
for theta in angles:
    Peasy.append(np.mean(np.abs(ant0 + ant1 * np.exp(-1j*theta))))

Peasy = NormalizeData(np.real(Peasy))
max_idx = np.argmax(Peasy)

# BARTLETT
Pbartlett = []
for teta in angles:
    # a = np.matrix(np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.sin(teta))).transpose()
    a = np.matrix([np.exp(np.arange(0,M,1)*1j*2*np.pi*d*teta)]).transpose()
    Pteta = ( a.getH() * Rxx * a )/( a.getH() * a ) 
    Pbartlett.append(Pteta)
Pbartlett = NormalizeData(np.real(np.array(Pbartlett)).flatten())

fig, axs = plt.subplots(2)
fig.suptitle(r'Real signal received on antennas')
axs[0].plot(ant0)
axs[0].plot(ant1)
axs[0].legend(['Rx @ ant. 0', 'Rx @ ant. 1'])
axs[1].plot(np.degrees(angles),Peasy)
axs[1].plot(np.degrees(angles),Pbartlett)
axs[1].legend([r'P$_{easy}$($\theta$)',r'P$_{Bartlett}$($\theta$)'])
plt.show()