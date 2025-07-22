import random
from typing import Any
from queue import Queue as Cola
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    "Chequea si existe el archivo en la ruta dada"
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


def crear_tabla_vacia(filas: int, columnas: int) -> list[list[int]]:
    
    """ 
    Crea un tablero que cumple las condiciones pedidas, a partir de filas y columnas. vacio, todos sus elementos son 0.

    Args:
        filas: Número entero mayor estricto a 0.
        columnas: Numero entero mayor estricto a 0.
    
    Returns:
        Lista de listas de números enteros (un tablero) con elementos=0.
    """
    tablaVacia: list[list[int]] = []
    for i in range(filas):
        fila: list[int] = []
        for x in range(columnas):
            fila.append(0)
        tablaVacia.append(fila)
    return tablaVacia

def obtener_posiciones_tablero(tablero:list[list[int]]) -> list[tuple[int,int]] :

    """
    A partir de un tablero devuelve una lista de tuplas con cada posicion del tablero.

    Args:
        tablero: Lista de listas de numeros enteros, estrictamente len(tablero) mayor o igual a 1
    
    Returns:
        Lista de tuplas con posiciones(fila,columna).
    """
    posicion :tuple[int,int] = ()
    posiciones :list[tuple[int,int]] = []
    for fila in range (len(tablero)): 
        for pos in range(len(tablero[fila])):
            posicion = (fila, pos)
            posiciones.append(posicion)
    return posiciones


def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:

    """ Coloca minas en un tablero de x filas e y columnas dada la cantidad de minas indicadas 
    A partir de minas, filas y columnas, crea un tablero de donde elem=Vacio excepto por minas(cantidad) elementos donde elem=BOMBA en posicion al azar del tablero.
    
    Args:
        filas: numero entero mayor estricto a 0.
        columnas: numero entero mayor estricto a 0.
        minas: numero entero mayor estricto a 0 y menor estricto a (filas*columnas)
    
    Returns: 
        Lista de listas de enteros (un tablero) con cantidad=minas de elementos BOMBA.
    """
    if minas <1 or minas >= (columnas * filas): return [[]] 
    tablero : list[list[int]] = crear_tabla_vacia(filas, columnas)
    posiciones : list[tuple[int,int]] = obtener_posiciones_tablero(tablero) 
    pos_bombas : list[tuple[int,int]]  = random.sample(posiciones, minas) 
    for fila in range (len(tablero)):
        for pos in range(len(tablero[fila])):
            posicion : tuple[int,int] = (fila, pos)
            if posicion in pos_bombas :
                tablero[fila][pos] = -1
    return tablero


def calcular_numeros(tablero: list[list[int]]) -> None: 

    """
    Calcula y modifica los numeros las posiciones del tablero que no tienen bombas contando cuantas bombas adyacentes tiene cada celda

    Args:
        tablero: Lista de listas de numeros enteros, estrictamente len(tablero) mayor o igual a 1
        
    Returns:
        None

    """
    filas : int = len(tablero)
    columnas : int = len(tablero[0])

    for fila in range (len(tablero)):
        for col in range (len(tablero[fila])):
            if (tablero[fila][col] == -1) :
                for congruentesFilas in [-1,0,1] :
                    for congruentesColumnas in [-1,0,1]:
                        if (not(congruentesFilas == 0 and congruentesColumnas == 0)): 
                            nueva_fila = fila + congruentesFilas
                            nueva_col = col + congruentesColumnas
                            if (0<= nueva_fila < filas and 0 <= nueva_col < columnas) :
                                 if (tablero[nueva_fila][nueva_col] != -1):
                                    tablero[nueva_fila][nueva_col] += 1
      

def crear_tabla_visible_vacia(filas: int, columnas: int) -> list[list[str]]:

    """
    A partir de una cantidad entera mayor estricta a 0 de filas y columnas, se crea un tablero_visible donde todos sus valores son igual a VACIO

    Args:
        filas: Número entero mayor estricto a 0.
        columnas: Numero entero mayor estricto a 0.
        
    Returns:
        Lista de listas de strings, todos con valor igual a VACIO
    """
    tabla_visible_vacia: list[list[str]] = []
    for i in range(filas):
        fila: list[str] = []
        for x in range(columnas):
            fila.append(VACIO)
        tabla_visible_vacia.append(fila)
    return tabla_visible_vacia 


