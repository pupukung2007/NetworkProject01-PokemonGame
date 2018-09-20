from socket import *
import _pickle as pickle
import threading as thread
from Pokemon import *
from Trainer import *
from Item import *
from Move import *

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('server is starting')
trainers = []
trainers.append(Trainer("Job",
                        Pokemon("Charmander",5,19,11,9,9,10,11,
                                PhysicalMove("Scratch",40,35),
                                SpecialMove("Ember",40,25),
                                PhysicalMove("Fire Fang",65,15),
                                SpecialMove("Inferno",100,5)),
                        3000
                        )
                )
trainers.append(Trainer("Poon",
                        Pokemon("Squirtle",5,19,11,11,9,11,9,
                                PhysicalMove("Tackle",40,35),
                                SpecialMove("Water Gun",40,25),
                                SpecialMove("Water Pulse",60,20),
                                SpecialMove("Hydro Pump",110,5)),
                        3000
                        )
                )
trainers[0].buy_item(HPHealItem("Potion",20),5,0)
trainers[1].buy_item(HPHealItem("Potion",20),5,0)
trainers[0].buy_item(PPHealItem("Elixir",20),5,0)
trainers[1].buy_item(PPHealItem("Elixir",20),5,0)


def run(connectionSocket, addr):
    try:
        selected_trainer = Trainer("None",
                                   Pokemon("None",0,0,0,0,0,0,0,
                                            SpecialMove("None",0,0),
                                            SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0)
                                           ),
                                   0)
        while True:
            request = connectionSocket.recv(2048).decode()
            command = request.split()
            print(command)
            if command[0] == "continue":
                if(len(command)!=3):
                    response = "400 Unknown command"
                    connectionSocket.send(response.encode())
                elif selected_trainer.enemy.name != "None":
                    connectionSocket.send("403 You can't use this command while in a battle with another trainer".encode())
                else:
                    if command[1] == "as":
                        if selected_trainer.name != "None":
                            response = "403 You are already logged in as " + selected_trainer.name
                            connectionSocket.send(response.encode())
                        else:
                            user_found = False
                            for i in range(len(trainers)):
                                if (command[2] == trainers[i].name):
                                    if trainers[i].is_online:
                                        response = "403 This user is already online"
                                        user_found = True
                                        connectionSocket.send(response.encode())
                                    else:
                                        selected_trainer = trainers[i]
                                        user_found = True
                                        trainers[i].is_online = True
                                        trainers[i].connectionSocket = connectionSocket
                                        response = "200 Welcome back " + command[2] + "!" +"\nPokemon: "+trainers[i].pokemon.name+" Lvl: "+str(trainers[i].pokemon.level)+"\nMoney: "+str(trainers[i].money)
                                        connectionSocket.send(response.encode())
                            if not user_found:
                                response = "404 Trainer not found"
                                connectionSocket.send(response.encode())
                    else:
                        response = "400 Unknown command"
                        connectionSocket.send(response.encode())


            elif command[0] == "view" :
                if(len(command)!=2):
                    response = "400 Unknown command"
                    connectionSocket.send(response.encode())
                elif selected_trainer.enemy.name != "None":
                    connectionSocket.send("403 You can't use this command while in a battle with another trainer".encode())
                else:
                    if(command[1] == "player"):
                        if selected_trainer.name == "None":
                            response = "428 Please select your trainer before using this command\n" + "(Select player by using command <continue as (trainer name)>)"
                            connectionSocket.send(response.encode())
                        else:
                            response = "200 \nCurrently Online Players: \n"
                            for i in range(len(trainers)):
                                if (trainers[i].is_online):
                                    response += trainers[i].name + "\n"
                            connectionSocket.send(response.encode())
                    else:
                        response = "400 Unknown command"
                        connectionSocket.send(response.encode())
            
            elif command[0] == "challenge":
                if selected_trainer.name == "None":
                    response = "428 Please select your trainer before using this command\n" + "(Select player by using command <continue as (trainer name)>)"
                    connectionSocket.send(response.encode())
                elif selected_trainer.enemy.name != "None":
                    connectionSocket.send("403 You can't use this command while in a battle with another trainer".encode())
                else:
                    if (len(command) != 2):
                        connectionSocket.send("400 Unknown command".encode())
                    else:
                        if (command[1] == selected_trainer.name):
                            connectionSocket.send("403 You can't challenge yourself".encode())
                        else:
                            user_found = False
                            for i in range(len(trainers)):
                                if (command[1] == trainers[i].name):
                                    user_found = True
                                    if trainers[i].is_online:
                                        if not trainers[i].is_in_battle():
                                            selected_trainer.enemy = trainers[i]
                                            # for j in range(len(trainers)):
                                            #     if selected_trainer.name == trainers[j].name:
                                            #         trainers[j].enemy = trainers[i]
                                            trainers[i].enemy = selected_trainer
                                            response = "300 You challenged Trainer " + command[
                                                    1] + " to a Pokemon battle" + "\n"+display_battle_info(selected_trainer,selected_trainer.enemy)
                                            connectionSocket.send(response.encode())

                                            challenge_message = "301 You are challenged by Trainer " + selected_trainer.name + "\n"+display_battle_info(selected_trainer.enemy,selected_trainer)
                                            trainers[i].connectionSocket.send(challenge_message.encode())

                                        else:
                                            connectionSocket.send("403 This Trainer is currently in battle with another trainer".encode())
                                    else:
                                        connectionSocket.send("403 This Trainer is currently offline".encode())
                            if not user_found:
                                connectionSocket.send("404 Trainer not found".encode())

            elif command[0] == "use":
                if selected_trainer.name == "None":
                    response = "428 Please select your trainer before using this command\n" + "(Select player by using command <continue as (trainer name)>)"
                    connectionSocket.send(response.encode())
                elif selected_trainer.enemy.name == "None":
                    connectionSocket.send("403 You have to challenge another player before using this command".encode())
                elif len(command)<3:
                    response = "400 Unknown command"
                    connectionSocket.send(response.encode())
                else:
                    if command[1] == "move":
                        if command[2].isalpha(): #Use move (movename)
                            move_name = ""
                            for i in range (2,len(command)):
                                move_name += command[i]+" "
                            move_name = move_name.strip()
                            response = selected_trainer.pokemon.use_move_name(move_name,selected_trainer.enemy.pokemon)
                            if "403" in response or "404" in response or "400" in response:
                                connectionSocket.send(response.encode())
                            elif "306" in response: #Battle Ends
                                #Decide Winner and give rewards
                                if selected_trainer.pokemon.hp == 0:
                                    response += selected_trainer.enemy.name+" has won the battle and recieve 1000 poke"
                                    selected_trainer.enemy.money+=1000
                                else:
                                    response += selected_trainer.name + " has won the battle and recieve 1000 poke"
                                    selected_trainer.money += 1000
                                connectionSocket.send(response.encode())
                                selected_trainer.enemy.connectionSocket.send(response.encode())
                                #Restore HP,PP and Enemy Status to default
                                selected_trainer.heal_pokemon()
                                selected_trainer.enemy.heal_pokemon()
                                selected_trainer.enemy.enemy = NoTrainer("None")
                                selected_trainer.enemy = NoTrainer("None")
                                #Update Trainers
                                for i in range(len(trainers)):
                                    if trainers[i].name == selected_trainer.name:
                                        trainers[i] = selected_trainer
                                    elif trainers[i].name == selected_trainer.enemy.name:
                                        trainers[i] = selected_trainer.enemy
                                    else:
                                        continue
                            else:
                                connectionSocket.send(("202 "+response+"\n"+display_battle_info(selected_trainer,selected_trainer.enemy)).encode())
                                selected_trainer.enemy.connectionSocket.send(("200 "+response+"\n"+display_battle_info(selected_trainer.enemy,selected_trainer)).encode())
                        elif command[2].isnumeric(): #Use move (moveslot):
                            response = selected_trainer.pokemon.use_move(int(command[2]), selected_trainer.enemy.pokemon)
                            if "403" in response or "404" in response or "400" in response :
                                connectionSocket.send(response.encode())
                            elif "306" in response:  # Battle Ends
                                # Decide Winner and give rewards
                                if selected_trainer.pokemon.hp == 0:
                                    response += selected_trainer.enemy.name + " has won the battle and recieve 1000 poke"
                                    selected_trainer.enemy.money += 1000
                                else:
                                    response += selected_trainer.name + " has won the battle and recieve 1000 poke"
                                    selected_trainer.money += 1000
                                connectionSocket.send(response.encode())
                                selected_trainer.enemy.connectionSocket.send(response.encode())
                                # Restore HP,PP and Enemy Status to default
                                selected_trainer.heal_pokemon()
                                selected_trainer.enemy.heal_pokemon()
                                selected_trainer.enemy.enemy = NoTrainer("None")
                                selected_trainer.enemy = NoTrainer("None")
                                # Update Trainers
                                for i in range(len(trainers)):
                                    if trainers[i].name == selected_trainer.name:
                                        trainers[i] = selected_trainer
                                    elif trainers[i].name == selected_trainer.enemy.name:
                                        trainers[i] = selected_trainer.enemy
                                    else:
                                        continue
                            else:
                                connectionSocket.send(("202 " + response + "\n" + display_battle_info(selected_trainer,
                                                                                                      selected_trainer.enemy)).encode())
                                selected_trainer.enemy.connectionSocket.send(("200 " + response + "\n" + display_battle_info( selected_trainer.enemy,selected_trainer)).encode())

                    #Use item
                    elif command[1] == "item":
                        if command[2].isalpha():  # Use item (itemname)
                            item_name = ""
                            for i in range(2, len(command)):
                                item_name += command[i] + " "
                            item_name = item_name.strip()
                            response = selected_trainer.use_item_name(item_name)
                            if "403" in response or "404" in response or "400" in response:
                                connectionSocket.send(response.encode())
                            else:
                                connectionSocket.send(("202 " + response + "\n" + display_battle_info(selected_trainer,
                                                                                                      selected_trainer.enemy)).encode())
                                selected_trainer.enemy.connectionSocket.send((
                                                                                         "200 " + response + "\n" + display_battle_info(
                                                                                     selected_trainer.enemy,
                                                                                     selected_trainer)).encode())
                        elif command[2].isnumeric():  # Use item (itemslot):
                            response = selected_trainer.use_item(int(command[2]))
                            if "403" in response or "404" in response or "400" in response:
                                connectionSocket.send(response.encode())
                            else:
                                connectionSocket.send(("202 " + response + "\n" + display_battle_info(selected_trainer,
                                                                                                      selected_trainer.enemy)).encode())
                                selected_trainer.enemy.connectionSocket.send((
                                                                                         "200 " + response + "\n" + display_battle_info(
                                                                                     selected_trainer.enemy,
                                                                                     selected_trainer)).encode())
                    else:
                         connectionSocket.send("400 Unknown command".encode())
            elif command[0] == "Refresh":
                 connectionSocket.send("900 ".encode())
            else:
                response = "400 Unknown command"
                connectionSocket.send(response.encode())
    finally:
        for i in range(len(trainers)):
            if selected_trainer.name == trainers[i].name:
                trainers[i].is_online = False
                trainers[i].connectionSocket = 0
                trainers[i].enemy = NoTrainer("None")
        selected_trainer = Trainer("None",
                                   Pokemon("None", 0, 0, 0, 0, 0, 0, 0,
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0)
                                           ),
                                   0)

        connectionSocket.close()

def display_battle_info(trainer,enemy):
    info = trainer.pokemon.name+" HP: "+str(trainer.pokemon.hp)+"/"+str(trainer.pokemon.max_hp)+"\n"+enemy.pokemon.name + " HP: " + str(enemy.pokemon.hp) + "/" + str(enemy.pokemon.max_hp)+"\n"
    for i in range(len(trainer.pokemon.moves)):
        info += "Move"+str(i+1)+": "+trainer.pokemon.moves[i].name+"       PP: "+str(trainer.pokemon.moves[i].pp)+"\n"
    for i in range(len(trainer.items)):
        info += trainer.items[i].display_description()
    return info

while 1:
    c, a = serverSocket.accept()
    thread._start_new_thread(run, (c, a))





