import numpy as np
from scipy.signal import lfilter, firwin
from pylab import *
from scipy.fftpack import fft,fftshift
import scipy.signal as signal
from tool._fixedInt import *

sample_rate = 48000.

#------------------------------------------------
# Create a FIR filter and apply it to signal.
#------------------------------------------------
# The Nyquist rate of the signal.
nyq_rate = sample_rate / 2.
 
# The cutoff frequency of the filter: 6KHz
cutoff_hz = 8000.0
 
# Length of the filter (number of coefficients, i.e. the filter order + 1)
numtaps = 15
 
# Use firwin to create a lowpass FIR filter
fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)

taps= len(fir_coeff)

coeff = arrayFixedInt(8,6,fir_coeff)

hex_coeff = [a.__hex__() for a in coeff]

def hex_coeff_to_verilog(hex_coeff):
    for i,c in enumerate(hex_coeff):
        pattern = f'assign coeff[{i}] = 8h{c[2:]};'
        print(pattern)

hex_coeff_to_verilog(hex_coeff)