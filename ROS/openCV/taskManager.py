'''import detect_dice
import detect_gate
import detect_roulette
import detect_cashIn
import detect_buoy

This is the class which will handle all the tasks.
Gate,Dice,Roulette,CashIn
'''

from random import *


class taskManager():
    def __init__(self):
        self.coordinates = []
        self.coordinates.append(randint(-100,100))
        self.coordinates.append(randint(-100,100))

        
    def gateDetect(self):
        print("gateDetect")
        return self.coordinates
        
    def diceDetect(self):
        print("diceDetect")
        return self.coordinates

    def rouletteDetect(self):
        print("rouletteDetect")
        return self.coordinates

    def cashInDetect(self):
        print("cashInDetect")
        return self.coordinates

    def buoyDetect(self):
        print("buoyDetect")
        return self.coordinates