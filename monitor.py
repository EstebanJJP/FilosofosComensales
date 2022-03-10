"""Monitores para el problema de los filosofos comensales"""
from multiprocessing import Lock,Condition


class Table():
    def __init__(self, nphil, manager):
        self.mutex=Lock()
        self.manager = manager
        self.eaters = self.manager.list([False]*nphil)
        self.nphil = nphil
        self.free_fork = Condition(self.mutex)

    def set_current_phil(self,value: int):
        self.set_current_phil = value
        
    
    def free_sides(self):
        siguiente = self.set_current_phil + 1
        anterior = self.set_current_phil - 1
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

    
        