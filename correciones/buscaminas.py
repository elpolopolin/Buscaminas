import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

"""
--------------------------------------------------------------------------------
| #! ------ RESULTADO: DESAPROBADO ------ |
--------------------------------------------------------------------------------
* COMENTARIOS GENERALES de la corrección:
    - Muy dificil seguir todo el código. Hay muchas partes que parece que fueron hechas sin pensar mucho en la legibilidad y declaratividad del código. No solo tiene que funcionar, sino que también tiene que tener una buena estructura y organización.
    ! No se respeto el formato pedido de documentación con Docstrings en ningún ejercicio.
    - Además muchos comentarios describiendo funciones son un poco escuetos o no son del todo claros.
    - Se podría haber separado el archivo con comentarios que denoten que ejercicio se está trabajando (como lo deje haciendo yo).
    
    ! Muchisimas variables/funciones sin tipar o mal tipadas.
    - Faltaron tipar los archivos (en guardar y cargar estado), la forma de tipar era: `archivo_tablero : TextIO = ...` y se debía agregar a los Imports: `from typing import TextIO`.

    ! NO SE HICIERON NUEVOS TESTS PARA ALGUNAS FUNCIONES! Recuerden que es requisito fundamental conseguir el porcentage de coverage pedido.
    - No es necesario implementar todos los tests que liste en cada ejercicio. Solo di una lista de posibles tests que podrían hacer. Ustedes deben elegir los que consideren necesarios.
    
    ! MUCHO comentario innecesario.
    - No comenten solo por hacerlo, los comentarios deben ayudar a entender el código, no describirlo.
    
* OBSERVACIONES MENORES: 
    - Es recomendable ser más consistente con el nombre de funciones y variables. Por ejemplo, en algunos casos se usa el formato "funcion_Ejemplo" y en otros "funcionEjemplo".
    - También algo tan simple como dejar algo de espacio entre las líneas de código cuando separan lógicas distintas es parte de la legibilidad y claridad del código.
    - Tener en cuenta como se acomodan las funciones auxiliares, usualmente es una buena práctica que se ordenen por orden de aparición, o por prioridad. Tanto las funciones auxiliares de las principales, como los tests están muy desordenados
    - No es muy recomendable agregar los comentarios sobre las mismas líneas de código, ya que puede dificultar la lectura. Es mejor agregar comentarios en líneas separadas.
--------------------------------------------------------------------------------
* META COMENTARIOS:
    - La nota puesta en cada Ejercicio es solo para referencia del corrector, no es una calificación formal.
    - Para visualizar correctamente los comentarios de corrección, ver archivo LEEME.md
--------------------------------------------------------------------------------
"""

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    "Chequea si existe el archivo en la ruta dada"
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


""" ------------------------------------ EJERCICIO 1 ------------------------------------
    * NOTA: BIEN-
"""

""" recibe las filas y las columnas y en base a eso crea y devuelve una matriz vacia (sin bombas,numeros en base a adyacencia a bombas)"""
def crearTablaVacia(filas: int, columnas: int) -> list[list[int]]:
    tablaVacia: list[list[int]] = []
    for i in range(filas):
        fila: list[int] = []
        for x in range(columnas):
            fila.append(0)
        tablaVacia.append(fila)
    return tablaVacia

"""de un tablero devuelve un lista de tuplas con todas las posiciones. cada tupla representa una posicion (fila,columna)"""
def sacarPosicionesTablero(tablero:list[list[int]]) -> list[tuple[int,int]] :
    #? No es un buen nombre para la función, ya que no saca posiciones, sino que las OBTIENE.
    posicion :tuple(int,int) = () # #! Mal tipado
    posiciones :list[tuple[int,int]] = [] #:[(fila,col)]
    for fila in range (len(tablero)): 
        for pos in range(len(tablero[fila])):
            posicion = (fila, pos) #pos = col
            posiciones.append(posicion)
    return posiciones

