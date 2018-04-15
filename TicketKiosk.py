import socket, time, random

theaterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
theaterSocket.connect(("localhost", 8001))

movieSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
movieSocket.connect(("localhost", 8000))

configList = open("config.txt").read().splitlines()

numTickets = configList[0].split(":")[1]

global kioskNum
kioskNum = -1;
message = "kioskhandshake"
theaterSocket.sendall(message.encode())
kioskNum = int(theaterSocket.recv(1024).decode())

if kioskNum < 0:
    print("Handshake failed")

while True:
    if random.randint(1, 2) == 1:
        serverSocket = theaterSocket
    else:
        serverSocket = movieSocket

    ticketType = input("Enter ticket type (\'movie\' or \'play\'), or type \'quit\' to exit: ")

    if ticketType == "quit":
        serverSocket.close()
        break;

    elif ticketType != "movie" and ticketType != "play":
        print("Error: incorrect ticket type")
        continue

    else:
        numTickets = input("Please enter number of tickets: ")

        try:
            int(numTickets)
        except ValueError:
            print("Error: Invalid number of tickets")

        else:
            if int(numTickets) < 0:
                print("Error: Cannot purchase negative number of tickets")
            else:
                message = str(kioskNum) + ":" + ticketType + ":" + str(numTickets)
                serverSocket.sendall(message.encode())
                receipt = serverSocket.recv(1024).decode()
                origin, succeeded, numTickets = receipt.split(":", 2)

                if succeeded == "success":
                    print("Purchased " + numTickets + " " + ticketType + " tickets.")
                else:
                    print("Not enough tickets remaining to purchase " + numTickets + " tickets.")