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
            name='DBS precoder',   # will show up in GRC
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.angle = angle  # [-90 -> 90]

    def work(self, input_items, output_items):

        # self.F = np.transpose([np.exp(-1j*math.pi*math.sin(self.angle*math.pi/180)*np.arange(1,2+1))]) * (1/math.sqrt(2))
        # x = [np.transpose(input_items[0])]
        # x_precoded = np.matmul(self.F, x)
        # output_items[0][:] = x_precoded[0]
        # output_items[1][:] = x_precoded[1]
        F = np.exp(-1j*math.pi*math.sin((self.angle)*math.pi/180)*np.arange(0,2))
        output_items[0][:] = input_items[0] * F[0]
        # output_items[1][:] = input_items[1]*np.exp(-1j*self.angle*math.pi/180))
        output_items[1][:] = input_items[1]* F[1]
        return len(output_items[0])
