from Pokemon import *
from Item import*
from Move import *


class Trainer:

    def __init__(self,name,pokemon,money):
        self.name = name
        self.pokemon = pokemon
        self.money  = money
        self.items = []
        self.is_online = False
        self.connectionSocket = 0

    def buy_item(self,item,buy_amount,price):
        total_price = buy_amount*price
        if(self.money >= total_price):
            self.money -= total_price
            duplicate_found = False
            duplicate_slot = 0
            for i in range(len(self.items)):
                if item.name == self.items[i].name:
                    duplicate_found = True
                    duplicate_slot = i
                    break
            if duplicate_found:
                self.items[duplicate_slot].amount_in_bag += buy_amount
            else:
                self.items.append(Item(item.name,item.power))
                self.items[len(self.items)-1].amount_in_bag = buy_amount
            return "208 You have bought "+str(buy_amount)+" "+item.name+"(s) for "+str(total_price)+" Poke"
        else:
            return "404 Not enough money"


    def teach_move(self,move,replace_slot):
        message = "203 "+self.pokemon.name +" has forgotten "+self.pokemon.moves[replace_slot].name+" and learned "+ move.name
        self.pokemon.moves[replace_slot] = move
        return message

    def heal_pokemon(self):
        if(self.money >= 100):
            self.money -= 100
            self.pokemon.hp = self.pokemon.max_hp
            for i in range(4):
                self.pokemon.moves[i].pp = self.pokemon.moves[i].max_pp
            return "202 Your pokemon has been fully healed"
        else:
            return "404 Not enough money"

    def use_item(self,item):
        found = False
        found_slot = 0
        for i in range(len(self.items)):
            if item.name == self.items[i].name:
                found = True
                found_slot = i
                break
        if found and self.items[found_slot].amount_in_bag > 0:
            message = self.items[found_slot].use(self.pokemon)
            self.items[found_slot].amount_in_bag -= 1
            return "201 "+self.name+" used "+self.items[found_slot].name+"\n"+ message
        elif found and self.items[found_slot].amount_in_bag ==0:
            return "403 Not enough " + self.items[found_slot].name +"s"
        else:
            return "401 Item not found"

    def receive_money(self,amount):
        self.money += amount
        return "207 "+self.name+" has received "+str(amount)+" Poke"

    def lose_money(self,amount):
        self.money -= amount
        return "209 "+self.name+" has lost "+str(amount)+" Poke"

    def is_out_of_pokemon(self):
        if(self.pokemon.is_fainted()):
            return "300 "+self.name + " is out of usable pokemon!"

    def __eq__(self, other):
        return self.name == other.name




