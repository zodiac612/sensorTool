#!/usr/bin/python
# -*- coding: latin-1 -*-
# testskript for drawing a line chart 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys

def plotting(dictPlotSen, dictPlotAussen, vVerbose):
    
    for vKey in dictPlotSen:
#        print dictPlotSen[vKey]['ListTime']
#        print dictPlotSen[vKey]['ListT']
#        print dictPlotSen[vKey]['ListRH']
        vLenTime = len(dictPlotSen[vKey]['ListTime'])
#        print vLenTime
        if vLenTime > 0:
            sName = vKey
            vZeit = list()
            vTemp1 = list()
            vRH1 = list()
            vTemp1 = dictPlotSen[vKey]['ListT']
            vRH1 = dictPlotSen[vKey]['ListRH']

            for vE in dictPlotSen[vKey]['ListTime']:
#                print str(vE[11:16]).replace(':', '.')
                if vVerbose.startswith('test'):
#                    print str(vE[17:19]) + '-' + str(vE[14:16]) 
                    iA = float(str(vE[14:16]))
                    iB = float(str(vE[17:19]))
#                    print iA
#                    print iB
                    iA = iA + round(iB/60, 2)
#                    print iA
                    vZeit.append(iA)
                else:
                    iA = float(str(vE[11:13]))
                    iB = float(str(vE[14:16]))
                    iA = iA + round(iB/60, 2)
                    vZeit.append(iA)
             
#            print vZeit
             
#            sName2 = ''
#            vZeit2 = ()
#            vTemp2 = list()
#            vRH2 = list()
#            vLabel3 = ''
#            vLabel4 = ''
#            for vKey2 in dictPlotAussen:
#                sName2 = vKey2
#                vTemp2 = dictPlotAussen[vKey2]['ListT']
#                vRH2 = dictPlotAussen[vKey2]['ListRH']
#                vLabel3 = sName2 + '_T (' + str(vTemp2[-1]) + ')'
#                vLabel4 = sName2 + '_RH (' + str(vRH2[-1]) + ')'
#                
#            #vTemp3 = [33, 31, 31, 33, 31, 30]
            #vLF = [20.2, 40.5, 50.5, 45, 47, 50]
            try:
                plt.clf()
                plt.ylim([0,100])
                plt.xlabel('Zeit')
                plt.ylabel('Werte')
                plt.title('Chart')
                vLabel1 = sName + '_T (' + str(vTemp1[-1]) + ')'
                
                plt.plot(vZeit, vTemp1, marker='', linestyle='-',  color='g', label=vLabel1)
                #plt.plot(vZeit, vTemp1, marker='p', linestyle='-',  color='g', label=vLabel1)
                if len(vRH1) > 0:
                    vLabel2 = sName + '_RH (' + str(vRH1[-1]) + ')'
                    plt.plot(vZeit, vRH1, marker='', linestyle='-', color='c', label=vLabel2)
                    #plt.plot(vZeit, vRH1, marker='*', linestyle='-.', color='c', label=vLabel2)
                    
                #plt.plot(vZeit, vTemp2, marker='', linestyle='-', color='r', label=vLabel3)
                #plt.plot(vZeit, vTemp2, marker='o', linestyle='--', color='r', label=vLabel3)
                
                #plt.plot(vZeit, vRH2, marker='', linestyle='-',  color='b', label=vLabel4)
                #plt.plot(vZeit, vRH2, marker='D', linestyle=':',  color='b', label=vLabel4)
                lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.87))
                FileName = '/var/sensorTool/www/' + sName + '.png'
                plt.savefig(FileName, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
                #plt.savefig(FileName, format='png')
            except:
                print(sys.exc_info()[0])
                print(sName + ' fehler im Plot')
#plt.show()
#plt.plot.saveFile("test.png")
