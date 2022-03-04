
import matplotlib.pyplot as plt 
import numpy as np

from dataClass import Messung, Probe
from analyse import gaussAnpassung, linAnpassung

base = ".."

# DATEN

Co60 = Probe("Co60")
Cs137w = Probe("Cs137w")
Eu152 = Probe("Eu152")
Na22 = Probe("Na22")

Cs137s = Probe("Cs137s")



#Daten direkt
probenDirekt = [Co60, Cs137w, Eu152, Na22,]
dateinamenNah = [base + "/data/direkt/Nah_{0}.Tka".format(x.name) for x in probenDirekt] 
dateinamenBackgroundNah = [base + "/data/direkt/Nah_Rausch.Tka"] 


#Daten zyklisch
winkelZyklisch = ["10","20","30","40"]
dateinamenZirkular = [base + "/data/zyklisch/{0}grad.TKA".format(x) for x in winkelZyklisch]
dateinamenBackgroundZirkular = [base + "/data/zyklisch/{0}gradHIntergrund.TKA".format(x) for x in winkelZyklisch]



# AUSWERTUNG

#Auswertung Direkt

messungenDirekt = []
intervallPeakArrayDirekt = [[[830,880],[930,980]],[[450,550]],[],[[850,950]]]
peakEnergy = [[1173.2, 1332.5], [661.66],[None],[1274.5]] # wir lassen einen natrium peak weg, da diese später zur bestimmung genutzt wird
peakEnergy = [Co60.peakEnergy, Cs137w.peakEnergy, Eu152.peakEnergy, Na22.peakEnergy]

figEnergyChannel, axs = plt.subplots(2,1,figsize=(20,10))
for i in range(len(probenDirekt)):
    # einlesen und definieren der Messreihen mit Korrektur Offset
    messungenDirekt.append(Messung(dateinamenNah[i], dateinamenBackgroundNah[0],"Nah_direkt",probenDirekt[i].name ,probenDirekt[i]))
    
    messungenDirekt[i].anpassungen = []
    for j,intervall in enumerate(intervallPeakArrayDirekt[i]):
        messungenDirekt[i].anpassungen.append(gaussAnpassung(messungenDirekt[i],intervall, True, "Peak"+str(j+1)))

    plt.close("all")
    
    # plotten aller Daten
    #messungenDirekt[i].plotData("Nah & Direkt: "+ probenDirekt[i].name,"nah_dirket_"+ probenDirekt[i].name)

#Lineare Regression aus den bekannten Energie werten der Peaks und der Channel zahl
#Energy = x * Channel
energyData  = [1173.2, 1332.5, 661.66, 1274.5]
print(len(messungenDirekt))
channelData = [
                messungenDirekt[0].anpassungen[0].output.beta[0],
                messungenDirekt[0].anpassungen[1].output.beta[0],
                messungenDirekt[1].anpassungen[0].output.beta[0],
                messungenDirekt[3].anpassungen[0].output.beta[0],
                ]
linAnpassung(energyData, channelData, None, None, True)





#Auswertung Zyklisch
messungenZyklisch = []
intervallPeakArray = [[435, 545], [405, 515], [370, 480], [330, 435]]
if False:    
    for i in range(len(winkelZyklisch)):    
        #einlesen und definieren der Messreihen mit Korrektur Offset
        messungenZyklisch.append(Messung(dateinamenZirkular[i], dateinamenBackgroundZirkular[i],"zirkular", winkelZyklisch[i],"Cs173s"))
        
        #Gauss Anpassung an die Peaks 
        messungenZyklisch[i].analyse = gaussAnpassung(messungenZyklisch[i], intervallPeakArray[i], True )
        #messungZyklisch[i].analyse.output.beta[x] speichert die ergebnisse (x=0 Mittelwert, x=1, Breite)

        #Plotten aller Rohdaten
        #messungenZyklisch[i].plotData("Zirkular: " + winkelZyklisch[i] ,"zirkular"+ winkelZyklisch[i]+ "Gradd")

    #Plots der Messreihen
    if False:
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



