#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.2.0

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import pdu
from gnuradio import uhd
import time
from gnuradio import zeromq
import tx_rx_lora_USRP_epy_block_0_1_0_0 as epy_block_0_1_0_0  # embedded python block
import tx_rx_lora_USRP_epy_block_13 as epy_block_13  # embedded python block
import tx_rx_lora_USRP_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import tx_rx_lora_USRP_epy_block_1_1 as epy_block_1_1  # embedded python block
import tx_rx_lora_USRP_epy_block_3 as epy_block_3  # embedded python block
import tx_rx_lora_USRP_epy_block_6 as epy_block_6  # embedded python block
import tx_rx_lora_USRP_epy_block_6_0_0_0_0_0 as epy_block_6_0_0_0_0_0  # embedded python block
import tx_rx_lora_USRP_epy_block_7_0 as epy_block_7_0  # embedded python block
import tx_rx_lora_USRP_epy_block_8 as epy_block_8  # embedded python block




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
        self.h2_est = h2_est = 9
        self.h1_est = h1_est = 9
        self.bandwidth = bandwidth = int(125e3)
        self.samp_rate = samp_rate = bandwidth
        self.preamble_nitems = preamble_nitems = round(pow(2,SF)*(preamble_len+2.25))
        self.payload_nitems = payload_nitems = int(payload_nsymb*pow(2,SF))
        self.padding = padding = 100
        self.os_factor = os_factor = 1
        self.gain = gain = 50
        self.const_multiply = const_multiply = 1
        self.center_freq = center_freq = int(868e6)
        self.H_est = H_est = [[h1_est,h2_est]]

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pull_msg_source_0_0 = zeromq.pull_msg_source('tcp://10.10.8.27:5679', 100, False)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://10.10.8.27:5678', 100, False)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(("addr0=192.168.10.3, addr1=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
            "",
        )
        self.uhd_usrp_sink_0_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_sink_0_0.set_clock_source('mimo', 1)
        self.uhd_usrp_sink_0_0.set_time_source('mimo', 1)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_sink_0_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0.set_gain(gain, 0)

        self.uhd_usrp_sink_0_0.set_center_freq(center_freq, 1)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0_0.set_gain(gain, 1)
        self.pdu_random_pdu_0 = pdu.random_pdu(payload_len, payload_len, 0x0F, SF)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.epy_block_8 = epy_block_8.blk(SF=9)
        self.epy_block_7_0 = epy_block_7_0.blk(preamble_nitems=preamble_nitems, payload_nitems=payload_nitems, padding=padding)
        self.epy_block_6_0_0_0_0_0 = epy_block_6_0_0_0_0_0.Modulation(SF=SF)
        self.epy_block_6 = epy_block_6.blk(preamble_nitems=4224, payload_nitems=8192, padding=padding)
        self.epy_block_3 = epy_block_3.PreambleGenerator(SF=SF, preamble_len=preamble_len)
        self.epy_block_1_1 = epy_block_1_1.HammingTx(CR=CR)
        self.epy_block_1_0_0 = epy_block_1_0_0.Whitening(reset_key="tx_sob")
        self.epy_block_13 = epy_block_13.blk()
        self.epy_block_0_1_0_0 = epy_block_0_1_0_0.Interleaver(SF=SF, CR=CR)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, payload_nitems+preamble_nitems+padding)
        self.blocks_var_to_msg_0 = blocks.var_to_msg_pair('h1_est')
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, 'packet_len')
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, payload_nitems)
        self.blocks_null_sink_4 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("#t"), 5000)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_file_sink_0_3_0_0_0_0_1 = blocks.file_sink(gr.sizeof_int*1, 'dumpINsymb', False)
        self.blocks_file_sink_0_3_0_0_0_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_3_0_0_0 = blocks.file_sink(gr.sizeof_char*1, 'dumpIN', False)
        self.blocks_file_sink_0_3_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_2_0_0 = blocks.file_sink(gr.sizeof_gr_complex*payload_nitems, 'lora_tx_payload', False)
        self.blocks_file_sink_0_2_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'lora_tx', False)
        self.blocks_file_sink_0_1.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.pdu_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_var_to_msg_0, 'msgout'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.pdu_random_pdu_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.epy_block_13, 'h1_est'))
        self.msg_connect((self.zeromq_pull_msg_source_0_0, 'out'), (self.epy_block_13, 'h2_est'))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.blocks_file_sink_0_2_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.epy_block_6, 1))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.epy_block_7_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.epy_block_0_1_0_0, 0), (self.blocks_file_sink_0_3_0_0_0_0_1, 0))
        self.connect((self.epy_block_0_1_0_0, 0), (self.epy_block_8, 0))
        self.connect((self.epy_block_13, 0), (self.blocks_null_sink_4, 0))
        self.connect((self.epy_block_13, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.epy_block_13, 1), (self.uhd_usrp_sink_0_0, 1))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_1_1, 0))
        self.connect((self.epy_block_1_1, 0), (self.epy_block_0_1_0_0, 0))
        self.connect((self.epy_block_3, 0), (self.epy_block_6, 0))
        self.connect((self.epy_block_6, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.epy_block_6_0_0_0_0_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.epy_block_7_0, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.epy_block_7_0, 0), (self.epy_block_13, 0))
        self.connect((self.epy_block_8, 0), (self.epy_block_6_0_0_0_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_file_sink_0_3_0_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.epy_block_1_0_0, 0))


    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))

    def get_SF(self):
        return self.SF

    def set_SF(self, SF):
        self.SF = SF
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_0_1_0_0.SF = self.SF
        self.epy_block_3.SF = self.SF
        self.epy_block_6_0_0_0_0_0.SF = self.SF

    def get_CR(self):
        return self.CR

    def set_CR(self, CR):
        self.CR = CR
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.epy_block_0_1_0_0.CR = self.CR
        self.epy_block_1_1.CR = self.CR

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_3.preamble_len = self.preamble_len

    def get_payload_nsymb(self):
        return self.payload_nsymb

    def set_payload_nsymb(self, payload_nsymb):
        self.payload_nsymb = payload_nsymb
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))

    def get_h2_est(self):
        return self.h2_est

    def set_h2_est(self, h2_est):
        self.h2_est = h2_est
        self.set_H_est([[self.h1_est,self.h2_est]])

    def get_h1_est(self):
        return self.h1_est

    def set_h1_est(self, h1_est):
        self.h1_est = h1_est
        self.set_H_est([[self.h1_est,self.h2_est]])
        self.blocks_var_to_msg_0.variable_changed(self.h1_est)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_samp_rate(self.bandwidth)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)

    def get_preamble_nitems(self):
        return self.preamble_nitems

    def set_preamble_nitems(self, preamble_nitems):
        self.preamble_nitems = preamble_nitems
        self.epy_block_7_0.preamble_nitems = self.preamble_nitems

    def get_payload_nitems(self):
        return self.payload_nitems

    def set_payload_nitems(self, payload_nitems):
        self.payload_nitems = payload_nitems
        self.epy_block_7_0.payload_nitems = self.payload_nitems

    def get_padding(self):
        return self.padding

    def set_padding(self, padding):
        self.padding = padding
        self.epy_block_6.padding = self.padding
        self.epy_block_7_0.padding = self.padding

    def get_os_factor(self):
        return self.os_factor

    def set_os_factor(self, os_factor):
        self.os_factor = os_factor

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 0)
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 1)

    def get_const_multiply(self):
        return self.const_multiply

    def set_const_multiply(self, const_multiply):
        self.const_multiply = const_multiply

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0_0.set_center_freq(self.center_freq, 1)

    def get_H_est(self):
        return self.H_est

    def set_H_est(self, H_est):
        self.H_est = H_est




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
