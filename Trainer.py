from Pokemon import *
from Item import*
from Move import *


class Trainer:

    def __init__(self,name,pokemon,money):
        self.name = name
        self.pokemon = pokemon
        self.money  = money
        self.items = []
        self.is_online = True

    def buy_item(self,item,total_price):
        if(self.money >= total_price):
            self.money -= total_price;
            duplicate_found = False
            duplicate_slot = 0
            for i in range(self.items.len()):
                if item.name == self.items[i].name:
                    duplicate_found = True
                    duplicate_slot = i
                    break
            if duplicate_found:
                self.items[duplicate_slot].amount += 1
            else:
                self.items.append(item)


    def teach_move(self,move,replace_slot):
        if(replace_slot == 1):
            self.pokemon.move1 = move
        elif (replace_slot == 2):
            self.pokemon.move2 = move
        elif (replace_slot == 3):
            self.pokemon.move3 = move
        elif (replace_slot == 4):
            self.pokemon.move4 = move
        else:
            pass

    def heal_pokemon(self):
        if(self.money >= 100):
            self.money -= 100
            self.pokemon.hp = self.pokemon.max_hp
            self.pokemon.move1.pp = self.pokemon.move1.max_pp
            self.pokemon.move2.pp = self.pokemon.move2.max_pp
            self.pokemon.move3.pp = self.pokemon.move3.max_pp
            self.pokemon.move4.pp = self.pokemon.move4.max_pp





