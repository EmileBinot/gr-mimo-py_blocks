"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import matplotlib.pyplot as plt
import math

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

    def __init__(self,preamble_len = 6, payload_nitems = 1, threshold = 10000, SF = 1):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='LoRa Correlation Sync Payload',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        
        self.preamble_len = preamble_len
        self.preamble_nitems = round(pow(2,SF)*(preamble_len+2.25))
        self.payload_nitems = payload_nitems
        self.threshold = threshold
        self.SF = SF

        self.state = 0 # 0 if searching for preamble, 1 if found
        self.items_written0_old = 0
        self.set_output_multiple(self.preamble_nitems + self.payload_nitems + 1000)
        # self.set_history(4224+1)

    def work(self, input_items, output_items):

        in0 = input_items[0]
        
        # Preamble creation
        preamble_up = np.reshape(modulate_vect(self.SF, [0]*2, 1, 1), -1)       # generate preamble_len upchirps
        preamble_down = np.reshape((modulate_vect(self.SF, [0]*3, 1, -1)), -1)[0:int(2.25*pow(2,self.SF))]       # generate 3 downchirps
        preamble = np.concatenate((preamble_up, preamble_down))     # concatenate preamble_up and preamble_down[0:2.25*M]
    
        corr = np.abs(np.correlate(in0, preamble_down))**2
        corr_max = np.max(corr[2800:3400])
        corr_max_idx = np.argmax(corr[2800:3400]) + 2800

        fig, axs = plt.subplots(5)
        axs[0].specgram(in0, NFFT=64, Fs=32, noverlap=8)
        axs[1].specgram(in0[corr_max_idx:], NFFT=64, Fs=32, noverlap=8)
        axs[2].specgram(in0[corr_max_idx+len(preamble_down):], NFFT=64, Fs=32, noverlap=8)
        axs[3].plot(corr)
        axs[4].plot(in0)
        axs[4].axvline(corr_max_idx, 0, 1, color = "red", label = "Corr peak idx")
        plt.show()   

        if corr_max > self.threshold :
            tag_index = self.nitems_written(0) + corr_max_idx + len(preamble_down)
            self.add_item_tag(0,tag_index,  pmt.intern("payload_begin"),  pmt.intern(str(self.payload_nitems)))


        output_items[0][:] = in0[:len(output_items[0])]
        return len(output_items[0])