""" Coloca minas en un tablero de x filas e y columnas dada la cantidad de minas indicadas """
def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
   #cada lista de enteros es una columna de la matriz, la cantidad de filas igual
    if minas <1 or minas >= (columnas * filas): return [[]] #caso base
    tablero : list[list[int]] = crearTablaVacia(filas, columnas)
    posiciones : list[tuple[int,int]] = sacarPosicionesTablero(tablero) #saco las posiciones existentes dentro de la matriz
    #^ El comentario arriba de sacarPosicionesTablero no dice lo mismo que la documentación de la función y solo confunde más.
    pos_bombas : list[tuple[int,int]]  = random.sample(posiciones, minas) #posiciones en donde existira bomba por lo que su valor no sera 0 sera -1
    for fila in range (len(tablero)): #poner las bombas en el tablero
        for pos in range(len(tablero[fila])):
            posicion : tuple[int,int] = (fila, pos)
            if posicion in pos_bombas :
                tablero[fila][pos] = -1
    return tablero

""" ------------------------------------ EJERCICIO 2 ------------------------------------
    * NOTA: BIEN-
"""

"Calcula los numeros de las posiciones del tablero que no tienen bombas contando cuantas bombas tiene adyacentes cada celda"
def calcular_numeros(tablero: list[list[int]]) -> None: 
    filas : int = len(tablero)
    columnas : int = len(tablero[0])

    for fila in range (len(tablero)):
        for col in range (len(tablero[fila])):
            if (tablero[fila][col] == -1) :
                #^ Todo esto de abajo podría haber ido a una función auxiliar, con un comentario que explique qué hace.
                for congruentesFilas in [-1,0,1] :
                    for congruentesColumnas in [-1,0,1]:
                        if (not(congruentesFilas == 0 and congruentesColumnas == 0)): #creo q es al pedo pero lo dejamos
                            #! Si no es necesario se prueba sacarlo, se corren los tests y se ve si sigue funcionando bien.
                            nueva_fila = fila + congruentesFilas
                            nueva_col = col + congruentesColumnas
                            if (0<= nueva_fila < filas and 0 <= nueva_col < columnas) : #verificar si la nueva posicion congruente a bomba esta dentro del tablero
                                 if (tablero[nueva_fila][nueva_col] != -1):
                                    tablero[nueva_fila][nueva_col] += 1
                #^ Esto es confuso, no se entiende muy bien la lógica de cómo se están contando las bombas adyacentes. 

#? Falta documentación de la función.  
def todas_celdas_seguras_descubiertas(tablero:list[list[int]],tablero_visible:list[list[str]])->bool:
    filas = len(tablero)
    columnas = len(tablero[0])
    #if son_matriz_y_misma_dimension(tablero,tablero_visible):
    for fila in range(filas):
        for col in range(columnas):
            if tablero[fila][col] == -1:
                if not (tablero_visible[fila][col] == VACIO or tablero_visible[fila][col] == BANDERA):
                    return False #acá
            else:
                if tablero_visible[fila][col] != str(tablero[fila][col]):
                    return False
    return True

#? Evitar poner el comentario junto al código, es mejor ponerlo arriba de la función.
#? Y en los comentarios no es necesario de hablar acerca de lo que estás haciendo, sino de lo que hace la función.
def cuantas_minas_existen(tablero:list[list[int]])->int: #Hago una funcion aux que dado un tablero me cuente la cantidad de minas que hay
    contador :int = 0 
    filas :int = len(tablero)
    columnas :int = len(tablero[0])
    for fila in range(filas):
        for col in range(columnas):
            if tablero[fila][col] == -1:
                contador +=1
    return contador

#^ las 2 funciones superiores se usan del Ej7 en adelante, que hacen acá?

""" ------------------------------------ EJERCICIO 3 ------------------------------------
    * NOTA: BIEN
"""
#? Muy parecido a crearTablaVacia, se podría haber reutilizado esa función. 
#!POLO 25-6, LO DEJAMOS? porq es parecido pero es para un tab visible, ben:analizalo.
def crear_tabla_visible_vacia(filas: int, columnas: int) -> list[list[str]]: #Creo un tablero visible donde todas sus celdas son igual a VACIO
    tabla_visible_vacia: list[list[str]] = []
    for i in range(filas):
        fila: list[str] = []
        for x in range(columnas):
            fila.append(VACIO)
        tabla_visible_vacia.append(fila)
    return tabla_visible_vacia 

