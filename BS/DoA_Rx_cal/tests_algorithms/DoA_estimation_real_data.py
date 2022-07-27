import numpy as np
from matplotlib import pyplot as plt
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
from math import *
import scipy.signal

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def compute_shift(x, y):
    assert len(x) == len(y)
    c = abs(scipy.signal.correlate(x, y))**2
    # assert len(c) == len(x)
    zero_index = int(len(c) / 2)
    shift = zero_index - np.argmax(c)
    return shift


ant1 =np.real(np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/LoRa_Tx_Rx_MiSo/in_2ant/rx1"), dtype=np.complex64))[100:500]
ant2 =np.real(np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/LoRa_Tx_Rx_MiSo/in_2ant/rx2"), dtype=np.complex64))[100:500]
shift = compute_shift(ant1,ant2)
print(shift)

ant1 =np.real(np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/LoRa_Tx_Rx_MiSo/in_2ant/rx1"), dtype=np.complex64))[100-shift:500-shift]

d = 0.5 # Inter element spacing [lambda]
M = 2  # number of antenna elements in the antenna system (ULA)  

soi_matrix  = [ant1 ,ant2]
x = soi_matrix

Rxx = x * np.matrix.getH(np.asmatrix(x))/len(x)
iRxx = np.linalg.inv(Rxx)

angles = np.linspace(-pi/2,pi/2,100)

Pcapon = []
for teta in angles:
    a = np.matrix(np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.sin(teta))).transpose()
    w = np.dot(iRxx,a) / np.dot(np.dot(a.getH(),iRxx), a)
    Pteta = np.dot(np.dot(w.getH(),Rxx),w)
    Pcapon.append(Pteta)
Pcapon = NormalizeData(np.real(np.array(Pcapon)).flatten())

# BARTLETT
Pbartlett = []
for teta in angles:
    a = np.matrix(np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.sin(teta))).transpose()
    Pteta = ( a.getH() * Rxx * a )/( a.getH() * a ) 
    Pbartlett.append(Pteta)
Pbartlett = NormalizeData(np.real(np.array(Pbartlett)).flatten())

# MUSIC
D, E = np.linalg.eig(Rxx)
idx = D.argsort()[::-1]
lmbd = D[idx]# Vector of sorted eigenvalues
E = E[:, idx]# Sort eigenvectors accordingly
En = np.matrix(E[:, 1:len(E)])# Noise eigenvectors (ASSUMPTION: M IS KNOWN)

Pmusic = []
for teta in angles:
    a = np.matrix(np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.sin(teta))).transpose()
    Pteta = ( a.getH() * a )/( a.getH() * En * En.getH()* a ) 
    Pmusic.append(Pteta)
Pmusic = NormalizeData(np.real(np.array(Pmusic)).flatten())

fig, axs = plt.subplots(2)
fig.suptitle(r'Real signal received on antennas')
axs[0].plot(x[0])
axs[0].plot(x[1])
axs[0].legend(['Rx @ ant. 1', 'Rx @ ant. 2'])
axs[1].plot(np.degrees(angles),Pcapon)
axs[1].plot(np.degrees(angles),Pbartlett)
axs[1].plot(np.degrees(angles),Pmusic)
axs[1].legend([r'P$_{Bartlett}$($\theta$)', r'P$_{Capon}$($\theta$)', r'P$_{MUSIC}$($\theta$)'])
plt.show()