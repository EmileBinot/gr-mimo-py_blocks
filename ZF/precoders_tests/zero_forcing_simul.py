#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.2.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import zero_forcing_simul_epy_block_0 as epy_block_0  # embedded python block
import zero_forcing_simul_epy_block_1 as epy_block_1  # embedded python block
import zero_forcing_simul_epy_block_1_0 as epy_block_1_0  # embedded python block



from gnuradio import qtgui

class zero_forcing_simul(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "zero_forcing_simul")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.H = H = [[1+2j, 1+9j]]

        ##################################################
        # Blocks
        ##################################################
        self.epy_block_1_0 = epy_block_1_0.blk(angle=0)
        self.epy_block_1 = epy_block_1.blk(angle=0)
        self.epy_block_0 = epy_block_0.blk(H=H)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_null_sink_0_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(H[0][1])
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(H[0][0])
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'dumpIN', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'dumpOUT', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.epy_block_0, 1), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_1, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.epy_block_1_0, 0), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.epy_block_1_0, 1), (self.blocks_null_sink_0_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "zero_forcing_simul")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_H(self):
        return self.H

    def set_H(self, H):
        self.H = H
        self.blocks_multiply_const_vxx_0.set_k(self.H[0][0])
        self.blocks_multiply_const_vxx_1.set_k(self.H[0][1])
        self.epy_block_0.H = self.H




def main(top_block_cls=zero_forcing_simul, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
