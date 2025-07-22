import unittest
from buscaminas import * 
from buscaminas import BOMBA, BANDERA, VACIO, EstadoJuego

def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True



class colocar_minasTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
        



class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])

class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)
    

class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)



class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])


class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])
        


class obtener_estado_tableroTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

#! Por qué separaron los tests de la catedra de los suyos? Podían tenerlos todos juntos.

""" ------------------------------------ EJERCICIO 1 ------------------------------------
    ! Faltan multiples tests: como matriz no cuadrada, matriz grande, matriz con muchas bombas,...
"""

class TestColocarMinas(unittest.TestCase): #1
    def test_colocar_minas_dimensiones_y_minas(self):
        filas, columnas, minas = 4, 5, 6
        tablero = colocar_minas(filas, columnas, minas)
        self.assertEqual(len(tablero), filas)
        for fila in tablero:
            self.assertEqual(len(fila), columnas)
        total_minas = 0
        for fila in tablero:
            for celda in fila:
                if celda == -1:
                    total_minas += 1
        self.assertEqual(total_minas, minas)
    def test_colocar_minas_erroneo(self):
        resultado1 = colocar_minas(3, 3, 0)
        self.assertEqual(resultado1, [[]])
        resultado2 = colocar_minas(2, 2, 4)
        self.assertEqual(resultado2, [[]])

""" ------------------------------------ EJERCICIO 2 ------------------------------------
    ! Faltan multiples tests: matriz pequeña, matriz grande, matriz con solo un cero, ...
"""

class TestCalcularNumeros(unittest.TestCase): #2
    def test_calcular_numeros_suma_correcta(self):
        # creo un tablero con bomba y verifico numeros
        tablero = [
            [0, -1],
            [0, 0]
        ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[1, -1], [1, 1]])

""" ------------------------------------ EJERCICIO 3 ------------------------------------
    ! Faltan multiples tests: tablero grande, tablero pequeño, ...
"""

class TestCrearJuego(unittest.TestCase): #3
    def test_juego_valido(self):
        estado = crear_juego(3, 3, 3)
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(len(estado['tablero']), 3)
        self.assertEqual(len(estado['tablero_visible']), 3)
        for fila in estado['tablero_visible']:
            for celda in fila:
                assert celda == VACIO
        self.assertFalse(estado['juego_terminado'])
    
    #! Este test no está testeando nada relevante.
    def test_crear_juego_estado_valido(self): #capaz no es necesario por si borramos estado valido 
        estado = crear_juego(2, 2, 1)
        self.assertIn('tablero', estado)
        self.assertIn('tablero_visible', estado)
        self.assertIn('juego_terminado', estado)
        self.assertTrue(isinstance(estado['tablero'], list))
        self.assertEqual(estado['juego_terminado'], False)
    
""" -------------------------------- EJERCICIO 4 --------------------------------
    ! No se hizo ningún test nuevo! Se dejo solo el que ya venía.
    ! Ejemplo de tests: Juego sin finalizar, tablero finalizado, chequear que realmente sea una copia, modificar copia no afecta original, ...
"""

""" -------------------------------- EJERCICIO 5 --------------------------------
    * BIEN
"""
class TestMarcarCelda(unittest.TestCase): #5
    def test_marcar_y_desmarcar_celda(self):
        # marca y desmarca una celda y mira lo que pasa
        estado = crear_juego(2, 2, 1)
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], BANDERA)
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], VACIO)
    def test_marcar_celda_no_valida_si_no_es_vacia_ni_bandera(self):
        estado = {'filas': 2,'columnas': 2,'minas': 0,
                  'tablero': [[0, 1], [1, 1]],
                  'tablero_visible': [['0', '1'], [VACIO, VACIO]],
                  'juego_terminado': False}
        #no deberia hacer nada: la celda sigue siendo "1" 
        marcar_celda(estado, 0, 1)
        # marco una celda que ya fue descubierta (tiene un número)
        self.assertEqual(estado['tablero_visible'][0][1], '1')
    def test_no_marcar_si_juego_terminado(self):
        estado = {'filas': 2,'columnas': 2,'minas': 0,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
                  'juego_terminado': True}
        marcar_celda (estado,0,0)
        self.assertEqual(estado['tablero_visible'][0][0],VACIO)
    def test_marcar_celda_pone_y_saca_bandera(self):
        estado = {'filas': 2,'columnas': 2,'minas': 1,
              'tablero': [[-1, 1], [1, 1]],
              'tablero_visible': [[VACIO,VACIO], [VACIO, VACIO]],
              'juego_terminado': False}
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'][0][0], BANDERA)
        marcar_celda(estado,0,0)
        self.assertEqual(estado['tablero_visible'][0][0], VACIO)
  
