
import numpy as np
from matplotlib import pyplot as plt
from numpy.fft import fft, ifft, fft2, ifft2, fftshift
from math import *
import time as tm

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

d = 0.5 # Inter element spacing [lambda]
M = 5  # number of antenna elements in the antenna system (ULA)
N = 500  # sample size used for the simulation          
theta = -20 # incident angle of the test signal [deg]
fig, axs = plt.subplots(2)
# for theta in np.arange(-90,90,5) :
# print("theta=",theta)

# Array response vectors of the test signal
a = np.matrix(np.exp(np.arange(0,M,1)*1j*2*np.pi*d*np.sin(np.deg2rad(theta))))

frequency = 45
time = np.linspace(0,0.1,N)
soi = 1 * np.sin(2 * np.pi * frequency * time)

soi_matrix  = np.outer( soi, a).T 
# print(np.shape(soi_matrix))
# Generate multichannel uncorrelated noise
noise = np.random.normal(0,np.sqrt(10**-5),(M,N))
# print(np.shape(noise))
# Create received signal array
x = soi_matrix[:,50:-50] + noise[:,50:-50]
# print(np.shape(x))
# x = soi_matrix

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

axs[0].cla()
axs[1].cla()
fig.suptitle(r'Signal received at angle $\theta$ = %i° (simulation)' %theta)
# axs[0].plot(np.arange(len(x[0])),np.real(x[0]),'b', np.arange(len(x[0])) ,np.imag(x[0]),'c')
# axs[0].plot(np.arange(len(x[1])),np.real(x[1]),'r', np.arange(len(x[1])) ,np.imag(x[1]),'m')
axs[0].plot(np.real(x[0]))
axs[0].plot(np.real(x[1]))
axs[0].legend(['Rx @ ant. 1', 'Rx @ ant. 2'], loc='upper right')
axs[1].plot(np.degrees(angles),Pcapon)
axs[1].plot(np.degrees(angles),Pbartlett)
axs[1].plot(np.degrees(angles),Pmusic)
axs[1].legend([r'P$_{Capon}$($\theta$)', r'P$_{Bartlett}$($\theta$)', r'P$_{MUSIC}$($\theta$)'], loc='upper right')
#     fig.canvas.draw()
#     plt.pause(0.0001)

plt.show()