def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:

    """
    A partir de una cantidad entera mayor estricta a 0 de filas,columnas y minas, devuelve un diccionario de tipo EstadoJuego.
    Se utilizan las funciones previas de colocar minas y calcular numeros para poder crear un tablero que cumpla las condiciones

    Args:
        filas: numero entero mayor estricto a 0.
        columnas: numero entero mayor estricto a 0.
        minas: numero entero mayor estricto a 0 y menor estricto a (filas*columnas)
    Returns:
        EstadoJuego  que contiene como pares clave-valor: 
        la cantidad de minas dentro de tablero, 
        la cantidad de filas y columnas, 
        el tablero generado y calculado con colocar_minas y calcular_numeros, 
        el tablero_visible creado con crear_tabla_visible_vacia, y juego_terminado
    """
    res:dict[str,Any] = {}
    res['filas'] = filas
    res['columnas'] = columnas
    res['minas'] = minas
    tablero = colocar_minas(filas, columnas,minas) 
    calcular_numeros(tablero) 
    res['tablero'] = tablero
    tablero_visible = crear_tabla_visible_vacia(filas,columnas) 
    res['tablero_visible'] = tablero_visible 
    res['juego_terminado'] = False 
    return res


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]: 

    """
    A partir del tablero_visible contenido en estado, devuelve una copia del mismo
    Args:
        estado: EstadoJuego
    Returns:
        Lista de listas de strings, donde todas sus posiciones y valores corresponden al mismo tablero_visible dentro de estado
    
    """
    tablero_visible_copia =[]
    for fila in estado['tablero_visible']:
        tablero_visible_copia.append(fila.copy())
    return tablero_visible_copia


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:

    """ 
    Coloca o saca una bandera de estado['tablero_visible'] (modificandolo), teniendo en cuenta que posicion fue dada (fila,columna) 

    Args:
        estado: EstadoJuego
        filas: numero entero mayor estricto a 0.
        columna: numero entero mayor estricto a 0.
    Returns:
        None
    """
    
    if estado['juego_terminado']: 
        return 
    
    if estado['tablero_visible'][fila][columna] == VACIO:
        estado['tablero_visible'][fila][columna] = BANDERA
        
    elif estado['tablero_visible'][fila][columna] == BANDERA:
        estado['tablero_visible'][fila][columna] = VACIO



def caminos_descubiertos(tablero:list[list[int]], visible:list[list[str]], fila_inicial:int, columna_inicial:int)->list[tuple[int,int]]:

    """
    Args: 
        tablero: Lista de listas de numeros enteros, estrictamente len(tablero) mayor o igual a 1
        visible: Lista de listas de strings (con valores igual a VACIO,BANDERA o un numero que corresponda a tablero)
        fila_inicial: numero entero mayor estricto a 0.
        columna_inicial: numero entero mayor estricto a 0.
    Returns:
        Lista de tuplas de tipo (intXint)

    """
    filas:int = len(tablero)
    columnas:int = len(tablero[0])

    descubiertas:list[tuple[int,int]] = []
    visitados : list[tuple[int,int]] = []
    cola :Cola[tuple[int,int]] = Cola()
    
    cola.put((fila_inicial, columna_inicial)) 
    
    while not cola.empty():
        fila_actual, columna_actual = cola.get()

        if ((fila_actual, columna_actual) not in visitados and
        visible[fila_actual][columna_actual] != BANDERA and
        tablero[fila_actual][columna_actual] != -1):

            visitados.append((fila_actual, columna_actual))
            descubiertas.append((fila_actual, columna_actual))

            if tablero[fila_actual][columna_actual] == 0:
                for cambio_fila in [-1, 0, 1]:
                    for cambio_columna in [-1, 0, 1]:
                        if not(cambio_fila == 0 and cambio_columna == 0):
                            nueva_fila = fila_actual + cambio_fila
                            nueva_columna = columna_actual + cambio_columna

                        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                            if (nueva_fila, nueva_columna) not in visitados:
                                cola.put((nueva_fila, nueva_columna))

    return descubiertas


