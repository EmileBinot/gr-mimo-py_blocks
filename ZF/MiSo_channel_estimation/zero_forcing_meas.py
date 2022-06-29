#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: zero_forcing_meas
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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class zero_forcing_meas(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "zero_forcing_meas", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("zero_forcing_meas")
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

        self.settings = Qt.QSettings("GNU Radio", "zero_forcing_meas")

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
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_qpsk().base()
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(variable_constellation_0)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(variable_constellation_0)
        self.blocks_vector_source_x_0 = blocks.vector_source_b((0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3), True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (20, 20))
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(0.7071067, 1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, 'dumpIN', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'dumpOUT', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_random_uniform_source_x_0 = analog.random_uniform_source_b(0, 4, 42)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_uniform_source_x_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self, 1), (self, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "zero_forcing_meas")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)




def main(top_block_cls=zero_forcing_meas, options=None):

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