"""Crea un juego con los valores dados, usa las funciones previas de colocar minas y calcular numeros para poder crear un tablero que cumpla las condiciones """
#Funcion Principal EJ 3
def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:
    res = {} #es estado juego
    res['filas'] = filas
    res['columnas'] = columnas
    res['minas'] = minas
    tablero = colocar_minas(filas, columnas,minas) #te crea tablero con 0 y minas
    calcular_numeros(tablero) #te calcula proximidad de minas
    #print("tablero desde juego:",tablero)
    res['tablero'] = tablero
    tablero_visible = crear_tabla_visible_vacia(filas,columnas) #{Todas las celdas de res[′tablero visible′] tienen valor igual a VACIO
    res['tablero_visible'] = tablero_visible 
    res['juego_terminado'] = False 
    return res
#^Faltan tipar: res, tablero, tablero_visible.

""" ------------------------------------ EJERCICIO 4 ------------------------------------
    #* NOTA: BIEN
    #! No Se hizo ningún test para esta función.
"""
#EJ 4
#? Falta documentación de la función.
def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]: #si esto no se usa fijarse para q era
    tablero_visible_copia =[]
    for fila in estado['tablero_visible']:
        tablero_visible_copia.append(fila.copy())
    return tablero_visible_copia


""" ------------------------------------ EJERCICIO 5 ------------------------------------
    * NOTA: BIEN-
"""

#EJ 5
def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """ Pone y saca banderas a pedido del jugador colocando una bandera en una celda vacia
         tambien hace que no valga esto si es que la celda no es una celda vacia """
    
    if estado['juego_terminado'] or estado['tablero_visible'][fila][columna] != VACIO and estado['tablero_visible'][fila][columna] != BANDERA: #este tira q no pasa
        return estado
        #! Por qué devuelven estado??
    
    elif estado['tablero_visible'][fila][columna] == VACIO:
        estado['tablero_visible'][fila][columna] = BANDERA
        
    elif estado['tablero_visible'][fila][columna] == BANDERA:
        estado['tablero_visible'][fila][columna] = VACIO

""" ------------------------------------ EJERCICIO 6 ------------------------------------
    * NOTA: BIEN-
"""

#^ Lo que se hizo en este ejercicio es una implementación de un algoritmo de búsqueda en anchura (BFS) para descubrir celdas en el tablero del buscaminas. Pero esto es una optimización de la busqueda, no era necesario hacer algo así.
#! No se tipo los parametros de la función, ni el retorno. Además, no se documentó la función.
def caminos_descubiertos(tablero, visible, fila_inicial, columna_inicial):
    filas = len(tablero)
    columnas = len(tablero[0])

    descubiertas = []
    visitados : list[tuple[int,int]] = []
    cola :list[tuple[int,int]] = [(fila_inicial, columna_inicial)] #donde se define como cola?
    #! El comentario es cierto, por qué se define como cola si es una lista?
            
    cola.append((fila_inicial, columna_inicial)) #cola append? cola es una lista o una cola???
    #SI BIEN ESTO ESTA BIEN ESTAN TOMANDO A COLA NO COMO UNA "COLA" SI NO COMO UNA LISTA LA CUAL SACAN SU PRIMER ELEMENTO (COSA Q TMB SE HACE EN COLAS)..
    #^ Estos comentarios me suenan a que alguien del grupo hizo esto, pero el resto no lo entendió. No son comentarios que deberían quedar para la entrega de un TP.
    while cola: #! A pesar de que evaluar `cola` así funciona, no está bien.
        fila_actual, columna_actual = cola.pop(0)
        #! El usar `pop(0)` en una lista no es eficiente, por eso no se ve en clases.
        #^ Si se quiere hacer una cola, se debería usar una `FifoQueue` de la librería `queue`, y sacar con la función `get()`.0

        if (fila_actual, columna_actual) in visitados:
            continue

        if visible[fila_actual][columna_actual] == BANDERA:
            continue

        if tablero[fila_actual][columna_actual] == -1:
            continue
        #^ No es buena practica el uso de un `continue` sin una clara justificación. Es mejor hacer un "if else" que abarque todo el loop para continuar si no se cumple la condición.

        visitados.append((fila_actual, columna_actual))
        descubiertas.append((fila_actual, columna_actual))

        if tablero[fila_actual][columna_actual] == 0:
            for cambio_fila in [-1, 0, 1]:
                for cambio_columna in [-1, 0, 1]:
                    if cambio_fila == 0 and cambio_columna == 0:
                        continue
                    #^ Acá también se podría haber hecho un "if else" para evitar el uso de `continue`.
                    nueva_fila = fila_actual + cambio_fila
                    nueva_columna = columna_actual + cambio_columna

                    if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                        if (nueva_fila, nueva_columna) not in visitados:
                            cola.append((nueva_fila, nueva_columna))

    return descubiertas


