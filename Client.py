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
        elif int(status_code) >= 400 and int(status_code) < 500:
            print(response)
            print("Please re enter your command")
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
    elif int(status_code) >= 400 and int(status_code) < 500:
        print(response)
        print("Please re enter your command")
    elif status_code == "900":
        print()
    else:
        print(response)

clientSocket.close()
