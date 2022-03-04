
import matplotlib.pyplot as plt 
import numpy as np

from dataClass import Messung
from analyse import gaussAnpassung

base = ".."

# DATEN

#Daten direkt
probenDirekt = ["Co60", "Cs137w", "Eu152", "Na22",]
dateinamenNah = [base + "/data/direkt/Nah_{0}.Tka".format(x) for x in probenDirekt] 
dateinamenBackgroundNah = [base + "/data/direkt/Nah_Rausch.Tka"] 

#Daten zyklisch
winkelZyklisch = ["10","20","30","40"]
dateinamenZirkular = [base + "/data/zyklisch/{0}grad.TKA".format(x) for x in winkelZyklisch]
dateinamenBackgroundZirkular = [base + "/data/zyklisch/{0}gradHIntergrund.TKA".format(x) for x in winkelZyklisch]



# AUSWERTUNG

#Auswertung Zyklisch
messungenZyklisch = []
intervallPeakArray = [[435, 545], [405, 515], [370, 480], [330, 435]]
for i in range(len(winkelZyklisch)):    
    #einlesen und definieren der Messreihen mit Korrektur Offset
    messungenZyklisch.append(Messung(dateinamenZirkular[i], dateinamenBackgroundZirkular[i],"zirkular", winkelZyklisch[i],"Cs173s"))
    
    #Gauss Anpassung an die Peaks
    messungenZyklisch[i].analyse = gaussAnpassung(messungenZyklisch[i], intervallPeakArray[i], True )

    #Plotten aller Rohdaten
    #messungenZyklisch[i].plotData("Zirkular: " + winkelZyklisch[i] ,"zirkular"+ winkelZyklisch[i]+ "Gradd")

#Plots der Messreihen
if True:
    for i in range(len(winkelZyklisch)):
        plt.figure(figsize=(20,10))
        plt.title("Übersicht zyklisch")
        plt.grid()
        plt.errorbar(
            np.arange(len(messungenZyklisch[i].messreihe)),
            messungenZyklisch[i].messreihe,
            label= winkelZyklisch[i] + "°")
        plt.vlines(intervallPeakArray[i],0,1)
        plt.legend()
        plt.legend()
        plt.vlines(messungenZyklisch[i].analyse.output.beta[0],0,1, color="red")
        plt.savefig(base + "/plots/messungenZyklisch"+winkelZyklisch[i]+"Grad" )

# breite = [40]
# for x in breite:
#     gaussAnpassung(messungenZyklisch[3].messreihe, [385-x,385+x])



#Auswertung Direkt

messungenDirekt = []
for i in range(len(probenDirekt)):
    # einlesen und definieren der Messreihen mit Korrektur Offset
    messungenDirekt.append(Messung(dateinamenNah[i], dateinamenBackgroundNah[0],"Nah_direkt",probenDirekt[i] ,probenDirekt[i]))
    
    # plotten aller Daten
    #messungenDirekt[i].plotData("Nah & Direkt: "+ probenDirekt[i],"nah_dirket_"+ probenDirekt[i])
