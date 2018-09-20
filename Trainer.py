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
        self.is_waiting = False
        self.enemy = NoTrainer("None")

    def buy_HP_item(self,item,buy_amount,price):
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
                self.items.append(HPHealItem(item.name,item.power))
                self.items[len(self.items)-1].amount_in_bag = buy_amount
            return "200 You have bought "+str(buy_amount)+" "+item.name+"(s) for "+str(total_price)+" Poke"
        else:
            return "402 Not enough money"

    def buy_PP_item(self,item,buy_amount,price):
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
                self.items.append(PPHealItem(item.name,item.power))
                self.items[len(self.items)-1].amount_in_bag = buy_amount
            return "200 You have bought "+str(buy_amount)+" "+item.name+"(s) for "+str(total_price)+" Poke"
        else:
            return "402 Not enough money"


    def teach_move(self,move,replace_slot):
        message = "203 "+self.pokemon.name +" has forgotten "+self.pokemon.moves[replace_slot].name+" and learned "+ move.name
        self.pokemon.moves[replace_slot] = move
        return message

    def heal_pokemon(self):
        self.pokemon.hp = self.pokemon.max_hp
        for i in range(4):
            self.pokemon.moves[i].pp = self.pokemon.moves[i].max_pp


    def use_item_name(self,item):
        found = False
        found_slot = 0
        for i in range(len(self.items)):
            if item == self.items[i].name:
                found = True
                found_slot = i
                break
        if found and self.items[found_slot].amount_in_bag > 0:
            message = self.items[found_slot].use(self.pokemon)
            if "403" in message: #A stat is already Full
                return message
            else:
                self.items[found_slot].amount_in_bag -= 1
                return self.name+" used "+self.items[found_slot].name+"\n"+ message
        elif found and self.items[found_slot].amount_in_bag ==0:
            return "403 Not enough " + self.items[found_slot].name +"s"
        else:
            return "404 Item not found"

    def use_item(self,slot):
        slot -= 1
        if 0<=slot<len(self.items):
            if self.items[slot].amount_in_bag >0:
                message = self.items[slot].use(self.pokemon)
                self.items[slot].amount_in_bag -= 1
                return self.name + " used " + self.items[slot].name + "\n" + message
            elif self.items[slot].amount_in_bag == 0:
                return "403 Not enough " + self.items[slot].name + "s"
            else:
                return "404 Item not found"
        else:
            return "400 There is no item "+str(slot)

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

    def is_in_battle(self):
        if(self.enemy.name== "None"):
            return False
        return True


class NoTrainer:
    def __init__(self,name):
        self.name = name




