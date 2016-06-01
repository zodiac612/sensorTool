
    
print 'sensorService starting'

while 1:
    
    if refreshNDD <= time.time()
        if not qNDD.empty():
            #dictNetDevs = {}
            #dictNetDevs = qNDD.get()
            boolNDD = qNDD.get()
            if boolNDD == False:
                ActivateBew = True
            else:
                ActivateBew = False
            qNDD.task_done()
            DiscoveryInProgress = False
        refreshNDD = time.time() + iNDD
        #print 'Device present: ' + str(not ActivateBew)
                
    if time.time() >= refreshNDD:
        
