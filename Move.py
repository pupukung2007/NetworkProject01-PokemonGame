from abc import ABC, abstractmethod

class Move(ABC):
    def __init__(self,name,power,max_pp):
        self.name = name
        self.power = power
        self.pp = max_pp
        self.max_pp = max_pp
        super().__init__()

    @abstractmethod
    def use(self,user_pokemon,rival_pokemon):
        pass


class SpecialMove(Move):
    def __init__(self,name,power,max_pp):
        super().__init__(name,power,max_pp)


    def use(self,user_pokemon,rival_pokemon):
        if self.pp > 0:
            damage = ( (((2*user_pokemon.level/5)+2) *self.power*(user_pokemon.special_attack / rival_pokemon.special_defense) /50)+2  )
            rival_pokemon.set_hp(rival_pokemon.hp - damage)
            self.pp -= 1
            return str(user_pokemon.name+" uses "+self.name+" on "+rival_pokemon.name+" for "+str(damage)+" damage.")
        else:
            damage = ((((2 * user_pokemon.level / 5) + 2) * 50 * (
                        user_pokemon.attack / rival_pokemon.defense) / 50) + 2)
            rival_pokemon.set_hp(rival_pokemon.hp - damage)
            return str(user_pokemon.name + " uses Struggle on " + rival_pokemon.name + " for " + str(
                damage) + " damage.")













