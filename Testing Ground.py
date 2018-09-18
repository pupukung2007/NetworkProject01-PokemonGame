from Pokemon import *
from Move import *
from Trainer import *
from Item import *

job = Trainer("Job",
              Pokemon("Rayquaza",50,165,139,85,139,85,90,
                            SpecialMove("Dragon Pulse",85,10),
                            SpecialMove("Air Slash",75,15),
                            PhysicalMove("Outrage",120,10),
                            SpecialMove("Dragon Ascent",120,5)
                      ),
              3000)

poon = Trainer("Poon",
              Pokemon("Deoxys",50,110,139,49,139,49,139,
                        SpecialMove("Psychic", 90, 10),
                        SpecialMove("Psycho Boost", 140, 5),
                        PhysicalMove("Zen Headbutt", 80, 15),
                        SpecialMove("Hyper Beam", 150, 5)
                      ),
              3000)
#Test Buy item
print(poon.buy_item(HPHealItem("Potion",20,),1,100))
print(poon.buy_item(HPHealItem("Potion",20,),1,100))
print("Poon has "+str(poon.items[0].amount_in_bag)+" "+poon.items[0].name)
print(poon.buy_item(PPHealItem("PP restore",10),3,100))
print("Poon has "+str(poon.items[1].amount_in_bag)+" "+poon.items[1].name)
print("Poon has "+str(poon.money)+" Poke left")

