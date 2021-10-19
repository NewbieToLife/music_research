import fuga as fu

a = fu.pool()
a.define_parents(fraction_of_parents=1,global_harmonic_threshold=[6,10],local_harmonic_threshold=[6,10],range_threshold=[6,7],variability_threshold=[25,35],variability_chords_per_bar_threshold=[6,7])
print(a.parents)
#print(len(a.parents))
print(a.parents[3].chords)
w=a.breed_from_globalharscore(a.parents)
print(w[3].chords)
#print(len(w))

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

