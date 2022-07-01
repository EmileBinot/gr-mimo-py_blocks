#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.2.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import tx_rx_lora_USRP_epy_block_0 as epy_block_0  # embedded python block
import tx_rx_lora_USRP_epy_block_1 as epy_block_1  # embedded python block
import tx_rx_lora_USRP_epy_block_12 as epy_block_12  # embedded python block
import tx_rx_lora_USRP_epy_block_2 as epy_block_2  # embedded python block
import tx_rx_lora_USRP_epy_block_4_0 as epy_block_4_0  # embedded python block
import tx_rx_lora_USRP_epy_block_5 as epy_block_5  # embedded python block
import tx_rx_lora_USRP_epy_block_6_0 as epy_block_6_0  # embedded python block
import tx_rx_lora_USRP_epy_block_6_0_0 as epy_block_6_0_0  # embedded python block
import tx_rx_lora_USRP_epy_block_6_0_1 as epy_block_6_0_1  # embedded python block
import tx_rx_lora_USRP_epy_block_8_0 as epy_block_8_0  # embedded python block
import tx_rx_lora_USRP_epy_block_9 as epy_block_9  # embedded python block
import tx_rx_lora_USRP_epy_block_9_0 as epy_block_9_0  # embedded python block
import tx_rx_lora_USRP_epy_block_9_0_0 as epy_block_9_0_0  # embedded python block




