import socket, sys, json
from os import system, name
def clearS():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def sendT(sckt, srv, arg):
    if len(srv) < 5 or len(arg) < 1:
        print("Revisar argumentos")
        return
    lT = str(len(arg) + 5)
    while len(lT) < 5:
        lT = '0' + lT
    T = lT + srv + arg
    sckt.sendall(T.encode())

def listenB(sckt): #La respuesta que llega al cliente es todo el statu del mensaje
    amntRcvd = 0
    sT = None
    msgT = ''

    while True:
        data = sckt.recv(4096)
        if amntRcvd == 0:
            sT = int(data[:5].decode())
            nS = data[5:10].decode()
            msgT = msgT + data.decode() #Esta línea es la que filtra
            amntRcvd = amntRcvd + len(data)-5
        else:
            msgT = msgT + data.decode()
            amntRcvd = amntRcvd + len(data)
        if amntRcvd >= sT:
            break
    return nS, msgT