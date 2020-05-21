# Propag8

Make uncertainty propagation no longer a hassle.

# Why?

Come on you don't really want to propagate all those uncertainties yourself.

# How

Using propag8 is easy and should integrate with your already existing code.
Let's say you have measure a volatage of (4.5 +/- 0.1)V and a current of (0.012 +/- 0.001)A and want to calculate the resistance.

```python
from propag8.measure import Measure
 
voltage = Measure(4.5, 0.1)
current = Measure(0.012, 0.001)
print(voltage / current) # prints (375.0 +/- 39.583333333333336)

```

If you already have some function that calculates stuff you should be able to pass `Measure`s in place of foats. Many functions defined in python's `math` are defined in `propag8.math` to work with `Measure`s.

