from abc import ABC
class Item(ABC):
    def __init__(self,name,power):
        super().__init__()
        self.name = name
        self.amount_in_bag = 0
        self.power = power


class HPHealItem(Item):
    def __init__(self,name,power):
        super().__init__(name,power)

    def use(self,pokemon):
        if(pokemon.hp == pokemon.max_hp):
            return "403 HP is already full"
        pre_restore = pokemon.hp
        pokemon.hp += self.power
        if(pokemon.hp > pokemon.max_hp):
            pokemon.hp = pokemon.max_hp
        return pokemon.name+"'s HP was increased by "+str(pokemon.hp-pre_restore)+" points"


class PPHealItem(Item):
    def __init__(self,name,power):
        super().__init__(name,power)

    def use(self,pokemon,move_slot):
        if (pokemon.moves[move_slot].pp == pokemon.moves[move_slot].max_pp):
            return "403 PP is already full"
        pre_restore = pokemon.moves[move_slot].pp
        pokemon.moves[move_slot].pp += self.power
        if pokemon.moves[move_slot].pp > pokemon.moves[move_slot].max_pp:
            pokemon.moves[move_slot].pp = pokemon.moves[move_slot].max_pp
        return pokemon.moves[move_slot].name + "'s PP was increased by " + str(pokemon.moves[move_slot].pp-pre_restore)+" points"


