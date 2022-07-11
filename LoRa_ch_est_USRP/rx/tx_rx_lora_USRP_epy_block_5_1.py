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

class Demodulation(gr.sync_block):

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='LoRa est pwr',
            in_sig=[(np.complex64,16*512)],
            out_sig=[np.complex64]
        )

    def work(self, input_items, output_items):
        
        for i in range(len(input_items[0])):
            
            Power = np.sum(np.power(np.abs(input_items[0][i]),2))/len(input_items[0][i])
            # print(Power)
            output_items[0][i] = Power               # convert the frequency index to symbol index

        return len(output_items[0])
