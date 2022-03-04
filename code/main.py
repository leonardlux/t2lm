
import matplotlib.pyplot as plt 
import numpy as np

from dataClass import Messung
from analyse import gaussAnpassung

base = ".."

probenDirekt = ["Co60", "Cs137w", "Eu152", "Na22",]
dateinamenNah = [base + "/data/direkt/Nah_{0}.Tka".format(x) for x in probenDirekt] 
dateinamenBackgroundNah = [base + "/data/direkt/Nah_Rausch.Tka"] 

winkelZyklisch = ["10","20","30","40"]
dateinamenZirkular = [base + "/data/zyklisch/{0}grad.TKA".format(x) for x in winkelZyklisch]
dateinamenBackgroundZirkular = [base + "/data/zyklisch/{0}gradHIntergrund.TKA".format(x) for x in winkelZyklisch]

messungenZyklisch = []
intervallPeakArray = [[],[],[],[]]
for i in range(len(winkelZyklisch)):    
    messungenZyklisch.append(Messung(dateinamenZirkular[i], dateinamenBackgroundZirkular[i],"zirkular","Cs173s"))
    #gaussAnpassung(messungenZyklisch[3].messreihe, )

    #messungenZyklisch[i].plotData("Zirkular: " + winkelZyklisch[i] ,"zirkular"+ winkelZyklisch[i]+ "Gradd")

if False:
    fig = plt.figure(figsize=(20,10))
    plt.title("Übersicht zyklisch")
    for i in [3]:#range(len(winkelZyklisch)):
        plt.plot(messungenZyklisch[i].messreihe,label= winkelZyklisch[i] + "°")
    plt.legend()
    plt.vlines([340,440],0,1)
    plt.vlines([385],0,1, color="red")
    #plt.show()
    plt.savefig(base + "/plots/messungenZyklisch")

breite = [40]
for x in breite:
    gaussAnpassung(messungenZyklisch[3].messreihe, [385-x,385+x])


messungenDirekt = []
for i in range(len(probenDirekt)):
    messungenDirekt.append(Messung(dateinamenNah[i], dateinamenBackgroundNah[0],"Nah_direkt",probenDirekt[i]))
    #messungenDirekt[i].plotData("Nah & Direkt: "+ probenDirekt[i],"nah_dirket_"+ probenDirekt[i])
