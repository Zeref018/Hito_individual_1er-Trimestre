import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
from email_validator import validate_email, EmailNotValidError  # importar librerias
from password_validator import PasswordValidator
import csv

# declaración de variables globales
contrasena = None
correo = None
numero = None
phoneNumber = None
isSpain = None
DNI = None
nombre = None


# comprueba que la contraseña sea correcta
def validarContrasena():
    isValid = False  # contador para entrar y salir del bucle
    contrasena = None
    while not isValid:
        contrasena1 = None
        contrasena = input('introduce la contraseña: ')

        # creo un esquema con los datos que quiero que se introduzcan a la contraseña
        schema = PasswordValidator()

        # Añadir requisitos a la contraseña
        schema \
            .min(8) \
            .max(100) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits() \
            .has().no().spaces() \
            # comprueba que la contraseña sea válida
        isValid = schema.validate(contrasena)
        # devuelve el tipo de error de la contraseña
        if not isValid:
            print('La contraseña no es valida, debe tener mayusculas, minusculas, numeros, no debe contener '
                  'espacios y la longitud debe estar comprendida entre 8 y 100 caracteres')
        else:
            contrasena1 = input('vuelve a introducir la contraseña: ')
        # si la contraseña es correcta pero ambas no son iguales, muestra el fallo
        if contrasena1 != contrasena:
            print('las contraseñas no son iguales')
            isValid = False  # a valor a isValid para que no salga del bucle
    return contrasena


# comprueba que el correo introducido es correcto
def comprobarCorreo():
    # inicializa el contador y el email
    cont = False
    email = 0
    # bucle para repetir si no se introduce el correo correctamente
    while not cont:
        email = input('introduce el correo electronico: ')
        is_new_account = True

        try:
            # valida el correo
            validation = validate_email(email, check_deliverability=is_new_account)

            email = validation.email
            cont2 = True

            # comprueba que el correo introducido, además de ser valido, no está repetido
            canContinue = True
            with open('users.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == email:
                        print('este correo ya esta en uso')
                        canContinue = False
                        break
                if not canContinue:
                    continue
        # si da este error, muestra el error y vuelve al bucle
        except EmailNotValidError as e:

            print(str(e))
            cont2 = False
        # devuelve si el correo es correcto y se sale del bucle
        if cont2:
            cont = True
            print('email correcto')
        else:
            print('correo incorrecta')
    # devuelve el email
    return email


# funcion para comprobar que el numero introducido es correcto
def comprobarNumero():
    # creo un contador
    cont = False
    while not cont:
        numero = input('introduce el numero de teléfono: (+xx xxxxxxxxx):')

        try:
            # parseo el numero para que tenga el formato de phoneNumeber
            phoneNumber = phonenumbers.parse(numero)
            print(phoneNumber)
            # llamo a la variable global
            global isSpain
            # comprueba el prefijo del numero para saber el pais, si el pais es españa isSpain devuelve true
            isSpain = region_code_for_country_code(phoneNumber.country_code) == 'ES'
            # para salir del bucle
            cont = True
        # creo dos excepciones para los 2 errores que me da
        # y en ellos vuelvo a llamar al cont para que el bucle se repita si esntra en estas excepciones
        except UnboundLocalError:
            print('introduce un número en el formato mencionado')
            cont = False
        except phonenumbers.NumberParseException:
            cont = False
            print('introduce un número en el formato mencionado')
    # la funcion devuelve el numero antes de parsear
    return numero


# valida que el dni este bien y devuelve true o false si esta bien o mal
def validoDNI(dni):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
               and tabla[int(dni) % 23] == dig_control
    return False


# funcion para crear la cuenta
def crearCuenta():
    # contador para el bucle
    cont = False
    while not cont:
        x = input('Tienes una cuenta?(si, no) ')
        # crea la cuenta si no tiene ya
        if x == 'no':
            # pide los datos
            nombre = input('introduce el nombre y apellidos: ')

            dni = None
            # valida el DNI y repite si no es correcto
            dniIsValid = False
            while not dniIsValid:
                dni = input('introduce el dni')
                dniIsValid = validoDNI(dni)
                print('el dni es valido')
            # llama a las funciones y guarda los return en cada variable
            correo = comprobarCorreo()
            numero = comprobarNumero()
            contrasena = validarContrasena()

            # abre el archivo csv para escribir en el los datos que queremos guardar
            with open('users.csv', mode='a', newline='', encoding="utf-8") as csv_file:

                fieldnames = ['correo', 'contraseña', 'numero', 'DNI', 'nombre']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'correo': correo, 'contraseña': contrasena, 'numero': numero, 'DNI': dni,
                                 'nombre': nombre})

            print('vas a proceder a logearte')
            cont = True  # sale del bucle
        elif x == 'si':
            print('vas a proceder a logearte')
            cont = True  # sale del bucle


