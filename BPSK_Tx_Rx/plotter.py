import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.dpi'] = 120

# p = np.fromfile(open("/home/ebinot/Documents/blocks/preamble"), dtype=np.complex64)
# s = np.fromfile(open("/home/ebinot/Documents/blocks/sync"), dtype=np.complex64)
# c = np.fromfile(open("/home/ebinot/Documents/blocks/correlation"), dtype=np.complex64)
# loraFrame = np.fromfile(open("/home/ebinot/Documents/gr-lora-py_blocks/lora_frame"), dtype=np.complex64)
pkt = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/BPSK_Tx_Rx/pkt"), dtype=np.complex64)
# payloadOUT = np.fromfile(open("/home/ebinot/Documents/gr-lora-py_blocks/payloadOUT"), dtype=np.complex64)

# SF=9
# M = pow(2,SF)
# B = 250000
# f_vect = np.arange(0,M-1)*(B/M)
# print(p.shape())
# plt.plot(payloadOUT)

fig, axs = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')
axs[0].plot(np.arange(0, len(pkt)), np.real(pkt))
# # # axs[1].plot(np.arange(0, len(d)), np.real(d), np.arange(0, len(d)), np.imag(d))

# axs[0].specgram(pkt, NFFT=64, Fs=32, noverlap=8)
# axs[1].specgram(payloadOUT, NFFT=64, Fs=32, noverlap=8)
# axs[2].specgram(payloadOUT, NFFT=64, Fs=32, noverlap=8)
# plt.specgram(loraFrameBEF, NFFT=64, Fs=32, noverlap=8)

plt.show()