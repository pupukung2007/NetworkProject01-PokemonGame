from abc import ABC, abstractmethod

class Move:
    def __init__(self,name,power):
        self.name = name
        self.power = power
        super().__init__()

    @abstractmethod
    def use(self,user_pokemon,rival_pokemon):
        pass







