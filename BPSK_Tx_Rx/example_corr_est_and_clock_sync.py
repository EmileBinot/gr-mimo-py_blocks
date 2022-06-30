#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Example Corr Est And Clock Sync
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
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import example_corr_est_and_clock_sync_epy_block_0 as epy_block_0  # embedded python block



from gnuradio import qtgui

class example_corr_est_and_clock_sync(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Example Corr Est And Clock Sync", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Example Corr Est And Clock Sync")
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

        self.settings = Qt.QSettings("GNU Radio", "example_corr_est_and_clock_sync")

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
        self.sps = sps = 2
        self.hdr_const = hdr_const = digital.constellation_calcdist(digital.psk_2()[0], digital.psk_2()[1],
        2, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.hdr_const.gen_soft_dec_lut(8)
        self.eb = eb = 0.22
        self.rxmod = rxmod = digital.generic_mod(hdr_const, False, sps, True, eb, False, False)
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(sps, sps,1.0, eb, 11*sps)
        self.nfilts = nfilts = 32
        self.mark_delays = mark_delays = [0, 0, 34, 56, 87, 119]
        self.ac_hex = ac_hex = [0xac, 0xdd, 0xa4, 0xe2, 0xf2, 0x8c, 0x20, 0xfc]
        self.time_off = time_off = 1.0
        self.samp_rate = samp_rate = 10e3
        self.rx_psf_taps = rx_psf_taps = firdes.root_raised_cosine(nfilts, sps*nfilts,1.0, eb, 11*sps*nfilts)
        self.path_loss = path_loss = 10
        self.noise = noise = -50
        self.modulated_sync_word = modulated_sync_word = digital.modulate_vector_bc(rxmod.to_basic_block(), ac_hex, [1])
        self.mark_delay = mark_delay = mark_delays[sps]
        self.freq_off = freq_off = 0
        self.filt_delay = filt_delay = 1+(len(rrc_taps)-1)//2
        self.ac = ac = list(map(lambda x: int(x), list(digital.packet_utils.default_access_code)))

        ##################################################
        # Blocks
        ##################################################
        self._time_off_range = Range(0.9999, 1.0001, 0.00001, 1.0, 200)
        self._time_off_win = RangeWidget(self._time_off_range, self.set_time_off, "Time Off.", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._time_off_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._path_loss_range = Range(0, 140, 5, 10, 200)
        self._path_loss_win = RangeWidget(self._path_loss_range, self.set_path_loss, "Path Loss (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._path_loss_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_range = Range(-50, 10, 1, -50, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, "Noise Power", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._noise_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_off_range = Range(-0.25, 0.25, 0.0001, 0, 200)
        self._freq_off_win = RangeWidget(self._freq_off_range, self.set_freq_off, "Freq. Off.", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_off_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            200, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 15, 0, 'corr_start')
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
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


        for i in range(2):
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
        self.qtgui_sink_x_1 = qtgui.sink_c(
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
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
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
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(sps, rrc_taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(filt_delay)
        self.epy_block_0 = epy_block_0.my_basic_adder_block(tag_name="corr_start", len=80)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 6.28/400.0, rx_psf_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(modulated_sync_word, sps, mark_delay, 0.999, digital.THRESHOLD_DYNAMIC)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=sps * 10.0**(noise/10.0),
            frequency_offset=freq_off,
            epsilon=time_off,
            taps=[10.0**(-path_loss/20.0)],
            noise_seed=0,
            block_tags=True)
        self.blocks_vector_source_x_0 = blocks.vector_source_c([1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0] + ac, True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "corr_start")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, 1, len(ac)+16, "packet_len")
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (80, 80))
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(2)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(-1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.channels_channel_model_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "example_corr_est_and_clock_sync")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_mark_delay(self.mark_delays[self.sps])
        self.set_rrc_taps(firdes.root_raised_cosine(self.sps, self.sps, 1.0, self.eb, 11*self.sps))
        self.set_rx_psf_taps(firdes.root_raised_cosine(self.nfilts, self.sps*self.nfilts, 1.0, self.eb, 11*self.sps*self.nfilts))
        self.set_rxmod(digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False))
        self.channels_channel_model_0.set_noise_voltage(self.sps * 10.0**(self.noise/10.0))

    def get_hdr_const(self):
        return self.hdr_const

    def set_hdr_const(self, hdr_const):
        self.hdr_const = hdr_const
        self.set_rxmod(digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False))

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_rrc_taps(firdes.root_raised_cosine(self.sps, self.sps, 1.0, self.eb, 11*self.sps))
        self.set_rx_psf_taps(firdes.root_raised_cosine(self.nfilts, self.sps*self.nfilts, 1.0, self.eb, 11*self.sps*self.nfilts))
        self.set_rxmod(digital.generic_mod(self.hdr_const, False, self.sps, True, self.eb, False, False))

    def get_rxmod(self):
        return self.rxmod

    def set_rxmod(self, rxmod):
        self.rxmod = rxmod

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.set_filt_delay(1+(len(self.rrc_taps)-1)//2)
        self.interp_fir_filter_xxx_0.set_taps(self.rrc_taps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rx_psf_taps(firdes.root_raised_cosine(self.nfilts, self.sps*self.nfilts, 1.0, self.eb, 11*self.sps*self.nfilts))

    def get_mark_delays(self):
        return self.mark_delays

    def set_mark_delays(self, mark_delays):
        self.mark_delays = mark_delays
        self.set_mark_delay(self.mark_delays[self.sps])

    def get_ac_hex(self):
        return self.ac_hex

    def set_ac_hex(self, ac_hex):
        self.ac_hex = ac_hex

    def get_time_off(self):
        return self.time_off

    def set_time_off(self, time_off):
        self.time_off = time_off
        self.channels_channel_model_0.set_timing_offset(self.time_off)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_rx_psf_taps(self):
        return self.rx_psf_taps

    def set_rx_psf_taps(self, rx_psf_taps):
        self.rx_psf_taps = rx_psf_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rx_psf_taps)

    def get_path_loss(self):
        return self.path_loss

    def set_path_loss(self, path_loss):
        self.path_loss = path_loss
        self.channels_channel_model_0.set_taps([10.0**(-self.path_loss/20.0)])

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.channels_channel_model_0.set_noise_voltage(self.sps * 10.0**(self.noise/10.0))

    def get_modulated_sync_word(self):
        return self.modulated_sync_word

    def set_modulated_sync_word(self, modulated_sync_word):
        self.modulated_sync_word = modulated_sync_word

    def get_mark_delay(self):
        return self.mark_delay

    def set_mark_delay(self, mark_delay):
        self.mark_delay = mark_delay
        self.digital_corr_est_cc_0.set_mark_delay(self.mark_delay)

    def get_freq_off(self):
        return self.freq_off

    def set_freq_off(self, freq_off):
        self.freq_off = freq_off
        self.channels_channel_model_0.set_frequency_offset(self.freq_off)

    def get_filt_delay(self):
        return self.filt_delay

    def set_filt_delay(self, filt_delay):
        self.filt_delay = filt_delay

    def get_ac(self):
        return self.ac

    def set_ac(self, ac):
        self.ac = ac
        self.blocks_stream_to_tagged_stream_0.set_packet_len(len(self.ac)+16)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(len(self.ac)+16)
        self.blocks_vector_source_x_0.set_data([1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0] + self.ac, [])




def main(top_block_cls=example_corr_est_and_clock_sync, options=None):

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
