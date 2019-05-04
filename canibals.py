import logging
import time
import datetime
from threading import Thread, Lock, Event, enumerate

logging.basicConfig(level=logging.DEBUG)  #mostrar msg das threads

mutex = Lock()      # trava para garantir exclusao mutua

cauldron = 5        # variavel compartilhada entre os canibais e o cooker

canibalServing = 1      # intervalos definidos no trab
canibalEating = 3
cookerCooking = 5

canibals = []

class Canibal(object):

    def __init__(self, name):
        self.name = name
        self.meal = 0
        self.sleeping = False
        workingThread = Thread(target=self.run)
        workingThread.daemon = True  # usar threads como daemon sempre q possivel para evitar que alguma thread fique rodando
        workingThread.start()

    def run(self):
        #logging.debug("I'm the {}".format(self.name))
        #t_end = time.time() + 60 * 2
        # while True and time.time() < t_end:
        global timeIni
        while True and (datetime.datetime.today() - timeIni).seconds < 120:     # run for 120 seconds
            self.serving()
            self.eating()
        CanibalEvent.set()
        CookerEvent.set()

    def serving(self):
        global cauldron
        global canibals

        if cauldron == 0:
            sleepingCannibals = 0       #verifica se o caldeirao ta vazio e apos o ultimo canibal dormir, acorda cozinheiro, isso garante q todos os canibais estejam dormindo
            for canibal in canibals:
                if (canibal.sleeping):
                    sleepingCannibals += 1
            if not CookerEvent.is_set() and sleepingCannibals == 2: # is_set retorna verdadeiro somente se a flag interna for V
                logging.debug('Waking up the cooker!')
                CookerEvent.set()
            self.sleep()

        else:
            mutex.acquire()
            logging.debug('{} is serving the food'.format(self.name))
            cauldron -= 1
            time.sleep(canibalServing)
            mutex.release()

    def eating(self):
        logging.debug('{} is eating'.format(self.name))
        self.meal += 1
        time.sleep(canibalEating)

    def wakeUp(self):
        logging.debug('{} woke up'.format(self.name))
        self.sleeping = False
        CanibalEvent.set()

    def sleep(self):
        self.sleeping = True
        logging.debug('{} went to sleep'.format(self.name))
        CanibalEvent.clear()
        CanibalEvent.wait()


class Cooker(object):
    def __init__(self, name):
        self.name = name
        workingThread2 = Thread(target=self.run)
        workingThread2.daemon = True
        workingThread2.start()

    def run(self):
        CookerEvent.wait()
        #logging.debug('I'm the {}'.format(self.name))
        # t_end = time.time() + 60 * 2
        #while True and time.time() < t_end:
        while True and (datetime.datetime.today() - timeIni).seconds < 120:
            self.cooking()
        CanibalEvent.set()
        CookerEvent.set()

    def cooking(self):
        mutex.acquire()
        global cauldron
        logging.debug('The diner is being cooked')
        cauldron = 5
        time.sleep(cookerCooking)
        logging.debug('the diner is ready')
        logging.debug('waking canibals')
        mutex.release()
        self.sleep()

    #def wakeUp(self):
    #    logging.debug('{} woke up'.format(self.name))
     #   CookerEvent.set()

    def sleep(self):
        global canibals
        logging.debug('{} went to sleep'.format(self.name))
        for canibal in canibals:
            canibal.wakeUp()
        CanibalEvent.set()
        CookerEvent.clear()
        CookerEvent.wait()


'''uso de event objects, uma thread sinaliza um evento e a outra espera por ele'''
CanibalEvent = Event()  # usado de threading
CookerEvent = Event()

if __name__ == '__main__':

    timeIni = datetime.datetime.today()

    for i in range(3):
        canibals.append(Canibal(name='Canibal {}'.format(i+1)))
    cooker = Cooker(name='Cooker')

    for i in enumerate():       #enumerate para saber qual a posicao do item atual no for
        if i != enumerate()[0]:
           i.join()     #join para fzr uma thread esperar q a outra termine

    for canibal in canibals:
        logging.debug('canibal {} ate {}'.format(canibal.name, canibal.meal))
