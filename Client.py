from socket import *
import _pickle as pickle

serverName = "localhost"
serverPort = 12001
selectHero = ""
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
waiting = False
while 1:
    command = input("Enter your command: ")
    if(command == exit):
        break
    else:
        clientSocket.sendto(command.encode(),(serverName,serverPort))
    response = clientSocket.recv(2048).decode()
    print(response)
    # # before hero selection
    # while not selectHero:
    #     hero = input('choose your hero :')
    #     clientSocket.send(pickle.dumps({
    #         'user': selectHero,
    #         'command': ['select-hero', hero]
    #     }))
    #     response = pickle.loads(clientSocket.recv(2048))
    #     selectHero = response['user']
    #     if not selectHero:
    #         print("{} is unavailable".format(hero))
    #     else:
    #         print("You are selecting '{}'".format(hero))
    #         data = response['data']
    #         print(data)
    # # waiting for server response
    # if waiting:
    #     response = pickle.loads(clientSocket.recv(2048))
    #     if response['status'] == 'death':
    #         clientSocket.send(pickle.dumps({
    #             'user': '',
    #             'command': ['exit']
    #         }))
    #         break
    #     elif response['status'] == 'fighting':
    #         print(response)
    #     else:
    #         print(response['user'], response['status'])
    #         print(response['enemy'], response['enemyStatus'])
    #     waiting = 0
    #
    # # get command
    # command = input('{} :'.format(selectHero))
    # command = command.split(" ")
    # # send command to server
    # clientSocket.send(pickle.dumps({
    #     'user': selectHero,
    #     'command': command
    # }))
    # if command[0] == 'exit':
    #     break
    # # response
    # response = pickle.loads(clientSocket.recv(2048))
    # if 'error' in response.keys():
    #     print(response['error'])
    # else:
    #     print('Server said:', response['user'])
    #     if command[0] == 'find':
    #         print(response[command[1]])
    #     if command[0] == 'ask':
    #         print(response['answer'], 'for', response['target'])
    #         if (response['answer'] == "wait"):
    #             waiting = 1
    #             print(response)
    #     if command[0] == 'atk':
    #         print(response)
    #         waiting = 1
    #         if response['enemyStatus'] == 'death':
    #             waiting = 0
clientSocket.close()