def todas_celdas_seguras_descubiertas(tablero:list[list[int]],tablero_visible:list[list[str]])->bool:

    """
    Verifica si todas las celdas seguras de tablero_visible fueron descubiertas
    
    Args:
        tablero: Lista de listas de numeros enteros, estrictamente len(tablero) mayor o igual a 1
        tablero_visible: Lista de listas de strings (posibles str: VACIO,BANDERA,o un entero [0,8])
    Returns:
        True si para toda posición válida (i, j) ∈ Z x Z se cumple que:
        (tablero[i][j] = -1 ∧ (tablero visible[i][j] = v VACIO v tablero visible[i][j] = BANDERA) V
        (tablero[i][j] ̸= -1 ∧ tablero visible[i][j] = str(tablero[i][j]))

        Falso en caso contario.
    """
    filas:int = len(tablero)
    columnas:int = len(tablero[0])
    for fila in range(filas):
        for col in range(columnas):
            if tablero[fila][col] == -1:
                if not (tablero_visible[fila][col] == VACIO or tablero_visible[fila][col] == BANDERA):
                    return False
            else:
                if tablero_visible[fila][col] != str(tablero[fila][col]):
                    return False
    return True



def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:

    """ 
    Descubre la celda que elija el jugador modificando tablero_visible, puede pasar que el juego ya haya terminado(no pasa nada),
    o que se descubra una celda con bomba(se termina el juego y se muestran todas las bombas),
    o que se descubra una celda con 0 (se abren los caminos hasta llegar a un numero mas grande que 0)
    o que se descubra una celda con un numero mayor a 0(solo se descubre esa celda). 
    Para toda celda descubierta, se copia el numero del tablero real al visible.
    Si todas las celdas buenas se descubren ganas  

    Args:
        estado: EstadoJuego
        fila: Numero entero mayor estricto a 0
        columna: Numero entero mayor estricto a 0
    Returns:
        None  
 
    """
    if estado['juego_terminado']:
        return
    
    if estado['tablero'][fila][columna] == -1:
        for f in range(estado["filas"]):
            for c in range(estado["columnas"]):
                if estado["tablero"][f][c] == -1:
                    estado["tablero_visible"][f][c] = BOMBA
        estado["juego_terminado"] = True
        return
    
    caminos = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna) #1
    for camino in caminos:
        for (f, c) in caminos:
            estado["tablero_visible"][f][c] = str(estado["tablero"][f][c]) #2

    if todas_celdas_seguras_descubiertas(estado['tablero'],estado['tablero_visible']): #3
        estado['juego_terminado'] = True

def verificar_victoria(estado: EstadoJuego) -> bool:

    """ Verifica si ganaste con la funcion aux de todas_celdas_seguras_descubiertas 
         de manera que si no queda ninguna celda segura sin mostrar en tablero visible, ganas el juego

    Args:
        estado: EstadoJuego
    Returns:
        True si todas_celdas_seguras_descubiertas == True, o False en caso contrario.     
         
    """
    return todas_celdas_seguras_descubiertas(estado['tablero'],estado['tablero_visible'])


def reiniciar_juego(estado: EstadoJuego) -> None:

    """ 
    Reinicia el juego y crea un tablero nuevo mirando que
    el tablero nuevo sea distinto al tablero viejo

    Args:
        estado: EstadoJuego
    Returns:
        None 
          
    """
    filas = estado['filas']
    columnas = estado['columnas']
    minas = estado['minas'] 
    nuevo_estado = crear_juego(filas,columnas,minas)
        
    while (nuevo_estado["tablero"] == estado["tablero"]) :
        nuevo_estado = crear_juego(filas,columnas,minas)

    estado['juego_terminado'] = False
    estado['tablero'] = nuevo_estado["tablero"]
    estado['tablero_visible'] = nuevo_estado["tablero_visible"]
    return

