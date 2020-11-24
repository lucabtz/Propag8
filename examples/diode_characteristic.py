"""
    Data analysis of a diode characteristic curve from values obtained in the lab
"""

import sys
sys.path.insert(0, '.')

from propag8.measure import Measure, StatisticalMeasure
from propag8.numpy import print_array, to_measure, unpack_into_values_errors_array
from propag8.math import log

import numpy as np
import matplotlib.pyplot as plt

vi_measures_data = [
  #(div, volt/div, milliamps)
  [4  , 0.100, 0.02],
  [4.2, 0.100, 0.03],
  [4.6, 0.100, 0.04],
  [4.8, 0.100, 0.06],
  [5  , 0.100, 0.08],
  [5.2, 0.100, 0.10],
  [5.4, 0.100, 0.15],
  [5.6, 0.100, 0.21],
  [5.8, 0.100, 0.30],
  [6  , 0.100, 0.44],
  [6.2, 0.100, 0.60],
  [6.4, 0.100, 0.91],
  [6.6, 0.100, 1.35],
  [6.8, 0.100, 1.92]
]

def data_to_measure(measure_data):
    # compute the volt value and its error
    volts = measure_data[0] * measure_data[1]
    volts_err = 0.2 * measure_data[1]
    volts = StatisticalMeasure.from_mean_and_deviation(volts, volts_err).with_added_deviation(0.03 * volts)
    current = measure_data[2]
    return [volts.to_measure(1), Measure(current, 0)] # the current error is negligible

vi_measures = np.array([data_to_measure(data) for data in vi_measures_data])

print('Measures are:')
print_array(vi_measures)
V = vi_measures[:, 0]
I = vi_measures[:, 1]

logI = log(I)
print_array(logI)
V, Verr = unpack_into_values_errors_array(V)
logI, _ = unpack_into_values_errors_array(logI)
coeffs = np.polyfit(V, logI, 1)
fit_function = lambda x: coeffs[0] * x + coeffs[1]

plt.errorbar(V, logI, xerr=Verr, linestyle='None', fmt='o')
plt.plot(V, fit_function(V))
plt.show()
