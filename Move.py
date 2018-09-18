from abc import ABC

class Move(ABC):
    def __init__(self,name,power,max_pp):
        self.name = name
        self.power = power
        self.pp = max_pp
        self.max_pp = max_pp
        super().__init__()

    def use(self,user_pokemon,rival_pokemon):
        if(self.pp == 0):
            if user_pokemon.move1.pp > 0 or user_pokemon.move2.pp > 0 or user_pokemon.move3.pp > 0 or user_pokemon.move4.pp > 0:
                return self.name + " ran out of PP, Please use other moves."
            else:
                damage = ((((2 * user_pokemon.level / 5) + 2) * 50 * (
                        user_pokemon.attack / rival_pokemon.defense) / 50) + 2)
                rival_pokemon.set_hp(rival_pokemon.hp - damage)
                user_pokemon.set_hp(user_pokemon.hp - (damage / 2))
                return str(user_pokemon.name + " used Struggle on " + rival_pokemon.name + " for " + str(
                    damage) + " damage and took " + str(damage / 2) + " damage as a recoil.")


class SpecialMove(Move):
    def __init__(self,name,power,max_pp):
        super().__init__(name,power,max_pp)

    def use(self,user_pokemon,rival_pokemon):
        message = super().use(user_pokemon,rival_pokemon)
        if self.pp > 0:
            damage = ( (((2*user_pokemon.level/5)+2) *self.power*(user_pokemon.special_attack / rival_pokemon.special_defense) /50)+2  )
            rival_pokemon.set_hp(rival_pokemon.hp - damage)
            self.pp -= 1
            message =  str(user_pokemon.name+" used "+self.name+" on "+rival_pokemon.name+" for "+str(damage)+" damage.")
        return message


class PhysicalMove(Move):
    def __init__(self,name,power,max_pp):
        super().__init__(name,power,max_pp)

    def use(self,user_pokemon,rival_pokemon):
        message = super().use(user_pokemon, rival_pokemon)
        if self.pp > 0:
            damage = ( (((2*user_pokemon.level/5)+2) *self.power*(user_pokemon.attack / rival_pokemon.defense) /50)+2  )
            rival_pokemon.set_hp(rival_pokemon.hp - damage)
            self.pp -= 1
            message =  str(user_pokemon.name+" used "+self.name+" on "+rival_pokemon.name+" for "+str(damage)+" damage.")
        return message











