from socket import *
import _pickle as pickle
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("server is starting")
heroes = {
    "job": {
        "atk": 1.99,
        "hp": 12,
        "spd": 2,
    },
    "ker": {
        "atk": 3000,
        "hp": 2,
        "spd": 1
    },
    "yo": {
        "atk": 900000,
        "hp": 9000000,
        "spd":5000
    }
}
while 1:
    connectionSocket, addr = serverSocket.accept()
    # pre-command
    # check login
    # check
    # input command
    request = pickle.loads(connectionSocket.recv(1024))
    command = request["command"]
    # post-command
    print(command)
    if command[0] == "select-hero":
        if (command[1] in heroes):
            connectionSocket.send(pickle.dumps({
                'user': command[1],
                'data': heroes[command[1]]
                }))
        else:
            connectionSocket.send(pickle.dumps({'user':'', 'error': 'This user is not available'}));
    elif command[0] == "find":
        if (command[1] == "enemy"):
            connectionSocket.send(pickle.dumps({
                'user': request['user'],
                'enemy':[key for key, val in heroes.items() if key != request['user']]
                }))
    else:
        connectionSocket.send(pickle.dumps({'user':request['user']}))
    if command[0] == "exit":
        break
    connectionSocket.close()
