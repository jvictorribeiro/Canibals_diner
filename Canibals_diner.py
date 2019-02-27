from threading import Thread, Lock, Event
import time, random


caldron = 4  #4 o caldeirao esta vazio e 0 esta cheio


canibalTimeMin = 5
canibalTimeMax = 10
cookerTimeMin = 3
cookerTimeMax = 12

class Canibal:
    def __int__(self, name):
        self.name = name

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
        



