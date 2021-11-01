"""
Transformar score de harmonia local em função que olha para os vizinhos simetricamente
Colocar números primos nos scores
Teremos um vetor de scores e um score global com thresholds para cada um deles
"""


import funcoes as f, random as r, warnings, matplotlib.pyplot as plt
from datetime import date
from midiutil import MIDIFile
from math import ceil

harmonic_reference = [[0,7,14],[3,4,10,11],[2,5,9,12],[1,6,8,13]]
modes_from_tonics = {"C":"maior","D":"dorico","E":"frigio","F":"lidio","G":"mixolidio","A":"menor"}
tonics_from_modes = {"maior":"C","menor":"A","jonio":"C","dorico":"D","frigio":"E","lidio":"F","mixolidio":"G","eolio":"A"}

def getchords(number_of_bars):
    chords = []
    for i in range(0,number_of_bars):  #####defining number of chords per bar. Maximum of two chords per bar
        num_chords = r.choices([1,2])[0]
        if num_chords == 1:
            chords.append(r.choices(list(range(-14,15)))[0])
        elif num_chords == 2:
            x = []
            for k in range(0,2):
                x.append(r.choices(list(range(-14,15)))[0])
            chords.append(x)
    
    return chords


class fuga:       ###############init function
    def __init__(self, chords=None, num_bar=None, num_voices=None, mode=None, tonic=None):  ##initializing fugue object

        self.chords=chords
        if self.chords==None:
            self.num_bar=num_bar
        else:
            self.num_bar=len(self.chords)
        self.num_voices=num_voices
        self.mode=mode
        self.tonic=tonic

        self.check_parameters()

        self.get_midi_tonic()

        self.get_midi_scale()

        self.score = self.getChordsharscore()

############################################### seeding functions

    def seed_chords(self):                      ####getting random chords
        self.chords = getchords(self.num_bar)
        
    def seed_num_bar(self):                     ####getting random number of bars 
        self.num_bar = r.choices([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])[0]   

    def seed_num_voices(self):                 #####getting random number of voices
        self.num_voices = r.choices(list(range(1,7)))[0]

    def seed_tonic_and_mode(self):                             ######getting random tonic
        self.tonic = r.choices(["C","D","E","F","G","A"])[0]
        self.mode = modes_from_tonics[self.tonic]

#####################################################checking parameters

    def check_parameters(self):

        if self.num_bar == None:           #########checking number of bars
            self.seed_num_bar()

        if self.num_voices == None:          #####checking voices parameter
            self.seed_num_voices()

        if self.chords == None:        ##########checking chords parameter
            self.seed_chords()

        if self.tonic == None and self.mode == None:           #####checking tonic and mode parameters
            self.seed_tonic_and_mode()
        elif self.tonic == None and self.mode != None:
            if self.mode in ["maior","menor","jonio","dorico","frigio","lidio","mixolidio","eolio"]:
                self.tonic = tonics_from_modes[self.mode]
            else:
                print("Invalid mode. Enter valid mode: ")
                self.mode = input("")
                self.check_parameters()
        elif self.tonic != None and self.mode == None:
            if self.tonic in ["C","D","E","F","G","A"]:
                self.tonic=self.tonic
            else:
                print("Invalid tonic. Enter valid tonic: ")
                while self.tonic not in ["C","D","E","F","G","A"]:
                    self.tonic = input("")
                    print("Invalid tonic. Enter valid tonic: ")
            self.mode = modes_from_tonics[self.tonic]
        elif self.mode != None and self.tonic != None:
            if self.tonic in ["C","D","E","F","G","A"]:
                if self.mode in ["maior","menor","jonio","dorico","frigio","lidio","mixolidio","eolio"]:
                    if self.tonic == tonics_from_modes[self.mode]:
                        pass
                    elif self.tonic != tonics_from_modes[self.mode]:
                        self.tonic = tonics_from_modes[self.mode]
                        print("Invalid tonic for this mode. Switching tonic to "+self.tonic)

