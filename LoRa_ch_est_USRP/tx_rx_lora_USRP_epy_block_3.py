"""
Preamble Generation Block:
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - None
OUTPUT:
    - out_sig[0]: IQ complex vector, length = M * os_factor * (preamble_len + 2.25)
"""

import numpy as np
from gnuradio import gr
import math
import time
import pmt

def modulate_vect(SF, id, os_factor, sign) :
    M  = pow(2,SF)
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = np.zeros((len(id),M*os_factor), dtype=np.complex64)
    for i in range(len(id)) :
        chirp[i] = fact1*np.exp(2j*math.pi*(id[i]/M)*ka)
    return chirp

class PreambleGenerator(gr.sync_block):

    def __init__(self, SF = 9, preamble_len = 6):
        gr.sync_block.__init__(
            self,
            name='LoRa Preamble Generator',
            in_sig=None,
            out_sig=[(np.complex64,round(pow(2,SF)*(preamble_len+2.25)))]   # !!! will cause problem if os_factor > 1 !!! 
        )
        self.SF = SF
        self.preamble_len = preamble_len

    def work(self, input_items, output_items):
        # t = time.time()
        preamble_up = np.reshape(modulate_vect(self.SF, [0]*self.preamble_len, 1, 1), -1)      # generate preamble_len upchirps
        preamble_down = np.reshape(np.conjugate(modulate_vect(self.SF, [0]*3, 1, 1)), -1)      # generate 3 downchirps
        output_items[0][:] = np.concatenate((preamble_up, preamble_down[0:int(2.25*pow(2,self.SF))])) # concatenate preamble_up and preamble_down[0:2.25*M]
        # # TAGS
        # key = pmt.intern("tx_sob")
        # value = pmt.from_bool(True)
        # self.add_item_tag(0, # Write to output port 0
        #         self.nitems_written(0), # Index of the tag in absolute terms
        #         key, # Key of the tag
        #         value # Value of the tag
        # )
        return len(output_items[0])