""" -------------------------------- EJERCICIO 6 --------------------------------
    - Faltan algunos tests como: descubrir celda segura y ganar, descubrir bomba al primer intento.
    - En los tests actuales no se está testeando que el estado no haya sido modificado por la función.
    - También tendrían que haber hecho tests con tableros más grandes y con celdas seguras dispuestas en patrones dificiles para saber que caminos_descubiertos funciona bien en todos los casos.
"""
class TestDescubrirCelda(unittest.TestCase): #6
    def test_descubrir_bomba_termina_juego(self):
        # si hay una bomba el juego se termina
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
                  'juego_terminado': False}
        descubrir_celda(estado, 0, 0)
        self.assertTrue(estado['juego_terminado'])
        self.assertEqual(estado['tablero_visible'][0][0], BOMBA)
        #self.assertFalse(todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']))
    def test_descubrir_celda_no_hace_nada_si_juego_terminado(self):
        estado = {'filas': 2,'columnas': 2,'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[BOMBA, VACIO], [VACIO, VACIO]],
                  'juego_terminado': True}
        descubrir_celda(estado, 0, 1)
        self.assertEqual(estado['tablero_visible'], [[BOMBA, VACIO], [VACIO, VACIO]])
        
    def test_descubrir_segura_no_termina_juego(self):
        # si no hay una bomba(celda segura) el juego sigue 
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[1, -1], [1, 1]],
                  'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
                  'juego_terminado': False}
        descubrir_celda(estado, 0, 0)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero_visible'][0][0], '1')
    def test_caminos_descubiertos_ignora_bandera(self):
        tablero = [[0, 0], [0, 0]]
        visible = [[VACIO, BANDERA],[VACIO, VACIO]]
        resultado = caminos_descubiertos(tablero, visible, 0, 0) #la celda (0, 1) tiene una bandera, no tiene que estar en el resultado
        self.assertNotIn((0, 1), resultado)
    def test_caminos_descubiertos_ignora_mina(self):
        tablero = [[0, -1],[0, 0]]
        visible = [[VACIO, VACIO],[VACIO, VACIO]]
        resultado = caminos_descubiertos(tablero, visible, 0, 0)
        self.assertNotIn((0, 1), resultado) # la celda (0, 1) tiene una mina, no tiene que estar en el resultado
    def test_caminos_descubiertos_no_repite_visitados(self):
        tablero = [[0, 0],[0, 0]]
        visible = [[VACIO, VACIO],[VACIO, VACIO]]
        resultado = caminos_descubiertos(tablero, visible, 0, 0)
        self.assertEqual(len(resultado), len(set(resultado))) # No se tienen que repetir celdas en el resultado

""" -------------------------------- EJERCICIO 7 --------------------------------
    * BIEN
"""
class TestVerificarVictoria(unittest.TestCase): #7
    def test_victoria_cuando_todas_seguras_descubiertas(self):
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[VACIO, '1'], ['1', '1']],
                  'juego_terminado': False}
        self.assertTrue(verificar_victoria(estado))
    def test_victoria_cuando_no_gano(self):
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[BOMBA, '1'], ['1', '1']],
                  'juego_terminado': False}
        self.assertFalse(verificar_victoria(estado))
    def test_verificar_victoria(self):
        estado = {'filas': 2,'columnas': 2,'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[VACIO, '1'], ['1', '1']],
                  'juego_terminado': False}
        descubrir_celda(estado, 0, 1) #descubro la ultima celda 
        self.assertTrue(estado['juego_terminado']) # deberia ganar 
        
""" -------------------------------- EJERCICIO 8 --------------------------------
    - Faltan algunos tests: reiniciar juego perdido, reiniciar juego ganado.
"""
class TestReiniciarJuego(unittest.TestCase): #8
    # mira que al reiniciar el juego se cree un nuevo tablero distinto 
    def test_reiniciar_juego_resetea_estado(self):
        estado = crear_juego(2, 2, 1)
        estado['tablero_visible'][0][0] = '1'
        estado['juego_terminado'] = True
        viejo_tablero = estado['tablero']
        reiniciar_juego(estado)
        self.assertEqual(estado['juego_terminado'], False)
        self.assertTrue(all(cell == VACIO for fila in estado['tablero_visible'] for cell in fila))
        #^ No vimos la función all() en clases.
        self.assertNotEqual(viejo_tablero, estado['tablero'])
        #! Falta chequear el resto de los atributos del estado.

