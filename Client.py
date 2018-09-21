from socket import *
import _pickle as pickle

serverName = "localhost"
serverPort = 12001
selectHero = ""
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
waiting = False
in_battle = False
exited = False
while 1:
    # while not in_battle:
    #     command = input("Enter your command: ")
    #     if command == '':
    #         command = "Refresh"
    #     clientSocket.sendto(command.encode(), (serverName, serverPort))
    #     response = clientSocket.recv(2048).decode()
    #     response_list = response.split()
    #     status_code = response_list[0]
    #     if status_code == "600":
    #         exited = True
    #         break
    #     if status_code =="900":
    #         print()
    #     elif status_code == "200" :
    #         print(response)
    #         in_battle = True
    #         break
    #     elif status_code == "202":
    #         print(response)
    #         in_battle = True
    #         waiting = True
    #         break
    #     elif int(status_code) >= 400 and int(status_code) < 500:
    #         print(response)
    #         print("Please re enter your command")
    #         print(">>>>", sep='')
    #     else:
    #         print(response)
    while waiting:
        #clientSocket.settimeout(10)
        #try:
            print("Waiting for another Trainer")
            response = clientSocket.recv(2048).decode()
            print(response)
            response_list = response.split()
            status_code = response_list[0]
            if("202" == status_code):
                pass
            else:
                waiting = False
        # except:
        #      clientSocket.send("reject".encode())
        #      waiting = False

    command = input("Enter your command: ")
    # if command == '':
    #     command = "Refresh"
    clientSocket.sendto(command.encode(), (serverName, serverPort))
    response = clientSocket.recv(2048).decode()
    if "challenged by" in response:
        print(response)
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
        print("Please re enter your command\n>>>>",sep='')
        #print("",sep='')
    elif status_code == "600":
        break
    # elif status_code == "900":
    #     print()
    else:
        print(response)

clientSocket.close()
