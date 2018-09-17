from Special_Move import Special_Move
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
        self.move1 = move1
        self.move2 = move2
        self.move3 = move3
        self.move4 = move4
        self.is_poisoned = False
        self.is_burned = False
        self.is_frozen = False
        self.is_paralyzed = False
        self.is_asleep = False

    def level_up(self):
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

    def use_move1(self, other):
        if not self.is_fainted():
            return self.move1.use(self,other)

    def use_move2(self, other):
        if not self.is_fainted():
            return self.move2.use(self,other)

    def use_move3(self, other):
        if not self.is_fainted():
            return self.move3.use(self,other)

    def use_move4(self, other):
        if not self.is_fainted():
            return self.move4.use(self,other)

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

p1 = Pokemon("Rayquaza",1,1,1,1,1,1,1,Special_Move("Dragon Ascent",100,'n1'),Special_Move("2",200,'n2'),Special_Move("3",300,'n3'),Special_Move("4",400,'n4'))
p2 = Pokemon("Suicune",1,1,1,1,1,1,1,Special_Move("1",100,'n1'),Special_Move("2",200,'n2'),Special_Move("3",300,'n3'),Special_Move("4",400,'n4'))

print(p1.use_move1(p2))

