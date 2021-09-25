import fuga as fu

po = fu.pool(number=1000,global_harmonic_score_threshold=[-14,-14])

a=po.define_parents(0.1)
a[0].write_file()



#globalhar=0
#localhar=0
#rang=0
#variability=0
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

