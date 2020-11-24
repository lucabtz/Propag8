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

import math
import numbers
import statistics

class Measure(object):
    def __init__(self, val, err):
        if err < 0:
            raise ValueError('Uncertainty cannot be negative')
        self.val = val
        self.err = err

    def get_relative_error(self):
        return self.err / self.val

    def __add__(self, other):
        if isinstance(other, Measure):
            return Measure(self.val + other.val, self.err + other.err)
        elif isinstance(other, numbers.Real):
            return Mesaure(self.val + other, self.err)
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __sub__(self, other):
        if isinstance(other, Measure):
            return Measure(self.val - other.val, self.err + other.err)
        elif isinstance(other, numbers.Real):
            return Measure(self.val - other, self.err)
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __mul__(self, other):
        if isinstance(other, Measure):
            res = self.val * other.val
            return Measure(res, res * (self.get_relative_error() + other.get_relative_error()))
        elif isinstance(other, numbers.Real):
            res = self.val * other
            return Measure(res, other * self.err)
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __rmul__(self, value):
        return Measure(self.val * value, self.err * value)

    def __neg__(self):
        return Measure(-self.val, self.err)

    def __truediv__(self, other):
        if isinstance(other, Measure):
            res = self.val / other.val
            return Measure(res, res * (self.get_relative_error() + other.get_relative_error()))
        elif isinstance(other, numbers.Real):
            res = self.val / other
            return Measure(res, res * self.get_relative_error())

    def __rtruediv__(self, value):
        res = value / self.val
        return Measure(res, res * self.get_relative_error())

    def __pow__(self, pow):
        return Measure(self.val ** pow, abs(pow * (self.val ** (pow - 1))) * self.err)

    def __abs__(self):
        return Measure(abs(self.val), self.err)

    def __lt__(self, other):
        if isinstance(other, Measure):
            return self.val < other.val
        elif isinstance(other, numbers.Real):
            return self.val < other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __le__(self, other):
        if isinstance(other, Measure):
            return self.val <= other.val
        elif isinstance(other, numbers.Real):
            return self.val <= other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __gt__(self, other):
        if isinstance(other, Measure):
            return self.val > other.val
        elif isinstance(other, numbers.Real):
            return self.val > other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __ge__(self, other):
        if isinstance(other, Measure):
            return self.val >= other.val
        elif isinstance(other, numbers.Real):
            return self.val >= other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __str__(self):
        return f'({self.val} +/- {self.err})'


class StatisticalMeasure(object):
    def __init__(self, val, variance):
        if variance < 0:
            raise ValueError('Variance cannot be negative')
        self.val = val
        self.variance = variance

    def get_standard_deviation(self):
        return math.sqrt(self.variance)

    def to_measure(self, coverage_factor):
        return Mesaure(self.val, coverage_factor * self.get_standard_deviation())

    @staticmethod
    def from_sample(sample):
        mean = statistics.fmean(sample)
        variance = statistics.variance(sample)
        mean_variance = variance / len(sample)
        return StatisticalMeasure(mean, mean_variance)

    def __add__(self, other):
        if isinstance(other, StatisticalMeasure):
            return StatisticalMeasure(self.val + other.val, self.variance + other.variance)
        elif isinstance(other, numbers.Real):
            return Mesaure(self.val + other, self.variance)
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __sub__(self, other):
        if isinstance(other, StatisticalMeasure):
            return Measure(self.val - other.val, self.variance + other.variance)
        elif isinstance(other, numbers.Real):
            return Measure(self.val - other, self.variance)
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __mul__(self, other):
        if isinstance(other, StatisticalMeasure):
            res = self.val * other.val
            variance = self.val * self.val * other.variance + other.val * other.val * self.variance
            return StatisticalMeasure(res, variance)
        elif isinstance(other, numbers.Real):
            res = self.val * other
            variance = other * other * self.variance
            return StatisticalMeasure(res, variance)
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __rmul__(self, value):
        res = self.val * value
        variance = value * value * self.variance
        return StatisticalMeasure(res, variance)

    def __neg__(self):
        return Measure(-self.val, self.variance)

    def __truediv__(self, other):
        if isinstance(other, StatisticalMeasure):
            inv_other = 1 / other.val
            inv_self = 1 / self.val
            derivative = other.val * inv_self * inv_self
            res = self.val * inv_other
            variance = inv_other * inv_other * self.variance + derivative * derivative * other.variance
            return StatisticalMeasure(res, variance)
        elif isinstance(other, numbers.Real):
            inv_other = 1 / other
            res = self.val * inv_other
            variance = inv_other * inv_other * self.variance
            return StatisticalMeasure(res, variance)

    def __rtruediv__(self, value):
        inv_value = 1 / value
        res = self.val * inv_value
        variance = inv_value * inv_value * self.variance
        return StatisticalMeasure(res, variance)

    def __pow__(self, pow):
        res = self.val ** pow
        derivative = abs(pow * (self.val ** (pow - 1)))
        variance = derivative * derivative * self.variance
        return StatisticalMeasure(res, variance)

    def __lt__(self, other):
        if isinstance(other, StatisticalMeasure):
            return self.val < other.val
        elif isinstance(other, numbers.Real):
            return self.val < other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __le__(self, other):
        if isinstance(other, StatisticalMeasure):
            return self.val <= other.val
        elif isinstance(other, numbers.Real):
            return self.val <= other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __gt__(self, other):
        if isinstance(other, StatisticalMeasure):
            return self.val > other.val
        elif isinstance(other, numbers.Real):
            return self.val > other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __ge__(self, other):
        if isinstance(other, StatisticalMeasure):
            return self.val >= other.val
        elif isinstance(other, numbers.Real):
            return self.val >= other
        raise TypeError(f'Unsupported operand type {type(other)}')

    def __str__(self):
        return f'(µ={self.val}, σ²={self.variance})'
