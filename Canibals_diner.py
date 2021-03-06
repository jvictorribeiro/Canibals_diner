from threading import Thread, Lock, Event
import time, logging

logging.basicConfig(level=logging.DEBUG)

mutex = Lock()

caldron = 5  

canibalServing = 1
canibalEating = 3
cookerCooking = 5

class Canibal(object):

    def __init__(self, name):
        self.name = name
        workingThread = Thread()
        self.run()
        workingThread.start()
    
    def run(self):
        self.serving()
        
    def serving(self):
        global caldron
        global CanibalEvent
        
        mutex.acquire()
        if caldron == 0:
            logging.debug('Waking up cooker')
            mutex.release()

        else:
            caldron -= 1
            logging.debug('{} is serving the food'.format(self.name))
            time.sleep(canibalServing)
            mutex.release()
            self.eating()
            
    def eating(self):
        global porcoes
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
        mutex.acquire()

        logging.debug('The diner is being cooked')
    
        caldron = 5
        mutex.release()

        time.sleep(cookerCooking)

        logging.debug('the diner is ready')
        logging.debug('waking canibals')

if __name__ == '__main__':
    
    porcoes1 = 0 
    porcoes2 = 0
    porcoes3 = 0
    t_end = time.time() + 60 * 2        #run for 120 seconds
    while time.time() < t_end:
        canibals = []
        canibals.append(Canibal('Canibal1'))
        porcoes1+=1
        canibals.append(Canibal('Canibal2'))
        porcoes2+=1
        canibals.append(Canibal('Canibal3'))
        porcoes3+=1
        cooker = Cooker()

    print('Canibal1 comeu %i' % porcoes1)
    print('Canibal2 comeu %i' % porcoes2)
    print('Canibal3 comeu %i' % porcoes3)