def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:

    """
    A partir de un estado y una ruta de un directorio, crea 2 archivos dentro de ese directorio.
    Uno sera tablero.txt, el cual tendra los mismo valores que el tablero dentro de estado.
    El otro sera tablero_visible, el cual tendra los mismos valores que el tablero_visible dentro
    de estado. Las BANDERAS serán representadas con un *, y VACIO sera representado como ?.

    Args:
        estado: EstadoJuego
        ruta_directorio: string que representa una ruta existente
    Returns:
        None  
    """
    lineas = [] 
    
    for fila in range (len(estado['tablero'])): 
        linea = '' 
        for col in range(len(estado['tablero'][fila])) : 
            linea+= str(estado['tablero'][fila][col]) 
            if col < (len(estado['tablero'][fila]) - 1): 
                linea+=','
        lineas.append(linea + '\n')  
        
    ruta_tablero = os.path.join(ruta_directorio,'tablero.txt') 
    archivo = open(ruta_tablero, "w",)  
    archivo.writelines(lineas) 
    archivo.close()  
    
    lineas = []
    for fila in range (len(estado['tablero_visible'])):
        linea = ''
        for col in range(len(estado['tablero_visible'][fila])) :
            if(estado['tablero_visible'][fila][col] == BANDERA) :
                linea += '*'
            elif(estado['tablero_visible'][fila][col] == VACIO):
                linea += '?'
            else :
                linea += estado['tablero_visible'][fila][col]
            if col < (len(estado['tablero_visible'][fila]) - 1):
                linea+=','
        lineas.append(linea + '\n')
    ruta_tablero_visible =  os.path.join(ruta_directorio,'tablero_visible.txt')
    archivo = open(ruta_tablero_visible, "w")
    archivo.writelines(lineas)
    archivo.close()


def cuantas_minas_existen(tablero:list[list[int]])->int: 

    """ 
    Dado un tablero me devuelve la cantidad entera de minas (-1) que hay dentro del tablero

    Args:
        tablero: Lista de listas de numeros enteros, estrictamente len(tablero) mayor o igual a 1
    Returns:
        Número entero
    
    """
    contador :int = 0 
    filas :int = len(tablero)
    columnas :int = len(tablero[0])
    for fila in range(filas):
        for col in range(columnas):
            if tablero[fila][col] == -1:
               contador +=1
    return contador




def palabras_a_lista(lineas: list[str]) -> list[str]: 

    """
    Dada una lista de lineas, devuelvo una lista de string que 
    contiene los mismos caracteres sacando los saltos de linea

    Args:
        lineas: lista de string que representa las lineas de algun archivo ya leido
    Returns:
        Devuelve una lista con los mismos elementos de lineas, pero sin los saltos de linea
    """
    lista_palabras: list[str] = [] 
    palabra_actual: str = ""

    for linea in lineas:
        for caracter in linea:
            if caracter not in ["\n"]:
                palabra_actual += caracter  
            else:
                lista_palabras.append(palabra_actual)  
                palabra_actual = ""  
        
        if len(palabra_actual) > 0:
            lista_palabras.append(palabra_actual)
            palabra_actual = ""

    return lista_palabras

def cantidad_comas_lineas(lineas: list[str]) -> int:

    """
    Cuenta la cantidad de comas en una lista de líneas.
    
    Args:
        lineas: lista de string que representa las lineas de algun archivo ya leido
    Returns:
        Número entero mayor o igual a 0
    
    """
    contador = 0
    for linea in lineas:
        for caracter in linea:
            if caracter == ',':
                contador += 1
    return contador

def pasar_tablero_archivo_a_tablero_real(lineas: list[str]) -> list[list[int]]:

    """
    Dado una lista de lineas de un archivo que representa un tablero de numeros enteros, devuelve 
    una lista de listas de enteros que contienen los mismos valores, posiciones y dimensiones que
    el tablero que estaba siendo representado en lineas.

    Args:
        lineas: lista de string que representa las lineas de un archivo ya leido
    Returns:
        Lista de listas de números enteros representados dentro de lineas
    
    """
    lineas_limpias = palabras_a_lista(lineas)
    filas = [] 
    for linea in lineas_limpias: 
        caracter_suplente = ""
        columna = [] 
        for caracter in linea: 
            if caracter != ',' and caracter != ' ': 
                caracter_suplente += caracter 
                if caracter_suplente == '-': 
                    continue
                elif caracter_suplente == '-1': 
                    caracter_suplente = "" 
                    numero = -1 
                    columna.append(numero) 
                elif caracter_suplente in ['0','1','2','3','4','5','6','7','8']: 
                    numero = int(caracter_suplente) 
                    caracter_suplente = "" 
                    columna.append(numero)  
        filas.append(columna) 
    return filas


