import socket, json
from db import databas
from comunicacion import sendT, listenB, registerS
srv = 'ccddb'

# Obtener datos
def seleccionarHilos():
    crsr = databas.cursor()
    fetched = None
    crsr.execute("SELECT * FROM Hilo")
    #crsr.execute("SELECT `hilo_id`, `usuario_id`, Categoria.nombre, `fecha_creacion`, `contenido`, `es_anonimo`, `esta_abierto` FROM `Hilo`, `Categoria` WHERE Categoria.categoria_id = Hilo.categoria_id;")   
    fetched = crsr.fetchall()
    hilos=[]
    if fetched:
        for row in fetched:
            hilos.append(json.dumps(row, indent=None, sort_keys=True, default=str))
        response = json.dumps(hilos, indent=2, sort_keys=True, default=str)
        sendT(sckt, srv, response)
    else:
        response = {"respuesta":"Error al consultar datos."}
        sendT(sckt, srv, json.dumps(response))

def borrarHilo(id):
    crsr = databas.cursor()
    crsr.execute(f"DELETE FROM `Hilo` WHERE `Hilo`.`hilo_id` = {id};")   
    databas.commit()
    response = {"respuesta":"El hilo ha sido eliminado correctamente."}
    sendT(sckt, srv, json.dumps(response))

def mostrar_comentarios(mensaje):
    crsr = databas.cursor()
    crsr.execute(f"SELECT Comentario.comentario_id, Comentario.contenido, Comentario.fecha_creacion, Usuario.nombre, Hilo.es_anonimo FROM Comentario, Usuario, Hilo WHERE Comentario.hilo_id = 7 and Comentario.usuario_id = Usuario.usuario_id and Comentario.hilo_id = Hilo.hilo_id")
    fetched = crsr.fetchall()
    hilos=[]
    if fetched:
        for row in fetched:
            hilos.append(json.dumps(row, indent=None, sort_keys=True, default=str))
        response = json.dumps(hilos, indent=2, sort_keys=True, default=str)
        sendT(sckt, srv, response)
    else:
        response = {"respuesta":"Error al consultar datos."}
        sendT(sckt, srv, json.dumps(response))

def GenerarReporte():#Vencimiento
    crsr = databas.cursor()
    crsr.execute("SELECT Hilo.hilo_id, Categoria.nombre FROM Hilo, Categoria WHERE Hilo.categoria_id = Categoria.categoria_id and TIMESTAMPDIFF(MONTH, Hilo.fecha_creacion, NOW()) >= 1")

    fetched = crsr.fetchall()
    reporte=[]
    if fetched:
        for row in fetched:
            reporte.append(json.dumps(row, indent=None, sort_keys=True, default=str))
        response = json.dumps(reporte, indent=2, sort_keys=True, default=str)
        sendT(sckt, srv, response)
    else:
        response = {"respuesta":"Error al consultar datos."}
        sendT(sckt, srv, json.dumps(response))

def GenerarReporteC():
    crsr = databas.cursor()
    crsr.execute("SELECT Categoria.nombre, COUNT(*) FROM Hilo, Categoria WHERE Hilo.categoria_id = Categoria.categoria_id GROUP BY Categoria.nombre")
    reporte= []
    fetched = crsr.fetchall()
    if fetched:
        for row in fetched:
            reporte.append(json.dumps(row, indent=None, sort_keys=True, default=str))
        response = json.dumps(reporte, indent=2, sort_keys=True, default=str)
        sendT(sckt, srv, response)
    else:
        response = {"respuesta":"Error al consultar datos."}
        sendT(sckt, srv, json.dumps(response))

if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost',  5000)
        print('Servicio: Conectándose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except:
        print('No es posible la conexión al bus')
        quit()

    registerS(sckt, srv)

    while True:
        nS, mT = listenB(sckt)
        msg = json.loads(mT)
        if nS == srv:
            if msg["opcion"] == 1:
                seleccionarHilos()
            elif msg["opcion"] == 2:
                borrarHilo(int(msg["id"]))
            elif msg["opcion"] ==3:
                mostrar_comentarios(msg["hilo_id"])
            elif msg["opcion"] == 4:
                GenerarReporte()
            elif msg["opcion"] == 5:
                GenerarReporteC()
        else:
            response = {"respuesta":"servicio incorrecto"}
            sendT(sckt, srv, json.dumps(response))

    print('Se cierra socket')
    sckt.close()