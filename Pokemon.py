from Move import SpecialMove
MAX_LEVEL = 100
# MAX_STAT = 255
# MIN_STAT = 0


class Pokemon:
    def __init__(self, name, level, max_hp, attack, defense, special_attack,special_defense,speed,move1,move2,move3,move4):
        if level >= MAX_LEVEL:
            level = MAX_LEVEL
        if level < 1:
            level = 1
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.required_exp = level*level*level
        self.exp = 0
        self.moves = [move1,move2,move3,move4]

    def gain_exp(self,exp):
        message = self.name+" has gained "+str(exp)+" Exp."
        pre_gained_level = self.level
        self.exp += exp
        while self.exp >= self.required_exp and self.level < MAX_LEVEL:
            self.level += 1
            self.set_hp(self.hp+3)
            self.max_hp += 3
            self.attack += 3
            self.defense += 3
            self.special_attack += 3
            self.special_defense += 3
            self.speed += 3
            self.exp -= self.required_exp
            self.required_exp = self.level*self.level*self.level
        if(self.level != pre_gained_level):
            message+= "\n"+self.name+" has grown to level "+str(self.level)+"!\n"
        return message

    def use_move(self,move_slot,other):
        move_slot -= 1
        if(move_slot <0 or move_slot>3):
            return "400 There is no move "+str(move_slot)
        else:
            if not self.is_fainted():
                return self.moves[move_slot].use(self,other)
            else:
                return self.name+" is already knocked out. It can't use any move!"
    def use_move_name(self,name,other):
        found = False
        for i in range(len(self.moves)):
            if name == self.moves[i].name:
                found = True
                return self.moves[i].use(self,other)
        if not found:
            return "404 Move not found"

    def set_hp(self, amount):
        self.hp = amount
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def is_fainted(self):
        if self.hp == 0:
            return True
        else:
            return False
#Test
# p1 = Pokemon("Rayquaza",1,1,1,1,1,1,1,SpecialMove("Dragon Ascent",100,1),SpecialMove("2",200,1),SpecialMove("3",300,0),SpecialMove("4",400,0))
# p2 = Pokemon("Suicune",1,1,1,1,1,1,1,SpecialMove("1",100,0),SpecialMove("2",200,0),SpecialMove("3",300,0),SpecialMove("4",400,0))
#
# print(p1.use_move(1,p2))
# print(p1.use_move(2,p2))

