import socket, json
from db import databas
from comunicacion import sendT, listenB, registerS
srv = 'ccdli'

#log in usuario
def loginU(login):
    crsr = databas.cursor()
    crsr.execute("SELECT * FROM Usuario WHERE nombre = %s AND contrasena = %s", (login["username"],login["password"]))
    fetched = crsr.fetchone()
    print("fetched")
    if fetched:
        print(fetched)
        response = {"respuesta":{"username":fetched[1],"password":fetched[2],"es_admin":fetched[4]}}
        sendT(sckt, srv, json.dumps(response))
    else:
        response = {"respuesta":"No es posible entrar con el usuario ingresado."}
        sendT(sckt, srv, json.dumps(response))

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print("No es posible la conexión al bus")
        quit() 

    registerS(sckt, srv)

    while True:
        nS, mT = listenB(sckt)
        if nS == srv:
            loginU(login = json.loads(mT))
        else:
            response = {"respuesta":"servicio equivocado"}
            sendT(sckt, srv, json.dumps(response))