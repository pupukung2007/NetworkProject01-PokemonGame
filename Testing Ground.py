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
print("###################################################################")
#Test Pokemon Fight
while(not poon.is_out_of_pokemon() and not job.is_out_of_pokemon()):
    if(poon.pokemon.speed >= job.pokemon.speed):
        ##Poon starts First
        #Display HP
        print("Poon's "+poon.pokemon.name + " HP: "+str(poon.pokemon.hp)+"\nJob's "+job.pokemon.name+" HP: "+str(job.pokemon.hp))
        #Display Move's PP
        for i in range(4):
            print(str(i+1)+". "+poon.pokemon.moves[i].name + " PP: "+str(poon.pokemon.moves[i].pp))
        move_slot = int(input("Which move should Poon's "+poon.pokemon.name+" use? [1-4]: "))
        #Attack with selected move
        print(poon.pokemon.use_move(move_slot,job.pokemon))
        #####Switch Turn#######
        # Display HP
        print("Job's " + job.pokemon.name + " HP: " + str(
            job.pokemon.hp) + "\nPoon's " + poon.pokemon.name + " HP: " + str(poon.pokemon.hp))
        # Display Move's PP
        for i in range(4):
            print(str(i+1) + ". " + job.pokemon.moves[i].name + " PP: " + str(job.pokemon.moves[i].pp))
        move_slot = int(input("Which move should Job's " + job.pokemon.name + " use? [1-4]: "))
        # Attack with selected move
        print(job.pokemon.use_move(move_slot, poon.pokemon))
    else:
        ##Job starts First
        # Display HP
        print("Job's " + job.pokemon.name + " HP: " + str(
            job.pokemon.hp) + "\nPoon's " + poon.pokemon.name + " HP: " + str(poon.pokemon.hp))
        # Display Move's PP
        for i in range(4):
            print(str(i+1) + ". " + job.pokemon.moves[i].name + " PP: " + str(job.pokemon.moves[i].pp))
        move_slot = int(input("Which move should Job's " + job.pokemon.name + " use? [1-4]: "))
        # Attack with selected move
        print(job.pokemon.use_move(move_slot, poon.pokemon))
        #####Switch Turn#######
        # Display HP
        print("Poon's " + poon.pokemon.name + " HP: " + str(
            poon.pokemon.hp) + "\nJob's " + job.pokemon.name + " HP: " + str(job.pokemon.hp))
        # Display Move's PP
        for i in range(4):
            print(str(i+1) + ". " + poon.pokemon.moves[i].name + " PP: " + str(poon.pokemon.moves[i].pp))
        move_slot = int(input("Which move should Poon's " + poon.pokemon.name + " use? [1-4]: "))
        # Attack with selected move
        print(poon.pokemon.use_move(move_slot, job.pokemon))



