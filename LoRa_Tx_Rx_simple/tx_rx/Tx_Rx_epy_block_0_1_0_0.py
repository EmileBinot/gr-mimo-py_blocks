"""
Interleaving block
Scrambles bits together to fight error bursts.
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - in_sig[0]: SF bytes input sequence (4+CR useful bits per byte)
OUTPUT:
    - out_sig[0]: CR int32 output sequence
"""

import numpy as np
from gnuradio import gr
import time 

class Interleaver(gr.basic_block):
    def __init__(self, SF=9, CR=4):
        gr.basic_block.__init__(self,
            name="LoRa Interleaver",
            in_sig=[np.uint8],
            out_sig=[np.uint32])
        self.SF = SF
        self.CR = CR

    def forecast(self, noutput_items, ninputs) :
        #ninput_items_required[i] is the number of items that will be consumed on input port i
        ninput_items_required = [self.SF]*ninputs   # we need SF items to produce anything
        return ninput_items_required

    def general_work(self, input_items, output_items):
        if(len(input_items[0]) >= self.SF and len(output_items[0]) >= self.CR+4) :    # if we have enough items to process
            in0 = input_items[0][:self.SF]  # input buffer reference

            # formatting the input buffer
            input_matrix = np.zeros((self.SF, self.CR+4), dtype=np.uint8)
            for i in range(len(in0)):
                bits_crop = [int(x) for x in bin(in0[i])[2:]]                                       # convert to binary  
                input_matrix[i][:] = ([0]*(self.CR+4-len(bits_crop)) + bits_crop)[-(self.CR+4):]    # crop to 4+CR bits

            # interleaving
            output_matrix = np.zeros((self.CR+4, self.SF), dtype=np.uint8)
            for i in range(0,(self.CR+4)) :
                for j in range(0,(self.SF)) :
                    idi=self.SF-1-(j-i)%self.SF
                    idj=self.CR+4-1-i
                    output_matrix[i][j]=input_matrix[idi][idj]
            
            # # debug
            # print("\n--- GENERAL WORK : INTERLEAVER ---")
            # print("in0 :")
            # print(in0)
            # print("len(in0) (should be SF): ")
            # print(len(in0))
            # print("input_matrix (SF x CR+4):")
            # print(input_matrix)
            # print("output_matrix (CR+4 x SF):")
            # print(output_matrix)
            # print("output_items[0] = ")
            # print(output_items[0])


            # to uint32
            output_items[0][0:(self.CR+4)] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

            self.consume(0, self.SF)    # consume inputs (should be SF)
            return self.CR+4            # return produced outputs (should be CR+4)

        else :
            return 0



