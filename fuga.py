"""
Transformar score de harmonia local em função que olha para os vizinhos simetricamente
Colocar números primos nos scores
Teremos um vetor de scores e um score global com thresholds para cada um deles
"""


import funcoes as f
import random as r
from datetime import date
from midiutil import MIDIFile

harmonic_reference = [[0,7,14],[3,4,10,11],[2,5,9,12],[1,6,8,13]]
modes_from_tonics = {"C":"maior","D":"dorico","E":"frigio","F":"lidio","G":"mixolidio","A":"menor"}
tonics_from_modes = {"maior":"C","menor":"A","jonio":"C","dorico":"D","frigio":"E","lidio":"F","mixolidio":"G","eolio":"A"}

def getchords(number_of_bars):
    chords = []
    for i in range(0,number_of_bars):  #####defining number of chords per bar. Maximum of two chords per bar
        num_chords = r.choices([1,2])[0]
        if num_chords == 1:
            chords.append(r.choices([0]+list(range(-14,15)))[0])
        elif num_chords == 2:
            x = []
            for k in range(0,2):
                x.append(r.choices([0]+list(range([-14,15]))])[0])
            chords.append(x)
    
    return chords


class fuga:       ###############init function
    def __init__(self, chords=None, num_bar=None, num_voices=None, mode=None, tonic=None):  ##initializing fugue object

        self.chords=chords
        self.num_bar=num_bar
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
        return({"Global harmonic score":global_fugue_score/self.num_bar,"Local harmonic score":local_fugue_score/self.num_bar, "Range score":range_score/self.num_bar, "Variability score":var_score/self.num_bar})
            

class pool:   ##########class responsible for generating, breeding, analyzing and mutating fugues
    
    def __init__(self,number=100,fugues=None,global_harmonic_score_threshold=[-7,6]):
        self.number=number
        self.global_harmonic_score_threshold=global_harmonic_score_threshold

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
        a = fuga()
        return(a)

    def define_parents(self,percentage_of_parents):
        scores=[]
        scores_diffs=[]
        parents=[]
        average=(self.global_harmonic_score_threshold[0]+self.global_harmonic_score_threshold[1])/2
        for i in self.fugues:
            scores.append(i)
            scores_diffs.append(abs(i.getChordsharscore()["Global harmonic score"]-average))
        while len(parents)<percentage_of_parents*self.number:
            parents.append(scores[scores_diffs.index(min(scores_diffs))])
            popit=scores_diffs.index(min(scores_diffs))
            scores.pop(popit)
            scores_diffs.pop(popit)

        return(parents)