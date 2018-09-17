from socket import *
import _pickle as pickle
serverName = "localhost"
serverPort = 12001
selectHero = ""
while 1:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    if not selectHero:
        hero = input('choose your hero :')
        clientSocket.send(pickle.dumps({
            'user': selectHero,
            'command':['select-hero',hero]
            }))
        response = pickle.loads( clientSocket.recv(1024))
        selectHero = response['user']
        if not selectHero:
            print("{} is unavailable".format(hero))
        else:
            print("You are selecting '{}'".format(hero))
            data = response['data']
            print(data)
        continue
    
        
    #connect
    command = input('{} :'.format(selectHero))
    command = command.split(" ")
    clientSocket.send(pickle.dumps({
        'user': selectHero,
        'command': command
    }))
    response = pickle.loads(clientSocket.recv(1024))
    print('Server said:', response['user'])
    if command[0] == 'find':
        print(response[command[1]])
    if command[0] == 'exit':
        break
    clientSocket.close()
