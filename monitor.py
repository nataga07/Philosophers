#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROBLEMA DE LOS FILOSOFOS 

Alumna:Natalia Garcia
"""
from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager, Value
from multiprocessing import current_process
from time import sleep
from random import random


class Table():
    def __init__(self, nphil: int, manager):
        self.nphil = nphil
        self.manager = manager
        self.mutex = Lock()  #Definimos los semaforos mutex
        self.phil = self.manager.list([False]* nphil) #Los comensales entran pensando
        self.eating = Value('i',0)
        self.current_phil = None
        self.free_fork = Condition(self.mutex)
        
    def set_current_phil(self, num):
        self.current_phil = num 
    
    def no_comen_lados(self): #Asegurar que hay tenedores libres 
        n = self.current_phil
        return (not self.phil[(n-1)%(self.nphil)]) and (not self.phil[(n+1)%(self.nphil)])
    
    def wants_eat(self, num):
        self.mutex.acquire() #Ponemos en wait el semáforo de comer
        self.current_phil = num #Identificamos al filosofo que quiere comer
        self.free_fork.wait_for(self.no_comen_lados) #Si se cumple no_comen_lados, tenemos tendores libres
        self.phil[num] = True #Cambiamos en la lista a True
        self.eating.value += 1 #Sumamos 1 al valor de eating
        self.mutex.release() #Mandamos el signal al semaforo 
        
    
    def wants_think(self,num):
        self.mutex.acquire() #Ponemos en wait el semaforo de pensar
        self.phil[num] = False #Como no estamos comiendo, cambiamos a False
        self.eating.value -= 1 #Restamos 1 al valor de eating
        self.free_fork.notify() #Avisamos de que dejamos tenedor libre
        self.mutex.release() #Mandamos signal al semaforo
        