"""
Phase Compensation block :
Apply phase shift to in1

INPUT:
    - in_sig[0]: IQ complex samples (carrier with phase phi0)
    - in_sig[1]: IQ complex samples (carrier with phase phi1)
    - in_sig[2]: phase shift to apply to in1
OUTPUT:
    - out_sig[0]: in_sig[0] (pass thru)
    - out_sig[1]: in_sig[1] * np.exp(-1j*self.phase_diff)
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Phase Compensation',
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        self.message_port_register_in(pmt.intern("phase_diff"))
        self.set_msg_handler(pmt.intern("phase_diff"), self.handle_msg)
        self.phase_diff = 0
        self.set_tag_propagation_policy(gr.TPP_ONE_TO_ONE)
    
    def handle_msg(self, msg):  
        self.phase_diff = pmt.to_float(msg)

    def work(self, input_items, output_items):
        output_items[0][:] = input_items[0]
        output_items[1][:] = input_items[1] * np.exp(-1j*self.phase_diff)
        return len(output_items[0])
