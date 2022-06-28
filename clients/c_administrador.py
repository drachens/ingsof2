import socket, json
from os import system, name
from comunicacion import clearS, sendT, listenB


lgin = "ccdli"  # Ingreso
gtdb = "ccddb"  # Consultar datos

sesion = {"username":None,"password":None}
sckt = None

def menuSULI():
    clearS()
    menu = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Log in (Ingresar con usuario)    *
    ***************************************

    Opción: """
    option = input(menu)
    if option =="1":
        menuLI()
    else:
        print("Opción ingresada no válida.")
        menuSULI()


def menuLI():
    username = None
    password = None
    #rol = 1 # Usuario administrador

    menuUN = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """   
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    arg = {"username": username, "password": password}
    #arg = {"username": username, "password": password, "rol": rol}
    sendT(sckt, lgin, json.dumps(arg))
    nS, msgT=listenB(sckt)
    msg = json.loads(msgT[12:])
    if nS == lgin:
        if msg["respuesta"] == "No es posible entrar con el usuario ingresado.":
            input("No se ha podido iniciar sesión.")
            menuLI() 
        else:
            global sesion
            sesion=msg["respuesta"]
            if sesion["es_admin"] == 1:
                menuCRUD()
            else:
                menuLI()

def menuCRUD():
    clearS()
    menuCRUD2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Menu                                *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Menu Foros                       *
    * 2) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuCRUD2))
    if opcion == 1:
        menuHILOS()
    else:
        menuSULI()

def menuHILOS():
    clearS()
    menuHILOS2 = """
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * Agregar entidad                     *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Ver  Foros                       *
    * 2) Ver vencidos                     *
    * 3) Generar reporte                  *                                     
    * 4) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuHILOS2))
    if opcion == 4:
        menuSULI()
        
    elif opcion == 2:
        arg = {"opcion": 4}
        sendT(sckt, gtdb, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = msgT[12:]
        if nS == gtdb:
            if msg:
                data = json.loads(msg)
                for fila in data:
                    hilo_id, hilo_categoria, *resto = json.loads(fila)
                    contenido_comen = f"""
        ***************************************
        * ADMINISTRADOR                       *
        *-------------------------------------*
        * 1) Siguiente vencido                *          
        * 2) Volver                           *
        ***************************************                      
        ID: {hilo_id}                                            
        Categoría: {hilo_categoria}  
        Opción: """   
                    opcion = int(input(contenido_comen))
                    if opcion == 1:
                        continue
                    else:
                        menuHILOS()
                clearS()
                menuHILOS()
                
    elif opcion == 3:
        arg = {"opcion": 5}
        sendT(sckt, gtdb, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = msgT[12:]
        if nS == gtdb:
            if msg:
                data = json.loads(msg)
                for fila in data:
                    nombre, contador, *resto = json.loads(fila)
                    contenido_comen = f"""
        ***************************************
        * REPORTES CATEGORIAS                 *
        *-------------------------------------*                       
        * 1) Siguiente                        *
        * 2) Volver                           *
        ***************************************                      
        Nombre: {nombre}                                            
        Cantidad: {contador}  
        Opción: """   
                    opcion = int(input(contenido_comen))
                    if opcion == 1:
                        continue
                    else:
                        menuHILOS()
                clearS()
                menuHILOS()
    else:   
        arg = {"opcion": opcion}
        sendT(sckt, gtdb, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = msgT[12:]
        if nS == gtdb:
            if msg:
                data = json.loads(msg)
                mostrarFORO(data)
                enter = input("Presione enter para continuar. ")
                clearS()
                menuHILOS()


def mostrarFORO(data):
    
    for foro in data:
        id, usuario_id, categoria, fecha, contenido, *resto = json.loads(foro)
        contenido_foro = f"""
    ***************************************
    * Usuario administrador               *
    *-------------------------------------*
    * 1) Siguiente foro                   *
    * 2) Eliminar foro actual             *
    * 3) Volver                           *
    ***************************************

    Foro ID: {id}                       
    Usuario ID: {usuario_id}            
    Categoría: {categoria}              
    Fecha: {fecha}                      
    Contenido: {contenido}  
              
    Opción: """

        opcion = int(input(contenido_foro))
        if opcion == 1:
            continue
        if opcion == 2:
            arg = {"opcion": opcion, "id": id}
            sendT(sckt, gtdb, json.dumps(arg))
            nS, msgT = listenB(sckt)
            msg = msgT[12:]
            if nS == gtdb:
                if msg:
                    data = json.loads(msg)
                    print(data["respuesta"])
                    enter = input("Presione enter para continuar. ")
        elif opcion == 3:
            menuHILOS()
            break
        
if __name__ == "__main__":
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', 5000)
        print('Cliente: Conectandose a {} puerto {}'.format(*server_address))
        sckt.connect(server_address)
    except: 
        print('No es posible la conexión al bus')
        quit()

    menuSULI()