"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, SF=1):
        gr.sync_block.__init__(
            self,
            name='LoRa Gray Tx',
            in_sig=[np.int32],
            out_sig=[np.int32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.SF = SF

    def work(self, input_items, output_items):
        in0 = input_items[0][:len(output_items[0])]
        out = output_items[0]

        for i in range(len(out)):
            out[i] = in0[i] ^ (in0[i] >> 1)
        return len(output_items[0])
