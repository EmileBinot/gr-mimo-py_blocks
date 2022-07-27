"""
Phase shift estimator block :
Calculate phase shift between in_sig[0] and in_sig[1]

INPUT:
    - in_sig[0]: IQ complex samples (carrier with phase phi0)
    - in_sig[1]: IQ complex samples (carrier with phase phi1)
OUTPUT:
    - out_sig[0]: in_sig[0] (pass thru)
    - out_sig[1]: in_sig[1] (pass thru)
    - out_sig[2]: phase estimation (phi0-phi1) as float stream 
    - out_sig[3]: phase estimation (phi0-phi1) as message

"""

import numpy as np
from gnuradio import gr
import pmt

def phase_estimator(in0,in1, angles_vect) :
    sum = []
    for theta in angles_vect:
        sum.append(np.mean(np.abs(in0 + in1 * np.exp(-1j*theta))))
    max_idx = np.argmax(sum)
    return angles_vect[max_idx]


class blk(gr.sync_block):
    def __init__(self, num_samples_to_process = 10000, threshold = 0.01):
        gr.sync_block.__init__(
            self,
            name='Phase shift estimator',
            in_sig=[np.complex64,np.complex64],
            out_sig=[np.complex64,np.complex64,np.float32]
        )
        self.message_port_register_out(pmt.intern("phase_diff"))
        self.num_samples_to_count = num_samples_to_process
        self.counter = 0
        self.set_output_multiple(self.num_samples_to_count)
        self.threshold = threshold

    def work(self, input_items, output_items):
        output_items[0][:] = input_items[0] 
        output_items[1][:] = input_items[1]
        
        angles_vect = np.arange(-np.pi,np.pi,np.pi/180)
        
        in0 = input_items[0][:100]
        in1 = input_items[1][:100]
        if np.mean(np.abs(in0)) > self.threshold :

            phase_diff = phase_estimator(in0, in1, angles_vect)

            PMT_msg = pmt.from_float(phase_diff)
            self.message_port_pub(pmt.intern("phase_diff"), PMT_msg)

            output_items[2][:] = np.degrees(phase_diff)
        return len(output_items[0])
