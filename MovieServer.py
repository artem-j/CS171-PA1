import socket, threading, time
from _thread import *

numTickets = 50
ticketLock = threading.Lock()
sendTheaterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvTheaterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ticketSale(connection):
    global kioskCounter
    global numTickets

    while True:
        data = connection.recv(1024).decode()

        if data:
            currentKiosk, ticketType, num = data.split(":", 2)

            if currentKiosk == "theaterServer":
                if ticketType == "movie":
                    print("Request for " + num + " tickets received from theater server")
            else:
                print("Request for " + num + " tickets received from kiosk #" + currentKiosk)

            num = int(num)

            if ticketType == "play":
                data = "movieServer:" + ticketType + ":" + str(num)

                #time.sleep(5)
                sendTheaterSocket.sendall(data.encode())
                print("Request for " + str(num) + " tickets forwarded to theater server")

                receipt = sendTheaterSocket.recv(1024).decode()
                connection.sendall(receipt.encode())

            elif ticketType == "movie":
                ticketLock.acquire()

                if numTickets >= num:
                    numTickets -= num
                    receipt = "movieServer:success:" + str(num)
                    print("Sold " + str(num) + " tickets.")
                else:
                    receipt = "movieServer:failed:" + str(num)
                    print("Failed to sell " + str(num) + " tickets.")

                ticketLock.release()

                print(str(numTickets) + " movie tickets remaining.")

                #time.sleep(5)
                connection.sendall(receipt.encode())

            else:
                connection.close()

def Main():
    requestListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requestListener.bind(("", 8000))
    requestListener.listen(1)

    global sendTheaterSocket
    recvTheaterSocket.connect(("localhost", 8001))
    sendTheaterSocket.connect(("localhost", 8001))
    start_new_thread(ticketSale, (recvTheaterSocket,))

    while True:
        connection, address = requestListener.accept()
        start_new_thread(ticketSale, (connection,))

    requestListener.close()

if __name__ == '__main__':
    Main()