import socket, threading, time
from _thread import *

numTickets = 50
ticketLock = threading.Lock()
sendTheaterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recvTheaterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def ticketSale(connection):
    global numTickets
    global sendTheaterSocket
    while True:
        data = connection.recv(1024).decode()

        if data:
            currentKiosk, ticketType, num = data.split(":", 2)

            if currentKiosk == "theaterServer":
                print("Request for " + num + " " + ticketType + " tickets forwarded from theater server")
            else:
                print("Request for " + num + " " + ticketType + " tickets received from kiosk #" + currentKiosk)

            num = int(num)

            if ticketType == "play":
                data = "movieServer:" + ticketType + ":" + str(num)
                # time.sleep(5)
                sendTheaterSocket.sendall(data.encode())
                print("Request for " + num + " " + ticketType + " tickets forwarded to theater server")

            else:
                ticketLock.acquire()
                if numTickets >= num:
                    numTickets -= num
                    receipt = "movieServer:success:" + str(num)
                else:
                    receipt = "movieServer:failed:" + str(num)
                ticketLock.release()
            print("im just gonna send it-- " + receipt)
            #time.sleep(5)
            connection.sendall(receipt.encode())
            print("i fokken sent it m8")
        else:
            connection.close()

def Main():
    requestListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requestListener.bind(("", 8000))
    requestListener.listen(1)   # Change later

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