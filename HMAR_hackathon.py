# Steve Essinger
# HMAR Project
# 3/29-3/30/14

import numpy as np

class Node():
    def __init__(self,parent=None,neigh=None,data=None,prob=None):
        self.parent = parent
        self.neigh = neigh
        self.data = data
        self.prob = prob

    def getSeq(self):
        if self.prob.any():
            self.data = np.random.choice(np.arange(len(self.prob)),p=self.prob)
        else:
            return
            
    def computeProb(self,prior,number,lookup):
        if self.parent:
            trans = np.zeros(self.parent.prob.shape)
            x = lookup[:,0:3]==lookup[self.parent.data,number]
            ind = np.arange(len(lookup))[x[:,0] & x[:,1]]
            trans[ind] = 5
            if self.neigh:
                x = trans + prior
            else:
                x = trans + prior
        elif self.neigh:
            #x = prior
            x = self.neigh.prob
        else:
            x = prior
        self.prob = x/sum(x)

def generateSeq(Order,Size):
    Alphabet = range(Size)
    base = len(Alphabet)
    length = np.power(base,Order)
    lookup =  np.zeros((length,Order))
    for vari in range(Order):
        for gen in range(base):
            for i in range(gen * np.power(base,vari), length, np.power(base,vari+1)):
                span = np.power(base,vari) + i
                lookup[i:span,vari] = gen
  
    for ind,item in enumerate(lookup):
        lookup[ind] = item[::-1]
    return lookup

def find(LOOKUP,chords):
    ind = 0
    X = LOOKUP.items()
    while True:
        if X[ind][1] == chords:
            return ind
        else:
            ind += 1


if __name__ == "__main__":
    Duration = 8 # Length of Song = # Measures * Order
    Order = 4 # Order of the model

    # Create Lookup Table of All Note Combinations (12 Notes, Choose 4)
    lookup = generateSeq(Order,12)

    # Map Index to Musical Note
    Map = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']

    p = np.zeros(len(lookup)) + 0.5
    # Manually Entry of Priors
    #p[[0,13104,9360,9425,12900,6660,13195,17290]] = 0.5
    prior = np.array(p)/sum(p)

    Measure, Bar, Sixteen  = [], [], []    
    # Build Graph Structure
    for i in range(Duration/Order):
        # Measure Nodes
        if i == 0:
            S = Node()
        else:    
            S = Node(neigh=S)
        S.computeProb(prior,i,lookup)
        S.getSeq()
        Measure.append(S.data)
        for j in range(Order):
            # Bar Nodes
            if j == 0 :
                N = Node()
            else:
                N = Node(neigh=N)
            N.computeProb(prior,j,lookup)
            N.getSeq()
            Bar.append(N.data)    
            for k in range(Order):
                # Sixteenth Note Nodes
                if k == 0:
                    M = Node(parent=N)
                else:
                    M = Node(parent=N,neigh=M)
                M.computeProb(prior,k,lookup)
                M.getSeq()
                Sixteen.append(M.data)

    # Bass Note Mappings - Structure Nodes
    TNum,Top,Bass = [], [], []
    for ind in range(len(Measure)):
        for item in lookup[Measure[ind]]:
            TNum.append(int(item))
            Top.append(Map[int(item)])
            Bass.append((str.lower(Map[int(item)]),1))            
    print 'Top: %s \n' % Top
    Bass = tuple(Bass)

    # Trebel Note Mappings - Bar Nodes
    MNum, Middle, Trebel = [], [], []
    for ind in range(len(Bar)):
        for item in lookup[Bar[ind]]:
            MNum.append(int(item))
            Middle.append(Map[int(item)])
            Trebel.append((str.lower(Map[int(item)]),4))            
    print 'Middle: %s \n' % Middle
    Trebel = tuple(Trebel)

    # Melody Note Mappings - Sixteenth Note Nodes
    BNum, Bottom, Melody = [], [], []
    for ind in range(len(Sixteen)):
        for item in lookup[Sixteen[ind]]:
            BNum.append(int(item))
            Bottom.append(Map[int(item)])
            Melody.append((str.lower(Map[int(item)]),16))            
    print 'Bottom: %s \n' % Bottom
    Melody = tuple(Melody)

 
'''
# Lookup Table Mapping Numbers to Notes
    LOOKUP = {}
    for i in range(len(lookup)):
        for j in range(len(lookup[i,:])):
            if i in LOOKUP.keys():
                LOOKUP[i].append(Map[int(lookup[i,j])])
            else:
                LOOKUP[i] = [Map[int(lookup[i,j])]]
                
'''

# Generate Audio Files using pysynth
from pysynth import *

print
print "Creating Song... "
print

# SONG 
# Trebel
make_wav(Trebel, bpm = 120, transpose = -2, pause = .1, boost = 2, fn = "trebel.wav")
# Bass
make_wav(Bass, bpm = 120, transpose = -1, pause = .1, boost = 0.5, fn = "bass.wav")
# Melody
make_wav(Melody, bpm = 120, transpose = 1, pause = .01, boost = 1, fn = "melody.wav")
# Mix Trebel and Melody files together
mix_files("trebel.wav", "melody.wav", "song.wav")
