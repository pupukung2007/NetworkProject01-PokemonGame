#จัดทำโดย
#นาย ปิยณัฐ กันเดช 5910401092 หมู่เรียน 1
#นาย ปุญญพัฒน์ ญาณวิสิฏฐ์ 5910401106 หมู่เรียน 1
from abc import ABC,abstractmethod
class Item(ABC):
    def __init__(self,name,power):
        super().__init__()
        self.name = name
        self.amount_in_bag = 0
        self.power = power
    @abstractmethod
    def use(self, pokemon):
        pass
    @abstractmethod
    def display_description(self):
        pass


class HPHealItem(Item):
    def __init__(self,name,power):
        super().__init__(name,power)

    def use(self,pokemon):
        super().use(pokemon)
        if(pokemon.hp == pokemon.max_hp):
            return "403 HP is already full"
        pre_restore = pokemon.hp
        pokemon.hp += self.power
        if(pokemon.hp > pokemon.max_hp):
            pokemon.hp = pokemon.max_hp
        return pokemon.name+"'s HP was restored by "+str(pokemon.hp-pre_restore)+" points"

    def display_description(self):
        super().display_description()
        return self.name + ": Heal your pokemon HP for "+str(self.power)+" points"+" [Amount in bag: "+str(self.amount_in_bag)+"]\n"


class PPHealItem(Item):
    def __init__(self,name,power):
        super().__init__(name,power)

    def use(self,pokemon):
        super().use(pokemon)
        found = False
        for i in range(len(pokemon.moves)):
            if (pokemon.moves[i].pp != pokemon.moves[i].max_pp):
                found = True
                break
        if found:
            for i in range(len(pokemon.moves)):
                pokemon.moves[i].pp += self.power
                if pokemon.moves[i].pp > pokemon.moves[i].max_pp:
                    pokemon.moves[i].pp = pokemon.moves[i].max_pp
        else:
            return "403 PP is already full"
        return pokemon.name + "'s Move PP was restored by " + str(self.power)+" points\n"

    def display_description(self):
        super().display_description()
        return self.name + ": Heal all your pokemon move's PP for "+str(self.power)+" points"+" [Amount in bag: "+str(self.amount_in_bag)+"]\n"


