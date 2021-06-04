from tkinter import *
from tkinter import ttk
import numpy as np
import random
import time

#PSO

class Particle:
    pos = np.array([0,0]) #pozycja cząsteczki
    localBest = 0 #wartość lokalnego minimum
    localBest_pos = np.array([0,0]) #pozycja lokalnego minimum
    velocity = np.array([0,0]) #prędkość cząsteczki z poprzedniego kroku
    movement = np.array([0,0]) #prędkość cząsteczki
    funkcja = None #funkcja celu
    wagaVel = 0 #współczynnik bezwładności
    wagaLocal = 0 #współczynnik lokalny
    wagaGlobal = 0 #współczynnik stada
    globalBest_pos = np.array([0,0]) #pozycja globalnego minimum
    
    def __init__(self,funkcja,wagaVel,wagaLocal,wagaGlobal,posX,posY):
        self.pos = np.array([posX,posY])
        self.velocity = np.array([0,0])
        self.localBest = funkcja(self.pos[0],self.pos[1])
        self.localBest_pos = np.array([self.pos[0],self.pos[1]])
        self.movement = np.array([random.uniform(-2,2),random.uniform(-2,2)])
        self.funkcja = funkcja
        self.wagaVel = wagaVel
        self.wagaLocal = wagaLocal
        self.wagaGlobal = wagaGlobal

    def move(self,globalBestPos):
        self.globalBest_pos = globalBestPos #Pobieranie globalnego minimum
        self.velocity = self.movement #Zapisywanie ruchu z poprzedniej iteracji
        inertial = self.velocity*self.wagaVel
        self_confidence = self.wagaLocal * random.random() * (self.localBest_pos-self.pos)
        swarm_confidence = self.wagaGlobal * random.random() * (self.globalBest_pos-self.pos)
        self.movement = inertial + self_confidence + swarm_confidence #Obliczanie ruchu
        self.pos += self.movement #Aktualizacja pozycji
        self.pos = np.round(self.pos,decimals=5) #Zaokrąglenie
        if(self.funkcja(self.pos[0],self.pos[1])<self.localBest): #Sprawdzanie lokalnego minimum
            self.localBest = self.funkcja(self.pos[0],self.pos[1])
            self.localBest_pos = np.array([self.pos[0],self.pos[1]])

    def getLocalBest(self):
        return self.localBest

    def getLocalBestPos(self):
        return self.localBest_pos

def PSO(funk,ileCzastek,ileCycli,wagaVel,wagaLocal,wagaGlobal,zakresStart,zakresEnd):
    particles = []
    globalBest = 1000000
    globalBest_pos = np.array([0,0])
    funkcja = funk

    #Tworzenie cząsteczek
    for i in range(ileCzastek):
        particles.append(Particle(funkcja,wagaVel,wagaLocal,wagaGlobal,random.uniform(zakresStart,zakresEnd),random.uniform(zakresStart,zakresEnd)))

    #Wyszukiwanie początkowego minimum globalnego
    for i in particles:
        if i.getLocalBest() < globalBest:
            globalBest = i.getLocalBest()
            globalBest_pos = i.getLocalBestPos()

    #Cykle
    for j in range(ileCycli):
        for i in particles:
            i.move(globalBest_pos)
            if i.getLocalBest() < globalBest:
                globalBest = i.getLocalBest()
                globalBest_pos = i.getLocalBestPos()
        wypisz("Najlepsze minimum przejścia nr "+str(j+1)+": " + str(globalBest))

    wypisz("Globalne minimum: "+str(globalBest)+" na pozycji "+str(globalBest_pos)+"\n")

root = Tk()
root.title("Algorytm PSO - Mateusz Birkholz | Robert Chyrek")
root.configure(bg='#444444')
root.configure(padx=25, pady=25)
root.resizable(False,False)

#Inputs

scWlasne = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
scWlasne.grid(row=2,column=2,pady=15, padx=15)
scWlasne.insert(0,"0.5")

scLocal = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
scLocal.grid(row=3,column=2,pady=15, padx=15)
scLocal.insert(0,"0.8")

scGlobal = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
scGlobal.grid(row=4,column=2,pady=15, padx=15)
scGlobal.insert(0,"0.9")

zakStartEntry = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
zakStartEntry.grid(row=5,column=2,pady=15, padx=15)
zakStartEntry.insert(0,"-100")

zakEndEntry = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
zakEndEntry.grid(row=6,column=2,pady=15, padx=15)
zakEndEntry.insert(0,"100")

partEntry = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
partEntry.grid(row=7,column=2,pady=15, padx=15)
partEntry.insert(0,"30")

