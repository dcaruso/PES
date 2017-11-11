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
    parser.add_argument("-q", "--quantity", type=int, default=20, help="Quantity of coefficient")
    parser.add_argument("-f1", "--fcutoff1", type=float, default=0.1, help="Frequency cut off 1")

def quantize (bits, array):
    q = []
    qf = []
    for i in range (len(array)):
        q.append(int(array[i]*(2**(bits-1))/np.amax(array)))
        qf.append((q[i]*1.0)/(2**(bits-1)))
    return q, qf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Filter Generator")
    configure_parser(parser)
    args = parser.parse_args()

    
    b = sig.firwin(args.quantity, args.fcutoff1)
    qb, qf = quantize(args.bits,b)

    coef_values_str = ','.join(str(x) for x in qb)
    print(coef_values_str)

    with open(args.input, 'r') as f:
        file_content = f.read()

    file_content = file_content.format(coef_qty=args.quantity, coef_values=coef_values_str, coef_bits=args.bits, coef_max=(2**(args.bits-1)), coef_min=(-2**(args.bits-1)))

    with open(args.output, 'w') as f:
        f.write(file_content)

    print('Created file %s' % args.output)

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