from dataClass import Messung
base = "/Users/leolux/projects/fortgeschrittenenPraktikum/t2lm"

probenDirekt = ["Co60", "Cs137w", "Eu152", "Na22",]
dateinamenNah = [base + "/data/direkt/Nah_{0}.Tka".format(x) for x in probenDirekt] 
dateinamenBackgroundNah = [base + "/data/direkt/Nah_Rausch.Tka".format(x)] 

winkelZyklisch = ["10","20","30"]
dateinamenZirkular = [base + "/data/zyklisch/{0}grad.TKA".format(x) for x in winkelZyklisch]
dateinamenBackgroundZirkular = [base + "/data/zyklisch/{0}gradHIntergrund.TKA".format(x) for x in winkelZyklisch]
for i in range(len(winkelZyklisch)):    
    Messung(dateinamenZirkular[i], dateinamenBackgroundZirkular[i],"zirkular","Cs173s").plotData("","zirkular"+ winkelZyklisch[i]+ "Gard")


for i in range(len(probenDirekt)):
    Messung(dateinamenNah[i], dateinamenBackgroundNah,"Nah_direkt",probenDirekt[i]).plotData("Nah & Direkt: "+ probenDirekt[i],"nah_dirket_"+ probenDirekt[i])
