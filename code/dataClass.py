from tokenize import String
from turtle import color
import numpy as np
import matplotlib.pyplot as plt 


class Messung:
    def __init__(self, dateiname, dateinameBackground, messtyp, probename=None):
        self.messtyp = messtyp
        
        #Raw Data 
        datei = open(dateiname, "r")
        lines = []
        for line in datei:
            lines.append(int(line.replace("\n","")))
        
        self.liveTime = lines[0]    #live Time in der ersten Zeile 
        self.realTime = lines[1]    #real Time in der zweiten Zeile 

        self.messreiheRaw = lines[2:]  #Bins der Channel in den restlichen Zeilen
        
        #Hintergrund
        datei = open(dateinameBackground, "r")
        lines = []
        for line in datei:
            lines.append(int(line.replace("\n","")))
        
        self.liveTimeBackground = lines[0]    #live Time in der ersten Zeile 
        self.realTimeBackground = lines[1]    #real Time in der zweiten Zeile 

        self.messreiheBackground = lines[2:]  #Bins der Channel in den restlichen Zeilen

        #Corrected and normed
        self.messreihe = np.array(self.messreiheRaw)/self.liveTime - np.array(self.messreiheBackground)/self.liveTimeBackground

        #print( messtyp +" " + str(probename) + " " + str(self.liveTime) +" " +  str(self.realTime))
        if probename!=None:
            self.Probe = Probe(probename)
        
    def plotData(self,title,filename):
        plt.figure(figsize=(20,10))
        plt.title(title)
        plt.ylabel("Häufigkeit (normiert aufs maximum)")
        plt.xlabel("Channels")
        plt.plot(np.array(self.messreiheRaw)/max(self.messreiheRaw), color="green")
        plt.plot(np.array(self.messreiheBackground)/max(self.messreiheBackground), color="yellow")
        plt.plot(np.array(self.messreihe)/max(self.messreihe),color="black")
        plt.savefig("../plots/"+ filename)


class Probe:
    def __init__(self, probename):
        name = probename
        if name == "Na22":
            a0 = 37 *10**3 #Bq 
            time = 6567 *24*60*60 #alter der probe seit a0 (Quelle: https://www.topster.de/kalender/tagerechner.php?styp=datum&stag=10&smonat=03&sjahr=2004&etag=&emonat=&ejahr=&typ=heute&subDazu=%2B&dazu=0)
            
            peaks_engery = [511, 1274.5]     #(only gamma)
            peaks_intensity = [179.8, 99.94]

            t2 = 950.5 *24*60*60 # Halbwertszeit
            t2e = 0.4 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = a0 * np.exp(-np.log(2) * t2)
            ae = a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif name =="Co60":
            a0 = 37 *10**3 #Bq
            time = 6897 *24*60*60

            peaks_engery = [1173.2, 1332.5]     #(only gamma)
            peaks_intensity = [99.85, 99.9826]

            t2 = 1925.3 *24*60*60 # Halbwertszeit
            t2e = 0.4 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = a0 * np.exp(-np.log(2) * t2)
            ae = a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e 
        elif name =="Cs137s": #starkes Cäsium (die neuere)
            a0 = 24.8 *10**6 #Bq
            time = 4901 *24*60*60

            peaks_engery = [661.66]     #(only gamma)
            peaks_intensity = [85.00]

            t2 = 11000 *24*60*60 # Halbwertszeit
            t2e = 90 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = a0 * np.exp(-np.log(2) * t2)
            ae = a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif name =="Cs137w": #weak (schwaches) Cäsium
            a0 = 24.8 *10**6 #Bq
            time = 6567 *24*60*60

            peaks_engery = [661.66]     #(only gamma)
            peaks_intensity = [85.00]

            t2 = 11000 *24*60*60 # Halbwertszeit
            t2e = 90 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = a0 * np.exp(-np.log(2) * t2)
            ae = a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif name =="Eu152": 
            a0 = 37 *10**3 #Bq
            time = 6567 *24*60*60

            peaks_engery = [121.78, 344.28, 778.9, 964.08, 1085.9, 1112.1, 1408.0]     #(only gamma)
            peaks_intensity = [28.58, 26.5, 12.94, 14.60, 10.21, 13.64, 21.00]

            t2 = 4943 *24*60*60 # Halbwertszeit
            t2e = 5 *24*60*60 # Unsicherheit auf die halbwertszeit
            
            a = a0 * np.exp(-np.log(2) * t2)
            ae = a0 *np.log(2) * np.exp(-np.log(2)* t2) * t2e
        elif name =="Rausch":
            pass



   