cycleEntry = Entry(root,fg='white',bg='#444444',width=30,font='Helvetica 15')
cycleEntry.grid(row=8,column=2,pady=15, padx=15)
cycleEntry.insert(0,"50")

options = [
    "Funkcja Beale'a",
    "Funkcja Himmelblau",
    "Funkcja Ackley'a N.2",
    "Funkcja Bartelsa",
    "sin(x)*sin(y)"
]

funkcjaDrop = ttk.Combobox(root,value=options)
funkcjaDrop.current(0)
funkcjaDrop.bind("<<ComboboxSelected>>")
funkcjaDrop.grid(row=9,column=2,pady=15, padx=15)

#Labels
lbWlasne = Label(text="Współczynnik bezwładności",fg='white',bg='#444444',font='Helvetica 15 bold')
lbWlasne.grid(row=2,column=1,pady=15, padx=15)

lbLocal = Label(text="Wpływ doświadczenia własnego",fg='white',bg='#444444',font='Helvetica 15 bold')
lbLocal.grid(row=3,column=1,pady=15, padx=15)

lbGlobal = Label(text="Wpływ stada",fg='white',bg='#444444',font='Helvetica 15 bold')
lbGlobal.grid(row=4,column=1,pady=15, padx=15)

zakStartLabel = Label(text="Początek zakresu",fg='white',bg='#444444',font='Helvetica 15 bold')
zakStartLabel.grid(row=5,column=1,pady=15, padx=15)

zakEndLabel = Label(text="Koniec zakresu",fg='white',bg='#444444',font='Helvetica 15 bold')
zakEndLabel.grid(row=6,column=1,pady=15, padx=15)

partLabel = Label(text="Ilość cząsteczek",fg='white',bg='#444444',font='Helvetica 15 bold')
partLabel.grid(row=7,column=1,pady=15, padx=15)

cycleLabel = Label(text="Ilość cykli",fg='white',bg='#444444',font='Helvetica 15 bold')
cycleLabel.grid(row=8,column=1,pady=15, padx=15)

funkcjaLabel = Label(text="Funkcja",fg='white',bg='#444444',font='Helvetica 15 bold')
funkcjaLabel.grid(row=9,column=1,pady=15, padx=15)

#Outputs
txInfo = Text(root,state=DISABLED, height=55)
txInfo.grid(row=2,rowspan=15,column=5)

def wypisz(text):
    txInfo.configure(state=NORMAL)
    txInfo.insert(index=INSERT ,chars=str(text)+"\n")
    txInfo.configure(state=DISABLED)
    return

def przygotujPSO():
    funk = lambda x,y: np.sin(x)*np.sin(y)
    try:
        if funkcjaDrop.get()=="Funkcja Beale'a":
            wypisz("Funkcja Beale'a  -  Oczekiwane minimum 0 w punkcie (3;0,5)")
            funk = lambda x,y: (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2
        elif funkcjaDrop.get()=="Funkcja Himmelblau":
            wypisz("Funkcja Himmelblau  -  Oczekiwane minimum 0")
            funk = lambda x,y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2
        elif funkcjaDrop.get()=="Funkcja Ackley'a N.2":
            wypisz("Funkcja Ackley'a N.2  -  Oczekiwane minimum -200 w punkcie (0;0)")
            funk = lambda x,y: -200*np.e**(-0.2*np.sqrt((x**2)+(y**2)))
        elif funkcjaDrop.get()=="Funkcja Bartelsa":
            wypisz("Funkcja Bartelsa  -  Oczekiwane minimum 1")
            funk = lambda x,y: np.abs((x**2)+(y**2)+(x*y)) + np.abs(np.sin(x)) + np.abs(np.cos(y))
        elif funkcjaDrop.get()=="sin(x)*sin(y)":
            wypisz("Funkcja sin(x)*sin(y)")
            funk = lambda x,y: np.sin(x)*np.sin(y)
        ileCz = int(partEntry.get())
        ileCy = int(cycleEntry.get())
        wagaVel = float(scWlasne.get())
        wagaLocal = float(scLocal.get())
        wagaGlobal = float(scGlobal.get())
        zakSt = float(zakStartEntry.get())
        zakEnd = float(zakEndEntry.get())
        PSO(funk,ileCz,ileCy,wagaVel,wagaLocal,wagaGlobal,zakSt,zakEnd)
    except Exception as e:
        wypisz("Błędne dane")
        wypisz(e)

#Buttons
btPSO = Button(root,command=przygotujPSO,text="PSO",fg='white',bg='#444444', width=50, height=3)
btPSO.grid(row=11,column=1,pady=15, padx=15, columnspan=4)

root.mainloop()
