import socket, select, queue

numTickets = 50

movieSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
movieSocket.setblocking(0)
movieSocket.bind(("", 8000))
movieSocket.listen(1)   # Change later

inputs = [movieSocket]
outputs = []
buffer = {}

while inputs:
    read, write, error = select.select(inputs, outputs, inputs, 60000)

    for sock in read:
        if sock is movieSocket:
            clientSocket, clientAddress = sock.accept()
            clientSocket.setblocking(0)
            inputs.append(clientSocket)
            buffer[clientSocket] = queue.Queue()
        else:
            message = sock.recv(1024).decode()
            if message:
                buffer[sock].put(message)
                if sock not in outputs:
                    outputs.append(sock)
            else:
                if sock in outputs:
                    outputs.remove(sock)
                inputs.remove(sock)
                sock.close()
                del buffer[sock]

    for sock in write:
        try:
            currentMessage = buffer[sock].get_nowait()
        except queue.Empty:
            outputs.remove(sock)
        else:
            ticketType, num = currentMessage.split(":", 1)
            num = int(num)
            # if ticketType is "play" --> send to playserver
            # else:
            if numTickets >= num:
                numTickets -= num
                receipt = "success:" + str(num)
            else:
                receipt = "failed:" + str(num)

            sock.sendall(receipt.encode())

    for sock in error:
        inputs.remove(sock)
        if sock in outputs:
            outputs.remove(sock)
        sock.close()
        del buffer[sock]

