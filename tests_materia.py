import unittest
import os
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)

'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
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

# Tarea: Pensar cómo testear  guardar_estado y cargar_estado

class guardar_estadoTest(unittest.TestCase):
    def test_ejemplo (self):
        return

class cargar_estadoTest(unittest.TestCase):
    def test_ejemplo (self):
        return


"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

def ver_comas_por_linea(ruta:str,comas_esperadas:int)->int:
    archivo = open(ruta,"r")
    lineas = archivo.readlines()
    archivo.close()
    for linea in lineas:
        contador = 0
        for caracter in linea:
            if caracter == ',':
                contador += 1
        if comas_esperadas != contador:
            return False
    return True        

def contar_espacios(ruta:str)->int:
    archivo = open(ruta,"r")
    lineas = archivo.readlines()
    archivo.close()
    contador = 0
    for linea in lineas:
        for caracter in linea:
            if caracter == ' ':
                contador += 1
    return contador

class guardar_estadoTest(unittest.TestCase):
    #En ruta directorio se guardan exactamente 2 archivos:
    def test_archivos_creados(self):
        ruta = "ruta_valida_existente"  
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
        ruta = "direc"
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
    def test_tablero_visible_solo_banderas_y_vacios_contenido_correcto(self):
        ruta = "direc"
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

    #Chequea con tableros 3x3, donde tab vis contiene numeros visibles (ya no era todo bandera/vacio como antes)
    #Si las lineas estan joyanga
    def test_ambos_tableros_mas_grandes(self):
        ruta = "direc"
        estado = {
            'filas': 3,
            'columnas': 3,
            'minas' : 2,
            'juego_terminado': False,
            'tablero': [[1, 2, -1], [-1, 2, 1], [1, 1, 0]],
            'tablero_visible': [ 
                ['1','2',BANDERA], 
                [BANDERA,VACIO,'1'], 
                ['1', VACIO,VACIO]] } 
        
        guardar_estado(estado, ruta)

        ruta_tablero = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero, "r")
        lineas_tablero_visible = archivo.readlines()
        archivo.close()

        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero, "r")
        lineas_tablero = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas_tablero, ["1,2,-1\n","-1,2,1\n","1,1,0\n"])

        self.assertEqual(lineas_tablero_visible, ["1,2,*\n","*,?,1\n","1,?,?\n"])


#asegura: {La cantidad de l´ıneas de cada archivo guardado es igual a estado[filas]
#considerando una linea cuando
#la cantidad de caracteres sea mayor a 0.}

    def test_tableros_filas_correctas(self):
        ruta = "direc"
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

        ruta_tablero_vis = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_visible = archivo.readlines()
        archivo.close()


        ruta_tablero_txt = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        self.assertEqual(len(lineas_visible), estado['filas'])
        self.assertEqual(len(lineas_txt), estado['filas'])
#Chequeo que la cantidad de comas de cada archivo sea igual a ( estado['columnas'] -1)
    def test_comas_correctas(self):
        ruta = "direc"
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

        self.assertEqual(ver_comas_por_linea(ruta_tablero_vis, estado['columnas'] -1))
        self.assertEqual(ver_comas_por_linea(ruta_tablero_txt, estado['columnas'] -1))

    #chequeo que no existan espacios  ' '

    def test_no_hay_espacios(self):
        ruta = "direc"
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

        self.assertEqual(contar_espacios(ruta_tablero_txt),0)
        self.assertEqual(contar_espacios(ruta_tablero_vis),0)
    
    #Hago un chequeo de casi todo lo anterior pero con un tablero mas grande donde hay 6 col y 4 filas
    def test_tableros_grandes_y_mas_col_que_filas(self):

        ruta = "direc"
        estado = {
            'filas': 4,
            'columnas': 6,
            'minas' : 5,
            'juego_terminado': False,
            'tablero': 
            [[2, 3, -1, 1, 1, 1], [-1, -1, 2, 1, 1, -1], [2, 2, 1, 1, 2, 2], [0, 0, 0, 1, -1, 1]],
        'tablero_visible': [[VACIO,'3',BANDERA,'1',VACIO,'1'],[BANDERA,VACIO,'2',VACIO,VACIO,BANDERA],['2',VACIO,'1','1',VACIO,VACIO],[VACIO,VACIO,VACIO,'1',BANDERA,VACIO]]}

        guardar_estado(estado, ruta)

        ruta_tablero_vis = os.path.join(ruta, 'tablero_visible.txt')
        ruta_tablero_txt = os.path.join(ruta, 'tablero.txt')

    
        ruta_tablero_vis = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_visible = archivo.readlines()
        archivo.close()


        ruta_tablero_txt = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_txt = archivo.readlines()
        archivo.close()
        #me fijo que esten bien las filas, lo de las comas y espacios
        self.assertEqual(len(lineas_txt), estado['filas'])
        self.assertEqual(len(lineas_visible), estado['filas'])
        self.assertTrue((ver_comas_por_linea(ruta_tablero_txt, estado['columnas'] - 1)))
        self.assertTrue((ver_comas_por_linea(ruta_tablero_vis, estado['columnas'] - 1)))
        self.assertEqual(contar_espacios(ruta_tablero_txt), 0)
        self.assertEqual(contar_espacios(ruta_tablero_vis), 0)

        tab_esperado_visible = ["?,3,*,1,?,1\n", "*,?,2,?,?,*\n", "2,?,1,1,?,?\n", "?,?,?,1,*,?\n"]
        tab_esperado_tablero = ["2,3,-1,1,1,1\n", "-1,-1,2,1,1,-1\n", "2,2,1,1,2,2\n", "0,0,0,1,-1,1\n"]
        #veo que coincidas las lineas
        self.assertEqual(lineas_visible, tab_esperado_visible)
        self.assertEqual(lineas_txt, tab_esperado_tablero)


          
if __name__ == '__main__':
    unittest.main(verbosity=2)
