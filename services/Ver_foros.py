import socket, json
import comunicacion as com
import socket, json
from db import databas
from comunicacion import sendT, listenB, registerS

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea socket

        direccion = ('localhost', 5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*direccion))
        sckt.connect(direccion)
    except:
        print('No es posible la conexión al bus')
        quit()

    com.registerS(sckt,'postr') #Inicia el servicio comentar

    while True:
        nS, mT = com.listenB(sckt) #A la espera del Bus
        if nS == 'postr':
            print("Contenido : ", mT , "  Nombre del servicio :",nS)
            Agregar_post(mensaje=json.loads(mT))
        else:
            print(nS)
            response = {"Respuesta":"error nombre del servicio"}
            com.sendT(sckt, 'comen', json.dumps(response))