#EJ 6
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """ Descubre la celda que elija el jugador, puede pasar que el juego ya haya terminado(no pasa nada)
         que se descubra una celda con bomba(se termina el juego y se muestran todas las bombas)
           que se descubra una celda con 0(se abren los caminos hasta llegar a un numero mas grande que 0)
             que se descubra una celda con un numero mayor a 0(solo se descubre esa celda) """
    #! No se entiende el comentario.
    if estado['juego_terminado']: #si se termina el juego no se hace nada 
        return
    
    if estado['tablero'][fila][columna] == -1:
        for f in range(estado["filas"]):
            for c in range(estado["columnas"]):
                if estado["tablero"][f][c] == -1:
                    estado["tablero_visible"][f][c] = BOMBA
        estado["juego_terminado"] = True
        return
    
    caminos = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna) #si no es bomba miro el camino
    for camino in caminos:
        for (f, c) in caminos:
            estado["tablero_visible"][f][c] = str(estado["tablero"][f][c]) #copia el numero del tablero real al visible 

    if todas_celdas_seguras_descubiertas(estado['tablero'],estado['tablero_visible']): #si todas las celdas buenas se descubren ganas   
        estado['juego_terminado'] = True
    #* El código de esta función fue bien estructurado. Se entiende que se quiere hacer.

""" ------------------------------------ EJERCICIO 7 ------------------------------------
    * NOTA: BIEN
"""

#EJ 7
def verificar_victoria(estado: EstadoJuego) -> bool:
    """ Mira si ganaste con la funcion aux de todas_celdas_seguras_descubiertas 
         de manera que si no queda ninguna celda segura sin mostrar en tablero visible ganas"""
    if todas_celdas_seguras_descubiertas(estado['tablero'],estado['tablero_visible']) == True:
        return True
    else:
        return False
    #^ El código es correcto, pero se podría haber simplificado a `return todas_celdas_seguras_descubiertas(...)` ya que la función devuelve un bool.

""" ------------------------------------ EJERCICIO 8 ------------------------------------
    * NOTA: BIEN-
"""
#EJ 8
def reiniciar_juego(estado: EstadoJuego) -> None:
    """ Reinicia el juego y crea un tablero nuevo mirando que
          el tablero nuevo sea distinto a el tablero viejo """
    visible = estado['tablero_visible'] 
    for fila in range(len(visible)): 
        for columna in range (len(visible[0])):
            visible[fila][columna] = VACIO
    estado['juego_terminado'] = False
    filas = estado['filas']
    columnas = estado['columnas']
    minas = estado['minas']
    nuevo_tab = colocar_minas(filas,columnas,minas)
    calcular_numeros(nuevo_tab) #le calculo los numeros
    #^ Todo el código de arriba no es lo mismo que lo que se hace en `crear_juego`?
    tablero_viejo = []
    for fila in range (len(estado['tablero'])) :
        tablero_viejo.append(estado['tablero'][fila])
        #! Este for es innecesario, para qué se obtiene una copia del tablero viejo si este todavía es accesible?
    
    #* Bien por generar tableros hasta que sea distinto al viejo.  
    while (nuevo_tab == tablero_viejo) :
        nuevo_tab = colocar_minas(filas,columnas,minas)
        calcular_numeros(nuevo_tab)
        #^ código repetido con lo de arriba. Como podrían evitarlo?

    estado['tablero'] = nuevo_tab #y finalmente reemplazo en el tablero previo al nuevo que recien hice 
    return

