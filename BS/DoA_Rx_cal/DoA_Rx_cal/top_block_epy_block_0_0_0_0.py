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

    def __init__(self, num_samples_to_process = 10000, threshold = 0.01):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='PLLs phase shift detector',   # will show up in GRC
            in_sig=[np.complex64,np.complex64],
            out_sig=[np.complex64,np.complex64,np.float32]
        )
        self.message_port_register_out(pmt.intern("phase_diff"))
        self.num_samples_to_count = num_samples_to_process
        self.counter = 0
        self.set_output_multiple(self.num_samples_to_count)
        self.threshold = threshold

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        # print("call")
        output_items[0][:] = input_items[0] 
        output_items[1][:] = input_items[1]
        
        angles = np.arange(-np.pi,np.pi,np.pi/180)
        sum = []
        
        in0 = input_items[0][:100]
        in1 = input_items[1][:100]
        if np.mean(np.abs(in0)) > self.threshold :
            for theta in angles:
                sum.append(np.mean(np.abs(in0 + in1 * np.exp(-1j*theta))))
            
            max_idx = np.argmax(sum)

            PMT_msg = pmt.from_float(angles[max_idx])
            self.message_port_pub(pmt.intern("phase_diff"), PMT_msg)

            output_items[2][:] = np.degrees(angles[max_idx])
        return len(output_items[0])
