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

    def __init__(self, preamble_nitems = 4224, payload_nitems = 8192):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""

        self.payload_nitems = payload_nitems
        self.preamble_nitems = preamble_nitems
        self.frame_counter = 0
        gr.sync_block.__init__(
            self,
            name='LoRa Frame Constructor',   # will show up in GRC
            in_sig=[(np.complex64,self.preamble_nitems),(np.complex64,self.payload_nitems)],
            out_sig=[(np.complex64,self.preamble_nitems+self.payload_nitems)]
        )
        
    def work(self, input_items, output_items):
        if len(input_items[0][0]) == self.preamble_nitems and len(input_items[1][0]) == self.payload_nitems :
            output_items[0][:] = np.concatenate((input_items[0],input_items[1]),axis=1)
            # TAGS
            key = pmt.intern("tx_sob")
            value = pmt.from_bool(True)
            self.add_item_tag(0, # Write to output port 0
                    self.nitems_written(0), # Index of the tag in absolute terms
                    key, # Key of the tag
                    value # Value of the tag
            )
            # tx_time tag is optional : https://discuss-gnuradio.gnu.narkive.com/c2r83OZW/uhd-usrp-sink-stream-tagging
            # TAGS
            key = pmt.intern("packet_len")
            value = pmt.from_long(self.preamble_nitems+self.payload_nitems)
            self.add_item_tag(0, # Write to output port 0
                    self.nitems_written(0), # Index of the tag in absolute terms
                    key, # Key of the tag
                    value # Value of the tag
            )

            self.frame_counter += 1
            print("\n\n[TX] Constr. : Frame #%d sent" % (self.frame_counter))
            return len(output_items[0])
        else :
            return 0
        # out = np.concatenate((input_items[0][0],input_items[1][0]))
        # print(len(out))
        # output_items[0][:] = out
        