""" ------------------------------------ EJERCICIO 8 ------------------------------------
    * NOTA: BIEN
"""
#EJ 9
def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    lineas = [] #variable para ir apendeanddo las lineas
    #primero lo hacemos para estado['tablero'], osea vamos a crear a 'tablero.txt'
    for fila in range (len(estado['tablero'])): #empiezo a recorrera cadad fila del tablero
        linea = '' #creo una variable que es "vacia" para ir agregandole cada caracter
        for col in range(len(estado['tablero'][fila])) : #empiezo a recorrer cada columna
            linea+= str(estado['tablero'][fila][col]) #voy formando mi linea
            if col < (len(estado['tablero'][fila]) - 1): #esto me asegura no poner una coma al final de la linea
                linea+=','
        lineas.append(linea + '\n') #y aca apendeo mi linea construida y el espacio 
        #! Hay mucho comentario. Los comentarios debén ayudar a entender, estos obstruyen la lectura del código.
        
    ruta_tablero = os.path.join(ruta_directorio,'tablero.txt') #aca usamos lo que decia en el tp que poddiamos usar para unir dos rutas de archivo
    archivo = open(ruta_tablero, "w",)  # abrimos el archivo en modo escritura
    #? Recomendación: Usar la configuración encoding='utf8' al abrir los archivos.
    archivo.writelines(lineas) #leemos las lineas
    archivo.close()  # y lo cerramos
    #^ Para qué se agregan estos comentarios de líneas de código que explicitamente se ve que hacen? No hay que agregar comentarios de código obvios.
    
    #ahora lo hacemos para estado['tablero_visible'], osea vamos a crear a 'tablero_visible.txt'
    #la logica es la misma que lo anteriormente explicado, solo que agregamos 3 condiciones mas que las pedia el enunciado
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
    return


""" ------------------------------------ EJERCICIO 10 ------------------------------------
    ! NOTA: MAL
    ! FALLAN TODOS LOS TESTS DE ESTE EJERCICIO.
    - No se donde están los errores, por lo que van a tener que armar de vuelta la idea
    - No se entienden muchas de las partes, y además hay MUCHO código.
    - Hay comentarios en las llamadas a funciones, luego las funciones dice otra cosa. Está muy dificil corregirlo. Piensen que hay una persona detras que debe entender y corregir lo que quisieron hacer.
    ! No abusar de comentar cada línea de código, solo empeora la comprensión del código.
        - Se que puede sonar a que soy muy minusioso, pero diganme si es necesario comentar por ejemplo que el close() cierra el archivo y que el open() lo abre?
    - No poner los comentarios sobre la misma línea de código, es mejor ponerlo arriba de la función.
"""

#10
def contar_lineas(ruta:str,nombre_archivo:str)->int: #dada una ruta y un nombre de archivo, me dice cuantas lineas tiene ese archivo
    nueva_ruta = ruta + '/' + nombre_archivo 
    archivo = open(nueva_ruta,"r")
    cant_lineas = len(archivo.readlines())
    archivo.close()
    return cant_lineas

#! Por qué devuelve un int??
#^ Mal nombre para la función, por qué se llama `mostrar_lineas`?
def mostrar_lineas(ruta:str,nombre_archivo:str)->int: #Dada una ruta y un nombre de archivo, me devuelve la lista de lineas de ese archivo
    nueva_ruta = ruta + '/' + nombre_archivo 
    archivo = open(nueva_ruta,"r")
    lineas = archivo.readlines()
    archivo.close()
    return lineas

def palabras_a_lista(lineas: list[str]) -> list[str]: #Dada una lista de lineas, devuelvo una lista de str que contiene los mismos caracteres sacando blancos, tabs y espacios
    lista_palabras: list[str] = [] 
    palabra_actual: str = ""

    for linea in lineas:
        for caracter in linea:
            if caracter not in ["\n"]:
                palabra_actual += caracter  # sigo armando la palabra
            else:
                if len(palabra_actual) > 0:
                    lista_palabras.append(palabra_actual)  # guardo la palabra completa
                    palabra_actual = ""  # empiezo una nueva palabra
        # por si la línea termina en una palabra sin espacio al final
        if len(palabra_actual) > 0:
            lista_palabras.append(palabra_actual)
            palabra_actual = ""

    return lista_palabras

