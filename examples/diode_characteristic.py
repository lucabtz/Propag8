"""
    Data analysis of a diode characteristic curve from values obtained in the lab
"""

import sys
sys.path.insert(0, '.')

from propag8.measure import Measure, StatisticalMeasure
from propag8.numpy import (
    print_array,
    unpack_value_error
)
from propag8.math import log, exp

import numpy as np
import matplotlib.pyplot as plt

vi_measures_data = [
  #(div * volt/div, milliamps)
  [1   , 0.050, 0.02],
  [1.4 , 0.050, 0.03],
  [1.8 , 0.050, 0.04],
  [2.2 , 0.050, 0.05],
  [2.4 , 0.050, 0.06],
  [2.6 , 0.050, 0.07],
  [2.8 , 0.050, 0.08],
  [3   , 0.050, 0.10],
  [3.2 , 0.050, 0.12],
  [3.4 , 0.050, 0.14],
  [3.6 , 0.050, 0.16],
  [3.8 , 0.050, 0.19],
  [4   , 0.050, 0.22],
  [4.2 , 0.050, 0.27],
  [4.4 , 0.050, 0.31],
  [4.6 , 0.050, 0.38],
  [4.8 , 0.050, 0.44],
  [5   , 0.050, 0.52],
  [5.2 , 0.050, 0.61],
  [5.4 , 0.050, 0.71],
  [5.6 , 0.050, 0.85],
  [5.8 , 0.050, 0.98],
  [6   , 0.050, 1.12],
  [6.2 , 0.050, 1.33],
  [6.4 , 0.050, 1.53],
  [6.6 , 0.050, 1.76],
  [6.8 , 0.050, 2.03]
]

def data_to_measure(measure_data):
    # compute the volt value and its error
    volts = measure_data[0] * measure_data[1]
    volts_err = 0.2 * measure_data[1]
    volts = StatisticalMeasure.from_mean_and_deviation(volts, volts_err).with_added_deviation(0.03 * volts)
    current = measure_data[2]
    return [volts.to_measure(1), Measure.from_relative_error(current, 0.015, digits=2)]

vi_measures = np.array([data_to_measure(data) for data in vi_measures_data])

print('Measures are:')
print_array(vi_measures)
V = vi_measures[:, 0]
I = vi_measures[:, 1]

logI = log(I)
print_array(logI)

I, _ = unpack_value_error(I)
V, Verr = unpack_value_error(V)
logI, _ = unpack_value_error(logI)
coeffs = np.polyfit(logI, V, 1, w=Verr)

etaVt = coeffs[0]
lnI0 = - coeffs[1] / etaVt
print(f'EtaVt: {etaVt} V, lnI0: {lnI0}')

fit_function = lambda x: exp(x / etaVt + lnI0)

plt.figure()
plt.errorbar(V, I, xerr=Verr, linestyle='None', fmt='x', label='Dati sperimentali')
plt.plot(V, fit_function(V), label='Fit lineare')
plt.legend()
plt.xlabel('Tensione (V)')
plt.ylabel('Corrente (mA)')
plt.yscale('log')
plt.grid()
plt.show()
