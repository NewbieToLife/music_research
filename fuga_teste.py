import fuga as fu

a = fu.pool()
a.define_parents(fraction_of_parents=0.8,global_harmonic_threshold=[6,7],local_harmonic_threshold=[6,7],range_threshold=[6,7],variability_threshold=[6,7],variability_chords_per_bar_threshold=[6,7])
print(a.parents)
print(len(a.parents))


#for i in range(0,len(a.fugues)):
#    c=a.fugues[i].getChordsharscore()
#    globalhar=globalhar+c["Global harmonic score"]
#    localhar=localhar+c["Local harmonic score"]
#    rang=rang+c["Range score"]
#    variability=variability+c["Variability score"]

#print(i)
#print("Global Har: "+str(globalhar/i))
#print("Local var: "+str(localhar/i))
#print("Range: "+str(rang/i))
#print("Variability: "+str(variability/i))