def login():
    # contador para el bucle
    cont = False
    while not cont:
        # lee el archivo csv
        data = []
        with open('users.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data.append(row)
        # print(data)
        # pide el correo
        name = input('introduce el correo: ')

        # llamo a las variables locales
        global numero
        global contrasena
        global correo
        global phoneNumber
        global isSpain
        global DNI
        global nombre
        # nos da una lista de lo que hay en la columna 0
        col = [x[0] for x in data]

        # print(col)
        # si el correo introducido esta en el csv, coge todos los datos de esa fila
        if name in col:
            for i in range(0, len(data)):
                # comprueba el correo introducido en que fila esta y devuelve todos los datos de esa fila
                if name == data[i][0]:  # el 0 es la columna primera, donde se guardan los correos
                    correo = data[i][0]
                    contrasena = data[i][1]
                    numero = data[i][2]
                    DNI = data[i][3]
                    nombre = data[i][4]
        # si el correo es correcto pide la contraseña y si el correo introducido es 'correo'
        # que haria mencion al titulo de la columna no entraria para que no puedan entrar sin cuenta
        if (name == correo) and (name != 'correo'):
            password = input('introduce la contraseña: ')
            # si la contraseña es correcta pasa el login
            if password == contrasena:
                cont = True  # sale del bucle
                print('login correcto')

                # saco si el usuario logeado es español y se actualiza la variable global
                phoneNumber = phonenumbers.parse(numero)

                isSpain = region_code_for_country_code(phoneNumber.country_code) == 'ES'
            else:
                print('contraseña incorrecta')
        else:
            print('el correo no existe')


crearCuenta()

login()


# creo la clase producto con los datos
class Producto():
    # constructor
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    # funcion para sacar el precio dependiendo de si es extrangero o no
    def getPrice(self):
        global isSpain
        return self.price * 1.21 if isSpain else self.price * 2
        # 21% de iva para los españoles, 100% de iva para los extrangeros


# llama a la clase y le da los valores de los productos y su id
producto1 = Producto(1, 'Playstation 5', 550)
producto2 = Producto(2, 'Alienware m15 Ryzen™ Edition R7', 3493.17)
producto3 = Producto(3, 'Nintendo Switch Oled ', 349.99)
producto4 = Producto(4, 'Final Fantasy XVI', 80)

# diccionario con los productos
productos = {
    str(producto1.id): producto1,
    str(producto2.id): producto2,
    str(producto3.id): producto3,
    str(producto4.id): producto4
}
# variable para el bucle
prod = 0
# creo usuarioFav para almacenar los productos que son seleccionados
usuarioFav = []
# muestr por pantalla los productos y les pinta un * si selecciona el producto
while prod > 0 or prod <= 4:
    try:
        if prod == -1:
            break
        if prod != 0:
            usuarioFav.append(prod)
        for i in productos:
            if productos[i].id in usuarioFav:
                print(productos[i].id, ':', productos[i].name, '*')
            else:
                print(productos[i].id, ':', productos[i].name)

        prod = int(input('Elige el producto que quieras añadir, si quieres parar pon -1: '))
    except ValueError:
        print('    Dato introducido no valido')

# muetra los productos que estan en usuarioFav y suma el percio total de los productos
total = 0
for i in usuarioFav:
    print(productos[str(i)].name)
    total = total + productos[str(i)].getPrice()
# muestra el precio
if total != 0:
    print(f'el precio total de su compra sería: {total}€')
# si el precio es 0 no se realiza compra
else:
    print('no se realizará ninguna compra')


# funcion para pagar (muchos print)
def pagar():
    # le muestra las opciones para pagar
    print("1. Pago en efectivo")
    print("2. Pago con tarjeta")
    print("3. Pago con Paypal")
    # contador para el bucle
    cont = False
    while not cont:
        # le pide la opcion que se va a realizar
        try:
            opcion = int(input("Elige una opcion (1 - 3), para cancelar la compra escribe otro numero: "))

            if opcion == 1:
                print('Se cobrará el producto cuando se entregue')
            elif opcion == 2:
                print('se le redirigirá a la página de su banco')
            elif opcion == 3:
                print('se le redirigirá a la página de Paypal para su registro')
            else:
                print('se cancela el pago')
            cont = True  # sale del bucle
        # se realizan las excepciones
        except TypeError:
            print('valor no valido')
        except ValueError:
            print('valor no valido')
    # llamo a las variables globales
    global correo
    global phoneNumber
    global nombre
    global DNI
    global total
    # si se elige pagar, le manda un PDF y pide la dirección
    if (opcion > 0) and (opcion < 4):
        direccion = input('introduce la dirección a la que se enviará el producto, si la dirección es erronea no le '
                          'llegará el producto: ')
        print("el metodo de pago se ha realizado correctamente")
        print(f'se enviará un PDF con la factura al correo: {correo}')
        print('------------------------------------------------------------------------')
        print('FACTURA.PDF:')
        print(f'Nombre: {nombre}')
        print(f'DNI: {DNI}')
        print(f'Correo: {correo}')
        print(f'Dirección: {direccion}')
        print(f'Cantidad pagada: {total}€')
        print('------------------------------------------------------------------------')
        print('se le enviará un SMS con el codigo de localización al número: ')
        print(phoneNumber)


# solo se realiza la funcion de pagar si el total del precio anterior es distinto de 0
if total != 0:
    pagar()
