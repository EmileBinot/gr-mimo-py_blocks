"""
Demodulation Block:
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - in_sig[0]: IQ complex vectors input sequence
OUTPUT:
    - out_sig[0]: 
"""

import numpy as np
from gnuradio import gr
import math
import matplotlib.pyplot as plt
# def modulate(SF, id, os_factor) :
#     M  = pow(2,SF)
#     n_fold = M * os_factor - id * os_factor
#     chirp = np.zeros(M*os_factor, dtype=np.complex64)
#     for n in range(0,M*os_factor):
#         if n < n_fold:
#             chirp[n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id/M-0.5)*n/os_factor))
#         else:
#             chirp[n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id/M-1.5)*n/os_factor))
#     return chirp

def modulate(SF, id, os_factor, sign) :
    M  = pow(2,SF)*os_factor
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = fact1*np.exp(2j*math.pi*(id/M)*ka)
    return chirp

class Demodulation(gr.sync_block):

    def __init__(self, SF = 9, B = 250000, os_factor = 1):
        gr.sync_block.__init__(
            self,
            name='LoRa Demodulation',
            in_sig=[(np.complex64,pow(2,SF)*os_factor)],
            out_sig=[np.uint32]
        )
        self.SF = SF
        self.B = B
        self.os_factor = os_factor

    def work(self, input_items, output_items):

        M = pow(2,self.SF)

        base_downchirp = modulate(self.SF, 0, self.os_factor, -1)
        freq_vect = np.arange(0,M*self.os_factor)                                    # !!!! WILL INTRODUCE PROBLEMS WHEN OS_FACTOR IS NOT 1 !!!!
        max_array = np.zeros(len(input_items[0]), dtype=np.float32)
        
        for i in range(len(input_items[0])):
            demod_signal = np.multiply(input_items[0][i], base_downchirp)   # multiply every symbol with the downchirp
            demod_signal_fft = np.fft.fft(demod_signal)                     # perform FFT on demodulated signal    
            idx = np.argmax(np.abs(demod_signal_fft))                       # find the frequency index of the maximum value
            output_items[0][i] = round(round(freq_vect[idx]))               # convert the frequency index to symbol index
            # debug
            max_array[i] = np.max(np.abs(demod_signal_fft[idx]))

            # vect = np.arange(0,M)
            # fig, axs = plt.subplots(2)
            # fig.suptitle('Vertically stacked subplots')
            # axs[0].specgram(input_items[0][i], NFFT=64, Fs=32, noverlap=8)
            # axs[1].plot(vect, np.abs(demod_signal_fft))
            # plt.show()   

            # print("[RX] Demod.  : max (should be 2**SF):", max_array[i])
            # if max_array[i] < 2**self.SF:
            # print("[RX] Demod.  :  max_array[i] < 2**self.SF :", max_array[i])

        # # debug
        # print("\n--- GENERAL WORK : DEMODULATION ---")
        print("[RX] Demod.  : mean max (should be 2**SF):", np.mean(max_array))
        print("[RX] Demod.  : nreceived symbols:", i)
        return len(output_items[0])
