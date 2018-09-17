from Move import Move
class Special_Move(Move):
    def __init__(self,name,power,new):
        super().__init__(name,power)


    def use(self,user_pokemon,rival_pokemon):
        damage = ( (((2*user_pokemon.level/5)+2) *self.power*(user_pokemon.special_attack / rival_pokemon.special_defense) /50)+2  )
        rival_pokemon.set_hp(rival_pokemon.hp - damage)
        return str(user_pokemon.name+" uses "+self.name+" on "+rival_pokemon.name+" for "+str(damage)+" damage.")
