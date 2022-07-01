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

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Channel estimator',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.SF = 9
        self.preamble_len = 6
        preamble_up = np.reshape(modulate_vect(self.SF, [0]*self.preamble_len, 1, 1), -1)      # generate preamble_len upchirps
        preamble_down = np.reshape(np.conjugate(modulate_vect(self.SF, [0]*3, 1, 1)), -1)      # generate 3 downchirps
        self.preamble = np.concatenate((preamble_up, preamble_down[0:int(2.25*pow(2,self.SF))])) # concatenate preamble_up and preamble_down[0:2.25*M]
        self.set_output_multiple(len(self.preamble))

    def work(self, input_items, output_items):

        in0 = input_items[0][:len(self.preamble)]

        h_est = in0.T*self.preamble# https://www.youtube.com/watch?v=XCe0xanaPFo
        print("[RX] Channel : h^est =",h_est[0])
        
        fig, axs = plt.subplots(4)
        axs[0].specgram(in0, NFFT=64, Fs=32, noverlap=8)
        axs[1].specgram(self.preamble, NFFT=64, Fs=32, noverlap=8)
        axs[2].plot(in0)
        axs[3].plot(self.preamble)
        # axs[4].plot(np.arange(0,len(h)),np.real(h),np.arange(0,len(h)), np.imag(h))
        # axs[4].set_ylim([-1,1])
        plt.show()

        
        output_items[0][:len(in0)] = in0
        return len(in0)
