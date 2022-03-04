from tokenize import String
from turtle import color
import numpy as np
import matplotlib.pyplot as plt 


class Messung:
    def __init__(self, dateiname, dateinameBackground, messtyp, messparameter, Probe=False):
        self.typ = messtyp
        self.parameter = messparameter
        #Raw Data 
        with open(dateiname,"r") as datei: 
            tmp = np.array(list(map(int , datei.read().split("\n")[:-1]))) #we need to remove the last part of the list because it ist equal to ""
            self.liveTime, self.realTime = tmp[:2]  #live Time in der ersten Zeile 
            self.messreiheRaw = tmp[2:]
            self.messreiheRawError = np.sqrt(self.messreiheRaw)

        #Background
        with open(dateinameBackground,"r") as datei: 
            tmp = np.array(list(map(int , datei.read().split("\n")[:-1]))) #we need to remove the last part of the list because it ist equal to ""
            self.liveTimeBackground, self.liveTimeBackground = tmp[:2]  #live Time in der ersten Zeile 
            self.messreiheBackground = tmp[2:]
            self.messreiheBackgroundError = np.sqrt(self.messreiheBackground)
        

        #   Fehler fortpflanzung
        #Corrected (messreihe sind ereignisse pro zeit)
        self.messreihe = self.messreiheRaw/self.liveTime - self.messreiheBackground/self.liveTimeBackground
        self.messreiheError = np.sqrt((self.messreiheRawError/self.liveTime)**2 + (self.messreiheBackgroundError/self.liveTimeBackground)**2)
        
        #normieren 
        self.messreihe = self.messreihe /max(self.messreihe)
        self.messreiheError = self.messreiheError/ max(self.messreihe)

        #print( messtyp +" " + str(probename) + " " + str(self.liveTime) +" " +  str(self.realTime))
        if Probe:
            self.Probe = Probe
        
    def plotData(self,title,filename):
        fig1 = plt.figure(figsize=(20,10))
        plt.title(title + "(Rohdaten)")
        plt.ylabel("Häufigkeit pro Zeit")
        plt.xlabel("Channels")
        plt.plot(np.arange(len(self.messreihe)),self.messreiheRaw/self.liveTime, label="Rohdaten Messung")
        plt.plot(np.arange(len(self.messreihe)),self.messreiheBackground/self.liveTimeBackground, label="Hintergrund")
        plt.legend()
        #plt.show()
        plt.savefig("../plots/"+ filename+"Raw")

        fig2 = plt.figure(figsize=(20,10))
        plt.title(title + "(Background korriegiert und normiert)")
        plt.ylabel("normierte Häufigkeit pro Zeit")
        plt.xlabel("Channels")
        plt.plot(np.arange(len(self.messreihe)),np.array(self.messreihe),label="relative Häufigkeit der Messdaten-Background")
        plt.legend()
        plt.savefig("../plots/"+ filename+"Corrected")
        plt.close("all")




class Probe:
    def __init__(self, probename):
        self.name = probename
        if self.name == "Na22":
            self.a0 = 37 *10**3 #Bq 
            self.time= 6567 *24*60*60 #alter der probe seit self.a0 (Quelle: https://www.topster.de/kalender/tagerechner.php?styp=datum&stag=10&smonat=03&sjahr=2004&etag=&emonat=&ejahr=&typ=heute&subDazu=%2B&dazu=0)
            
            self.peakEnergy = [511, 1274.5]     #(only gamma) first one is for calculation of m_e
            self.peaksIntensity = [179.8, 99.94]

            t2 = 950.5 *24*60*60 # Halbwertszeit
            t2e = 0.4 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = self.a0 * np.exp(-np.log(2) * t2)
            ae = self.a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif self.name =="Co60":
            self.a0 = 37 *10**3 #Bq
            self.time= 6897 *24*60*60

            self.peakEnergy = [1173.2, 1332.5]     #(only gamma)
            self.peaksIntensity = [99.85, 99.9826]

            t2 = 1925.3 *24*60*60 # Halbwertszeit
            t2e = 0.4 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = self.a0 * np.exp(-np.log(2) * t2)
            ae = self.a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e 
        elif self.name =="Cs137s": #starkes Cäsium (die neuere)
            self.a0 = 24.8 *10**6 #Bq
            self.time= 4901 *24*60*60

            self.peakEnergy = [661.66]     #(only gamma)
            self.peaksIntensity = [85.00]

            t2 = 11000 *24*60*60 # Halbwertszeit
            t2e = 90 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = self.a0 * np.exp(-np.log(2) * t2)
            ae = self.a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif self.name =="Cs137w": #weak (schwaches) Cäsium
            self.a0 = 24.8 *10**6 #Bq
            self.time= 6567 *24*60*60

            self.peakEnergy = [661.66]     #(only gamma)
            self.peaksIntensity = [85.00]

            t2 = 11000 *24*60*60 # Halbwertszeit
            t2e = 90 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = self.a0 * np.exp(-np.log(2) * t2)
            ae = self.a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif self.name =="Eu152": 
            self.a0 = 37 *10**3 #Bq
            self.time= 6567 *24*60*60

            self.peakEnergy = [121.78, 344.28, 778.9, 964.08, 1085.9, 1112.1, 1408.0]     #(only gamma)
            self.peaksIntensity = [28.58, 26.5, 12.94, 14.60, 10.21, 13.64, 21.00]

            t2 = 4943 *24*60*60 # Halbwertszeit
            t2e = 5 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = self.a0 * np.exp(-np.log(2) * t2)
            ae = self.a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif self.name =="Rausch":
            pass



   