import subprocess
import argparse
import time
import binascii
import re
import scipy.signal as sig
import numpy as np
import pylab as plt
from scipy.fftpack import fft, ifft, fftshift

def configure_parser(parser):
    parser.add_argument("-o", "--output", type=str, default='coef_pkg.vhdl', help="File with coefficients")
    parser.add_argument("-i", "--input", type=str, default='tmp_coef_pkg.vhdl', help="Template Input vhdl")
    parser.add_argument("-b", "--bits", type=int, default=10, help="Bit width of each coefficient")
    parser.add_argument("-n", "--numtaps", type=int, default=20, help="numtaps of coefficient")
    parser.add_argument("-fc", "--fcutoff", type=float, default=0.2, help="Frequency cut off")
    parser.add_argument("-w", "--trans_width", type=float, default=0.4, help="Transband width")
    parser.add_argument("-t", "--filter_type", type=str, default='low_pass', help="Filter types [low_pass, band_pass, high_pass]")

def quantize (bits, array):
    q = []
    qf = []
    for i in range (len(array)):
        q.append(int(array[i]*(2**(bits-1)-1)/np.amax(array)))
        qf.append((q[i]*1.0)/(2**(bits-1)))
    return q, qf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Filter Generator")
    configure_parser(parser)
    args = parser.parse_args()

    if (args.filter_type=='low_pass'):
        b = sig.firwin(args.numtaps, args.fcutoff)
    if (args.filter_type=='high_pass'):
        b = sig.firwin(args.numtaps, args.fcutoff, pass_zero=False)
    if (args.filter_type=='band_pass'):
        b = sig.firwin(args.numtaps, [args.fcutoff, args.fcutoff+ args.trans_width], pass_zero=False)

    qb, qf = quantize(args.bits,b)

    coef_values_str = ','.join(str(x) for x in qb)

    with open(args.input, 'r') as f:
        file_content = f.read()

    file_content = file_content.format(coef_qty=args.numtaps, coef_values=coef_values_str, coef_bits=args.bits, coef_max=(2**(args.bits-1)), coef_min=(-2**(args.bits-1)))

    with open(args.output, 'w') as f:
        f.write(file_content)

    print('Created file %s' % args.output)

    qb = np.concatenate((np.zeros(10),qb,np.zeros(10)), axis=1)
    w, h = sig.freqz(b)
    wq, hq = sig.freqz(qf)
    w = w/(2*np.pi)
    fig = plt.figure()
    plt.title('Digital filter frequency response')
    ax1 = fig.add_subplot(111)
    plt.plot(w, 20 * np.log10(abs(h)), 'b')
    plt.ylabel('Amplitude [dB]', color='b')
    plt.plot(w, 20 * np.log10(abs(hq)), 'r')
    plt.ylabel('Amplitude int [dB]', color='r')
    plt.xlabel('Frequency [rad/sample]')
    ax2 = ax1.twinx()
    angles = np.unwrap(np.angle(h))
    angles_q = np.unwrap(np.angle(hq))
    plt.plot(w, angles, 'g')
    plt.ylabel('Angle (radians)', color='g')
    plt.plot(w, angles_q, 'y')
    plt.ylabel('Angle int (radians)', color='y')
    plt.grid()
    plt.axis('tight')
    plt.show()
    
    plt.show()