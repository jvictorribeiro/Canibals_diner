from threading import Thread, Lock, Event
import time, random

mutex = Lock()

caldron = []  #4 o caldeirao esta vazio e 0 esta cheio

canibalTimeMin = 1
canibalTimeMax = 3
cookerTimeMin = 3
cookerTimeMax = 12

class Canibal:
    CanibalEvent = Event()

    def __int__(self, name):
        self.name = name

    def serving(self):
        global caldron
        self.CanibalEvent.clear()
        caldron += 1
        print('The canibal is serving the food')

        randomServingTime = random.randrange(canibalTimeMin, canibalTimeMin+1)
        time.sleep(randomServingTime)

    def eating(self):
        self.CanibalEvent.clear()

        print('The canibal is eating')

        randomEatingTime = random.randrange(canibalTimeMax, canibalTimeMax+1)
        time.sleep(randomEatingTime)

    def sleep(self):
        self.CanibalEvent.wait()


class Cooker:
    CookerCookingEvent = Event()    #usado de threading

    def sleep(self):
        self.CookerCookingEvent.wait()

    def wakeUp(self):
        self.CookerCookingEvent.set()

    def cooking(self):
        #cooker busy
        self.CookerCookingEvent.clear()

        print ('The diner is being cooked')

        randomCookingTime = random.randrange(cookerTimeMin, cookerTimeMax+1)
        time.sleep(randomCookingTime)


if __name__ == '__main__':
    canibals = []
    canibals.append(Canibal('Canibal1'))
    canibals.append(Canibal('Canibal2'))
    canibals.append(Canibal('Canibal3'))

    cooker = Cooker()