def pasar_tablero_archivo_a_tablero_visible_real(lineas: list[str])->list[list[str]]:

    """
    Dado una lista de lineas de un archivo que representa un tablero_visible,devuelve
    una lista de listas de string que contienen los mismos valores, posiciones y dimensiones que
    el tablero_visible que estaba siendo representado en lineas.

    Args:
        lineas: lista de string que representa las lineas de un archivo ya leido
    Returns:
        Lista de listas de string que representan los valores dentro de lineas
    
    """
    lineas_limpias = palabras_a_lista(lineas) 
    filas = []
    for linea in lineas_limpias: 
        caracter_suplente = ""
        columna = [] 
        for caracter in linea: 
            if caracter != ',':
                caracter_suplente += caracter 
                if caracter_suplente == '-': 
                    continue
                elif caracter_suplente == '-1': 
                    caracter_suplente = "" 
                    numero = '-1' 
                    columna.append(numero) 
                elif caracter_suplente in ['?','*','0','1','2','3','4','5','6','7','8']: 
                    numero = (caracter_suplente) 
                    caracter_suplente = "" 
                    columna.append(numero)  
        filas.append(columna) 
    return filas



def chequear_valores_separados_coma_tab_int(lineas: list[str])->bool:

    """
    Dada una lista de string que representa las lineas de un archivo que representa un tablero
    de números enteros, chequea si todos sus valores estan separados por una coma
    
    Args:
        lineas: lista de string que representa las lineas de un archivo ya leido
    Returns:
        True si todos los valores dentro de lineas estan separados por una coma, False en caso contrario
    """
    lista_lineas = palabras_a_lista(lineas) 
    long_filas = len(lista_lineas) 
    caracteres = ['-','0','1','2','3','4','5','6','7','8'] 
    for fila in range (long_filas):
        long_columnas = len(lista_lineas[fila]) 
        if lista_lineas[fila][0] == ',' or lista_lineas[fila][long_columnas-1] == ',': 
            return False
        for columna in range (long_columnas):
            if lista_lineas[fila][columna] == ',': 
                if lista_lineas[fila][columna-1] not in caracteres or lista_lineas[fila][columna+1] not in caracteres and columna < long_columnas:
                    return  False
    return True


def chequear_valores_separados_coma_tab_vis(lineas: list[str])->bool:

    """
    Dada una lista de string que representa las lineas de un archivo que representa un tablero_visible
    chequea si todos sus valores estan separados por una coma

    Args:
        lineas: lista de string que representa las lineas de un archivo ya leido
    Returns:
        True si todos los valores dentro de lineas estan separados por una coma, False en caso contrario
    
    """
    lista_lineas = palabras_a_lista(lineas)
    long_filas = len(lista_lineas)
    caracteres = ['*','?','0','1','2','3','4','5','6','7','8'] 
    for fila in range (long_filas):
        long_columnas = len(lista_lineas[fila])
        if lista_lineas[fila][0] == ',' or lista_lineas[fila][long_columnas-1] == ',':
            return False
        for columna in range (long_columnas):
            if lista_lineas[fila][columna] == ',': 
                if lista_lineas[fila][columna-1] not in caracteres or lista_lineas[fila][columna+1] not in caracteres and columna < long_columnas:
                    return  False
    return True



def chequear_numeros_iguales_en_tableros(tablero:list[list[int]],tablero_visible:list[list[str]])->bool: 

    """
    Dado un tablero y un tablero visible chequeo que tengan el mismo numero (salvo el -1 y los caracteres especiales de tablero_visible)

    Args:
        tablero: Lista de listas de numeros enteros, estrictamente len(tablero) mayor o igual a 1
        tablero_visible: Lista de listas de strings (posibles str: VACIO, BANDERA, o un entero [0,8])
    Returns:
        True si toda posicion dentro de tablero, es igual a toda posicion dentro de tablero_visible,
        (salvo el -1 y los caracteres especiales de tablero_visible). False en caso contrario.

    """
    for i in range (len(tablero)):
        for j in range (len(tablero[0])):
            if tablero_visible[i][j] not in ['?','*'] and tablero[i][j] != -1:
                if tablero_visible[i][j] != str(tablero[i][j]):
                    return False
            if tablero_visible[i][j] == '-1':
                return False
    return True


