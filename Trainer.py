from Pokemon import *


class Trainer:

    def __init__(self,name,pokemon,money):
        self.name = name
        self.pokemon = pokemon
        self.money  = money
        self.items = []
        self.is_online = True

    def increase_item(self,item,amount):
        duplicate_found = False
        duplicate_slot = 0
        for i in range(self.items.len()):
            if item.name == self.items[i].name:
                duplicate_found = True
                duplicate_slot = i
                break
        if duplicate_found:
            self.items[duplicate_slot].amount +=1
        else:
            self.items.append(Item(item.name,amount))




