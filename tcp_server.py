from socket import *
import _pickle as pickle
import threading as thread


def send_error(client, user, code, msg):
    client.send(pickle.dumps({
        'user': user,
        'status code': code,
        'error': msg
    }))


def run(connectionSocket, addr):
    try:
        while 1:
            request = pickle.loads(connectionSocket.recv(2048))
            command = request['command']
            print(command)
            if command[0] == 'select-hero':
                if (command[1] in heroes and not heroes[command[1]]['connection']):
                    heroes[command[1]]['connection'] = connectionSocket
                    connectionSocket.send(pickle.dumps({
                        'user': command[1],
                        'status code': 200,
                        'data': heroes[command[1]]['status']
                    }))
                elif command[1] in heroes and heroes[command[1]]['connection']:
                    connectionSocket.send(pickle.dumps({
                        'user': '',
                        'status code': 403,
                        'error': 'This user is unavailable'
                    }))
                else:
                    connectionSocket.send(pickle.dumps({
                        'user': '',
                        'status code': 404,
                        'error': 'User is not found'
                    }))
            elif command[0] == 'find':
                if len(command) != 2:
                    send_error(connectionSocket,
                               request['user'], 400, 'command is incomplete')
                elif (command[1] == 'enemy'):
                    enemies = [key for key, val in heroes.items(
                    ) if key != request['user'] and val['connection']]
                    if len(enemies):
                        connectionSocket.send(pickle.dumps({
                            'user': request['user'],
                            'status code': 200,
                            'enemy': enemies
                        }))
                    else:
                        connectionSocket.send(pickle.dumps({
                            'user': request['user'],
                            'status code': 204,
                            'enemy': enemies,
                        }))
                else:
                    send_error(connectionSocket,
                               request['user'], 403, 'Unknown command')
            elif command[0] == 'ask':
                if len(command) != 3:
                    send_error(connectionSocket,
                               request['user'], 400, 'command is incomplete')
                elif len(command) and command[2] == 'fight':
                    if command[1] in heroes.keys():
                        if heroes[command[1]]['connection']:
                            if command[1] == request['user']:
                                send_error(
                                    connectionSocket, request['user'], 403, 'Target cannot be yourself')
                            else:
                                connectionSocket.send(pickle.dumps({
                                    'user': request['user'],
                                    'status code': 200,
                                    'answer': 'wait',
                                    'target': command[1]
                                }))
                                heroes[request['user']
                                       ]['fightingWith'] = command[1]
                                heroes[request['user']]['waiting'] = 1

                                if heroes[command[1]]['waiting'] and heroes[command[1]]['fightingWith'] == request['user']:
                                    heroes[command[1]]['waiting'] = 0
                                    heroes[request['user']]['waiting'] = 0
                                    if heroes[request['user']]['status']['spd'] > heroes[command[1]]['status']['spd']:
                                        connectionSocket.send(pickle.dumps({
                                            'user': request['user'],
                                            'status code': 200,
                                            'status': 'fighting',
                                            'target': command[1]
                                        }))
                                    else:
                                        heroes[command[1]]['connection'].send(pickle.dumps({
                                            'user': command[1],
                                            'status code': 200,
                                            'status': 'fighting',
                                            'target': request['user']
                                        }))
                        else:
                            send_error(connectionSocket,
                                       request['user'], 403, 'Enemy is offline')
                    else:
                        send_error(connectionSocket,
                                   request['user'], 404, 'Enemy is not found')
                else:
                    send_error(connectionSocket,
                               request['user'], 403, 'Unknown command')
            elif command[0] == 'atk':
                if len(command) != 2:
                    send_error(connectionSocket,
                               request['user'], 403, 'command is incomplete')
                elif heroes[heroes[request['user']]['fightingWith']]['fightingWith'] != request['user']:
                    send_error(connectionSocket, request['user'], 400, 'Unable to attakc this user')
                else:
                    hero = heroes[request['user']]
                    if command[1] in hero['skills']:
                        enemy = heroes[hero['fightingWith']]
                        enemy['status']['hp'] -= hero['status']['atk'] * \
                            hero['skills'][command[1]]
                        if enemy['status']['hp'] < 0:
                            enemy['status']['hp'] = 0
                            enemy['connection'].send(pickle.dumps({
                                'user': hero['fightingWith'],
                                'status': 'death'
                            }))
                            connectionSocket.send(pickle.dumps({
                                'user': request['user'],
                                'status': hero['status'],
                                'enemyStatus': 'death'
                            }))
                            del enemy
                        else:
                            enemy['connection'].send(pickle.dumps({
                                'user': hero['fightingWith'],
                                'status': enemy['status'],
                                'enemy': request['user'],
                                'enemyStatus': hero['status']
                            }))
                            connectionSocket.send(pickle.dumps({
                                'user': request['user'],
                                'status': hero['status'],
                                'enemy': hero['fightingWith'],
                                'enemyStatus': enemy['status']
                            }))
                    else:
                        send_error(
                            connectionSocket, request['user'], 404, 'This skill is not found')
            elif command[0] == 'exit':
                break
            else:
                send_error(connectionSocket,
                           request['user'], 403, 'Unknown command')
    finally:
        if (request['user'] in heroes):
            print(heroes[request['user']])
            heroes[request['user']]['connection'] = 0
            heroes[request['user']]['fightingWith'] = '',
            heroes[request['user']]['waiting'] = 0
        connectionSocket.close()


serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('server is starting')
heroes = {
    'job': {
        'status': {
            'atk': 1.99,
            'hp': 12,
            'spd': 2,
        },
        'skills': {
            "tackle": 1,
            "headbutt": 1.25,
        },
        'connection': 0,
        'fightingWith': '',
        'waiting': 0,
    },
    'ker': {
        'status': {
            'atk': 3000,
            'hp': 2,
            'spd': 1,
        },
        'skills': {
            'fire-blast': 20,
            'hydro-pump': 30,
            'tackle': 1
        },
        'connection': 0,
        'fightingWith': '',
        'waiting': 0,
    },
    'yo': {
        'status': {
            'atk': 900000,
            'hp': 9000000,
            'spd': 5000,
        },
        'skills': {
            'tackle': 1,
            'hyper-beam': 99999
        },
        'connection': 0,
        'fightingWith': '',
        'waiting': 0,
    }
}
while 1:
    c, a = serverSocket.accept()
    thread._start_new_thread(run, (c, a))
