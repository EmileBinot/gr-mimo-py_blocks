"""
Tagged Stream Cropper:
Reference : https://dsp.stackexchange.com/questions/80751/gnu-radiotagged-stream-how-to-clip-the-stream-as-packet-length-tag-long

INPUTS:
    - in_sig[0]: IQ complex stream
OUTPUT:
    - out_sig[0]: IQ complex stream
"""

import numpy as np
from gnuradio import gr
import pmt

class my_basic_adder_block(gr.basic_block):
    def __init__(self,tag_name = 'packet_len'):
        gr.basic_block.__init__(self,
                                name="Tagged Stream Cropper",
                                in_sig  = [np.complex64],
                                out_sig = [np.complex64])

        self.previous_tag_n_remainder = 0
        self.tag_name                 = tag_name
        self.set_tag_propagation_policy(gr.TPP_DONT)

    def general_work(self, input_items, output_items):
        len_out = len(output_items[0])

        # DO PROCESSING
        out_produced = 0 # output produced 

        #-> Write the remaining data of the previous tag
        if self.previous_tag_n_remainder > 0: 
            if self.previous_tag_n_remainder < len_out: # if the length of the input items is sufficient to write the remainder of the previous tag items 
                output_items[0][:self.previous_tag_n_remainder] = input_items[0][:self.previous_tag_n_remainder] #write to output 
                out_produced                                   += self.previous_tag_n_remainder                  #inccrease the number of item produced
                self.previous_tag_n_remainder = 0                                                                #reset the counter 
                # the RETURN is at the end of the work()

            else: # self.previous_tag_n_remainder >= len_out
                output_items[0][:len_out]      = input_items[0][:len_out]
                self.previous_tag_n_remainder -= len_out
                self.consume(0, len_out)
                return len_out

        # READ TAGS AND PARSE THE RECEIVED STREAM
        tags = self.get_tags_in_window(0, out_produced, len_out)

        #if there exist tag
        if len(tags) > 0:
            #for each tag apply
            for tag in tags:
                tag_name   = pmt.to_python(tag.key)            # packet_tag
                tag_len    = int(pmt.to_python(tag.value))          # packet_len
                tag_pos    = tag.offset - self.nitems_read(0)  # packet_position_index
                if tag_name == self.tag_name:       #check if the tag name is appropriate
                    # print("[RX] Cropper : Payload Tag found at position {} with length {}".format(tag_pos,tag_len))
                    if tag_pos + tag_len < len_out: # if all the elements correspding to the "tag" are included in the input_items

                        # write the elements to the output
                        output_items[0][out_produced:(out_produced+tag_len)] = input_items[0][tag_pos:(tag_pos+tag_len)]

                        # add tag to the corresponding start point                     
                        self.add_item_tag(0,                                   # Write to output port 0
                                         self.nitems_written(0)+out_produced,  # Index of the tag in absolute terms
                                         tag.key,                              # Key of the tag
                                         tag.value                             # Value of the tag
                                         )
                        #increase the number of output element produced counter
                        out_produced += tag_len

                    else: #tag_pos+tag_len >= len_out:
                        n_item_to_wrt = len_out - tag_pos
                        output_items[0][out_produced:(out_produced + n_item_to_wrt)] = input_items[0][tag_pos:(tag_pos+n_item_to_wrt)]

                        self.add_item_tag(0,                                     # Write to output port 0
                                          self.nitems_written(0)+out_produced,   # Index of the tag in absolute terms
                                          tag.key,                               # Key of the tag
                                          tag.value                              # Value of the tag
                                          )

                        self.previous_tag_n_remainder = tag_len - n_item_to_wrt
                        out_produced                 += n_item_to_wrt
                        self.consume(0,len_out)
                        return out_produced

        #if there is no tag exits
        self.consume(0,len_out)

        #recall that the first "if" state is producing element!
        return out_produced

# """
# Preamble removal block
# Correlation method
# """

# import numpy as np
# from gnuradio import gr
# import pmt

# class Preamble_Remover(gr.basic_block):
#     def __init__(self, SF=9, preamble_len = 6):
#         gr.basic_block.__init__(self,
#             name="LoRa Preamble Remover",
#             in_sig=[(np.complex64)],
#             out_sig=[(np.complex64)])
#         self.SF = SF

#     def forecast(self, noutput_items, ninputs) :
#         ninput_items_required = [1]*ninputs #ninput_items_required[i] is the number of items that will be consumed on input port i
#         return ninput_items_required

#     def general_work(self, input_items, output_items):

#         #buffer references
#         in0 = input_items[0] #input signal

#         tags = self.get_tags_in_window(0, 0, len(input_items[0]))
#         for tag in tags:
#             key = pmt.to_python(tag.key) # convert from PMT to python string
#             value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
#             print('key:', key)
#             print('value:', value, type(value))
#             print('')
#             croppedInput = in0[int(value):]
#             output_items[0][0:len(in0)] = croppedInput[:len(output_items[0])]
#             self.consume(0, len(in0[:len(output_items[0])]))
#         return len(in0[:len(output_items[0])])