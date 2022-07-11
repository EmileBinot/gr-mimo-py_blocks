"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import math
import matplotlib.pyplot as plt

def modulate(SF, id, os_factor, sign) :
    M  = pow(2,SF)
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = fact1*np.exp(2j*math.pi*(id/M)*ka)
    return chirp

def gamma(k) :
    # print("gamma , ", k)
    if k >= 0 and k < 256 :
        return k
    if k >= 256 and k < 512 :
        return k - 512

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, SF = 9):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.symbcounter = 0
        self.SF = SF
        self.f_up = 5555555
        self.f_down = 1693653

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        self.symbcounter += 1 
        M = pow(2,self.SF)
        freq_vect = np.arange(0,M)
        base_downchirp = modulate(self.SF, 0, 1, -1)
        base_upchirp = modulate(self.SF, 0, 1, 1)

        if self.symbcounter == 1 :
            in0 = input_items[0][:512]
            demod_signal = np.multiply(in0, base_downchirp)   # multiply every symbol with the downchirp
            demod_signal_fft = np.fft.fft(demod_signal)                     # perform FFT on demodulated signal    
            idx = np.argmax(np.abs(demod_signal_fft))                       # find the frequency index of the maximum value
            self.f_up = round(round(freq_vect[idx]))               # convert the frequency index to symbol index
            print("f_up = ", self.f_up)

        if self.symbcounter == 2 :
            in0 = input_items[0][:512-(self.f_up)]
            # in0 =  input_items[0][:512]

        if self.symbcounter == 8 :
            in0 = input_items[0][:512]
            demod_signal = np.multiply(in0, base_upchirp)   # multiply every symbol with the downchirp
            demod_signal_fft = np.fft.fft(demod_signal)                     # perform FFT on demodulated signal    
            idx = np.argmax(np.abs(demod_signal_fft))                       # find the frequency index of the maximum value
            self.f_down = round(round(freq_vect[idx]))               # convert the frequency index to symbol index
            print("f_down = ", self.f_down)
            # print(gamma(65))
            CFO = 1/2*gamma(np.mod(self.f_up + self.f_down, 512))
            STO = np.mod(self.f_up - CFO, 512) 
            print("STO = ", STO)
            print("CFO = ", CFO)

            CFO_test =(self.f_down+self.f_up)/2
            STO_test =(self.f_down-self.f_up)/2+1
            print("STO_test = ", STO_test)
            print("CFO_test = ", CFO_test)

        if self.symbcounter > 2 and self.symbcounter < 8 :
            in0 = input_items[0][:512]
            # demod_signal = np.multiply(in0, base_downchirp)   # multiply every symbol with the downchirp
            # demod_signal_fft = np.fft.fft(demod_signal)                     # perform FFT on demodulated signal    
            # idx = np.argmax(np.abs(demod_signal_fft))                       # find the frequency index of the maximum value
            # f_up = round(round(freq_vect[idx]))               # convert the frequency index to symbol index
            # print("f_up = ", f_up )

        # # debug
        vect = np.arange(0,len(in0))
        print(self.symbcounter)
        print(len(in0))
        # plt.plot(vect, np.real(in0))
        plt.specgram(in0, NFFT=64, Fs=32, noverlap=8)
        plt.show()

        output_items[0][:len(in0)] = in0 
        return len(in0)
