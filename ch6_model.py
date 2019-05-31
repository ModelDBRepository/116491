from itertools import chain
from neuron import h
Section = h.Section

# --------------------- Model specification ---------------------

# topology
soma = Section()                    #       create soma, apical, basilar, axon
apical = Section()
basilar = Section()
axon = Section()

apical.connect(soma, 1, 0)          #       connect apical(0), soma(1)
basilar.connect(soma, 0, 0)         #       connect basilar(0), soma(0)
axon.connect(soma, 0, 0)            #       connect axon(0), soma(0)

# geometry
                                    #       soma {
soma.L = 30                         #           L = 30
soma.nseg = 1                       #           nseg = 1
soma.diam = 30                      #           diam = 30
                                    #       }
                                    #       apical {
apical.L = 600                      #           L = 600
apical.nseg = 23                    #           nseg = 23
apical.diam = 1                     #           diam = 1
                                    #       }
                                    #       basilar {
basilar.L = 200                     #           L = 200
basilar.nseg = 5                    #           nseg = 5
basilar.diam = 2                    #           diam = 2
                                    #       }
                                    #       axon {
axon.L = 1000                       #           L = 1000
axon.nseg = 37                      #           nseg = 37
axon.diam = 1                       #           diam = 1
                                    #       }

# biophysics
for sec in h.allsec():              #       forall {
    sec.Ra = 100                    #           Ra = 100
    sec.cm = 1                      #           cm = 1
                                    #       }
        
soma.insert('hh')                   #       soma {
                                    #           insert hh
                                    #       }
apical.insert('pas')                #       apical {
                                    #           insert pas
basilar.insert('pas')               #           g_pas = 0.0002
                                    #           e_pas = -65
for seg in chain(apical, basilar):  #       }
    seg.pas.g = 0.0002              #       basilar {
    seg.pas.e = -65                 #           insert pas
                                    #           g_pas = 0.0002
                                    #           e_pas = -65
                                    #       }
axon.insert('hh')                   #       axon {
                                    #           insert hh
                                    #       }

# --------------------- Instrumentation ---------------------

# synaptic input                    #       objref syn
syn = h.AlphaSynapse(0.5, sec=soma) #       soma syn = new AlphaSynapse(0.5)
syn.onset = 0.5                     #       syn.onset = 0.5
syn.gmax = 0.05                     #       syn.gmax = 0.05
syn.e = 0                           #       syn.e = 0

                                    #       objref g
g = h.Graph()                       #       g = new Graph()
g.size(0, 5, -80, 40)               #       g.size(0, 5, -80, 40)
g.addvar('v(0.5)', sec=soma)        #       g.addvar("soma.v(0.5)")

# --------------------- Simulation control ---------------------

h.dt = 0.025                        #       dt = 0.025
tstop = 5                           #       tstop = 5
v_init = -65                        #       v_init = -65

def initialize():                   #       proc initialize() {
    h.finitialize(v_init)           #           finitialize(v_init)
    h.fcurrent()                    #           fcurrent()
                                    #       }

def integrate():                    #       proc integrate() {
    g.begin()                       #       g.begin()
    while h.t < tstop:              #       while (t < tstop) {
        h.fadvance()                #           fadvance()
        g.plot(h.t)                 #           g.plot(t)
                                    #       }
    g.flush()                       #       g.flush()
    
def go():                           #       proc go() {
    initialize()                    #           initialize()
    integrate()                     #           integrate()
                                    #       }
                                         
go()                                #       go()

