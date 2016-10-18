#!/usr/bin/python
# -*- coding: latin-1 -*-
# testskript for drawing a line chart 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

def plotting_DeviceValues(dictGraph, sName,  vVerbose, iMinValue = 0,  iMaxValue  = 100):
    vLenTime = len(dictGraph['time'])
    if vLenTime > 0:
        plt.clf()
        plt.ylim([iMinValue,iMaxValue])
        plt.xlabel('Zeit')
        plt.ylabel('Werte')
        plt.title('Chart')
        vZeit = list()
        for vE in dictGraph['time']:
            if vVerbose.startswith('test'):
                iA = float(str(vE[14:16]))
                iB = float(str(vE[17:19]))
                iA = iA + round(iB/60, 2)
                vZeit.append(iA)
            else:
                iA = float(str(vE[11:13]))
                iB = float(str(vE[14:16]))
                iA = iA + round(iB/60, 2)
                vZeit.append(iA)
#
#        dictColors={}
#        dictColors[1] = 'g'
#        dictColors[2] = 'c'
#        dictColors[3] = 'b'
#        dictColors[4] = 'r'
#        dictColors[5] = 'y'
#        dictColors[6] = 'b'
#        dictColors[7] = 'r'
        iCC = 1
        try:
            for vKey in dictGraph:
                if vKey <> 'time':
                    vLabel = vKey + '(' + str(dictGraph[vKey].GetActualValue()) + ')'
                    vLine = list()
                    vLine = dictGraph[vKey].GetListValue()
                    #vColor = dictColors[iCC]
                    if iCC < 7:
                        iCC = iCC + 1
                    #plt.plot(vZeit, vLine, marker='', linestyle='-',  color=vColor, label=vLabel)
                    plt.plot(vZeit, vLine, marker='', linestyle='-',  label=vLabel)

            lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.87))
            FileName = '/var/sensorTool/www/' + sName + '.png'
            plt.savefig(FileName, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
            #plt.savefig(FileName, format='png')
        except:
            print(sys.exc_info()[0])
            print(sName + ' fehler im Plot') 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