""" -------------------------------- EJERCICIO 9 --------------------------------
    - Faltan algunos tests: - Tableros de tamaño minimo y máximo, con muchas minas o con solo una, tablero con todos los símbolos...
"""

#TEST EJ 9
def contar_comas(ruta:str)->int:
    archivo = open(ruta,"r")
    lineas = archivo.readlines()
    archivo.close()
    contador = 0
    for linea in lineas:
        for caracter in linea:
            if caracter == ',':
                contador += 1
    return contador


class guardar_estadoTest(unittest.TestCase):
    #En ruta directorio se guardan exactamente 2 archivos:
    def test_archivos_creados(self):
        ruta = "./data"  #asumimos que ya existe el directorio
        estado = {
            'filas': 2,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [
                [-1,1],
                [1,1]],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]]}

        guardar_estado(estado, ruta)

        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta, 'tablero_visible.txt')

        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_tablero_visible))

    #tablero.txt: se guarda el estado de estado[′tablero′], separando por comas (‘,’) los valores del tablero

    def test_tablero_txt_contenido_correcto(self):
        ruta = "./data"
        estado = {
            'filas': 2,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [
                [-1,1],
                [1,1]],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]]}
        
        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero, "r")
        lineas = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas, ["-1,1\n", "1,1\n"])

    #tablero visible.txt: se guarda el estado de estado[′tablero visible′], separando por comas (‘,’) los valores 
    #del tablero visible, guardando ′∗′en lugar de BANDERA y guardando ′?′ en lugar de VACIO}
    def test_tablero_visible_contenido_correcto(self):
        ruta = "./data"
        estado = {
            'filas': 2,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [
                [-1,1],
                [1,1]],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]]}
        
        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero, "r")
        lineas = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas, ["*,?\n", "?,?\n"])


#asegura: {La cantidad de l´ıneas de cada archivo guardado es igual a estado[filas]
#considerando una linea cuando
#la cantidad de caracteres sea mayor a 0.}
    #! TESTS con nombre igual, uno de los dos no se está ejecutando por ello.
    def test_tablero_visible_contenido_correcto(self):
        ruta = "./data"
        estado = {
            'filas': 3,
            'columnas': 2,
            'minas' : 2,
            'juego_terminado': False,
            'tablero': [
                [-1,1],
                [1,1],
                [1,-1]],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO,'1'],
                [VACIO, BANDERA]]}
        guardar_estado(estado, ruta)

        ruta_tablero = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero, "r")
        lineas_visible = archivo.readlines()
        archivo.close()


        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        self.assertEqual(len(lineas_visible), estado['filas'])
        self.assertEqual(len(lineas_txt), estado['filas'])
#
    def test_comas_correctas(self):
        ruta = "./data"
        estado = {
            'filas': 3,
            'columnas': 2,
            'minas' : 2,
            'juego_terminado': False,
            'tablero': [
                [-1,1],
                [1,1],
                [1,-1]],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO,VACIO],
                [VACIO, BANDERA]]}
        
        guardar_estado(estado, ruta)

        ruta_tablero_vis = os.path.join(ruta,'tablero_visible.txt')
        ruta_tablero_txt = os.path.join(ruta,'tablero.txt')

        self.assertEqual(contar_comas(ruta_tablero_vis), estado['filas'] * (estado['columnas'] - 1))
        self.assertEqual(contar_comas(ruta_tablero_txt), estado['filas'] * (estado['columnas'] - 1))

""" -------------------------------- EJERCICIO 10 --------------------------------
    ! MUY POCOS TESTS. Por esta razon el porcentage de Coverage es tan bajo, pues más de la mitad de su código no está testeado.
    - Piensen que tests debén agregar, puede ser que es la función que más cosas hace, así que piensenlos bien.
"""

