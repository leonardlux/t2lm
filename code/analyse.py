

import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np

true = True
def gf(B,x):
    #B[0] ist der Erwartunswert
    #B[1] ist die Standardabweichung
    #B[2] da messwerte nicht auf 1 normiert sind 
    #B[3] offset in y richtung
    #B[2] * g(x,B[0]=µ, B[1]=std) + B[3]; g() is true gauss

    return B[2]*1/np.sqrt(2*np.pi*B[1]**2) * np.exp(-1*(x-B[0])**2/(2*B[1]**2)) + B[3]

def lf(B,x):
    #B[0] ist die Steigung
    #B[1] ist die Verschiebung
    return B[0]*x + B[1]

gauss = odr.Model(gf)
linear = odr.Model(lf)

def gaussAnpassung(Messung,channelRange, plot=False, extraTitle="", halbwert=False):

    cutMessreihe = Messung.messreihe[channelRange[0]:channelRange[1]]
    cutMessreiheError = Messung.messreiheError[channelRange[0]:channelRange[1]]
    cutChannels = np.arange(channelRange[0],channelRange[1])
    guess = [cutChannels[list(cutMessreihe).index(max(cutMessreihe))],(channelRange[1]-channelRange[0])/4,sum(cutMessreihe), cutMessreihe[0]*0.1]
    #guess[0] höchster messwert auf dem intervall
    #guess[1] wir nehmen an das wir mit dem auge ein 2 sigma intervall gewählt haben 
    #guess[3] wir summieren über alle bins um den linearen Faktor abzuschätzen
    
    #print(guess)


    myData = odr.RealData(cutChannels, cutMessreihe, sy=cutMessreiheError, sx=1/np.sqrt(12)) #Unsicherheit auf die Messwerte ist die Wurzel des ersten guesses
    myOdr = odr.ODR(myData, gauss, beta0=guess)
    myOdr.run()

    if halbwert:
        deltaChannel = np.sqrt(2*np.log(2))*myOdr.output.beta[1]
        
    if False:
        print(myOdr.output.beta)
        myOdr.output.pprint()

    if plot:
        addChannel = 12
        channelsPlot = np.arange(channelRange[0] -addChannel,channelRange[1]+ addChannel)

        fig, axs = plt.subplots(2,1, sharex=True, figsize=(20,10),gridspec_kw={'height_ratios': [3,1]})
        
        dataY = [
            Messung.messreihe[channelsPlot[0]:channelsPlot[-1]+1],
            Messung.messreihe[channelsPlot[0]:channelsPlot[-1]+1]-gf(myOdr.output.beta,channelsPlot)
            ]

        for i in range(len(dataY)):
            axs[i].grid()
            axs[i].vlines(
                channelRange,
                min(dataY[i])-(max(dataY[i])-min(dataY[i]))/15,
                max(dataY[i])+(max(dataY[i])-min(dataY[i]))/15,
                color="red")

            axs[i].vlines(
                myOdr.output.beta[0],
                min(dataY[i])-(max(dataY[i])-min(dataY[i]))/15,
                max(dataY[i])+(max(dataY[i])-min(dataY[i]))/15,
                color="green")

            axs[i].errorbar(
                channelsPlot,
                dataY[i],
                yerr=Messung.messreiheError[channelsPlot[0]:channelsPlot[-1]+1],
                fmt=".")

            if halbwert:
                axs[i].vlines(
                    [myOdr.output.beta[0] - deltaChannel, myOdr.output.beta[0] + deltaChannel, ],
                    min(dataY[i])-(max(dataY[i])-min(dataY[i]))/15,
                    max(dataY[i])+(max(dataY[i])-min(dataY[i]))/15,
                    color="blue")
        
        if halbwert:
            axs[0].hlines(
                [myOdr.output.beta[2]/np.sqrt(2*np.pi*myOdr.output.beta[1]**2) + myOdr.output.beta[3],myOdr.output.beta[3]]
                ,min(channelsPlot),max(channelsPlot),color="gold")
            
            axs[0].hlines([0.5*myOdr.output.beta[2]/np.sqrt(2*np.pi*myOdr.output.beta[1]**2)+myOdr.output.beta[3]],min(channelsPlot),max(channelsPlot),color="limegreen")



        axs[0].plot(
            np.linspace(channelsPlot[0],channelsPlot[-1]),
            gf(myOdr.output.beta,np.linspace(channelsPlot[0],channelsPlot[-1]))
            )
        

        axs[0].title.set_text("Anpassung und Residuenplot: " + Messung.typ + " " + Messung.parameter + " " + extraTitle )
        axs[1].hlines(0,channelsPlot[0],channelsPlot[-1])
        
        fig.savefig("../plots/anpassung" + Messung.typ + Messung.parameter + extraTitle)
    if not halbwert:   
        return myOdr
    else: 
        return myOdr, deltaChannel


def linAnpassung(xValues, yValues, exValues, eyValues,plot=False):
    guess = [(yValues[-1]-yValues[0])/(xValues[-1]-xValues[0]),5]
    #print(guess)

    myData = odr.RealData(xValues,yValues)#,sx=exValues, sy=eyValues)
    myOdr = odr.ODR(myData, linear, beta0=guess)
    myOdr.run()
    if True:
        print(myOdr.output.beta)
        #myOdr.output.pprint()
    
    if plot:
        fig, axs = plt.subplots(2,1, sharex=True, figsize=(20,10),gridspec_kw={'height_ratios': [3,1]})
        
        dataY = [
            yValues,
            np.array(yValues)-lf(myOdr.output.beta,np.array(xValues))
            ]
        for i in range(len(dataY)):
            axs[i].grid()
            axs[i].errorbar(
                xValues,
                dataY[i],
                fmt=".")
                # yerr=eyValues,
                # xerr=exValues,
        
        axs[0].plot(np.linspace(min(xValues),max(xValues)), lf(myOdr.output.beta,np.linspace(min(xValues),max(xValues))))
        axs[1].hlines(0,min(xValues),max(xValues))
        axs[0].title.set_text("Anpassung und Residuenplot: Energie zu Channels" )
        fig.savefig("../plots/anpassungEnergie" )
    
    return myOdr 

