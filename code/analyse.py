from cProfile import label
from pprint import pprint
from matplotlib import gridspec
import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np

def gf(B,x):
    #B[0] ist der Erwartunswert
    #B[1] ist die Standardabweichung
    #B[3] da messwerte nicht auf 1 normiert sind 
    return B[2]/np.sqrt(2*np.pi*B[1]**2) * np.exp(-1*(x-B[0])**2/(2*B[1]**2))

gauss = odr.Model(gf)

def gaussAnpassung(Messung,channelRange, plot=False):

    cutMessreihe = Messung.messreihe[channelRange[0]:channelRange[1]]
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

    if plot:
        addChannel = 0
        channelsPlot = np.arange(channelRange[0] -addChannel,channelRange[1]+ addChannel)

        fig, axs = plt.subplots(2,1, sharex=True, figsize=(20,10),gridspec_kw={'height_ratios': [3,1]})
        
        dataY = [Messung.messreihe[channelsPlot[0]:channelsPlot[-1]+1],Messung.messreihe[channelsPlot[0]:channelsPlot[-1]+1]-gf(myOdr.output.beta,channelsPlot)]

        for i in range(len(dataY)):
            axs[i].grid()
            axs[i].vlines(channelRange,min(dataY[i])-(max(dataY[i])-min(dataY[i]))/15,max(dataY[i])+(max(dataY[i])-min(dataY[i]))/15,color="red")
            axs[i].vlines(myOdr.output.beta[0],min(dataY[i])-(max(dataY[i])-min(dataY[i]))/15,max(dataY[i])+(max(dataY[i])-min(dataY[i]))/15,color="green")

            axs[i].scatter(channelsPlot,dataY[i])
        
        axs[0].title.set_text("Anpassung und Residuenplot: " + Messung.typ + " " + Messung.parameter)
        axs[0].plot(np.linspace(channelsPlot[0],channelsPlot[-1]),gf(myOdr.output.beta,np.linspace(channelsPlot[0],channelsPlot[-1])))
        axs[1].hlines(0,channelsPlot[0],channelsPlot[-1])
        fig.savefig("../plots/anpassungResiduen" + Messung.typ + Messung.parameter)
    return myOdr.output