def cantidad_comas(ruta:str,nombre_archivo:str)->int: #Dada una ruta y un nombre de archivo, me cuenta la cant de comas de ese archivo
    nueva_ruta = ruta + '/' + nombre_archivo 
    archivo = open(nueva_ruta,"r").read()
    #! NO se cierra el archivo, esto está causando problemas de memoria.
    contador = 0
    for caracter in archivo:
        if caracter == ',':
            contador += 1
    return contador

#! El agregar comentarios por cada línea hace más dificil entender lo que hacen. 
#! No hay que explicar línea por línea, sino explicar que hace en general un bloque de código.
#^ Incluso se dice que "un buen código no necesita comentarios", ya que el código debería ser lo suficientemente claro por sí mismo. No lo digo para que no pongan ningún comentarios, sino para que lo tengan en cuenta cada que agregan un comentario.
#^ Por cierto, hago la diferenciación entre "comentario" y "documentación", lo cual si es requerido por el TP.
def pasar_tablero_archivo_a_tablero_real(ruta:str,nombre_archivo:str)->list[list[int]]:
    lineas_sin_limpiar = mostrar_lineas(ruta,nombre_archivo) #obtenemos las lineas del archivo 
    lineas_limpias = palabras_a_lista(lineas_sin_limpiar) #limpiamos los saltos de linea para trabajar comodamente
    filas = [] #aca voy a ir appendeando las columnas para formar mi matriz
    for linea in lineas_limpias: #empiezo a ver linea por linea
        if len(linea) > 1:
            caracter_suplente = ""
            columna = [] #aca voy a ir metiendo los numeros
            for caracter in linea: #empiezo a ver cada caracter dentro de mi linea 
                if caracter != ',' and caracter != ' ': #si no es una coma entonces debo analizarlo (las comas con el append se van a ir poniendo solas entonces las ignoro)
                    caracter_suplente += caracter #le agrego el caracter
                    if caracter_suplente == '-': #Si es un menos, continuo viendo porque entonces voy a encontrar una mina
                        continue
                    elif caracter_suplente == '-1': #Cuando ya forme mi -1
                        caracter_suplente = "" #reseteo mi variable
                        numero = -1 
                        columna.append(numero) #y apendeo el -1
                    elif caracter_suplente in ['0','1','2','3','4','5','6','7','8']: #si mi caracter es un valor valido de un tablero
                        numero = int(caracter_suplente) #lo convierto en entero
                        caracter_suplente = "" #reseteo la variable
                        columna.append(numero) #y lo agrego
                    else: #en el caso de que sea un numero mayor a 8, entonces estoy viendo un tablero que es erroneo, y returneo la funcion
                        return # Habra que agregar un return false, o que podemos hacer en ese caso ???
            filas.append(columna) #y cada vez que termine de recorrer una linea del archivo, agrego mi columna a mi lista de filas
    return filas

#^ Esta función se parece mucho a la anterior, pensar como se las podría condensar a una sola función. 
#!falta verlo
#Dada una ruta y un tablero_visible.txt, me construyo mi tablero_visible de tipo list[list[str]]
def pasar_tablero_archivo_a_tablero_visible_real(ruta:str,nombre_archivo:str)->list[list[str]]:
    lineas_sin_limpiar = mostrar_lineas(ruta,nombre_archivo) #obtenemos las lineas del archivo 
    lineas_limpias = palabras_a_lista(lineas_sin_limpiar) #limpiamos los saltos de linea para trabajar comodamente
    filas = [] #aca voy a ir appendeando las columnas para formar mi matriz
    for linea in lineas_limpias: #empiezo a ver linea por linea
        if len(linea) > 1:
            caracter_suplente = ""
            columna = [] #aca voy a ir metiendo los numeros
            for caracter in linea: #empiezo a ver cada caracter dentro de mi linea 
                if caracter != ',': #si no es una coma entonces debo analizarlo (las comas con el append se van a ir poniendo solas entonces las ignoro)
                    caracter_suplente += caracter #le agrego el caracter
                    if caracter_suplente == '-': #Si es un menos, continuo viendo porque entonces voy a encontrar una mina
                        continue
                    elif caracter_suplente == '-1': #Cuando ya forme mi -1
                        caracter_suplente = "" #reseteo mi variable
                        numero = '-1' 
                        columna.append(numero) #y apendeo el -1
                    elif caracter_suplente in ['?','*','0','1','2','3','4','5','6','7','8']: #si mi caracter es un valor valido de un tablero
                        numero = (caracter_suplente) #lo agrego
                        caracter_suplente = "" #reseteo la variable
                        columna.append(numero) #y lo agrego
                    else: #en el caso de que sea un numero mayor a 8, entonces estoy viendo un tablero que es erroneo, y returneo la funcion
                        return # Habra que agregar un return false, o que podemos hacer en ese caso ???
            filas.append(columna) #y cada vez que termine de recorrer una linea del archivo, agrego mi columna a mi lista de filas
    return filas



