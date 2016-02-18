#!/usr/bin/python
# -*- coding: latin-1 -*-
# testskript for drawing a line chart 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

vZeit = [1, 2, 3, 4, 5, 6]
vTemp1 = [10, 12.56636, 11, 15, 16, 10]
vTemp2 = [22, 21, 21, 22, 21, 20]
vTemp3 = [33, 31, 31, 33, 31, 30]
vLF = [20.2, 40.5, 50.5, 45, 47, 50]

plt.ylim([0,100])
plt.xlabel('Zeit')
plt.ylabel('Werte')
plt.title('Chart')
plt.plot(vZeit, vLF,    marker='o', linestyle='--', color='r', label='RH')
plt.plot(vZeit, vTemp1, marker='p', linestyle='-',  color='g', label='T1')
plt.plot(vZeit, vTemp2, marker='*', linestyle='-.', color='c', label='T2')
plt.plot(vZeit, vTemp3, marker='D', linestyle=':',  color='b', label='T3')
lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.87))
plt.savefig('/var/sensorTool/example01.png', format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
#plt.show()
#plt.plot.saveFile("test.png")