class tx_rx_lora_USRP(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.payload_len = payload_len = 18
        self.SF = SF = 9
        self.CR = CR = 4
        self.preamble_len = preamble_len = 6
        self.payload_nsymb = payload_nsymb = int((payload_len/SF)*(CR+4))
        self.bandwidth = bandwidth = int(125e3)
        self.threshold = threshold = 0.1
        self.samp_rate = samp_rate = bandwidth
        self.preamble_nitems = preamble_nitems = round(pow(2,SF)*(preamble_len+2.25))
        self.payload_nitems = payload_nitems = int(payload_nsymb*pow(2,SF))
        self.os_factor = os_factor = 1
        self.corr_threshold = corr_threshold = int(8e3)
        self.const_multiply = const_multiply = 1
        self.center_freq = center_freq = int(868e6)

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(("addr=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_1.set_clock_source('mimo', 0)
        self.uhd_usrp_source_1.set_time_source('mimo', 0)
        self.uhd_usrp_source_1.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_1.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_1.set_antenna("RX2", 0)
        self.uhd_usrp_source_1.set_gain(10, 0)
        self.uhd_usrp_source_1.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_1.set_auto_iq_balance(True, 0)
        self.epy_block_9_0_0 = epy_block_9_0_0.blk(preamble_len=preamble_len, payload_nitems=payload_nitems, threshold=corr_threshold, SF=9)
        self.epy_block_9_0 = epy_block_9_0.blk(preamble_len=preamble_len, payload_nitems=payload_nitems, threshold=corr_threshold, SF=9)
        self.epy_block_9 = epy_block_9.blk(preamble_nitems=preamble_nitems*os_factor, payload_nitems=payload_nitems*os_factor, threshold=threshold)
        self.epy_block_8_0 = epy_block_8_0.blk(SF=9)
        self.epy_block_6_0_1 = epy_block_6_0_1.my_basic_adder_block(tag_name="preamble_begin")
        self.epy_block_6_0_0 = epy_block_6_0_0.my_basic_adder_block(tag_name="threshold_exceeded")
        self.epy_block_6_0 = epy_block_6_0.my_basic_adder_block(tag_name="payload_begin")
        self.epy_block_5 = epy_block_5.Demodulation(SF=SF, B=250000, os_factor=os_factor)
        self.epy_block_4_0 = epy_block_4_0.blk(SF=9, preamble_nitems=61)
        self.epy_block_2 = epy_block_2.LoraDewhitening(reset_key="payload_begin")
        self.epy_block_12 = epy_block_12.blk()
        self.epy_block_1 = epy_block_1.HammingRx(CR=CR, payload_len=payload_len)
        self.epy_block_0 = epy_block_0.Deinterleaver(SF=SF, CR=CR)
        self.blocks_tagged_stream_align_1_1 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "preamble_begin")
        self.blocks_tagged_stream_align_1_0 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "threshold_exceeded")
        self.blocks_tagged_stream_align_1 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "payload_begin")
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, pow(2,SF)*os_factor)
        self.blocks_null_sink_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_file_sink_0_3_0_0_0_0_0 = blocks.file_sink(gr.sizeof_int*1, 'dumpOUTsymb', False)
        self.blocks_file_sink_0_3_0_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_3_0_0_0_0 = blocks.file_sink(gr.sizeof_char*1, 'dumpOUT', False)
        self.blocks_file_sink_0_3_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_1_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'lora_rx_crop', False)
        self.blocks_file_sink_0_1_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'lora_rx', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_5, 0))
        self.connect((self.blocks_tagged_stream_align_1, 0), (self.epy_block_6_0, 0))
        self.connect((self.blocks_tagged_stream_align_1_0, 0), (self.epy_block_6_0_0, 0))
        self.connect((self.blocks_tagged_stream_align_1_1, 0), (self.epy_block_6_0_1, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))
        self.connect((self.epy_block_12, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_file_sink_0_3_0_0_0_0, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_4_0, 0), (self.blocks_null_sink_2, 0))
        self.connect((self.epy_block_5, 0), (self.epy_block_8_0, 0))
        self.connect((self.epy_block_6_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_6_0_0, 0), (self.blocks_file_sink_0_1_0_0, 0))
        self.connect((self.epy_block_6_0_0, 0), (self.epy_block_9_0, 0))
        self.connect((self.epy_block_6_0_0, 0), (self.epy_block_9_0_0, 0))
        self.connect((self.epy_block_6_0_1, 0), (self.epy_block_12, 0))
        self.connect((self.epy_block_6_0_1, 0), (self.epy_block_4_0, 0))
        self.connect((self.epy_block_8_0, 0), (self.blocks_file_sink_0_3_0_0_0_0_0, 0))
        self.connect((self.epy_block_8_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_9, 0), (self.blocks_tagged_stream_align_1_0, 0))
        self.connect((self.epy_block_9_0, 0), (self.blocks_tagged_stream_align_1, 0))
        self.connect((self.epy_block_9_0_0, 0), (self.blocks_tagged_stream_align_1_1, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.epy_block_9, 0))


    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.epy_block_1.payload_len = self.payload_len

    def get_SF(self):
        return self.SF

    def set_SF(self, SF):
        self.SF = SF
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_0.SF = self.SF
        self.epy_block_5.SF = self.SF

    def get_CR(self):
        return self.CR

    def set_CR(self, CR):
        self.CR = CR
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.epy_block_0.CR = self.CR
        self.epy_block_1.CR = self.CR

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_9_0.preamble_len = self.preamble_len
        self.epy_block_9_0_0.preamble_len = self.preamble_len

    def get_payload_nsymb(self):
        return self.payload_nsymb

    def set_payload_nsymb(self, payload_nsymb):
        self.payload_nsymb = payload_nsymb
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_samp_rate(self.bandwidth)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.epy_block_9.threshold = self.threshold

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate)

    def get_preamble_nitems(self):
        return self.preamble_nitems

    def set_preamble_nitems(self, preamble_nitems):
        self.preamble_nitems = preamble_nitems
        self.epy_block_9.preamble_nitems = self.preamble_nitems*self.os_factor

    def get_payload_nitems(self):
        return self.payload_nitems

    def set_payload_nitems(self, payload_nitems):
        self.payload_nitems = payload_nitems
        self.epy_block_9.payload_nitems = self.payload_nitems*self.os_factor
        self.epy_block_9_0.payload_nitems = self.payload_nitems
        self.epy_block_9_0_0.payload_nitems = self.payload_nitems

    def get_os_factor(self):
        return self.os_factor

    def set_os_factor(self, os_factor):
        self.os_factor = os_factor
        self.epy_block_5.os_factor = self.os_factor
        self.epy_block_9.payload_nitems = self.payload_nitems*self.os_factor
        self.epy_block_9.preamble_nitems = self.preamble_nitems*self.os_factor

    def get_corr_threshold(self):
        return self.corr_threshold

    def set_corr_threshold(self, corr_threshold):
        self.corr_threshold = corr_threshold
        self.epy_block_9_0.threshold = self.corr_threshold
        self.epy_block_9_0_0.threshold = self.corr_threshold

    def get_const_multiply(self):
        return self.const_multiply

    def set_const_multiply(self, const_multiply):
        self.const_multiply = const_multiply

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_source_1.set_center_freq(self.center_freq, 0)




def main(top_block_cls=tx_rx_lora_USRP, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
