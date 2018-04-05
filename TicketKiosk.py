import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.connect(("localhost", 8000))

while True:
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
                message = ticketType + ":" + numTickets
                serverSocket.sendall(message.encode())
                receipt = serverSocket.recv(1024).decode()
                print(receipt)
                succeeded, numTickets = receipt.split(":", 1)
                print(succeeded)

                if succeeded == "success":
                    print("Purchased " + numTickets + " " + ticketType + " tickets.")
                else:
                    print("Not enough tickets remaining to purchase " + numTickets + " tickets.")