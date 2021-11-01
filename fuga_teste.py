import fuga as fu
import matplotlib.pyplot as plt
import numpy as np

a = fu.pool(number=1000,fraction_of_parents=0.1,global_harmonic_reference=0,local_harmonic_reference=0,range_reference=14,variability_reference=22.5,variability_chords_per_bar_reference=0.5,num_bar_reference=7.5)
a.converge(plot="yes",iterations=50)