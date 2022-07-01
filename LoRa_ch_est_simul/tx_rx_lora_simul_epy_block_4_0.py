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

import numpy as np
from gnuradio import gr
import math
import matplotlib.pyplot as plt


def modulate_vect(SF, id, os_factor, sign) :
    M  = pow(2,SF)
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = np.zeros((len(id),M*os_factor), dtype=np.complex64)
    for i in range(len(id)) :
        chirp[i] = fact1*np.exp(2j*math.pi*(id[i]/M)*ka)
    return chirp

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, SF = 9,preamble_nitems = 61):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Frequency Shift Detector',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.SF = SF
        self.preamble_nitems = preamble_nitems
        self.symbcounter = 0
        self.SF = SF
        self.f_up = 5555555
        self.f_down = 1693653
        self.set_output_multiple(preamble_nitems)

    def work(self, input_items, output_items):

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
            print("[RX] Freq.   : f_up = ", self.f_up)


        output_items[0][:len(input_items[0][:self.preamble_nitems])] = input_items[0][:self.preamble_nitems]
        return len(input_items[0][:self.preamble_nitems])
