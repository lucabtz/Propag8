'''
 *   Propag8
 *   Copyright (C) 2019 Luca "ekardnam" Bertozzi <luca.bertozzi11@studio.unibo.it>
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from .measure import Measure, StatisticalMeasure
from .derivative import calculate_gradient

import numpy as np

def override_math_function(func):
    def decorator(wrapped):
        def wrapper(x):
            if isinstance(x, Measure):
                value, derivative = wrapped(x)
                return Measure(value, abs(derivative) * x.err)
            elif isinstance(x, StatisticalMeasure):
                value, derivative = wrapped(x)
                return StatisticalMeasure(value, derivative * derivative * x.variance)
            return func(x)
        return np.vectorize(wrapper)
    return decorator

def propagate_with_partial(num_args):
    def decorator(func):
        def wrapper(*args):
            if all([isinstance(arg, Measure) for arg in args]):
                vals = tuple([args[i].val for i in range(0, num_args)])
                partials = calculate_gradient(func, vals, num_args)
                err = 0
                for i in range(0, num_args):
                    err += (abs(partials[i]) * args[i].err)
                return Measure(func(*vals), err)
            elif all([isinstance(arg, StatisticalMeasure) for arg in args]):
                vals = tuple([args[i].val for i in range(0, num_args)])
                partials = calculate_gradient(func, vals, num_args)
                variance = 0
                for i in range(0, num_args):
                    variance += (partials[i] * partials[i] * args[i].variance)
                return Measure(func(*vals), variance)
            else:
                return func(*args)
        return wrapper
    return decorator