######################################################## interpreting music numbers etc.

    def get_midi_tonic(self):
        if self.tonic not in ["A","G"]:
            self.midi_tonic=f.nota(self.tonic,5)
        elif self.tonic in ["A","G"]:
            self.midi_tonic=f.nota(self.tonic,4)

    def get_midi_scale(self):
        scale = []
        scale.append(self.midi_tonic)
        for i in range(1,len(f.dic_modos[self.mode])):
            scale.append(scale[i-1]+f.dic_modos[self.mode][i-1])
        self.midi_scale = scale

    def get_definitive_music(self):    ####returns a vector with midi numbers for each chord and a vector with the duration of
                                       ####each note
        defi =[[],[]]
        for i in self.chords:
            if type(i) == int:
                if i < len(self.midi_scale) and i >= 0:
                    defi[0].append(self.midi_scale[i])
                    defi[1].append(2)
                elif i >= len(self.midi_scale):
                    count = 0
                    while i >= len(self.midi_scale):
                        i = i-7
                        count = count+1
                    defi[0].append(self.midi_scale[i]+(count*12))
                    defi[1].append(2)
                elif i < 0:
                    count = 0
                    while i < 0:
                        i = i + 7
                        count = count+1
                    defi[0].append(self.midi_scale[i]-(count*12))
                    defi[1].append(2)
            elif type(i) == list:
                for k in i:
                    if k < len(self.midi_scale) and k >= 0:
                        defi[0].append(self.midi_scale[k])
                        defi[1].append(2)
                    elif k >= len(self.midi_scale):
                        count = 0
                        while k >= len(self.midi_scale):
                            k = k - 7
                            count = count + 1
                        defi[0].append(self.midi_scale[k]+(count*12))
                        defi[1].append(1)
                    elif k < 0:
                        count = 0
                        while k < 0:
                            k = k + 7
                            count = count+1
                        print("#########K: "+str(k))
                        print("midi scale: "+str(self.midi_scale))
                        print("mode: "+str(self.mode))
                        defi[0].append(self.midi_scale[k]-(count*12))
                        defi[1].append(1)
        
        return(defi)

 ########################################### writing file

    def write_file(self,filename=None):
        if filename==None:
            filename="Fugue_in_"+str(self.tonic)+"_"+str(self.mode)+str(date.today())
        track    = 0
        channel  = 0
        time     = 0    # In beats
        duration = 1    # In beats
        tempo    = 60   # In BPM
        volume   = 100  # 0-127, as per the MIDI standard

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
        MyMIDI.addTempo(track, time, tempo)

        MyMIDI.addTempo(track, time, tempo)

        definitive_music = self.get_definitive_music()
        time_count=0

#        for i, pitch in enumerate(degrees):
#            MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)
        
        for i in range(0,len(definitive_music[0])):
            MyMIDI.addNote(track, channel, definitive_music[0][i], time + time_count, definitive_music[1][i], volume)
            time_count = time_count + definitive_music[1][i]
            


        with open(filename+".mid", "wb") as output_file:
            MyMIDI.writeFile(output_file)
        
        arq = open(filename+".txt","w+")
        arq.write("Acordes: " + str(self.chords) + "\n")
        arq.write("Modo: " + str(self.mode) + "\n")
        arq.write("Tonic: " + str(self.tonic) + "\n")
        arq.write("Defi[0]: " + str(definitive_music[0])+"\n")
        arq.write("Defi[1]: " + str(definitive_music[1])+"\n")
        arq.write("Global Harmonic Score: " + str(self.score["Global harmonic score"])+"\n")
        arq.close()


################################# getting musical scores

    def getNumChordsPerBarScore(self,chords):
        if len(chords)==1:
            return(0)
        else:
            one=0
            two=0
            for i in chords:
                if type(i)==int or type(i)==float:
                    one+=1
                elif type(i)==list:
                    two+=1
            return(abs(one-two))

    def getChordslocalharscore(self,chords):
        score = 0
        for i in range(0,len(chords)-1):
            diff = chords[i+1]-chords[i]
            while diff<0:
                diff = diff+7
            if diff in harmonic_reference[0]:
                score = score + 7
            elif diff in harmonic_reference[1]:
                score = score + 3
            elif diff in harmonic_reference[2]:
                score = score - 3
            elif diff in harmonic_reference[3]:
                score = score - 7

        return(score)

    def getChordsglobalharscore(self,chords):
        score = 0
        for i in chords:
            while i < 0:
                i = i+7
            if i in harmonic_reference[0]:
                score = score + 7
            elif i in harmonic_reference[1]:
                score = score + 3
            elif i in harmonic_reference[2]:
                score = score - 3
            elif i in harmonic_reference[3]:
                score = score - 7
        
        return(score)

    def getRangescore(self,chords):
        return(max(chords)-min(chords))

    def getVariabilityscore(self,chords):
        score=0
        for i in range(0,len(chords)-1):
            for k in range(i,len(chords)-1):
                score=score+abs(chords[i]-chords[k])*(1/(k-i+1))
        return(score)

    def getChordsharscore(self):
        linear_chords = []
        for i in (self.chords):
            if type(i)==int:
                linear_chords.append(i)
            elif type(i)==list:
                for k in i:
                    linear_chords.append(k)
        
        global_fugue_score = self.getChordsglobalharscore(linear_chords)
        local_fugue_score = self.getChordslocalharscore(linear_chords)
        range_score = self.getRangescore(linear_chords)
        var_score = self.getVariabilityscore(linear_chords)
        number_of_chords_per_bar=self.getNumChordsPerBarScore(self.chords)
        return({"Global harmonic score":global_fugue_score/self.num_bar,"Local harmonic score":local_fugue_score/self.num_bar, "Range score":range_score, "Variability score":var_score/self.num_bar,"Variability in number of chords per bar":number_of_chords_per_bar/self.num_bar, "Number of bars":self.num_bar})

