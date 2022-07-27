"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Phase Compensation',   # will show up in GRC
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        self.message_port_register_in(pmt.intern("phase_diff"))
        self.set_msg_handler(pmt.intern("phase_diff"), self.handle_msg)
        self.phase_diff = 0
        self.set_tag_propagation_policy(gr.TPP_ONE_TO_ONE)
    
    def handle_msg(self, msg):  
        self.phase_diff = pmt.to_float(msg)
        # print(self.phase_diff)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0]
        output_items[1][:] = input_items[1] * np.exp(-1j*self.phase_diff)
        return len(output_items[0])
