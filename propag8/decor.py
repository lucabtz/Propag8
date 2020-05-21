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

from .measure import Measure
from .derivative import calculate_gradient

def override_math_function(func):
    def decorator(wrapped):
        def wrapper(x):
            if isinstance(x, Measure):
                return wrapped(x)
            return func(x)
        return wrapper
    return decorator

def propagate_with_partial(num_args):
    def decorator(func):
        def wrapper(*args):
            vals = tuple([args[i].val for i in range(0, num_args)])
            partials = calculate_gradient(func, vals, num_args)
            err = 0
            for i in range(0, num_args):
                err += (abs(partials[i]) * args[i].err)
            return Measure(func(*vals), err)
        return wrapper
    return decorator
