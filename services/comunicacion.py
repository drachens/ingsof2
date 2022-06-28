import socket, sys, json
from os import system, name
from db import databas

#srv = arg = cssda

#Armado y envío transacción
def sendT(sckt, srv, arg): #Envia un sendall con 00010sinitccdsu
    if len(srv) < 5 or len(arg) < 1: 
        print("Revisar argumentos")
        return
    lT = str(len(arg) + 5) 
    while len(lT) < 5:
        lT = '0' + lT
    T = lT + srv + arg # 00010sinitccdsu

    sckt.sendall(T.encode())  #Envia el mensaje al bus

#Comunicación bus
def listenB(sckt):
    amntRcvd = 0
    sT = None
    msgT = ''

    while True:
        data = sckt.recv(4096)
        if amntRcvd == 0: 
            sT = int(data[:5].decode()) #Tamaño del mensaje
            nameSrv = data[5:10].decode() #Nombre del servicio "ssinit"
            msgT = msgT + data[10:].decode() #Nombre del servicio
            amntRcvd = amntRcvd + len(data)-5 
        else:
            msgT = msgT + data.decode()
            amntRcvd = amntRcvd + len(data)
        if amntRcvd >= sT:
            break
    print("soy un nameSrv  : ", nameSrv, "soy un msgT  : ", msgT)
    return nameSrv, msgT 

#Inicia el servicio, envia su
def registerS(sckt, srv): #socket nombre del servicio ccdsu
    sendT(sckt, 'sinit', srv)  #Inicia un servicio y envía el mensaje al  bus 
    nS, mT = listenB(sckt) #Escucha la respuesta del Bus
    if nS == 'sinit' and mT[:2] == 'OK':
        print('Servicio activado exitosamente.')
    else:
        print('No ha sido posible activar el servicio: ', srv, '.')

