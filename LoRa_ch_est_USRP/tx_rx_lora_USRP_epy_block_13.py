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
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Estimation + Precoding',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        self.message_port_register_in(pmt.intern("h1_est"))
        self.message_port_register_in(pmt.intern("h2_est"))

        self.h1_est = []
        self.h2_est = []
        self.state = 'est_h1'
        self.set_msg_handler(pmt.intern("h1_est"), self.handle_msg_h1)
        self.set_msg_handler(pmt.intern("h2_est"), self.handle_msg_h2)

    def handle_msg_h1(self,msg) :
        print("message received h1")
        self.h1_est.append(pmt.to_complex(msg))
        self.state = 'est_h2'

    def handle_msg_h2(self,msg) :
        print("message received h2")
        self.h1_est.append(pmt.to_complex(msg))
        self.state = 'est_h1'
    

    def work(self, input_items, output_items):
        
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key) # convert from PMT to python string
            value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
            if key == 'tx_sob':
                pass
        
        if self.state == 'est_h1' :
            output_items[0][:] = input_items[0] * 1
            output_items[1][:] = input_items[0] * 0
            return len(output_items[0])

        if self.state == 'est_h2' :
            output_items[0][:] = input_items[0] * 0
            output_items[1][:] = input_items[0] * 1
            return len(output_items[0])
