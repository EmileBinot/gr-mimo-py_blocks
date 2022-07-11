"""
Hamming encoding block
Forward Error Correction encoding block.
Reference : "MIT EECS II : http://web.mit.edu/6.02/www/f2012/handouts/L05_slides.pdf"

INPUT:
    - in_sig[0]: binary input sequence (4 useful bits per byte)
OUTPUT:
    - out_sig[0]: binary output sequence (4+CR useful bits per byte)
"""

import numpy as np
from gnuradio import gr


class HammingTx(gr.sync_block):
    def __init__(self, CR = 4):
        gr.sync_block.__init__(
            self,
            name='LoRa Hamming Tx',
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.CR = CR

    def work(self, input_items, output_items):
        
        in0 = input_items[0]    # input buffer reference
        out = output_items[0]   # output buffer reference
    
        output_matrix = np.zeros((len(in0), 4+self.CR), dtype=np.uint8)
        input_matrix = np.zeros((len(in0), 4), dtype=np.uint8)

        # Hamming encoding (iterate over matrix lines and encode each)
        for i in range(len(in0)):
            bits_crop = [int(x) for x in bin(in0[i])[2:]]                       # convert to binary    
            input_matrix[i][:] = ([0]*(4-len(bits_crop)) + bits_crop)[-(4):]    # crop to 4 bits

            if self.CR == 1: # CR = 1, add one parity bit
                p0 = input_matrix[i][0] ^ input_matrix[i][1] ^ input_matrix[i][2] ^ input_matrix[i][3]
                output_matrix[i] = np.asarray([input_matrix[i][0], input_matrix[i][1], input_matrix[i][2], input_matrix[i][3], p0], dtype=np.uint8)

            if self.CR == 2: # CR = 2, add two parity bits
                p0 = input_matrix[i][0] ^ input_matrix[i][1] ^ input_matrix[i][2]
                p1 = input_matrix[i][1] ^ input_matrix[i][2] ^ input_matrix[i][3]
                output_matrix[i] = np.asarray([input_matrix[i][0], input_matrix[i][1], input_matrix[i][2], input_matrix[i][3], p1, p0], dtype=np.uint8)

            if self.CR == 3: # CR = 3, add three parity bits (Hamming(7,4))
                Q = np.array([[0,1,1,1], [1,1,0,1], [1,1,1,0], [1,0,1,1]], np.uint8) 
                Id = np.identity(4, dtype=np.uint8)
                G = np.concatenate((Id, Q),axis=1)  # generator matrix
                output_matrix[i] = (np.dot(input_matrix[i],G)%2)[0:4+self.CR]

            if self.CR == 4: # CR = 4, add four parity bits (Hamming(8,4))
                Q = np.array([[0,1,1,1], [1,1,0,1], [1,1,1,0], [1,0,1,1]], np.uint8)
                Id = np.identity(4, dtype=np.uint8)
                G = np.concatenate((Id, Q),axis=1)  # generator matrix
                output_matrix[i] = (np.dot(input_matrix[i],G)%2)

        # binary to decimal conversion
        out[:] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

        # #debug
        # print("\n--- GENERAL WORK : HAMMING_ENC ---")
        # print("in0 :")
        # print(in0)
        # print("input_matrix :")
        # print(input_matrix)
        # print("output_matrix :")
        # print(output_matrix)
        # print("out :")
        # print(out)
        # print("--- HAMMING_ENC END---")

        return len(output_items[0])