def chequear_valores_separados_coma_tab_int(ruta:str,nombre_archivo:str)->bool:
    lineas_sin_limpiar = mostrar_lineas(ruta,nombre_archivo) #obtenemos las lineas del archivo 
    lista_lineas = palabras_a_lista(lineas_sin_limpiar) #obtengo las lineas del archivo sin espacios en blanco
    long_filas = len(lista_lineas) #mi longitud de filas
    caracteres = ['-','0','1','2','3','4','5','6','7','8'] #los caracteres validos dentro de un tablero de enteros
    for fila in range (long_filas):
        long_columnas = len(lista_lineas[fila]) 
        if lista_lineas[fila][0] == ',' or lista_lineas[fila][long_columnas-1] == ',': #me fijo si en la ultima fila y en la primera existe una coma (esos casos son totalmente invalidos)
            return False
        for columna in range (long_columnas):#esto es para ver caracter a caracter
            if lista_lineas[fila][columna] == ',': #si es una coma, tengo que ver si el valor de atras y adelante son caracteres validos de un tab visible
                if lista_lineas[fila][columna-1] not in caracteres or lista_lineas[fila][columna+1] not in caracteres and columna < long_columnas:
                    return  False
    return True

#Hago lo mismo pero para un tablero visible (pues tablero y tablero_visible manejan caracteres distintos)
def chequear_valores_separados_coma_tab_vis(ruta:str,nombre_archivo:str)->bool:
    lineas_sin_limpiar = mostrar_lineas(ruta,nombre_archivo) #obtenemos las lineas del archivo 
    lista_lineas = palabras_a_lista(lineas_sin_limpiar)
    print(lista_lineas)
    long_filas = len(lista_lineas)
    caracteres = ['*','?','0','1','2','3','4','5','6','7','8'] #los caracteres validos dentro de un tablero visible
    for fila in range (long_filas):
        long_columnas = len(lista_lineas[fila])
        if lista_lineas[fila][0] == ',' or lista_lineas[fila][long_columnas-1] == ',':
            return False
        for columna in range (long_columnas):#esto es para ver caracter a caracter
            if lista_lineas[fila][columna] == ',': #si es una coma, tengo que ver si el valor de atras y adelante son caracteres validos de un tab visible
                if lista_lineas[fila][columna-1] not in caracteres or lista_lineas[fila][columna+1] not in caracteres and columna < long_columnas:
                    return  False
    return True


#Dado un tablero y un tablero visible chequeo que tengan el mismo numero (salvo el -1 y los caracteres especiales de tab visible)
def chequear_numeros_iguales_en_tableros(tablero:list[list[int]],tablero_visible:list[list[str]])->bool: 
    for i in range (len(tablero)):
        for j in range (len(tablero[0])):
            if tablero_visible[i][j] not in ['?','*'] and tablero[i][j] != -1:
                if tablero_visible[i][j] != str(tablero[i][j]):
                    return False
    return True


