MAX_LEVEL = 100
class Pokemon:
    def __init__(this,name,level,maxHP,attack,defense,specialAttack):
        if(level >= MAX_LEVEL):
            level = MAX_LEVEL
        
        if(level < 1):
            level = 1
        
        this.name = name
        this.level = level
        this.maxHP = maxHP
        this.hp = maxHP
        this.attack = attack
        this.defense = defense
        this.specialAttack = specialAttack
        this.requiredExp = (level)*(level)*(level)
        this.exp = 0
        
    def levelUp(this):
        while (this.exp >= this.requiredExp and this.level<MAX_LEVEL):
            this.level+=1
            this.exp -= this.requiredExp;
            this.requiredExp = (this.level)*(this.level)*(this.level);

    def normalAttack(this,other):
      if (not this.isFainted()):
        if(this.attack >= other.defense):
          other.setHP(other.hp-(this.attack-other.defense))
        else:
          other.setHP(other.hp - 10)
        if(other.isFainted()):
          this.exp += other.level*100
        this.levelUp()

    def useSpecialMove(this,other):
      if(not this.isFainted()):
        other.setHP(other.hp-this.specialAttack)
      if(other.isFainted()):
        this.exp += other.level*100
      this.levelUp()
        
    def setHP(this,amount):
      this.hp = amount
      if (this.hp < 0):
        this.hp = 0
      if (this.hp >this.maxHP):
        this.hp = this.maxHP

    def isFainted(this):
        if this.hp == 0:
            return True
        else:
            return False
    def calculateNormalATKDamage(this,other):
      if(this.isFainted()):
        return 0
      if(this.attack >= other.defense):
        return this.attack-other.defense
      else:
        return 10


    
#p1 = Pokemon("Rayquaza",100,500,200,100,250)
#p2 = Pokemon("Something",100,500,10,20,4)
#while ((not p1.isFainted()) and (not p2.isFainted())):
  #p1.normalAttack(p2)
  #print(p2.name+" has received "+str(p1.calculateNormalATKDamage(p2))+" Damage.")
  #p2.normalAttack(p1)
  #print(p1.name+" has received "+str(p2.calculateNormalATKDamage(p1))+" Damage.")
#if(p1.isFainted()):
  #print(p1.name+" has fainted.")
#if(p2.isFainted()):
  #print(p2.name+" has fainted.")