class pool:   ##########class responsible for generating, breeding, analyzing and mutating fugues
    
    def __init__(self,number=100,fugues=None,fraction_of_parents=0.1,global_harmonic_threshold=[6,10],local_harmonic_threshold=[6,10],range_threshold=[6,7],variability_threshold=[25,35],variability_chords_per_bar_threshold=[6,7],num_bar_threshold=[4,5]):
        self.number=number
        self.fraction_of_parents=fraction_of_parents
        self.global_harmonic_threshold=global_harmonic_threshold
        self.local_harmonic_threshold=local_harmonic_threshold
        self.range_threshold=range_threshold
        self.variability_threshold=variability_threshold
        self.variability_chords_per_bar_threshold=variability_chords_per_bar_threshold
        self.num_bar_threshold=num_bar_threshold
        self.parents=None
        self.offspring=None
        
        if fugues == None:
            fugues = []
            for i in range(0,number):
                fugues.append(self.generate_seed())
            self.fugues=fugues

        elif fugues != None and type(fugues) == list:
            if len(fugues) == number:
                self.fugues = fugues
            else:
                x = len(fugues)
                for i in range(x,number):
                    fugues.append(self.generate_seed())
                self.fugues = fugues

    def generate_seed(self):
        return fuga()

    def define_parents(self):
        parents=self.sort_by_score()
        self.parents=[]
        for i in range(0,int(len(parents)*self.fraction_of_parents)):
            self.parents.append(parents[i][0])
        return(self.parents)

    def get_distance_from_reference(self,fugue):
        vec = []
        reference = [((self.global_harmonic_threshold[0]+self.global_harmonic_threshold[1])/2),((self.local_harmonic_threshold[0]+self.local_harmonic_threshold[1])/2),((self.range_threshold[0]+self.range_threshold[1])/2),((self.variability_threshold[0]+self.variability_threshold[1])/2),((self.variability_chords_per_bar_threshold[0]+self.variability_chords_per_bar_threshold[1])/2),((self.num_bar_threshold[0]+self.num_bar_threshold[1])/2)]
        point_in_score_space=list(fugue.score.values())
        distance=0
        for k in range(0,len(point_in_score_space)):
            distance=distance+(point_in_score_space[k]-reference[k])**2
        return distance**(1/2)
        
    def sort_by_score(self):
        vec = []
        for i in self.fugues:
            vec.append([i,self.get_distance_from_reference(i)])
        return(self.quick_sort_score(vec))
    
    def quick_sort_score(self,vector):
        less=[]
        equal=[]
        greater=[]

        if len(vector)>1:
            pivot = vector[0]
            for x in vector:
                if x[1] < pivot[1]:
                    less.append(x)
                elif x[1] == pivot[1]:
                    equal.append(x)
                elif x[1] > pivot[1]:
                    greater.append(x)
            return(self.quick_sort_score(less)+equal+self.quick_sort_score(greater))
        else:
            return(vector)
    
    def get_average_population_score(self,score_type):
        val = 0
        for i in self.fugues:
            val=val+i.score[score_type]
        return val/len(self.fugues)

    def get_distance_from_reference(self,fugue):
        ref_global = (self.global_harmonic_threshold[0]+self.global_harmonic_threshold[1])/2
        ref_local = (self.local_harmonic_threshold[0]+self.local_harmonic_threshold[1])/2
        ref_range = (self.range_threshold[0]+self.range_threshold[1])/2
        ref_variability = (self.variability_threshold[0]+self.variability_threshold[1])/2
        ref_variability_chords_per_bar = (self.variability_chords_per_bar_threshold[0]+self.variability_chords_per_bar_threshold[1])/2
        ref_num_bar = (self.num_bar_threshold[0]+self.num_bar_threshold[1])/2
        reference=[ref_global,ref_local,ref_range,ref_variability,ref_variability_chords_per_bar,ref_num_bar]
        distance=0
        point_in_score_space=list(fugue.score.values())
        for i in range(0,len(point_in_score_space)):
            distance=distance+(point_in_score_space[i]-reference[i])**2
        return distance**(1/2)
        
    def get_average_population_distance_from_reference(self):
        val=0
        for i in range(0,len(self.fugues)):
            val=val+self.get_distance_from_reference(self.fugues[i])
        return val/len(self.fugues)


    def get_average_parents_score(self,score_type):
        if self.parents==None:
            warnings.warn("Parents have not been defined!")
        else:
            val = 0
            for i in self.parents:
                val = val+i.score[score_type]
            return val/len(self.parents)

    def breed(self,random_comparison_percentage=0.1):
        def return_smaller_list(list1,list2):
            if len(list1)<=len(list2):
                return list1
            else:
                return list2

        def return_bigger_list(list1,list2):
            if len(list1)>len(list2):
                return list1
            else:
                return list2

        def repeated_index(li,element):
            aux_list=[]
            indexes=[]
            for i in li:
                aux_list.append(i)
            counter = 0
            while True:
                try:
                    indexes.append(aux_list.index(element)+counter)
                    aux_list.pop(aux_list.index(element))
                    counter=counter+1
                except:
                    if counter == 0:
                        return False
                    else:
                        return indexes
            return False

        def cyclic_list(li,index1,index2):
            if index2<=len(li):
                return li[index1:index2]
            else:
                return li[index1:]+li[:index2%len(li)]

        def is_subsequence(small_list,big_list):
            indexes = repeated_index(big_list,small_list[0])
            if indexes == False:
                return [False]
            for i in indexes:
                if small_list==cyclic_list(big_list,i,i+len(small_list)):
                    return [small_list,i,i+len(small_list)]
            return [False]

        def get_bigger_subsequence(x,y):
            small = return_smaller_list(x,y)
            big = return_bigger_list(x,y)
            memory=[]
            for i in range(0,len(small)-2):
                eval = is_subsequence(small[i:len(small)],big)
                if eval[0]!=False:
                    memory.append(eval+[i,len(small)])
                eval = is_subsequence(small[0:len(small)-i],big)
                if eval[0]!=False:
                    memory.append(eval+[0,len(small)-i])
            diffs=[]
            if len(memory)>0:
                for i in memory:
                    diffs.append(len(i[0]))
                return memory[diffs.index(max(diffs))]

            return None
        offspring = []
        for i in self.parents:
            if random_comparison_percentage<=1:
                breeding_candidates = r.sample(self.parents,k=ceil(random_comparison_percentage*len(self.parents)))
                for k in breeding_candidates:
                    if k.chords!=i.chords:
                        small = return_smaller_list(k.chords,i.chords)
                        big = return_bigger_list(k.chords,i.chords)
                        eval = get_bigger_subsequence(small,big)
                        if eval != None:
                            offspring.append(fuga(chords=small[:eval[-1]]+big[eval[-3]:]))
                            offspring.append(fuga(chords=big[:eval[-4]]+small[eval[-2]:]))
                        else:
                            divise = r.choices(list(range(0,len(small))))[0]
                            offspring.append(fuga(chords=big[0:divise]+small[divise:len(small)]))
                            offspring.append(fuga(chords=small[0:divise]+big[divise:len(big)]))
        self.offspring=offspring

    def mutate(self,fraction_of_parents_mutation=0.01,fraction_of_offspring_mutation=0.01):
        def insert_random_chord(fugue):
            new_chords=fugue.chords
            new_chords.insert(r.choices(list(range(0,len(fugue.chords))))[0],r.choices(list(range(-14,15)))[0])
            return fuga(chords=new_chords)
        def remove_random_chord(fugue):
            new_chords = fugue.chords
            new_chords.pop(r.choices(list(range(0,len(new_chords))))[0])
            return fuga(chords=new_chords)
        def change_random_chord(fugue):
            new_chords=fugue.chords
            new_chords[r.choices(list(range(0,len(new_chords))))[0]]=r.choices(list(range(-14,15)))[0]
            return fuga(chords=new_chords)
        if self.offspring!=None:
            indexes = r.choices(list(range(0,len(self.offspring))),k=ceil(fraction_of_offspring_mutation*len(self.offspring)))
            for i in indexes:
                if len(self.offspring[i].chords)<16 and len(self.offspring[i].chords)>1:
                    self.offspring[i]=r.choices([insert_random_chord(self.offspring[i]),remove_random_chord(self.offspring[i]),change_random_chord(self.offspring[i])])[0]
                elif len(self.offspring[i].chords)==16:
                    self.offspring[i]=r.choices([remove_random_chord(self.offspring[i]),change_random_chord(self.offspring[i])])[0]
                elif len(self.offspring[i].chords)==1:
                    self.offspring[i]=r.choices([insert_random_chord(self.offspring[i]),change_random_chord(self.offspring[i])])[0]
        if self.parents!=None:
            indexes = r.choices(list(range(0,len(self.parents))),k=ceil(fraction_of_parents_mutation*len(self.parents)))
            for i in indexes:
                if len(self.parents[i].chords)<16 and len(self.parents[i].chords)>1:
                    self.parents[i]=r.choices([insert_random_chord(self.parents[i]),remove_random_chord(self.parents[i]),change_random_chord(self.parents[i])])[0]
                elif len(self.parents[i].chords)==16:
                    self.parents[i]=r.choices([remove_random_chord(self.parents[i]),change_random_chord(self.parents[i])])[0]
                elif len(self.parents[i].chords)==1:
                    self.parents[i]=r.choices([insert_random_chord(self.parents[i]),change_random_chord(self.parents[i])])[0]

    def call_Darwin(self):
        ref_global = (self.global_harmonic_threshold[0]+self.global_harmonic_threshold[1])/2
        ref_local = (self.local_harmonic_threshold[0]+self.local_harmonic_threshold[1])/2
        ref_range = (self.range_threshold[0]+self.range_threshold[1])/2
        ref_variability = (self.variability_threshold[0]+self.variability_threshold[1])/2
        ref_variability_chords_per_bar = (self.variability_chords_per_bar_threshold[0]+self.variability_chords_per_bar_threshold[1])/2
        ref_num_bar = (self.num_bar_threshold[0]+self.num_bar_threshold[1])/2
        reference=[ref_global,ref_local,ref_range,ref_variability,ref_variability_chords_per_bar,ref_num_bar]
        vec = []
        death_pool=self.parents+self.offspring+self.fugues
        for i in death_pool:
            point_in_score_space=list(i.score.values())
            distance=0
            for k in range(0,len(point_in_score_space)):
                distance=distance+(point_in_score_space[k]-reference[k])**2
            distance=distance**(1/2)
            vec.append([i,distance])
        survivors=self.quick_sort_score(vec)
        for i in range(0,len(self.fugues)):
            self.fugues[i]=survivors[i][0]
        self.offspring=None
        self.parents=None
    
    def converge(self,plot="no",iterations=100):
        if plot=="yes":
            average_distance=[]
            iteration_number=[]
            counter=0
        average=0.1
        average_vec=[]
        recent_average=self.get_average_population_distance_from_reference()
        converge_var=0
        while converge_var==0 and counter<iterations:
            previous_average=recent_average
            print("Generation "+str(counter))
            self.define_parents()
            print("Defining parents...")
            self.breed(random_comparison_percentage=average**2)
            print("Breeding...")
            self.mutate(fraction_of_offspring_mutation=average,fraction_of_parents_mutation=average)
            print("Mutating...")
            self.call_Darwin()
            print("Calling Darwin...")
            recent_average=self.get_average_population_distance_from_reference()
            average = recent_average/previous_average
            counter=counter+1
            average_vec.append(average)
            if len(average_vec)>3:
                if average_vec[-1]>0.95 and average_vec[-2]>0.95 and average_vec[-3]>0.95:
                    converge_var=1
            if average>1:
                average=0
            if plot=="yes":
                average_distance.append(recent_average)
                iteration_number.append(counter)
        
        if plot=="yes":
            fig = plt.figure()
            plt.plot(iteration_number,average_distance,label="average distance")
            plt.plot(iteration_number,average_vec,label="mutation factor")
            fig.suptitle('Convergence')
            plt.xlabel('Generation')
            plt.ylabel('Distance from reference')
            plt.show()
