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

from .decor import override_math_function
from .measure import Measure

import math

class QuadraticSolution(object):
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def get_greater_solution(self):
        return self.x1 if self.x1 >= self.x2 else self.x2

    def get_least_solution(self):
        return self.x2 if self.x1 >= self.x2 else self.x2

@override_math_function(math.sqrt)
def sqrt(x):
    return x ** (0.5)

def solve_quadratic(a, b, c):
    delta = b**2 - 4*a*c
    if delta < 0:
        raise ValueError(f'Equation delta is negative: no solution to {a}x^2 + {b}x + {c} = 0')
    x1 = (b**2 + sqrt(delta)) / (2*a)
    x2 = (b**2 - sqrt(delta)) / (2*a)
    return QuadraticSolution(x1, x2)

@override_math_function(math.exp)
def exp(x):
    return Measure(math.exp(x.val), (math.exp(x.val)) * x.err)

@override_math_function(math.cos)
def cos(x):
    return Measure(math.cos(x.val), abs(math.sin(x.val)) * x.err)

@override_math_function(math.sin)
def sin(x):
    return Measure(math.sin(x.val), abs(math.cos(x.val)) * x.err)

@override_math_function(math.tan)
def tan(x):
    return Measure(math.tan(x.val), (1 / (math.cos(x.val) ** 2)) * x.err)

@override_math_function(math.acos)
def acos(x):
    return Measure(math.acos(x.val), (1 / math.sqrt(1 - x.val * x.val)) * x.err)

@override_math_function(math.asin)
def asin(x):
    return Measure(math.asin(x.val), (1 / math.sqrt(1 - x.val * x.val)) * x.err)

@override_math_function(math.atan)
def atan(x):
    return Measure(math.atan(x.val), (1/(1 + x.val * x.val)) * x.err)

@override_math_function(math.cosh)
def cosh(x):
    return Measure(math.cosh(x.val), abs(math.sinh(x.val)) * x.err)

@override_math_function(math.sinh)
def sinh(x):
    return Measure(math.sinh(x.val), abs(math.cosh(x.val)) * x.err)

@override_math_function(math.acosh)
def acosh(x):
    return Measure(math.acosh(x.val), ((1/math.sqrt(x.val - 1)) * (1/math.sqrt(x.val + 1))) * x.err)

@override_math_function(math.asinh)
def asinh(x):
    return Measure(math.asinh(x.val), (1/math.sqrt(1 + x.val * x.val)) * x.err)

@override_math_function(math.atanh)
def atanh(x):
    return Measure(math.atanh(x.val), abs(1/(1 - x.val * x.val)) * x.err)

@override_math_function(math.log)
def log(x):
    return Measure(math.log(x.val), abs(1/x.val) * x.err)

@override_math_function(math.fabs)
def fabs(x):
    return abs(x)
