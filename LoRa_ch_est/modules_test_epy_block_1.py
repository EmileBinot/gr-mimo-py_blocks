"""
Hamming decoding block
Forward Error Correction decoding block.
Reference : "MIT EECS II : http://web.mit.edu/6.02/www/f2012/handouts/L05_slides.pdf"

INPUT:
    - in_sig[0]: binary input sequence (4+CR useful bits per byte)
OUTPUT:
    - out_sig[0]: binary output sequence (4 useful bits per byte)
"""

import numpy as np
from gnuradio import gr
import pmt

class HammingRx(gr.sync_block):
    def __init__(self, CR = 2, payload_len = 16):
        gr.sync_block.__init__(
            self,
            name='LoRa Hamming Rx',
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.CR = CR
        self.payload_len = payload_len
        self.items_counter = 0 # debug
        self.success_counter = 0

    def decode(self, input_vect, CR_loc) : 

        output=input_vect
        success_state = 0 # 3 if 1 error detected, 2 if 2 errors detected, 1 if 1 error corrected,  0 if no error

        if CR_loc == 1: # CR = 1, no error correction
            
            syndrome = input_vect[0] ^ input_vect[1] ^ input_vect[2] ^ input_vect[3] ^ input_vect[4]
            success_state = 0 if syndrome == 0 else 3
            output = input_vect

        if CR_loc == 2: # CR = 2, no error correction
            
            syndrome = np.zeros((2,1), dtype=np.uint8)
            syndrome[0] = input_vect[0] ^ input_vect[1] ^ input_vect[2] ^ input_vect[5]
            syndrome[1] = input_vect[1] ^ input_vect[2] ^ input_vect[3] ^ input_vect[4]
            success_state = 0 if syndrome.all() == 0 else 3
            output = input_vect

        if CR_loc == 3: # CR = 3, 1 error correction is possible
            n = 4+CR_loc
            k = 4

            # compute syndrome of input_vect
            Q = np.array([[0,1,1], [1,1,0], [1,1,1], [1,0,1]], np.uint8)
            Id = np.identity(n-k, dtype=np.uint8)
            H = np.concatenate((Q.transpose(), Id),axis=1)
            syndrome = np.dot(input_vect[:], H.transpose())%2

            # compute syndromes lookup table
            tmp = np.zeros((1,n-k+4), dtype=np.uint8)
            tmp2 = np.identity(n-k+4, dtype=np.uint8)
            E = np.concatenate((tmp, tmp2),axis=0)
            S = np.dot(E,H.transpose())%2   
            for j in range(S.shape[0]):             # iterate through the syndromes lookup table
                if np.array_equal(S[j],syndrome):   # if found, correct the input_vect
                    output = input_vect ^ E[j][:]
                    success_state = 1               # 1 error corrected

        if CR_loc == 4: # CR = 4, 1 error correction is possible, 2 error detection is possible
            
            n = 4+CR_loc
            k = 4

            # compute syndrome of input_vect
            Q = np.array([[0,1,1,1], [1,1,0,1], [1,1,1,0], [1,0,1,1]], np.uint8)
            Id = np.identity(n-k, dtype=np.uint8)
            H = np.concatenate((Q.transpose(), Id),axis=1)
            syndrome = np.dot(input_vect[:], H.transpose())%2


            if np.array_equal(syndrome,np.array([0,0,0,0])):    # if no error, return input_vect
                output = input_vect

            else :
                # compute parity bit
                parity = input_vect[0] ^ input_vect[1] ^ input_vect[2] ^ input_vect[3] ^ input_vect[4] ^ input_vect[5] ^ input_vect[6] ^ input_vect[7]
                
                if parity : # 1 error correctable
                    output, success_state = self.decode(input_vect[:][0:7], 3) # correct the first 7 bits by sending them to the decoding function
        
                else :  # 2 errors detected
                    success_state = 2
                
        return output[:][0:4], success_state # return the first 4 bits (data bits) and success_state (integer)

    def work(self, input_items, output_items):

        in0 = input_items[0]    # input buffer reference
        out = output_items[0]   # output buffer reference
    
        output_matrix = np.zeros((len(in0), 4), dtype=np.uint8)
        input_matrix = np.zeros((len(in0), 4+self.CR), dtype=np.uint8)
        success_states = np.zeros((len(in0), 1), dtype=np.uint8)

        for i in range(len(in0)):
            bits_crop = [int(x) for x in bin(in0[i])[2:]]                                       # convert to binary
            input_matrix[i][:] = ([0]*(self.CR+4-len(bits_crop)) + bits_crop)[-(self.CR+4):]    # crop to 4+CR bits
            output_matrix[i][:], success_states[i] = self.decode(input_matrix[i][:],self.CR)    # send to decoding function
        
        arr,trash = np.histogram(success_states, bins = [-1, 0.5, 1.5, 2.5, 3.5])

        self.items_counter += len(in0)
        self.success_counter += arr[0]
        if self.items_counter >= self.payload_len:
            print("[RX] Hamming : symbols without errors = %d / %d" % (self.success_counter, self.payload_len))
            self.success_counter = 0
            self.items_counter = 0


        # convert output matrix to uint8
        out[:] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

        # display success states
        # print("Success states:")
        # print(success_states)
        # print("[RX] Hamming : n1_detected = %d, n2_detected = %d, n1_corrrected = %d, n0 = %d" % (arr[3], arr[2], arr[1], arr[0]))
        # print("[RX] Hamming : n0 = ", arr[0])
        # tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        # for tag in tags:
        #     key = pmt.to_python(tag.key) # convert from PMT to python string
        #     value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
        #     print('key:', key)
        #     print('value:', value, type(value))
        #     print('')
        # # debug
        # print("\n--- GENERAL WORK : HAMMING_DEC ---")
        # print("in0 :")
        # print(in0)
        # print("input_matrix :")
        # print(input_matrix)
        # print("output_matrix :")
        # print(output_matrix)
        # print("out :")
        # print(out)
        # print("--- HAMMING_DEC END---")

        return len(output_items[0])