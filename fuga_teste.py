import fuga as fu

a = fu.pool(number=1000)
v=a.define_parents(0.2)

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

