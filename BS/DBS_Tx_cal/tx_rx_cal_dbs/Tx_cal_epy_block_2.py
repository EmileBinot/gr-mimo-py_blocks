"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Max. Calculator',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.max_pwr = 0
        self.max_angl = 0
        
        self.message_port_register_in(pmt.intern("reset"))
        self.set_msg_handler(pmt.intern("reset"), self.handle_msg)
        self.message_port_register_out(pmt.intern("max_angle_out"))
        self.message_port_register_out(pmt.intern("max_pwr_out"))
    
    def handle_msg(self, msg):  
        self.max_pwr = 0 # reset

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] # pwr

        angles = input_items[0][1::2]
        pwr = input_items[0][::2]

        if np.max(pwr) > self.max_pwr :
            self.max_pwr = np.max(pwr)
            self.max_angl = angles[np.argmax(pwr)]
            # print(self.max_pwr)
            # print(self.max_angl)
            PMT_msg = pmt.cons(pmt.string_to_symbol("max_angle"), pmt.from_double(self.max_angl))
            self.message_port_pub(pmt.intern("max_angle_out"), PMT_msg)
            PMT_msg = pmt.cons(pmt.string_to_symbol("max_pwr"), pmt.from_double(self.max_pwr))
            self.message_port_pub(pmt.intern("max_pwr_out"), PMT_msg)

        return len(output_items[0])
