from cmath import phase
from math import isclose
import numpy as np
import matplotlib.pyplot as plt

class signal_to_tf():
    def __init__(self, step, Z_cord):
        
        # creating array with step 
        self.step = step
        self.steps = np.array([self.step*i for i in range(len(Z_cord))])
        self.Z_cord = Z_cord
        
    def DFT_method(self):
        # calcualte DFT 
        DFT = np.fft.fft(self.Z_cord)
        len_DFT = len(DFT)
        freq = np.fft.fftfreq(len_DFT, d=self.step)
        phases = np.angle(DFT)

        # amplitude
        ampli = 2 * np.abs(DFT) / len_DFT

        # filtre negative frequnce
        positive_index = np.where(freq >= 0)
        positive_freq = freq[positive_index]
        positive_ampli = ampli[positive_index]
        positive_phase = phases[positive_index]

        return positive_ampli, positive_freq, positive_phase 

    # find domein component 
    def dominant_components(self, ampli, freq, phase, number = 5):
        top_indices = np.argsort(ampli)[-int(number):]
        top_ampli = ampli[top_indices]
        top_freq = freq[top_indices]
        top_phase = phase[top_indices]

        # empty list 
        value_array = np.zeros((len(top_ampli), len(self.Z_cord)))
        for idx, (a, f, p) in enumerate(zip(top_ampli, top_freq, top_phase)):
            if f == 0:
                value_array[idx] = 0
            else:
                value_array[idx] = a * np.cos(2 * np.pi * f * self.steps + p)

        value_array_sum = np.sum(value_array, axis=0)

        return value_array, value_array_sum
