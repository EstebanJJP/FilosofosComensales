"""Monitores para el problema de los filosofos comensales"""
from multiprocessing import Lock,Condition, Manager
from multiprocessing import Value

class Table():
    def __init__(self, nphil, manager):
        self.mutex=Lock()
        self.manager = manager
        self.eaters = self.manager.list()
        self.nphil = nphil
        self.free_fork = Condition(self.mutex)
        self.eating = Value('i',0)

    def set_current_phil(self,value: int):
        self.set_current_phil = value
        
    def neaters(self):
        return self.eaters
        
    def free_sides(self):
        siguiente = (self.set_current_phil + 1)%self.nphil
        anterior = (self.set_current_phil - 1)%self.nphil
        return self.eaters.count(siguiente)==0 and self.eaters.count(anterior)==0
    
    def wants_eat(self,value:int):
        self.mutex.acquire()
        self.free_fork.wait_for(self.free_sides)
        self.eaters.append(value)
        self.mutex.release()
        
        
    def wants_think(self,value:int):
        self.mutex.acquire()
        self.eaters.remove(value)
        self.free_fork.notify_all()
        self.mutex.release()

    
class CheatMonitor():
    def __init__(self):
        self.mutex=Lock()
        self.eating = Value('i',0)
        self.chungry = Condition(self.mutex)
    
    def ready(self):
        return self.eating.value > 1
            
    def is_eating(self,value):
        self.mutex.acquire()
        self.eating.value +=1
        self.chungry.notify_all()
        self.mutex.release()
        
    def wants_think(self,value):
        self.mutex.acquire()
        self.chungry.wait_for(self.ready)
        self.eating.value -= 1
        self.mutex.release()
    
class AnticheatTable():
     def __init__(self, NPHIL,manager):
	     self.hungry = manager.list([False]*NPHIL)
	     self.phil = manager.list([False]*NPHIL)
	     self.neating = Value('i',0)
	     self.mutex = Lock()
	     self.freefork = Condition(self.mutex)
	     self.chungry = Condition(self.mutex)
         

	        
     def set_current_phil(self, i):
         self.currentphil = i
	        
     def free_sides_bool(self):
	        return self.phil[(self.currentphil - 1) % len(self.phil)] == False and self.phil[(self.currentphil +1)%len(self.phil)] == False
	    
     def next_hungry(self):
	        return self.hungry[(self.currentphil + 1) % len(self.phil)] == False
	    
     def wants_eat(self,i):
         self.mutex.acquire()
         self.chungry.wait_for(self.next_hungry)
         self.hungry[i] = True
         self.freefork.wait_for(self.free_sides_bool)
         self.phil[i] = True
         self.neating.value += 1
         self.hungry[i] = False
         self.chungry.notify_all()
         self.mutex.release()
	
     def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.neating.value -= 1
        self.freefork.notify_all()
	
	
	

        