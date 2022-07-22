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

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
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
from gnuradio import pdu
import pmt
from gnuradio import uhd
import time
from gnuradio import zeromq
import Tx_cal_epy_block_0 as epy_block_0  # embedded python block
import Tx_cal_epy_block_0_0_0 as epy_block_0_0_0  # embedded python block
import Tx_cal_epy_block_0_0_0_1 as epy_block_0_0_0_1  # embedded python block
import Tx_cal_epy_block_0_2 as epy_block_0_2  # embedded python block
import Tx_cal_epy_block_0_2_0 as epy_block_0_2_0  # embedded python block
import Tx_cal_epy_block_0_3_0_0 as epy_block_0_3_0_0  # embedded python block
import Tx_cal_epy_block_0_3_0_1 as epy_block_0_3_0_1  # embedded python block
import Tx_cal_epy_block_0_3_0_1_0 as epy_block_0_3_0_1_0  # embedded python block
import Tx_cal_epy_block_0_3_0_1_0_0 as epy_block_0_3_0_1_0_0  # embedded python block
import Tx_cal_epy_block_1 as epy_block_1  # embedded python block
import Tx_cal_epy_block_2 as epy_block_2  # embedded python block
import Tx_cal_epy_block_3 as epy_block_3  # embedded python block
import Tx_cal_epy_block_3_0 as epy_block_3_0  # embedded python block
import Tx_cal_python_mod as python_mod  # embedded python module
import threading



from gnuradio import qtgui

