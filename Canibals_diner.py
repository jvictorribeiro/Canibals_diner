from threading import Thread, Lock, Event
import time, logging

logging.basicConfig(level=logging.DEBUG)

mutex = Lock()

caldron = 5  

canibalServing = 1
canibalEating = 3
cookerCooking = 5

CanibalEvent = Event()  #usado de threading
CookerEvent = Event()


class Canibal(object):

    def __init__(self, name):
        self.name = name
        workingThread = Thread()
        self.run()
        self.porcao = 0
        workingThread.start()
         
    def run(self):
        while True:
        	self.serving()
        
    def serving(self):
        global caldron
        
        mutex.acquire()
        if caldron == 0:
        	mutex.release()
        	logging.debug('Waking up cooker')
        	CookerEvent.set()   
        	CanibalEvent.clear()
        	CanibalEvent.wait()
        else:
            caldron -= 1
            logging.debug('{} is serving the food'.format(self.name))
            time.sleep(canibalServing)
            mutex.release()
            self.eating()

    def eating(self):
        self.porcao += 1
        print('{} is eating'.format(self.name))
        time.sleep(canibalEating)

class Cooker(object):

    def __init__(self):
    	workingThread = Thread()
    	self.run()
    	workingThread.start()
    
    def run(self):
    	self.cooking()
        
    def cooking(self):
    	global CookerEvent
		global CanibalEvent
	
			logging.debug('The diner is being cooked')
   		mutex.acquire()

    	caldron = 5
    	mutex.release()
    	time.sleep(cookerCooking)

    	logging.debug('the diner is ready')
    	logging.debug('waking canibals')

    	CanibalEvent.set()

    	CookerEvent.clear() 
    	CookerEvent.wait()

  
if __name__ == '__main__':
    
    canibals = []
    canibals.append(Canibal('Canibal1'))
        #porcoes1+=1
    canibals.append(Canibal('Canibal2'))
        #porcoes2+=1
    canibals.append(Canibal('Canibal3'))
        #porcoes3+=1
    cooker = Cooker()

    for canibal in canibals:
    	print('canibal ate {}'.format(canibal.porcao))
