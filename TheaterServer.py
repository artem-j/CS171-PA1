import socket, threading, time
from _thread import *

numTickets = 50
myLock = threading.Lock()

def ticketSale(connection):
    global numTickets
    while True:
        data = connection.recv(1024).decode()

        if data:
            ticketType, num = data.split(":", 1)
            num = int(num)
            if ticketType is "movie":
                connection.sendall(data.encode())
            else:
                myLock.acquire()
                if numTickets >= num:
                    numTickets -= num
                    receipt = "success:" + str(num)
                else:
                    receipt = "failed:" + str(num)
                time.sleep(5)
                myLock.release()

            connection.sendall(receipt.encode())
        else:
            connection.close()

def Main():
    kioskListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kioskListener.bind(("", 8001))
    kioskListener.listen(1)   # Change later

    while True:
        connection, address = kioskListener.accept()
        start_new_thread(ticketSale, (connection,))

    kioskListener.close()

if __name__ == '__main__':
    Main()