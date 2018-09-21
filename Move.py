#จัดทำโดย
#นาย ปิยณัฐ กันเดช 5910401092 หมู่เรียน 1
#นาย ปุญญพัฒน์ ญาณวิสิฏฐ์ 5910401106 หมู่เรียน 1
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
            for i in range(4):
                if(user_pokemon.moves[i].pp > 0):
                    return "403 "+self.name + " ran out of PP, Please use other moves."

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
            if rival_pokemon.is_fainted():
                message = "306 "+rival_pokemon.name+" has fainted\n"
                message += user_pokemon.gain_exp(rival_pokemon.level * rival_pokemon.level * rival_pokemon.level)
            else:
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
            if rival_pokemon.is_fainted():
                message = "306 "+rival_pokemon.name+" has fainted\n"
                message += user_pokemon.gain_exp(rival_pokemon.level*rival_pokemon.level*rival_pokemon.level)
            else:
                message =  str(user_pokemon.name+" used "+self.name+" on "+rival_pokemon.name+" for "+str(damage)+" damage.")
        return message












