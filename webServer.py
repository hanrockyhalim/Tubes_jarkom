# import socket module
from socket import *
import sys  # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverSocket.bind(('192.168.56.1', 5000))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()  # Fill in start #Fill in end
        # Send one HTTP header line into socket
        connectionSocket.send(
            "HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n".encode())
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
    except IOError:
        # Send response message for file not found
        connectionSocket.send(
            "HTTP/1.1 404 Not Found\nContent-Type: text/html\r\n\r\n".encode())
        # Close client socket
    connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
