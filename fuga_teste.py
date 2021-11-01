import fuga as fu
import matplotlib.pyplot as plt
import numpy as np

a = fu.pool(number=1000,fraction_of_parents=0.1,global_harmonic_threshold=[-14,14],local_harmonic_threshold=[-10.5,10.5],range_threshold=[0,28],variability_threshold=[0,45],variability_chords_per_bar_threshold=[0,1],num_bar_threshold=[1,16])
a.converge(plot="yes",iterations=50)