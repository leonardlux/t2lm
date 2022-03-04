from cProfile import label
from pprint import pprint
import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np

def gf(B,x):
    #B[0] ist der Erwartunswert
    #B[1] ist die Standardabweichung
    #B[3] da messwerte nicht auf 1 normiert sind 
    return B[2]/np.sqrt(2*np.pi*B[1]**2) * np.exp(-1*(x-B[0])**2/(2*B[1]**2))

gauss = odr.Model(gf)

def gaussAnpassung(messreihe,channelRange):
    cutMessreihe = messreihe[channelRange[0]:channelRange[1]]
    cutChannels = np.arange(channelRange[0],channelRange[1])
    guess = [cutChannels[list(cutMessreihe).index(max(cutMessreihe))],(channelRange[1]-channelRange[0])/4,sum(cutMessreihe)]
    #guess[0] höchster messwert auf dem intervall
    #guess[1] wir nehmen an das wir mit dem auge ein 2 sigma intervall gewählt haben 
    #guess[3] wir summieren über alle bins um den linearen Faktor abzuschätzen
    
    #print(guess)

    myData = odr.RealData(cutChannels, cutMessreihe, sy=np.sqrt(guess[0]))
    myOdr = odr.ODR(myData, gauss, beta0=guess)
    myOutput = myOdr.run()
    print(myOdr.output.beta)
    #myOutput.pprint()

    if True:
        addChannel = 15
        channelsPlot = np.arange(channelRange[0] -addChannel,channelRange[1]+ addChannel)
        print(channelsPlot)
        print(messreihe[channelst[0]:channelsPlot[-1]])

        plt.figure(figsize=(20,10))
        plt.title("Anpassung")
        plt.scatter(channelsPlot,messreihe[channelsPlot[0]:channelsPlot[1]],label="Messwerte")
        #plt.plot(np.linspace(channelsPlot[0],channelsPlot[-1]),gf(myOdr.output.beta,np.linspace(channelsPlot[0],channelsPlot[-1])),label="Anpassung")
        #plt.vlines(myOdr.output.beta[0],0,1,label="MittelwertAnpassung",color="green")
        plt.legend()
        plt.savefig( "../plots/anpassung")
        plt.close("all")
    return myOdr.output.beta[:1]

