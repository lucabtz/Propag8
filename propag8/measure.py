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

import numbers

class Measure(object):
    def __init__(self, val, err):
        if err <= 0:
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
            return Measure(res, res * self.get_relative_error())
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
