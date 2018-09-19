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
                                        connectionSocket.send(response.encode())
                                    else:
                                        selected_trainer = trainers[i]
                                        user_found = True
                                        trainers[i].is_online = True
                                        trainers[i].connectionSocket = connectionSocket
                                        response = "200 Welcome " + command[2] + "!"
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
                else:
                    if (len(command) != 2):
                        connectionSocket.send("400 Unknown command".encode())
                    else:
                        if (command[1] == selected_trainer.name):
                            connectionSocket.send("403 You can't challenge yourself")
                        else:
                            user_found = False
                            for i in range(len(trainers)):
                                if (command[1] == trainers[i].name):
                                    user_found = True
                                    if trainers[i].is_online:
                                        response = "200 Challenging Trainer "+command[1]
                                        connectionSocket.send(response.encode())
                                        challenge_message = "300 You are challenged by Trainer "+selected_trainer.name
                                        trainers[i].connectionSocket.send(challenge_message.encode())
                                    else:
                                        connectionSocket.send("403 This Trainer is currently offline".encode())
                            if not user_found:
                                connectionSocket.send("404 Trainer not found".encode())


                    

            else:
                response = "400 Unknown command"
                connectionSocket.send(response.encode())
    finally:
        for i in range(len(trainers)):
            if selected_trainer.name == trainers[i].name:
                trainers[i].is_online = False
                trainers[i].connectionSocket = 0
        selected_trainer = Trainer("None",
                                   Pokemon("None", 0, 0, 0, 0, 0, 0, 0,
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0),
                                           SpecialMove("None", 0, 0)
                                           ),
                                   0)

        connectionSocket.close()




    #         if command[0] == 'select-hero':
    #             if (command[1] in heroes and not heroes[command[1]]['connection']):
    #                 heroes[command[1]]['connection'] = connectionSocket
    #                 connectionSocket.send(pickle.dumps({
    #                     'user': command[1],
    #                     'status code': 200,
    #                     'data': heroes[command[1]]['status']
    #                 }))
    #             elif command[1] in heroes and heroes[command[1]]['connection']:
    #                 connectionSocket.send(pickle.dumps({
    #                     'user': '',
    #                     'status code': 403,
    #                     'error': 'This user is unavailable'
    #                 }))
    #             else:
    #                 connectionSocket.send(pickle.dumps({
    #                     'user': '',
    #                     'status code': 404,
    #                     'error': 'User is not found'
    #                 }))
    #         elif command[0] == 'find':
    #             if len(command) != 2:
    #                 send_error(connectionSocket,
    #                            request['user'], 400, 'command is incomplete')
    #             elif (command[1] == 'enemy'):
    #                 enemies = [key for key, val in heroes.items(
    #                 ) if key != request['user'] and val['connection']]
    #                 if len(enemies):
    #                     connectionSocket.send(pickle.dumps({
    #                         'user': request['user'],
    #                         'status code': 200,
    #                         'enemy': enemies
    #                     }))
    #                 else:
    #                     connectionSocket.send(pickle.dumps({
    #                         'user': request['user'],
    #                         'status code': 204,
    #                         'enemy': enemies,
    #                     }))
    #             else:
    #                 send_error(connectionSocket,
    #                            request['user'], 403, 'Unknown command')
    #         elif command[0] == 'ask':
    #             if len(command) != 3:
    #                 send_error(connectionSocket,
    #                            request['user'], 400, 'command is incomplete')
    #             elif len(command) and command[2] == 'fight':
    #                 if command[1] in heroes.keys():
    #                     if heroes[command[1]]['connection']:
    #                         if command[1] == request['user']:
    #                             send_error(
    #                                 connectionSocket, request['user'], 403, 'Target cannot be yourself')
    #                         else:
    #                             connectionSocket.send(pickle.dumps({
    #                                 'user': request['user'],
    #                                 'status code': 200,
    #                                 'answer': 'wait',
    #                                 'target': command[1]
    #                             }))
    #                             heroes[request['user']
    #                                    ]['fightingWith'] = command[1]
    #                             heroes[request['user']]['waiting'] = 1
    #
    #                             if heroes[command[1]]['waiting'] and heroes[command[1]]['fightingWith'] == request['user']:
    #                                 heroes[command[1]]['waiting'] = 0
    #                                 heroes[request['user']]['waiting'] = 0
    #                                 if heroes[request['user']]['status']['spd'] > heroes[command[1]]['status']['spd']:
    #                                     connectionSocket.send(pickle.dumps({
    #                                         'user': request['user'],
    #                                         'status code': 200,
    #                                         'status': 'fighting',
    #                                         'target': command[1]
    #                                     }))
    #                                 else:
    #                                     heroes[command[1]]['connection'].send(pickle.dumps({
    #                                         'user': command[1],
    #                                         'status code': 200,
    #                                         'status': 'fighting',
    #                                         'target': request['user']
    #                                     }))
    #                     else:
    #                         send_error(connectionSocket,
    #                                    request['user'], 403, 'Enemy is offline')
    #                 else:
    #                     send_error(connectionSocket,
    #                                request['user'], 404, 'Enemy is not found')
    #             else:
    #                 send_error(connectionSocket,
    #                            request['user'], 403, 'Unknown command')
    #         elif command[0] == 'atk':
    #             if len(command) != 2:
    #                 send_error(connectionSocket,
    #                            request['user'], 403, 'command is incomplete')
    #             elif heroes[heroes[request['user']]['fightingWith']]['fightingWith'] != request['user']:
    #                 send_error(connectionSocket, request['user'], 400, 'Unable to attack this user')
    #             else:
    #                 hero = heroes[request['user']]
    #                 if command[1] in hero['skills']:
    #                     enemy = heroes[hero['fightingWith']]
    #                     enemy['status']['hp'] -= hero['status']['atk'] * \
    #                         hero['skills'][command[1]]
    #                     if enemy['status']['hp'] < 0:
    #                         enemy['status']['hp'] = 0
    #                         enemy['connection'].send(pickle.dumps({
    #                             'user': hero['fightingWith'],
    #                             'status': 'death'
    #                         }))
    #                         connectionSocket.send(pickle.dumps({
    #                             'user': request['user'],
    #                             'status': hero['status'],
    #                             'enemyStatus': 'death'
    #                         }))
    #                         del enemy
    #                     else:
    #                         enemy['connection'].send(pickle.dumps({
    #                             'user': hero['fightingWith'],
    #                             'status': enemy['status'],
    #                             'enemy': request['user'],
    #                             'enemyStatus': hero['status']
    #                         }))
    #                         connectionSocket.send(pickle.dumps({
    #                             'user': request['user'],
    #                             'status': hero['status'],
    #                             'enemy': hero['fightingWith'],
    #                             'enemyStatus': enemy['status']
    #                         }))
    #                 else:
    #                     send_error(
    #                         connectionSocket, request['user'], 404, 'This skill is not found')
    #         elif command[0] == 'exit':
    #             break
    #         else:
    #             send_error(connectionSocket,
    #                        request['user'], 403, 'Unknown command')
    # finally:
    #     if (request['user'] in heroes):
    #         print(heroes[request['user']])
    #         heroes[request['user']]['connection'] = 0
    #         heroes[request['user']]['fightingWith'] = '',
    #         heroes[request['user']]['waiting'] = 0
    #     connectionSocket.close()

while 1:
    c, a = serverSocket.accept()
    thread._start_new_thread(run, (c, a))

def send_error(client, user, code, msg):
    client.send(pickle.dumps({
        'user': user,
        'status code': code,
        'error': msg
    }))