def chequear_si_tablerotxt_correcto(tablero:list[list[int]])->bool:

    """
    Dado una lista de listas de enteros que representa un tablero, verifica
    si este mismo es una matriz con dimensiones validas, y si a este se le
    calcularon los numeros correctamente, utilizando la funcion calcular_numeros

    Args:
        tablero: Lista de listas de numeros enteros
    Returns:
        True si tablero fue creado correctamente, False en caso contrario
    """
    if (len(tablero) < 1 or len(tablero[0]) < 1): 
        return False
    for fila in range (len(tablero)):
        if ( len(tablero[fila]) != len(tablero[0]) ): 
            return False 
        
    copia_tab = []
    for i in range (len(tablero)):
        copia_tab.append(tablero[i].copy())
    for i in range (len(copia_tab)):
        for j in range (len(copia_tab[i])):
            if copia_tab[i][j] != -1:
                copia_tab[i][j] = 0  
    calcular_numeros(copia_tab) 
    if copia_tab == tablero: 
        return True
    else: 
        return False 
    
def contiene_espacios_invalidos(lineas:list[str])->bool:

    """
    Dada una lista de string que representa las lineas leídas
    de un archivo, verifica si los valores estan espaciados o no.

    Args:
        lineas: lista de string que representa las lineas leídas de un archivo

    Returns:
        True si hay minimo un espacio en blanco erroneo, False en caso contrario. 
    
    """
    for linea in lineas:
        for caracter in linea:
            if caracter == ' ':
                return True
    return False
    

def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:

   """
    Dado un estado y una ruta de un directorio donde existen los archivos tablero.txt y tablero_visible.txt,
    verifica si ambos cumplen ser archivos correctos y bien formados. En el caso que sean correctos, se 
    modifica el estado y retorna True.

    Args:
        estado: EstadoJuego
        ruta_directorio: string que representa la ruta donde se encuentran los dos archivos
    Returns:
        True si tablero.txt y tablero_visible.txt son archivos correctos y correspondidos entre si,
        False en caso contrario. 
   """

   res : bool = False
   condicion0: bool = existe_archivo(ruta_directorio,"tablero.txt") 
   
   condicion1: bool = existe_archivo(ruta_directorio,"tablero_visible.txt")

   if condicion0 == False or condicion1 == False:
       return res

   ruta_tablero :str = ruta_directorio + "/tablero.txt"
   ruta_tablero_visible :str = ruta_directorio + "/tablero_visible.txt"

   archivo_tablero = open(ruta_tablero,"r")
   archivo_tablero_vis = open(ruta_tablero_visible,"r")
   lineas_tablero :list[str] = archivo_tablero.readlines()
   lineas_tablero_vis :list[str] = archivo_tablero_vis.readlines()
   
   if contiene_espacios_invalidos(lineas_tablero) or contiene_espacios_invalidos(lineas_tablero_vis):
       return res

   condicion2 = len(lineas_tablero) == len(lineas_tablero_vis)

   if condicion2 == False:
       return res
   
   condicion3 :bool = cantidad_comas_lineas(lineas_tablero) == cantidad_comas_lineas(lineas_tablero_vis)

   if condicion3 == False:
       return res
   

   tablero = pasar_tablero_archivo_a_tablero_real(lineas_tablero) 
   
   condicion4 :bool = chequear_si_tablerotxt_correcto(tablero) 
   
   tablero_visible = pasar_tablero_archivo_a_tablero_visible_real(lineas_tablero_vis) 
   
   condicion5 :bool = chequear_valores_separados_coma_tab_vis(lineas_tablero_vis) 
   
   condicion6 :bool = chequear_valores_separados_coma_tab_int(lineas_tablero) 
   
   condicion7 :bool = chequear_numeros_iguales_en_tableros(tablero,tablero_visible) 
   archivo_tablero.close()
   archivo_tablero_vis.close()
   if condicion0 and condicion1 and condicion2 and condicion3 and condicion4 and condicion5 and condicion6 and condicion7:
        res = True
        estado['minas'] = cuantas_minas_existen(tablero)
        estado['juego_terminado'] = False
        estado['tablero'] = tablero
        for i in range(len(tablero_visible)):
            for j in range(len(tablero_visible[0])):
                if tablero_visible[i][j] == '?':
                    tablero_visible[i][j] = VACIO
                elif tablero_visible[i][j] == '*':
                    tablero_visible[i][j] = BANDERA
        estado['tablero_visible'] = tablero_visible
        estado['filas'] = len(tablero)
        estado['columnas'] = len(tablero[0])
       
   return res
