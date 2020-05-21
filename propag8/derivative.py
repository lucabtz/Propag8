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

EPSILON = 1e-10

def differenciate_one_par_function(func, x):
    return (func(x + EPSILON) - func(x - EPSILON))/(2*EPSILON)

def differenciate_func_wrt_par(func, x, par):
    low_value = list(x)
    low_value[par] -= EPSILON
    high_value = list(x)
    high_value[par] += EPSILON
    return (func(*tuple(high_value)) - func(*tuple(low_value)))/(2*EPSILON)

def calculate_gradient(func, x, num_args):
    ret = [differenciate_func_wrt_par(func, x, i) for i in range(0, num_args)]
    return tuple(ret)