class cargar_estadoTest(unittest.TestCase):

    
    def test_falla_sin_archivos(self):
        ruta = "./tests10/t1/"
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta)) #ESPERO FALSO PORQUE no existen archivos
        self.assertFalse(existe_archivo(ruta,'tablero.txt'))
        self.assertFalse(existe_archivo(ruta,'tablero_visible.txt'))

    # falla si # de líneas difiere
    def test_falla_lineas_distintas(self):
        ruta = "./tests10/t2/"
        estado = {}

        ruta_tablero_vis = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_visible = archivo.readlines()
        archivo.close()

        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero, "r")
        lineas_txt = archivo.readlines()
        archivo.close()
    
        self.assertNotEqual(len(lineas_visible),len(lineas_txt)) #Longitud de lineas distintas
        self.assertNotEqual(lineas_txt, lineas_visible) #Lineas distintas
        self.assertFalse(cargar_estado(estado, ruta)) #Esto nos dara false ya que la cant de lineas son distintas

    #! Por qué estos tests están comentados?
    """# 3) falla si # de comas total difiere
    def test_falla_comas_distintas(self):
        ruta = "test_ce3"
        os.mkdir(ruta)
        # ambas tienen 2 líneas, pero distinto total de comas
        with open(os.path.join(ruta, "tablero.txt"), "w") as f:
            f.write("-1,0\n0,-1\n")
        with open(os.path.join(ruta, "tablero_visible.txt"), "w") as f:
            f.write("*,?,?\n?,*\n")  # 3 comas vs. 1
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta))
        os.remove(os.path.join(ruta, "tablero.txt"))
        os.remove(os.path.join(ruta, "tablero_visible.txt"))
        os.rmdir(ruta)

    # 4) falla si tablero.txt no cumple la lógica de -1 y adyacentes
    def test_falla_tablero_invalido(self):
        ruta = "test_ce4"
        os.mkdir(ruta)
        # un “9” que no puede aparecer
        with open(os.path.join(ruta, "tablero.txt"), "w") as f:
            f.write("-1,9\n0,0\n")
        with open(os.path.join(ruta, "tablero_visible.txt"), "w") as f:
            f.write("?,?\n?,?\n")
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta))
        os.remove(os.path.join(ruta, "tablero.txt"))
        os.remove(os.path.join(ruta, "tablero_visible.txt"))
        os.rmdir(ruta)

    # 5) falla si tablero_visible.txt tiene caracteres no permitidos
    def test_falla_visible_con_invalido(self):
        ruta = "test_ce5"
        os.mkdir(ruta)
        with open(os.path.join(ruta, "tablero.txt"), "w") as f:
            f.write("-1,0\n0,0\n")
        # aquí “X” no está en [0–8], '*', '?'
        with open(os.path.join(ruta, "tablero_visible.txt"), "w") as f:
            f.write("X,?\n?,?\n")
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta))
        os.remove(os.path.join(ruta, "tablero.txt"))
        os.remove(os.path.join(ruta, "tablero_visible.txt"))
        os.rmdir(ruta)

    # 6) falla si no es matriz (líneas con distinto número de comas)
    def test_falla_formato_no_matriz(self):
        ruta = "test_ce6"
        os.mkdir(ruta)
        with open(os.path.join(ruta, "tablero.txt"), "w") as f:
            f.write("0,0,0\n1,1\n")
        with open(os.path.join(ruta, "tablero_visible.txt"), "w") as f:
            f.write("?,?,?\n?,?\n")
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta))
        os.remove(os.path.join(ruta, "tablero.txt"))
        os.remove(os.path.join(ruta, "tablero_visible.txt"))
        os.rmdir(ruta)

    # 7) caso exitoso
    def test_exito_cargar(self):
        ruta = "test_ce7"
        os.mkdir(ruta)
        # 3×2 tablero real
        with open(os.path.join(ruta, "tablero.txt"), "w") as f:
            f.write("-1,1\n")
            f.write("2,1\n")
            f.write("1,0\n")
        # visible: '*'->BANDERA, '?'->VACIO, números
        with open(os.path.join(ruta, "tablero_visible.txt"), "w") as f:
            f.write("*,?\n")
            f.write("2,1\n")
            f.write("1,*\n")
        estado = {
            'filas': 99, 'columnas': 99, 'minas': 99,
            'tablero': [], 'tablero_visible': [], 'juego_terminado': True
        }
        res = cargar_estado(estado, ruta)
        self.assertTrue(res)
        # debe actualizar todo según el enunciado
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 2)
        # minas = número de '-1' en tablero.txt
        self.assertEqual(estado['minas'], 1)
        self.assertFalse(estado['juego_terminado'])
        # contenido de tablero
        self.assertEqual(estado['tablero'], [[-1, 1], [2, 1], [1, 0]])
        # contenido visible convertido
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            ["2", "1"],
            ["1", BANDERA]
        ])
        # limpieza
        os.remove(os.path.join(ruta, "tablero.txt"))
        os.remove(os.path.join(ruta, "tablero_visible.txt"))
        os.rmdir(ruta)"""


if __name__ == '__main__':
    unittest.main()