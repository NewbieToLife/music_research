import fuga as fu
import matplotlib.pyplot as plt
import numpy as np

a = fu.pool(number=1000,fraction_of_parents=0.1,global_harmonic_threshold=[-14,14],local_harmonic_threshold=[-10.5,10.5],range_threshold=[0,28],variability_threshold=[0,45],variability_chords_per_bar_threshold=[0,1],num_bar_threshold=[1,16])
average_distance=[]
iteration_number=[]
counter=0
for i in range(0,100):
    #print("Generation "+str(i))
    a.define_parents()
    #print("Defining parents...")
    a.breed(random_comparison_percentage=0.1)
    #print("Breeding...")
    a.mutate(fraction_of_offspring_mutation=0.5,fraction_of_parents_mutation=0.5)
    #print("Throwing x-rays...")
    a.call_Darwin()
    #print("Calling Darwin...")
    average_distance.append(a.get_average_population_distance_from_reference())
    iteration_number.append(counter)
    counter=counter+1

fig = plt.figure()
plt.plot(iteration_number,average_distance)
fig.suptitle('Convergence')
plt.xlabel('Generation')
plt.ylabel('Distance from reference')
plt.show()
# fugas=[]
# for i in range(0,10000):
#     fugas.append(fu.fuga().score["Number of bars"])
# print(max(fugas))
# print(min(fugas))