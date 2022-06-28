import socket, json
import comunicacion as com
import socket, json
from db import databas
from comunicacion import sendT, listenB, registerS

srv = "postr"


def Agregar_post(mensaje):
    crsr = databas.cursor(buffered = True)
    crsr.execute("SELECT usuario_id FROM Usuario WHERE nombre = %s", (mensaje["nombre"],))
    fetched = crsr.fetchone()[0]
    crsr.execute("INSERT INTO Hilo (usuario_id, categoria_id, contenido, es_anonimo, esta_abierto) VALUES(%s,%s,%s,%s,%s)", (fetched,mensaje["categoria_id"],mensaje["contenido"],mensaje["es_anonimo"],1))
    databas.commit()
    sendT(sckt,srv,"Post agregado")
    return

def Enviar_comentario(mensaje):
    crsr = databas.cursor(buffered = True)
    crsr.execute("INSERT INTO Comentario (hilo_id, usuario_id, contenido) VALUES(%s,%s,%s)",(mensaje["hilo_id"],mensaje["usuario_id"],mensaje["contenido"]))
    databas.commit()
    response = {"respuesta":"Gracias por comentar."}
    sendT(sckt,srv,json.dumps(response))
    return 

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
        msg = json.loads(mT)
        if nS == 'postr':
            if(msg["opcion"] == 1):
                print("Contenido : ", mT , "  Nombre del servicio :",nS)
                Agregar_post(mensaje=json.loads(mT))
            elif(msg["opcion"] == 2):
                print("Comentario : ", mT , "  Nombre del servicio :",nS)
                Enviar_comentario(mensaje=json.loads(mT))
        else:
            print(nS)
            response = {"Respuesta":"error nombre del servicio"}
            com.sendT(sckt, 'comnt', json.dumps(response))

