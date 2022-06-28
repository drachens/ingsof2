import socket, json
from os import system, name
from comunicacion import clearS, sendT, listenB

categ = [0]*100
categ[1] = "Accidente"
categ[6] = "Asalto"


comentar = "comnt"
postear = "postr"
rgtr = "ccdsu"  # Registro
lgin = "ccdli"  # Ingreso
gtdb = "ccddb"  # Consultar datos


sesion = {"username":None,"password":None,"es_admin":None}
sckt = None

def menuSULI():
    clearS()
    menu = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Elija una opción:                   *
    * 1) Sign up (Registrar un usuario)   *
    * 2) Log in (Ingresar con usuario)    *
    ***************************************

    Opción: """
    option = input(menu)
    if option == "1":
        menuSU()
    elif option =="2":
        menuLI()
    else:
        print("Opción ingresada no válida.")
        menuSULI()

def menuSU():


    username = None
    password = None

    clearS()

    menuUN = """
    ***************************************
    * Usuario                             *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar nombre de usuario          *
    ***************************************

    Usuario: """    
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)


    menuEmail = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Ingresar contraseña                 *
    ***************************************
    
    Correo electrónico : """
    clearS()
    email = input(menuEmail)


    menuYN = f""""
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Registro de usuario                 *
    * Confirme sus datos [y/n]            *
    ***************************************
    
    Usuario: {username}
    Correo: {email}
    Contraseña: {password}
    
    Opción: """
    clearS()
    yn = input(menuYN)
    if yn == 'y':
        arg = {"username": username, "password": password, "email": email, "es_admin": 0}
        sendT(sckt, rgtr, json.dumps(arg))
        nS, msgT = listenB(sckt)
        msg = json.loads(msgT[12:])
        if nS == rgtr:
            if msg["respuesta"] == "El usuario introducido ya se encuentra registrado.":
                print(msg["respuesta"])
                enter = input("Ingrese tecla para continuar.")
                menuSULI()
            else:
                print(msg["respuesta"])
                menuLI()
    else:
        menuSU()

def menuLI():
    username = None
    password = None
    #rol = 2 # Usuario general

    menuUN = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar nombre de usuario          *
    ***************************************

    Nombre : """   
    clearS()
    username = input(menuUN)

    menuPW = """
    ***************************************
    * Usuario general                     *
    *-------------------------------------*
    * Inicio de sesión                    *
    * Ingresar contraseña                 *
    ***************************************
    
    Contraseña: """
    clearS()
    password = input(menuPW)

    arg = {"username": username, "password": password}
    sendT(sckt, lgin, json.dumps(arg)) # Chequeo de la existencia en bdd
    nS, msgT=listenB(sckt)
    msg = json.loads(msgT[12:])

    if nS == lgin:
        if msg["respuesta"] == "No es posible entrar con el usuario ingresado.":
            input("No se ha podido iniciar sesión.")
            menuLI() 
        else:
            global sesion
            sesion=msg["respuesta"]
            print(sesion)
            if sesion["es_admin"] == 0:
                menuGD()
            else:
                menuLI()

def menuGD():
    menuGD2 = f"""
    ***************************************
    *   Usuario {sesion["username"]}      *
    *-------------------------------------*
    * Consultar foro                      *
    * Elija una opción                    *
    *-------------------------------------*
    * 1) Postear en el foro               *                        
    * 2) Ver foros                        *
    * 0) Cerrar sesión                    *
    ***************************************
    
    Opción: """
    opcion = int(input(menuGD2))

    if opcion == 1:
        clearS()
        menuCategorias = """
    ***************************************
    * Seleccione una categoría            *
    *-------------------------------------*
    * 1) Accidente                        *
    * 2) Asalto                           *
    ***************************************

    Categoria : """
        temp_cat = int(input(menuCategorias))
        if(temp_cat > 2 ):
            print("Categoria inexistente")
            menuGD()
        
        else:

            if(temp_cat == 1):
                categoria = 1
            else:
                categoria = 6
            content  = input("Escriba su denuncia : ")
            clearS()
            menuAnonimo = """
                ***************************************
                * Confirme                            *
                *-------------------------------------*
                * Anónimo [y/n]                       *
                ***************************************
            """
            if(input(menuAnonimo) == 'y'):
                es_anonimo = 1
            else:
                es_anonimo = 0
            
            print(sesion)

            arg = {"nombre": sesion["username"],"categoria_id": categoria, "contenido": content, "es_anonimo":es_anonimo, "opcion":1}
            sendT(sckt,postear,json.dumps(arg))
            
            nombre, contenido = listenB(sckt)
            print("bugging",contenido[12:])

            if(contenido[12:] == "Post agregado"):
                menuGD()
        

    elif (opcion == 2):
        arg = {"opcion": 1}
        sendT(sckt, gtdb, json.dumps(arg))
        nS, msgT = listenB(sckt)
        print(msgT)
        msg = msgT[12:]
        
        if nS == gtdb:
            if msg:
                data = json.loads(msg)
                mostrarFORO(data)
                enter = input("Presione enter para continuar. ")
                clearS()
                menuGD()


        return

def mostrarFORO(data):
    
    for foro in data:
        id, usuario_id, categoria, fecha, contenido, *resto = json.loads(foro)
        contenido_foro = f"""
    ***************************************
    * Usuario {sesion["username"]}        *
    *-------------------------------------*
    * 1) Siguiente foro                   *
    * 2) Comentar foro                    *
    * 3) Ver comentarios                  *
    * 4) Volver                           *
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
            content = input("Comentario : ")
            arg = {"hilo_id": id, "usuario_id": usuario_id, "contenido":content, "opcion":2}
            sendT(sckt,'postr', json.dumps(arg))
            nS, msgT = listenB(sckt)

            enter = input("Presione enter para continuar. ")

        elif opcion == 3:
            arg = {"hilo_id":id, "opcion":3}
            sendT(sckt,gtdb,json.dumps(arg))
            nS, msgT = listenB(sckt)
            msg = msgT[12:]
            if nS == gtdb:
                if msg:
                    data = json.loads(msg)
                    print(data)
                    for fila in data:

                        comentario_id, contenido, fecha, nombre, es_anonimo, *resto = json.loads(fila)
                        
                        if(es_anonimo == 1):
                            contenido_comen = f"""
                            ***************************************
                            * Usuario {sesion["username"]}        *
                            *-------------------------------------*
                            * 1) Siguiente comentario             *          
                            * 2) Volver                           *
                            ***************************************
                            Usuario: Anónimo                      
                            Comentario ID: {comentario_id}                        
                            Fecha: {fecha}                      
                            Comentario: {contenido}  
                                    
                            Opción: """
                            enter = int(input(contenido_comen))
                            if enter == 1:
                                continue
                            else :
                                break
                        else:
                            contenido_comen = f"""
                            ***************************************
                            * Usuario {sesion["username"]}        *
                            *-------------------------------------*
                            * 1) Siguiente comentario             *          
                            * 2) Volver                           *
                            ***************************************
                            Usuario: {nombre}                      
                            Comentario ID: {comentario_id}                        
                            Fecha: {fecha}                      
                            Comentario: {contenido}  
                                    
                            Opción: """
                            enter = int(input(contenido_comen))
                            if enter == 1:
                                continue
                            else :
                                break
                    
            return



        elif opcion == 4:
            menuGD()
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