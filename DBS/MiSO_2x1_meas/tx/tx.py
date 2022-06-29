#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: ebinot
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
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import uhd
import time
from gnuradio import zeromq
import threading
import tx_epy_block_0 as epy_block_0  # embedded python block
import tx_epy_block_1 as epy_block_1  # embedded python block
import tx_python_mod as python_mod  # embedded python module



from gnuradio import qtgui

class tx(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "tx")

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
        self.fun_prob = fun_prob = 0
        self.samp_rate = samp_rate = 100000
        self.gain = gain = 50
        self.center_freq = center_freq = int(944.8e6)
        self.angle = angle = python_mod.sweeper(fun_prob)

        ##################################################
        # Blocks
        ##################################################
        self.probSign = blocks.probe_signal_c()
        self._gain_tool_bar = Qt.QToolBar(self)
        self._gain_tool_bar.addWidget(Qt.QLabel("'gain'" + ": "))
        self._gain_line_edit = Qt.QLineEdit(str(self.gain))
        self._gain_tool_bar.addWidget(self._gain_line_edit)
        self._gain_line_edit.returnPressed.connect(
            lambda: self.set_gain(int(str(self._gain_line_edit.text()))))
        self.top_layout.addWidget(self._gain_tool_bar)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_float, 1, 'tcp://10.10.8.27:5678', 100, False, -1)
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
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        def _fun_prob_probe():
          while True:

            val = self.probSign.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_fun_prob,val))
              except AttributeError:
                self.set_fun_prob(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _fun_prob_thread = threading.Thread(target=_fun_prob_probe)
        _fun_prob_thread.daemon = True
        _fun_prob_thread.start()
        self.epy_block_1 = epy_block_1.blk(angle=angle)
        self.epy_block_0 = epy_block_0.blk(angle=angle)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_float*1, (1, 1))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'beam_trace', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_SQR_WAVE, 10, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.epy_block_1, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.probSign, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.epy_block_0, 1), (self.blocks_stream_mux_0, 1))
        self.connect((self.epy_block_0, 1), (self.qtgui_number_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.epy_block_1, 1), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.epy_block_1, 1), (self.uhd_usrp_sink_0_0, 1))
        self.connect((self.epy_block_1, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.zeromq_pull_source_0, 0), (self.epy_block_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_fun_prob(self):
        return self.fun_prob

    def set_fun_prob(self, fun_prob):
        self.fun_prob = fun_prob
        self.set_angle(python_mod.sweeper(self.fun_prob))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        Qt.QMetaObject.invokeMethod(self._gain_line_edit, "setText", Qt.Q_ARG("QString", str(self.gain)))
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 0)
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 1)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0_0.set_center_freq(self.center_freq, 1)

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle
        self.epy_block_0.angle = self.angle
        self.epy_block_1.angle = self.angle




def main(top_block_cls=tx, options=None):

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
