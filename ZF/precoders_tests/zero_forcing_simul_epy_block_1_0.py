"""
DBS
"""

import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, angle=0.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='No precoder',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.F = np.transpose([np.ones((1,2))]) * (1/math.sqrt(2))
        print("no precoder : " ,self.F)

    def work(self, input_items, output_items):
        
        x = [np.transpose(input_items[0])]
        x_precoded = np.matmul(self.F, x)
        
        output_items[0][:] = x_precoded[0]
        output_items[1][:] = x_precoded[1]

        return len(output_items[0])
