
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





#Daten zyklisch
winkelZyklisch = ["10","20","30","40","50"]
dateinamenZirkular = [base + "/data/zyklisch/{0}grad.TKA".format(x) for x in winkelZyklisch]
dateinamenBackgroundZirkular = [base + "/data/zyklisch/{0}gradHintergrund.TKA".format(x) for x in winkelZyklisch]


#Daten konventionell
winkelKonventionell = ["50","65","80","105","135"]
dateinamenKonventionellAl = [base + "/data/konventionell/{0}grad_Alu.TKA".format(x) for x in winkelKonventionell]
dateinamenKonventionellFe = [base + "/data/konventionell/{0}grad_Eisen.TKA".format(x) for x in winkelKonventionell]
dateinamenBackgroundKonventionell = [base + "/data/konventionell/{0}gradHintergrund.TKA".format(x) for x in winkelKonventionell]


# AUSWERTUNG

#Auswertung Direkt
#Daten direkt
probenDirekt = [Co60, Cs137w, Eu152, Na22,]
dateinamenNah = [base + "/data/direkt/Nah_{0}.Tka".format(x.name) for x in probenDirekt] 
dateinamenBackgroundNah = [base + "/data/direkt/Nah_Rausch.Tka"] 

dateinamenFern = [base + "/data/direkt/Fern_{0}.Tka".format(x.name) for x in probenDirekt]
dateinamenBackgroundFern = [base + "/data/direkt/Fern_Rausch.Tka"] 

dateinamenDirekt = dateinamenNah + dateinamenFern
dateinamenBackgroundDirekt = dateinamenBackgroundNah + dateinamenBackgroundFern
messtypDirekt = ["direkt_Nah", "direkt_Fern"]

print(dateinamenDirekt)

#Anpassbare Parameter
intervallPeakArrayDirekt = [
                    [[820,880],[905,975]],
                    [[460,535]],
                    [[93, 110], [247, 283], [551, 615], [682, 744], [765, 850], [945, 1005]],
                    [[350, 423],[860,950]]]

peakEnergy = [Co60.peakEnergy, Cs137w.peakEnergy, Eu152.peakEnergy, Na22.peakEnergy]

def nahOrFernIndex(index):
    if index < len(dateinamenNah):
        return 0
    else:  
        return 1


messungenDirekt = []
figEnergyChannel, axs = plt.subplots(2,1,figsize=(20,10))
for i in range(len(dateinamenDirekt)):
    print(i)
    print(dateinamenDirekt[i])
    # einlesen und definieren der Messreihen mit Korrektur Offset
    messungenDirekt.append(Messung(dateinamenDirekt[i], dateinamenBackgroundDirekt[nahOrFernIndex(i)],messtypDirekt[nahOrFernIndex(i)],probenDirekt[i%len(dateinamenFern)].name ,probenDirekt[i%len(dateinamenFern)]))
    
    messungenDirekt[i].anpassungen = []
    messungenDirekt[i].deltaC = []

    for j, intervall in enumerate(intervallPeakArrayDirekt[i%len(dateinamenFern)]):
        anpassung = gaussAnpassung(messungenDirekt[i],intervall, True, "Peak"+str(j+1), halbwert=True)
        messungenDirekt[i].anpassungen.append(anpassung[0])
        messungenDirekt[i].deltaC.append(anpassung[1])
        #print(anpassung[1])

    plt.close("all")
    
    # plotten aller Daten
    #messungenDirekt[i].plotData("Nah & Direkt: "+ probenDirekt[i].name,"nah_dirket_"+ probenDirekt[i].name)

#Lineare Regression aus den bekannten Energie werten der Peaks und der Channel zahl
#Energy = x * Channel + o
energyData = []
channelData = []
source = []

for i in range(len(messungenDirekt)):
    for j in range(len(messungenDirekt[i].anpassungen)):
        if i == 3 and j == 0:
            continue 
        energyData.append(messungenDirekt[i].Probe.peakEnergy[j])
        channelData.append(messungenDirekt[i].anpassungen[j].output.beta[0])
        source.append(messungenDirekt[i].Probe.name +" Peak: " +str(j+1))

# print(energyData)
print(len(energyData))

# print(channelData)
print(len(channelData))



#print(source)
faktor, offset= linAnpassung(channelData, energyData, None, None, True).output.beta

#print(np.array(energyData) - (np.array(channelData) * faktor + offset))

#Plotten der anpassungen und der literatur werte 
for i in range(len(messungenDirekt)):
    plt.figure(figsize=(20,10))
    plt.title("aaDirekt" + messungenDirekt[i].parameter)
    plt.plot(np.arange(len(messungenDirekt[i].messreihe)) * faktor + offset,messungenDirekt[i].messreihe)
    colors = ["green","darkred","black","darkblue","sienna","green"]
    colors2 = ["limegreen","red","dimgray","blue","chocolate","limegreen"]
    for j,x in enumerate(messungenDirekt[i].anpassungen):
        plt.vlines(x.output.beta[0] * faktor + offset,min(messungenDirekt[i].messreihe),max(messungenDirekt[i].messreihe), color=colors[j])
        plt.vlines(messungenDirekt[i].Probe.peakEnergy[j],min(messungenDirekt[i].messreihe),max(messungenDirekt[i].messreihe), color=colors2[j])
        #print("\n"+ messungenDirekt[i].parameter +" peak " + str(j+1))
        #print(messungenDirekt[i].Probe.peakEnergy[j] - (x.output.beta[0] * faktor + offset))
    
    plt.savefig(base + "/plots/aaDirekt" + messungenDirekt[i].parameter )    





#Auswertung Zyklisch
messungenZyklisch = []
intervallPeakArray = [[435, 545], [405, 515], [370, 480], [330, 435],[0,1000]]
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


#Auswertung Konventionell

messungenFe = []
messungenAl = []

intervallPeakArrayFe = [[435, 545], [405, 515], [370, 480], [330, 435],[20,300]]
intervallPeakArrayAl = [[],[],[],[],[]]

if False:
    for i in range(len(winkelKonventionell)):
        #einlesen
        messungenFe.append(Messung(dateinamenKonventionellFe[i], dateinamenBackgroundKonventionell[i], "konventionellFe", winkelKonventionell[i],"Cs173s"))

        messungenFe[i].anpassungen = gaussAnpassung(messungenFe[i], intervallPeakArrayFe[i], True,)


        messungenAl.append(Messung(dateinamenKonventionellAl[i], dateinamenBackgroundKonventionell[i], "konventionellAl", winkelKonventionell[i],"Cs173s"))

        #messungenAl[i].anpassungen = gaussAnpassung(messungenAl[i], intervallPeakArrayAl[i], True,)