def chequear_si_tablerotxt_correcto(tablero:list[list[int]])->bool:
    #PPRIMERO chequeo si es matriz valida
    if (len(tablero) < 1 or len(tablero[0]) < 1): 
        return False
    for fila in range (len(tablero)):
        if ( len(tablero[fila]) != len(tablero[0]) ): 
            return False 
        
    copia_tab = []
    for i in range (len(tablero)):
        copia_tab.append(tablero[i].copy()) #hacemos una copia del tablero
    for i in range (len(copia_tab)):
        for j in range (len(copia_tab[i])):
            if copia_tab[i][j] != -1:
                copia_tab[i][j] = 0  #todo num dentro de copia tab != -1 va a pasar a ser 0
    calcular_numeros(copia_tab) #le calculo los numeros
    if copia_tab == tablero: #si son iguales entonces todo okey
        return True
    else: 
        return False #sino false
    
def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
   
   res = False #Mi booleano a devolver primero tomo como que es Falso, segun lo que pase despues lo voy a cambiar o no

   #Dividi el problema en analizar cada condicion por separado, no necesariamante cadda linea del asegura, hay 
   #condiciones que comparten algunos aseguras del ej 10 
   
   condicion0 = existe_archivo(ruta_directorio,'tablero.txt') #En ruta directorio, existe tablero txt
   
   condicion1 = existe_archivo(ruta_directorio,'tablero_visible.txt') #En ruta directorio, existe tablero_visible.txt
   
   condicion2 = contar_lineas(ruta_directorio,'tablero.txt') == contar_lineas(ruta_directorio,'tablero_visible.txt') #En ambos archivos me fijo si la cant de lineas es la misma
   
   condicion3 = cantidad_comas(ruta_directorio,'tablero.txt') == cantidad_comas(ruta_directorio,'tablero_visible.txt') #En ambos archivos me fijo si la cant de comas es igual

   tablero = pasar_tablero_archivo_a_tablero_real(ruta_directorio,'tablero.txt') #Dado el archivo de tablero.txt, creo un tablero de enteros
   
   condicion4 = chequear_si_tablerotxt_correcto(tablero) #Chequeo si es correcto, osea si hay -1 y los adyacentes corresponden con calcular numeros
   
   tablero_visible = pasar_tablero_archivo_a_tablero_visible_real(ruta_directorio,'tablero_visible.txt') #Dado el archivo de tablero_visible.txt, creo un tablero de enteros
   
   condicion5 = chequear_valores_separados_coma_tab_vis(ruta_directorio,'tablero_visible.txt') #Chequeo si sus valores estan separados por coma correctamente
   
   condicion6 = chequear_valores_separados_coma_tab_int(ruta_directorio,'tablero.txt') #Chequeo si sus valores estan separados por coma correctamente
   
   condicion7 = chequear_numeros_iguales_en_tableros(tablero,tablero_visible) #Chequeo que si hay numero visible en tab visible, este debe estar en tablero

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
        """ solucionados polo 25-6-2025 18:20hrs"""
        #! Por qué el return está dentro del if y del else? No se lo podría haber dejado afuera?.  
    
   else:
    return res

#* La estructura de cargar_estado es buena, mejor que la de otras funciones. Sin embargo se está cometiendo un error muy grave.
""" solucionados polo 25-6-2025 18:20hrs
#! Por qué cada función auxiliar lee el archivo?? Hagan una sola lectura del archivo con readlines() y pasen las líneas a las funciones auxiliares.
#! Este error de implementación hace que el código sea ineficiente y hasta genera errores con la lectura de archivos.
"""
#Aca probe con un ejemplo que nos dio el enunciado del TP
#Los archivos los tienen que crear ustedes y comprobar que en la terminal estan parados en tp_intro_progra
#Y que dentro de esa carpeta, este el buscaminas, y que exista la carpeta: data 
#En esta tienen que existir tablero.txt y tablero_visible.txt

#La ruta igual le pueden cambiar el nombre no hay drama, pero asegurense de eso!!

#estado = {'filas':50,'columnas':15,'minas':150,'tablero':[[1,7],[8,0]],'tablero_visible':[[' ','1'],['1','1']],'juego_terminado':False}

#ruta_archivo = './data'
#tablero = [[1, 1, 1], [2, -1, 2], [2, -1, 2]]
#print(tablero)


#print(cargar_estado(estado,ruta_archivo))
#print(estado)

#El output que me da esta acorde a lo que dice el ejemplo del enunciado del TP, despues nos queda hacer casos de test nomas y estamos
