"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
# Import writer class from csv module
from csv import writer


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Save Variables No Cal',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_in(pmt.intern("Rx_PLL_phase"))
        self.set_msg_handler(pmt.intern("Rx_PLL_phase"), self.handle_msgRx)

        self.message_port_register_in(pmt.intern("Tx_PLL_phase"))
        self.set_msg_handler(pmt.intern("Tx_PLL_phase"), self.handle_msgTx)

        self.message_port_register_in(pmt.intern("Max_angle"))
        self.set_msg_handler(pmt.intern("Max_angle"), self.handle_msgAng)

        self.message_port_register_in(pmt.intern("Max_pwr"))
        self.set_msg_handler(pmt.intern("Max_pwr"), self.handle_msgPwr)

        self.message_port_register_in(pmt.intern("Trigger"))
        self.set_msg_handler(pmt.intern("Trigger"), self.handle_msgTrig)

        self.rx_pll_phase = 0
        self.tx_pll_phase = 0
        self.max_angl = 0
        self.max_pwr = 0

    def handle_msgRx(self, msg) :
        self.rx_pll_phase = np.degrees(pmt.to_float(msg))
        # print("prod")

    def handle_msgTx(self, msg) :
        self.tx_pll_phase = np.degrees(pmt.to_float(msg))
        # print("oui")

    def handle_msgAng(self, msg) :
        # print("angl")
        self.max_angl = pmt.to_float(pmt.cdr(msg))

    def handle_msgPwr(self, msg) :
        # print("angl")
        self.max_pwr = pmt.to_float(pmt.cdr(msg))
        

    def handle_msgTrig(self, msg) :
        print("saving variables ...")
        List = [self.rx_pll_phase,self.tx_pll_phase,self.max_angl, self.max_pwr]
        with open('data_no_cal.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()

    def work(self, input_items, output_items):
        
        output_items[0][:] = input_items[0]
        return len(output_items[0])
