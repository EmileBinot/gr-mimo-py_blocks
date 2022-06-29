"""
ZERO FORCING
"""

import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, H=[[1, 0]]):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='ZF precoder',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        self.H = H
        self.F = np.linalg.pinv(self.H) * (1/math.sqrt(2))
        print("ZF precoder : " ,self.F)

    def work(self, input_items, output_items):
        x = [np.transpose(input_items[0])]
        x_precoded = np.matmul(self.F, x)
        
        output_items[0][:] = x_precoded[0]
        output_items[1][:] = x_precoded[1]

        return len(output_items[0])
