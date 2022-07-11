import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.dpi'] = 120

# p = np.fromfile(open("/home/ebinot/Documents/blocks/preamble"), dtype=np.complex64)
# s = np.fromfile(open("/home/ebinot/Documents/blocks/sync"), dtype=np.complex64)
# c = np.fromfile(open("/home/ebinot/Documents/blocks/correlation"), dtype=np.complex64)
# loraFrame = np.fromfile(open("/home/ebinot/Documents/gr-lora-py_blocks/lora_frame"), dtype=np.complex64)
# loratx = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/LoRa_ch_est_USRP/lora_tx"), dtype=np.complex64)
payload = np.fromfile(open("/home/ebinot84/Documents/gr-mimo-py_blocks/LoRa_ch_est_USRP/payload"), dtype=np.complex64)
preamble = np.fromfile(open("/home/ebinot84/Documents/gr-mimo-py_blocks/LoRa_ch_est_USRP/preamble"), dtype=np.complex64)
frame = np.fromfile(open("/home/ebinot84/Documents/gr-mimo-py_blocks/LoRa_ch_est_USRP/lora_rx_crop"), dtype=np.complex64)
pwr = np.fromfile(open("/home/ebinot84/Documents/gr-mimo-py_blocks/LoRa_ch_est_USRP/pwr"), dtype=np.complex64)
# lorarx_crop = np.fromfile(open("/home/ebinot/Documents/gr-mimo_blocks/LoRa_ch_est_USRP/lora_rx_crop"), dtype=np.complex64)
# lorarx_inter = np.fromfile(open("/home/ebinot/Documents/gr-lora-py_blocks/lora_rx_interpol"), dtype=np.complex64)
# SF=9
# M = pow(2,SF)
# B = 250000
# f_vect = np.arange(0,M-1)*(B/M)
# print(p.shape())
# plt.plot(payloadOUT)

fig, axs = plt.subplots(4)
fig.suptitle('Vertically stacked subplots')
# axs[0].plot(np.abs(lorarx))
# # # axs[1].plot(np.arange(0, len(d)), np.real(d), np.arange(0, len(d)), np.imag(d))

# axs[0].specgram(loratx, NFFT=64, Fs=32, noverlap=8)
axs[0].specgram(preamble, NFFT=64, Fs=32, noverlap=8)
axs[1].specgram(payload, NFFT=64, Fs=32, noverlap=8)
axs[2].specgram(frame, NFFT=64, Fs=32, noverlap=8)
axs[3].plot(pwr)
# axs[2].specgram(lorarx_crop, NFFT=64, Fs=32, noverlap=8)
# axs[2].specgram(lorarx_inter, NFFT=64, Fs=32, noverlap=8)
# axs[2].specgram(payloadOUT, NFFT=64, Fs=32, noverlap=8)
# plt.specgram(loraFrameBEF, NFFT=64, Fs=32, noverlap=8)

plt.show()