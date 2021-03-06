import socket, threading, time
from _thread import *

configList = open("config.txt").read().splitlines()

numTickets = int(configList[0].split(":")[1])

theaterIP = configList[1].split(":")[1]
theaterPort = int(configList[1].split(":")[2])

kioskCounter = 0
ticketLock = threading.Lock()

def ticketSale(connection):
    global kioskCounter
    global numTickets
    closed = True

    while True:
        try:
            data = connection.recv(1024).decode()
            closed = False
        except:
            if closed == False:
            	print("A kiosk has closed its connection")
            closed = True

        if data:
            if data == "kioskhandshake":
                connection.sendall(str(kioskCounter).encode())
                print("Handshake completed with kiosk #" + str(kioskCounter))
                kioskCounter += 1

            else:
                currentKiosk, ticketType, num = data.split(":", 2)

                if currentKiosk == "movieServer":
                    if ticketType == "play":
                        print("Request for " + num + " tickets received from movie server")
                else:
                    print("Request for " + num + " tickets received from kiosk #" + currentKiosk)

                num = int(num)

                if ticketType == "movie":
                    data = "theaterServer:" + ticketType + ":" + str(num)

                    time.sleep(5)
                    sendMovieSocket.sendall(data.encode())
                    print("Request for " + str(num) + " tickets forwarded to movie server")

                    receipt = sendMovieSocket.recv(1024).decode()
                    connection.sendall(receipt.encode())

                elif ticketType == "play":
                    ticketLock.acquire()

                    if numTickets >= num:
                        numTickets -= num
                        receipt = "theaterServer:success:" + str(num)
                        print("Sold " + str(num) + " tickets")
                    else:
                        receipt = "theaterServer:failed:" + str(num)
                        print("Failed to sell " + str(num) + " tickets")

                    ticketLock.release()

                    print(str(numTickets) + " play tickets remaining")

                    time.sleep(5)
                    connection.sendall(receipt.encode())

        else:
            connection.close()

def Main():
    requestListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requestListener.bind((theaterIP, theaterPort))
    requestListener.listen(1)

    global sendMovieSocket
    sendMovieSocket, address = requestListener.accept()
    recvMovieSocket, address = requestListener.accept()
    start_new_thread(ticketSale, (recvMovieSocket,))

    while True:
        connection, address = requestListener.accept()
        start_new_thread(ticketSale, (connection,))

    kioskListener.close()

if __name__ == '__main__':
    Main()