class Tx_cal(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "Tx_cal")

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
        self.samp_rate = samp_rate = 125000
        self.payload_len = payload_len = 65000
        self.max_angle = max_angle = 0
        self.gain = gain = 1
        self.chooser = chooser = 0
        self.center_freq = center_freq = 945000000
        self.angle = angle = python_mod.sweeper(fun_prob)

        ##################################################
        # Blocks
        ##################################################
        self.probSign = blocks.probe_signal_c()
        # Create the options list
        self._chooser_options = [0, 1, 2]
        # Create the labels list
        self._chooser_labels = ['Rx cal', 'Tx cal', 'Beamsteering']
        # Create the combo box
        # Create the radio buttons
        self._chooser_group_box = Qt.QGroupBox("Choose State" + ": ")
        self._chooser_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._chooser_button_group = variable_chooser_button_group()
        self._chooser_group_box.setLayout(self._chooser_box)
        for i, _label in enumerate(self._chooser_labels):
            radio_button = Qt.QRadioButton(_label)
            self._chooser_box.addWidget(radio_button)
            self._chooser_button_group.addButton(radio_button, i)
        self._chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chooser_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._chooser_options.index(i)))
        self._chooser_callback(self.chooser)
        self._chooser_button_group.buttonClicked[int].connect(
            lambda i: self.set_chooser(self._chooser_options[i]))
        self.top_grid_layout.addWidget(self._chooser_group_box, 0, 1, 1, 7)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_push_msg_sink_0 = zeromq.push_msg_sink('tcp://10.10.8.34:5678', 100, True)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_float, 1, 'tcp://10.10.8.27:5678', 100, False, -1)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("addr0=192.168.10.3, addr1=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_source_0_0.set_clock_source('mimo', 1)
        self.uhd_usrp_source_0_0.set_time_source('mimo', 1)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate*10)
        # No synchronization enforced.

        self.uhd_usrp_source_0_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0_0.set_gain(9, 0)

        self.uhd_usrp_source_0_0.set_center_freq(center_freq, 1)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_source_0_0.set_gain(9, 1)
        self.uhd_usrp_sink_0_0_0 = uhd.usrp_sink(
            ",".join(("addr0=192.168.10.3, addr1=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
            "",
        )
        self.uhd_usrp_sink_0_0_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_sink_0_0_0.set_clock_source('mimo', 1)
        self.uhd_usrp_sink_0_0_0.set_time_source('mimo', 1)
        self.uhd_usrp_sink_0_0_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_sink_0_0_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0_0.set_normalized_gain(gain, 0)

        self.uhd_usrp_sink_0_0_0.set_center_freq(center_freq, 1)
        self.uhd_usrp_sink_0_0_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_sink_0_0_0.set_normalized_gain(gain, 1)
        self.save2 = _save2_toggle_button = qtgui.MsgPushButton('Save Variables No Cal', 'pressed',1,"default","default")
        self.save2 = _save2_toggle_button

        self.top_grid_layout.addWidget(_save2_toggle_button, 10, 4, 1, 4)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 8):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.save = _save_toggle_button = qtgui.MsgPushButton('Save Variables', 'pressed',1,"default","default")
        self.save = _save_toggle_button

        self.top_grid_layout.addWidget(_save_toggle_button, 10, 0, 1, 4)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Received signal", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_1.enable_tags(False)
        self.qtgui_time_sink_x_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_1.enable_stem_plot(False)


        labels = ['Ant 0', 'Ant 1', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [2.0, 2.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_1_1_win, 3, 3, 2, 3)
        for r in range(3, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Tx PLLs Calibrated", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_0_0.enable_tags(False)
        self.qtgui_time_sink_x_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_0_0.enable_stem_plot(False)


        labels = ['Ant 0', 'Ant 1', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [2.0, 2.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_1_0_0_win, 5, 3, 2, 3)
        for r in range(5, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Rx PLLs Calibrated", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1_0.enable_tags(False)
        self.qtgui_time_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1_0.enable_stem_plot(False)


        labels = ['Ant 0', 'Ant 1', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [2.0, 2.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_1_0_win, 5, 0, 2, 3)
        for r in range(5, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Received signal", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(False)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['Ant 0', 'Ant 1', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [2, 2, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [2.0, 2.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_1_win, 3, 0, 2, 3)
        for r in range(3, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0_0_0.set_title("Phase Difference between USRPs Tx PLLs (degrees)")

        labels = ['Phase Shift :', '', '', '', '',
            '', '', '', '', '']
        units = ['°', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0_0_0_0.set_min(i, -180)
            self.qtgui_number_sink_0_0_0_0_0.set_max(i, 180)
            self.qtgui_number_sink_0_0_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_0_0_win, 8, 3, 1, 3)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0_0.set_title("Phase Difference between USRPs Rx PLLs (degrees)")

        labels = ['Phase Shift :', '', '', '', '',
            '', '', '', '', '']
        units = ['°', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0_0_0.set_min(i, -180)
            self.qtgui_number_sink_0_0_0_0.set_max(i, 180)
            self.qtgui_number_sink_0_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_0_win, 8, 0, 1, 3)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0_0_0 = self._qtgui_ledindicator_0_0_0_win = qtgui.GrLEDIndicator("Beamsteering", "green", "silver", chooser == 2, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0_0_0 = self._qtgui_ledindicator_0_0_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_0_0_win, 2, 6, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 7):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0_0 = self._qtgui_ledindicator_0_0_win = qtgui.GrLEDIndicator("Tx Calibration", "green", "silver", chooser == 1, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0_0 = self._qtgui_ledindicator_0_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_0_win, 2, 3, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("Rx Calibration", "green", "silver", chooser == 0, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0_0_0 = qtgui.edit_box_msg(qtgui.STRING, 'pmt.intern("#t")', 'Send Rx cal frame', False, True, 'pmt.intern("#t")', None)
        self._qtgui_edit_box_msg_0_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_0_0_win, 9, 0, 1, 3)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.STRING, 'pmt.intern("#t")', 'Send Tx cal frame', False, True, 'pmt.intern("#t")', None)
        self._qtgui_edit_box_msg_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_0_win, 9, 3, 1, 3)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pwr = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.pwr.set_update_time(0.10)
        self.pwr.set_title("Power Received")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.pwr.set_min(i, 0)
            self.pwr.set_max(i, 100)
            self.pwr.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.pwr.set_label(i, "Data {0}".format(i))
            else:
                self.pwr.set_label(i, labels[i])
            self.pwr.set_unit(i, units[i])
            self.pwr.set_factor(i, factor[i])

        self.pwr.enable_autoscale(False)
        self._pwr_win = sip.wrapinstance(self.pwr.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._pwr_win, 4, 6, 1, 3)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.push = _push_toggle_button = qtgui.MsgPushButton('Reset Max', 'pressed',1,"default","default")
        self.push = _push_toggle_button

        self.top_grid_layout.addWidget(_push_toggle_button, 5, 6, 1, 3)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pdu_random_pdu_0_0_0 = pdu.random_pdu(payload_len, payload_len, 0x01, payload_len)
        self.pdu_pdu_to_stream_x_0_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, payload_len)
        self._max_angle_tool_bar = Qt.QToolBar(self)

        if None:
            self._max_angle_formatter = None
        else:
            self._max_angle_formatter = lambda x: str(x)

        self._max_angle_tool_bar.addWidget(Qt.QLabel("Max Power Received @ :"))
        self._max_angle_label = Qt.QLabel(str(self._max_angle_formatter(self.max_angle)))
        self._max_angle_tool_bar.addWidget(self._max_angle_label)
        self.top_grid_layout.addWidget(self._max_angle_tool_bar, 6, 6, 1, 3)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.epy_block_3_0 = epy_block_3_0.blk()
        self.epy_block_3 = epy_block_3.blk()
        self.epy_block_2 = epy_block_2.blk()
        self.epy_block_1 = epy_block_1.blk(angle=angle)
        self.epy_block_0_3_0_1_0_0 = epy_block_0_3_0_1_0_0.blk()
        self.epy_block_0_3_0_1_0 = epy_block_0_3_0_1_0.blk()
        self.epy_block_0_3_0_1 = epy_block_0_3_0_1.blk()
        self.epy_block_0_3_0_0 = epy_block_0_3_0_0.blk()
        self.epy_block_0_2_0 = epy_block_0_2_0.blk()
        self.epy_block_0_2 = epy_block_0_2.blk()
        self.epy_block_0_0_0_1 = epy_block_0_0_0_1.blk(num_samples_to_process=samp_rate*2, threshold=0.05)
        self.epy_block_0_0_0 = epy_block_0_0_0.blk(num_samples_to_process=samp_rate*2, threshold=0.05)
        self.epy_block_0 = epy_block_0.blk(angle=angle)
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_stream_mux_0_1_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_stream_mux_0_1 = blocks.stream_mux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_float*1, (1, 1))
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_stream_demux_0_1 = blocks.stream_demux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_stream_demux_0_0 = blocks.stream_demux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_stream_demux_0 = blocks.stream_demux(gr.sizeof_gr_complex*1, (1, 1))
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,chooser-1 if chooser>0 else chooser,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,chooser)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_max_angle)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, 'beam_trace', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_copy_0_0 = blocks.copy(gr.sizeof_float*1)
        self.blocks_copy_0_0.set_enabled(chooser == 2)
        self.blocks_complex_to_real_0_1_0_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_1_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_1_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_1_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0_0_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0_0_0 = blocks.complex_to_real(1)
        self.ang = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.ang.set_update_time(0.10)
        self.ang.set_title("Angle")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.ang.set_min(i, -90)
            self.ang.set_max(i, 90)
            self.ang.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.ang.set_label(i, "Data {0}".format(i))
            else:
                self.ang.set_label(i, labels[i])
            self.ang.set_unit(i, units[i])
            self.ang.set_factor(i, factor[i])

        self.ang.enable_autoscale(False)
        self._ang_win = sip.wrapinstance(self.ang.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._ang_win, 3, 6, 1, 3)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(6, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_SQR_WAVE, 0.01, 1, 0, 0)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 1000, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0_0, 'phase_diff'), (self.epy_block_0_3_0_1, 'phase_diff'))
        self.msg_connect((self.epy_block_0_0_0, 'phase_diff'), (self.epy_block_0_3_0_1_0, 'phase_diff'))
        self.msg_connect((self.epy_block_0_0_0, 'phase_diff'), (self.epy_block_3, 'Rx_PLL_phase'))
        self.msg_connect((self.epy_block_0_0_0, 'phase_diff'), (self.epy_block_3_0, 'Rx_PLL_phase'))
        self.msg_connect((self.epy_block_0_0_0_1, 'phase_diff'), (self.epy_block_0_3_0_0, 'phase_diff'))
        self.msg_connect((self.epy_block_0_0_0_1, 'phase_diff'), (self.epy_block_0_3_0_1_0_0, 'phase_diff'))
        self.msg_connect((self.epy_block_0_0_0_1, 'phase_diff'), (self.epy_block_3, 'Tx_PLL_phase'))
        self.msg_connect((self.epy_block_0_0_0_1, 'phase_diff'), (self.epy_block_3_0, 'Tx_PLL_phase'))
        self.msg_connect((self.epy_block_2, 'max_angle_out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_2, 'max_pwr_out'), (self.epy_block_3, 'Max_pwr'))
        self.msg_connect((self.epy_block_2, 'max_angle_out'), (self.epy_block_3, 'Max_angle'))
        self.msg_connect((self.epy_block_2, 'max_angle_out'), (self.epy_block_3_0, 'Max_angle'))
        self.msg_connect((self.epy_block_2, 'max_pwr_out'), (self.epy_block_3_0, 'Max_pwr'))
        self.msg_connect((self.pdu_random_pdu_0_0_0, 'pdus'), (self.pdu_pdu_to_stream_x_0_0, 'pdus'))
        self.msg_connect((self.push, 'pressed'), (self.epy_block_2, 'reset'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.pdu_random_pdu_0_0_0, 'generate'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0_0, 'msg'), (self.zeromq_push_msg_sink_0, 'in'))
        self.msg_connect((self.save, 'pressed'), (self.epy_block_3, 'Trigger'))
        self.msg_connect((self.save2, 'pressed'), (self.epy_block_3_0, 'Trigger'))
        self.connect((self.analog_const_source_x_0, 0), (self.epy_block_0_2_0, 0))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.probSign, 0))
        self.connect((self.blocks_complex_to_real_0_0_0_0, 0), (self.qtgui_time_sink_x_0_1, 1))
        self.connect((self.blocks_complex_to_real_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0_1_0, 1))
        self.connect((self.blocks_complex_to_real_0_0_0_0_0_0, 0), (self.qtgui_time_sink_x_0_1_0_0, 1))
        self.connect((self.blocks_complex_to_real_0_0_0_0_1, 0), (self.qtgui_time_sink_x_0_1_1, 1))
        self.connect((self.blocks_complex_to_real_0_1_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_complex_to_real_0_1_0_0, 0), (self.qtgui_time_sink_x_0_1_0, 0))
        self.connect((self.blocks_complex_to_real_0_1_0_0_0, 0), (self.qtgui_time_sink_x_0_1_0_0, 0))
        self.connect((self.blocks_complex_to_real_0_1_0_1, 0), (self.qtgui_time_sink_x_0_1_1, 0))
        self.connect((self.blocks_copy_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.epy_block_0_2, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_mux_0_1_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_stream_mux_0_1_0, 1))
        self.connect((self.blocks_selector_0, 2), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_stream_demux_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_stream_demux_0_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_stream_demux_0_1, 0))
        self.connect((self.blocks_stream_demux_0, 0), (self.epy_block_0_0_0, 0))
        self.connect((self.blocks_stream_demux_0, 1), (self.epy_block_0_0_0, 1))
        self.connect((self.blocks_stream_demux_0_0, 1), (self.epy_block_0_3_0_1, 1))
        self.connect((self.blocks_stream_demux_0_0, 0), (self.epy_block_0_3_0_1, 0))
        self.connect((self.blocks_stream_demux_0_1, 0), (self.uhd_usrp_sink_0_0_0, 0))
        self.connect((self.blocks_stream_demux_0_1, 1), (self.uhd_usrp_sink_0_0_0, 1))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.epy_block_2, 0))
        self.connect((self.blocks_stream_mux_0_1, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.blocks_stream_mux_0_1_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.epy_block_0, 1), (self.ang, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.epy_block_0, 1), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.epy_block_0, 0), (self.pwr, 0))
        self.connect((self.epy_block_0_0_0, 1), (self.blocks_complex_to_real_0_0_0_0, 0))
        self.connect((self.epy_block_0_0_0, 0), (self.blocks_complex_to_real_0_1_0, 0))
        self.connect((self.epy_block_0_0_0, 1), (self.epy_block_0_3_0_1_0, 1))
        self.connect((self.epy_block_0_0_0, 0), (self.epy_block_0_3_0_1_0, 0))
        self.connect((self.epy_block_0_0_0, 2), (self.qtgui_number_sink_0_0_0_0, 0))
        self.connect((self.epy_block_0_0_0_1, 1), (self.blocks_complex_to_real_0_0_0_0_1, 0))
        self.connect((self.epy_block_0_0_0_1, 0), (self.blocks_complex_to_real_0_1_0_1, 0))
        self.connect((self.epy_block_0_0_0_1, 0), (self.epy_block_0_3_0_1_0_0, 0))
        self.connect((self.epy_block_0_0_0_1, 1), (self.epy_block_0_3_0_1_0_0, 1))
        self.connect((self.epy_block_0_0_0_1, 2), (self.qtgui_number_sink_0_0_0_0_0, 0))
        self.connect((self.epy_block_0_2, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.epy_block_0_2_0, 0), (self.epy_block_0_3_0_0, 0))
        self.connect((self.epy_block_0_2_0, 0), (self.epy_block_0_3_0_0, 1))
        self.connect((self.epy_block_0_3_0_0, 1), (self.epy_block_1, 1))
        self.connect((self.epy_block_0_3_0_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0_3_0_1, 1), (self.epy_block_0_0_0_1, 1))
        self.connect((self.epy_block_0_3_0_1, 0), (self.epy_block_0_0_0_1, 0))
        self.connect((self.epy_block_0_3_0_1_0, 1), (self.blocks_complex_to_real_0_0_0_0_0, 0))
        self.connect((self.epy_block_0_3_0_1_0, 0), (self.blocks_complex_to_real_0_1_0_0, 0))
        self.connect((self.epy_block_0_3_0_1_0_0, 1), (self.blocks_complex_to_real_0_0_0_0_0_0, 0))
        self.connect((self.epy_block_0_3_0_1_0_0, 0), (self.blocks_complex_to_real_0_1_0_0_0, 0))
        self.connect((self.epy_block_1, 1), (self.blocks_stream_mux_0_1, 1))
        self.connect((self.epy_block_1, 0), (self.blocks_stream_mux_0_1, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.pdu_pdu_to_stream_x_0_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 1), (self.blocks_stream_mux_0, 1))
        self.connect((self.zeromq_pull_source_0, 0), (self.blocks_copy_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Tx_cal")
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
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1_1.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate*10)

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.pdu_pdu_to_stream_x_0_0.set_max_queue_size(self.payload_len)

    def get_max_angle(self):
        return self.max_angle

    def set_max_angle(self, max_angle):
        self.max_angle = max_angle
        Qt.QMetaObject.invokeMethod(self._max_angle_label, "setText", Qt.Q_ARG("QString", str(self._max_angle_formatter(self.max_angle))))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0_0_0.set_normalized_gain(self.gain, 0)
        self.uhd_usrp_sink_0_0_0.set_normalized_gain(self.gain, 1)

    def get_chooser(self):
        return self.chooser

    def set_chooser(self, chooser):
        self.chooser = chooser
        self._chooser_callback(self.chooser)
        self.blocks_copy_0_0.set_enabled(self.chooser == 2)
        self.blocks_selector_0.set_output_index(self.chooser)
        self.blocks_selector_0_0.set_input_index(self.chooser-1 if self.chooser>0 else self.chooser)
        self.qtgui_ledindicator_0.setState(self.chooser == 0)
        self.qtgui_ledindicator_0_0.setState(self.chooser == 1)
        self.qtgui_ledindicator_0_0_0.setState(self.chooser == 2)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_sink_0_0_0.set_center_freq(self.center_freq, 1)
        self.uhd_usrp_source_0_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.center_freq, 1)

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle
        self.epy_block_0.angle = self.angle
        self.epy_block_1.angle = self.angle




def main(top_block_cls=Tx_cal, options=None):

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
