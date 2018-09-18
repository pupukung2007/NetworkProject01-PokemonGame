from abc import ABC,abstractmethod
class Item(ABC):
    def __init__(self,amount):
        super().__init__()
        self.amount = amount

    def use(self):
        pass


