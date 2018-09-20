from socket import *
import _pickle as pickle

serverName = "localhost"
serverPort = 12001
selectHero = ""
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
waiting = False
in_battle = False
while 1:
    while not in_battle:
        command = input("Enter your command: ")
        if command == '':
            command = "Refresh"
        clientSocket.sendto(command.encode(), (serverName, serverPort))
        response = clientSocket.recv(2048).decode()
        response_list = response.split()
        status_code = response_list[0]
        if status_code =="900":
            print()
        elif status_code == "300" :
            print(response)
            in_battle = True
            break
        elif status_code == "301":
            print(response)
            in_battle = True
            waiting = True
            break
        else:
            print(response)
    if waiting:
        print("Waiting for another Trainer")
        response = clientSocket.recv(2048).decode()
        print(response)
        response_list = response.split()
        status_code = response_list[0]
        #if status_code == "200":
        waiting = False
    command = input("Enter your battle command: ")
    if command == '':
        command = "Refresh"
    clientSocket.sendto(command.encode(), (serverName, serverPort))

    if command == "exit":
        break

    response = clientSocket.recv(2048).decode()
    response_list = response.split()
    status_code = response_list[0]
    if (status_code == "301"):
        while True:
            response = clientSocket.recv(2048).decode()
            response_list = response.split()
            status_code = response_list[0]
            if status_code == "200" or status_code == "202":
                break
    elif status_code == "202": #Other player Turn
        print(response)
        waiting = True
    elif status_code == "200":  # Other player Turn
        print(response)
        waiting = False
    elif status_code == "306":
        print(response)
        print("The battle has ended.")
        in_battle = False
    elif status_code == "900":
        print()
    else:
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
