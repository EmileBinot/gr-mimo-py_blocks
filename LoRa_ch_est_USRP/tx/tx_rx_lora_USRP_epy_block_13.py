"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import math
import matplotlib.pyplot as plt

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def gain(d, w):
    """Return the power as a function of azimuthal angle, phi."""
    lam = 1
    d = lam / 2
    phi = np.linspace(0, 2*np.pi, 1000)
    psi = 2*np.pi * d / lam * np.cos(phi)
    j = np.arange(len(w))
    A = np.sum(w[j] * np.exp(j * 1j * psi[:, None]), axis=1)
    g = np.abs(A)**2
    return phi, g

def plot(H) :

    lam = 1
    d = lam / 2

    F_dbs = np.exp(-1j*math.pi*math.cos(0*math.pi/180)*np.arange(1,3)) # should be pointing to 0
    # print(F_dbs)
    phi, g = gain(d, F_dbs)
    DdBi_dbs = NormalizeData(g)

    F_zf = (np.linalg.pinv(H) * (1/math.sqrt(2))).flatten()
    # print(F_zf)
    phi, g = gain(d, F_zf)
    DdBi_zf = NormalizeData(g)

    F_cb = np.array(np.matrix(H).getH()).flatten()
    # print(F_cb)
    phi, g = gain(d, F_cb)
    DdBi_cb = NormalizeData(g)

    F_mrt = (H / np.linalg.norm(H)).flatten()
    # print(F_mrt)
    phi, g = gain(d, F_mrt)
    DdBi_mrt = NormalizeData(g)

    fig = plt.figure()

    ax = fig.add_subplot(projection='polar')
    ax.plot(phi, DdBi_dbs)
    
    ax = fig.add_subplot(projection='polar')
    ax.plot(phi, DdBi_zf)

    ax = fig.add_subplot(projection='polar')
    ax.plot(phi, DdBi_cb)
    
    ax = fig.add_subplot(projection='polar')
    ax.plot(phi, DdBi_mrt)

    ax.set_rlabel_position(45)
    ax.legend(['dbs', 'zf', 'cb', 'mrt'])
    plt.show()


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Estimation + Precoding',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64, np.complex64]
        )
        self.message_port_register_in(pmt.intern("h_est"))
        # self.message_port_register_in(pmt.intern("h2_est"))

        self.h1_est = []
        self.h2_est = []
        self.state = 'est_h1'
        self.set_msg_handler(pmt.intern("h_est"), self.handle_msg)
        # self.set_msg_handler(pmt.intern("h2_est"), self.handle_msg_h2)

    def handle_msg(self,msg) :
        if self.state == "est_h1" :
            self.h1_est.append(pmt.to_complex(msg))
            print("h1 = ", self.h1_est)
            print("now estimating h2 ...")
            self.state = 'est_h2'
            return 

        if self.state == "est_h2" :
            self.h2_est.append(pmt.to_complex(msg))
            print("h2 = ", self.h2_est)
            if len(self.h2_est) >= 1 :
                print("h1 and h2 have been estimated, now precoding using both antennas")
                self.state = 'ZF_precoding'
            else :
                print("now estimating h1 ...")
                self.state = 'est_h1'
            return 

        if self.state == "ZF_precoding" :
            return
            
    

    def work(self, input_items, output_items):
        
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key) # Convert from PMT to python string
            value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was
            if key == 'tx_sob':
                pass
        
        if self.state == 'est_h1' :
            print("est_h1")
            output_items[0][:] = input_items[0] * 1
            # output_items[1][:] = input_items[0] * 0
            return len(output_items[0])

        if self.state == 'est_h2' :
            print("est_h2")
            # output_items[0][:] = input_items[0] * 0
            output_items[1][:] = input_items[0] * 1
            return len(output_items[1])

        if self.state == 'ZF_precoding' :
            print("ZF_precoding")

            h1 = np.mean(self.h1_est)
            h2 = np.mean(self.h2_est)
            H=[[h1, h2]]
            self.h1_est.clear()
            self.h2_est.clear()

            # F_zf = np.linalg.pinv(H) * (1/math.sqrt(2))
            # print("F = ",F_zf)
            # x = [np.transpose(input_items[0])]
            # x_precoded = np.matmul(F_zf, x)

            # output_items[0][:] = x_precoded[0]
            # output_items[1][:] = x_precoded[1]

            plot(H)
            self.state = 'est_h1'
            return len(output_items[0])

        # if self.state == 'DBS_precoding' : 
        #     print("DBS_precoding")

        #     h1 = np.mean(self.h1_est)
        #     h2 = np.mean(self.h2_est)
        #     H=[[h1, h2]]
        #     F_dbs = np.transpose([np.exp(-1j*math.pi*math.cos(0*math.pi/180)*np.arange(1,2+1))]) * (1/math.sqrt(2))
        #     print("[TX] precoder : F = ",F_dbs)
        #     x = [np.transpose(input_items[0])]
        #     x_precoded = np.matmul(F_dbs, x)

        #     output_items[0][:] = x_precoded[0]
        #     output_items[1][:] = x_precoded[1]
        #     return len(output_items[0])

        # if self.state == 'CB_precoding' :
        #     print("CB_precoding")

        #     h1 = np.mean(self.h1_est)
        #     h2 = np.mean(self.h2_est)
        #     H=[[h1, h2]]

        #     F_cb = H.getH()
        #     print("[TX] precoder : F = ",F_cb)
        #     x = [np.transpose(input_items[0])]
        #     x_precoded = np.matmul(F_cb, x)

        #     output_items[0][:] = x_precoded[0]
        #     output_items[1][:] = x_precoded[1]
        #     return len(output_items[0])
        
