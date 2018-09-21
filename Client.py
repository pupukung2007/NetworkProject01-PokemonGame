from socket import *
import _pickle as pickle

serverName = "localhost"
serverPort = 12001
selectHero = ""
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
waiting = False
while 1:
    while waiting:
        print("Waiting for another Trainer")
        response = clientSocket.recv(2048).decode()
        print(response)
        response_list = response.split()
        status_code = response_list[0]
        if("202" == status_code):
            pass
        else:
            waiting = False


    command = input("Enter your command: ")

    clientSocket.sendto(command.encode(), (serverName, serverPort))
    response = clientSocket.recv(2048).decode()
    if "challenged by" in response:
        print(response)
        response = clientSocket.recv(2048).decode()
    response_list = response.split()
    status_code = response_list[0]
    if status_code == "202": #Other player Turn
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
        print("Please re enter your command\n>>>>>>>>>>>>>>>>>",sep='')
    elif status_code == "600":
        break
    else:
        print(response)

clientSocket.close()
