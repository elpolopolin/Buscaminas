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


def contar_comas(ruta:str)->int:
    """
    A partir de una ruta de un archivo, me devuelve la cantidad ee comas que posee este archivo

    Args:
        ruta: string de una ruta valida
    Returns:
        Número entero mayor o igual a 0
    """
    archivo = open(ruta,"r")
    lineas = archivo.readlines()
    archivo.close()
    contador = 0
    for linea in lineas:
        for caracter in linea:
            if caracter == ',':
                contador += 1
    return contador

""" ------------------------------------ EJERCICIO 1 ------------------------------------

"""
class TestColocarMinas(unittest.TestCase): 

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

    def test_ejemplo2(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)
    
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

    def test_colocar_minas_matriz_grande_muchas_minas(self):
        filas, columnas, minas = 8, 8, 63
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
    def test_colocar_minas_matriz_pequeña(self):
        filas, columnas, minas = 2, 1, 1
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

    def test_colocar_minas_matriz_no_cuadrada_muchas_minas(self):
        filas, columnas, minas = 4,8,30
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
""" ------------------------------------ EJERCICIO 2 ------------------------------------
"""

class TestCalcularNumeros(unittest.TestCase): 

    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])
            
    def test_calcular_numeros_suma_correcta(self):
        # creo un tablero con una bomba y verifico numeros
        tablero = [
            [0, -1],
            [0, 0]
        ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[1, -1], [1, 1]])
    def test_calcular_numeros_suma_correcta_matriz_un_cero(self):
        # creo un tablero con una bomba y un solo cero y verifico numeros
        tablero = [
            [-1, -1],
            [0, -1]
        ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[-1, -1], [3, -1]])
    def test_calcular_numeros_suma_correcta_matriz_pequeña_un_cero(self):
        # creo el tablero mas chico posible y con un 0 
        tablero = [
            [0]
        ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[0]])
    def test_calcular_numeros_suma_correcta_matriz_pequeña_una_bomba(self):
        # creo el tablero mas chico posible y con una bomba 
        tablero = [
            [-1]
        ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[-1]])
    def test_calcular_numeros_suma_correcta_matriz_grande(self):
        # creo un tablero con varias bombas y verifico sus numeros. Interesante a analizar para ver que aparecen numeros mayores a 1 como el 2 y 3.
        tablero = [
            [-1,0,0,0,0,0,0,-1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,-1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,-1,0,0],
            [-1,0,0,0,0,-1,0,-1],
            ]
        tablero_calculado = [
            [-1, 1, 0, 0, 0, 0, 1, -1], 
            [1, 1, 0, 0, 0, 0, 1, 1], 
            [0, 1, 1, 1, 0, 0, 0, 0], 
            [0, 1, -1, 1, 0, 0, 0, 0], 
            [0, 1, 1, 1, 0, 0, 0, 0], 
            [0, 0, 0, 0, 1, 1, 1, 0], 
            [1, 1, 0, 0, 2, -1, 3, 1], 
            [-1, 1, 0, 0, 2, -1, 3, -1]
            ]
        
        calcular_numeros(tablero)
        self.assertEqual(tablero,tablero_calculado)
""" ------------------------------------ EJERCICIO 3 ------------------------------------
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
    
    def test_juego_valido_tablero_grande(self):
        estado = crear_juego(8, 8, 60)
        self.assertEqual(estado['filas'], 8)
        self.assertEqual(estado['columnas'], 8)
        self.assertEqual(estado['minas'], 60)
        self.assertEqual(len(estado['tablero']), 8)
        self.assertEqual(len(estado['tablero_visible']), 8)
        for fila in estado['tablero_visible']:
            for celda in fila:
                assert celda == VACIO
        self.assertFalse(estado['juego_terminado'])

    def test_juego_valido_tablero_pequeño(self):
        estado = crear_juego(2, 1, 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 1)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero_visible']), 2)
        for fila in estado['tablero_visible']:
            for celda in fila:
                assert celda == VACIO
        self.assertFalse(estado['juego_terminado'])

    def test_juego_valido_tablero_grande_no_cuadrado(self):
        estado = crear_juego(6, 8, 25)
        self.assertEqual(estado['filas'], 6)
        self.assertEqual(estado['columnas'], 8)
        self.assertEqual(estado['minas'], 25)
        self.assertEqual(len(estado['tablero']), 6)
        self.assertEqual(len(estado['tablero_visible']), 6)
        for fila in estado['tablero_visible']:
            for celda in fila:
                assert celda == VACIO
        self.assertFalse(estado['juego_terminado'])
    
    """ -------------------------------- EJERCICIO 4 --------------------------------
    """
class obtener_estado_tableroTest(unittest.TestCase):
    

    def test_ejemplo1(self):
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



    def test_ejemplo2(self):
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

    def test_modificar_copia_no_afecta_original(self):
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
        copia_tablero_vis = obtener_estado_tablero_visible(estado)
        self.assertEqual(copia_tablero_vis, [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó nada
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
        # Testeamos que al modificar la copia, mi tablero del estado no se modifica
        # Con este test aseguramos que mi tablero original no se modifica, y además,
        # Que efectivamente, la copia que cree, es un copia!

        # Cambio todos los valores de la copia, elijo poner bombas para ademas de paso chequear si 
        # Mi juego_terminado se modifica.

        for i in range (len(copia_tablero_vis)):
            for j in range (len(copia_tablero_vis[i])):
                copia_tablero_vis[i][j] = BOMBA

        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_juego_finalizado_por_bomba(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [BOMBA, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': True
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [BOMBA, "1"],
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
            [BOMBA, "1"],
            [VACIO, VACIO]
        ])
        self.assertTrue(estado['juego_terminado'])
    def test_juego_finalizado_por_ganar(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [BANDERA, "1"],
                ["1", "1"]
            ],
            'juego_terminado': True
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [BANDERA, "1"],
            ["1", "1"]
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
            [BANDERA, "1"],
            ["1", "1"]
        ])
        self.assertTrue(estado['juego_terminado'])
    def test_juego_recien_empezado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, VACIO],
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
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_crear_juego_enorme(self):
        estado: EstadoJuego = crear_juego(8, 8, 60)
        tab_vis = estado["tablero_visible"]
        tab = estado["tablero"]
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado),tab_vis)
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 8)
        self.assertEqual(estado['columnas'], 8)
        self.assertEqual(estado['minas'], 60)
        self.assertEqual(estado['tablero'], tab)
        self.assertEqual(estado['tablero_visible'], tab_vis)
        self.assertFalse(estado['juego_terminado'])


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

    def test_marcar_celda_bandera_pasa_a_vacio(self):
        estado = {'filas': 2,'columnas': 2,'minas': 1,
              'tablero': [[-1, 1], 
                          [1, 1]],
              'tablero_visible': [[VACIO,BANDERA], 
                                  [VACIO, VACIO]],
              'juego_terminado': False}
        marcar_celda(estado, 0, 1)
        self.assertEqual(estado['tablero_visible'],
                                 [[VACIO,VACIO], 
                                  [VACIO, VACIO]])

    
  
""" -------------------------------- EJERCICIO 6 --------------------------------
"""
class TestDescubrirCelda(unittest.TestCase): 
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


    def test_descubrir_bomba_primer_intento_termina_juego(self):
        # si hay una bomba el juego se termina
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
                  'juego_terminado': False}
        descubrir_celda(estado, 0, 0)
        self.assertTrue(estado['juego_terminado'])
        self.assertEqual(estado['tablero_visible'][0][0], BOMBA)

        # Testeamos que nada se modificó (excepto la bomba descubierta)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [BOMBA, VACIO],
            [VACIO, VACIO]
        ])
    def test_descubrir_celda_no_hace_nada_si_juego_terminado(self):
        estado = {'filas': 2,'columnas': 2,'minas': 1,
                  'tablero': [[-1, 1], [1, 1]],
                  'tablero_visible': [[BOMBA, VACIO], [VACIO, VACIO]],
                  'juego_terminado': True}
        descubrir_celda(estado, 0, 1)
        self.assertEqual(estado['tablero_visible'], [[BOMBA, VACIO], [VACIO, VACIO]])
        # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

        
    def test_descubrir_segura_no_termina_juego(self):
        # si no hay una bomba(celda segura) el juego sigue 
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[1, -1], [1, 1]],
                  'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
                  'juego_terminado': False}
        descubrir_celda(estado, 0, 0)
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['tablero_visible'][0][0], '1')

        # Testeamos que nada se modificó (excepto celda descubierta)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [1, -1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            ["1", VACIO],
            [VACIO, VACIO]
        ])


    def test_descubrir_bomba_gana_juego(self):
        #  descubro la ultima celda segura y gano
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], 
                              [1, 1]],
                  'tablero_visible': [[BANDERA, "1"], 
                                      [VACIO, "1"]],
                  'juego_terminado': False}
        descubrir_celda(estado, 1, 0)
        #Chequeo que gane el juego
        self.assertTrue(estado['juego_terminado'])
        self.assertEqual(estado['tablero_visible'][1][0], '1')
        # Testeamos que nada se modificó (excepto celda descubierta)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], 
            [[BANDERA, "1"], 
            ["1", "1"]
        ])

    def test_matriz_enorme_celda_complejo(self):
        # si hay una bomba el juego se termina
        estado = {'filas': 8, 'columnas': 8, 'minas': 20,
                  'tablero': [[2, -1, 2, 3, -1, 4, -1, -1], 
                              [-1, 3, 3, -1, -1, 4, -1, 4], 
                              [1, 2, -1, 5, 5, 4, 3, -1], 
                              [0, 2, 3, -1, -1, -1, 2, 1], 
                              [0, 1, -1, 5, 5, 4, 2, 1], 
                              [0, 1, 2, -1, -1, 3, -1, 2], 
                              [1, 2, 2, 3, 2, 3, -1, 2], 
                              [-1, 2, -1, 1, 0, 1, 1, 1]],


                  'tablero_visible': [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                                      [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']],
                  'juego_terminado': False}
        descubrir_celda(estado, 3, 0)
        tab = estado["tablero"]
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que nada se modificó  (excepto los caminos descubiertos )
        self.assertEqual(estado['filas'], 8)
        self.assertEqual(estado['columnas'], 8)
        self.assertEqual(estado['minas'], 20)
        self.assertEqual(estado['tablero'], tab)
        self.assertEqual(estado['tablero_visible'], 
                         [
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                    ['1', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                    ['0', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                    ['0', '1', ' ', ' ', ' ', ' ', ' ', ' '], 
                    ['0', '1', ' ', ' ', ' ', ' ', ' ', ' '], 
                    ['1', '2', ' ', ' ', ' ', ' ', ' ', ' '], 
                    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])  
        
    def test_pise_un_cero_sin_cascada(self):
        estado = {'filas': 6, 'columnas': 6, 'minas': 10, 
                'tablero': [[-1, 1, 1, -1, -1, 2], 
                            [2, 2, 1, 2, 3, -1], 
                            [-1, 2, 1, 0, 1, 1], 
                            [3, -1, 3, 1, 2, 1], 
                            [2, -1, 4, -1, 3, -1], 
                            [1, 1, 3, -1, 3, 1]], 
                'tablero_visible': [[' ', ' ', ' ', ' ', ' ', ' '], 
                                    [' ', ' ', ' ', ' ', ' ', ' '], 
                                    [' ', ' ', ' ', ' ', ' ', ' '], 
                                    [' ', ' ', ' ', ' ', ' ', ' '], 
                                    [' ', ' ', ' ', ' ', ' ', ' '], 
                                    [' ', ' ', ' ', ' ', ' ', ' ']], 
        'juego_terminado': False}
        tab = estado["tablero"]
        descubrir_celda(estado, 2, 3)

        self.assertEqual(estado['tablero_visible'], 
                         [          [VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
                                    [VACIO,VACIO,'1','2','3',VACIO],
                                    [VACIO,VACIO,'1','0','1',VACIO],
                                    [VACIO,VACIO,'3','1','2',VACIO],
                                    [VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
                                    [VACIO,VACIO,VACIO,VACIO,VACIO,VACIO]])
        # Testeamos que nada se modificó
        
        self.assertFalse(estado['juego_terminado'])
        self.assertEqual(estado['filas'], 6)
        self.assertEqual(estado['columnas'], 6)
        self.assertEqual(estado['minas'], 10)
        self.assertEqual(estado['tablero'], tab)

    # Se gana un juego gracias a un efecto cascada
    def test_cascada_con_bandera_bloquea_parcial(self):
        estado = {
            'filas': 6, 'columnas': 6, 'minas': 2,
            'tablero': [
                [0, 0, 0, 0, 1, -1],
                [0, 1, 1, 1, 2, 1],
                [0, 1, -1, 1, 1, 0],
                [0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0]
            ],
            'tablero_visible': [[VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO], 
                                [VACIO, VACIO ,BANDERA ,VACIO ,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO],
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO]],
            'juego_terminado': False
        }
        tab = estado['tablero']
        descubrir_celda(estado, 0, 0)
        
    # Tablero visible esperado despues de aplicar descubrir_celda 
        esperado = [
        ['0', '0', '0', '0', '1', VACIO],
        ['0', '1', '1', '1', '2', '1'],
        ['0', '1', BANDERA, '1', '1', '0'],
        ['0', '1', '1', '1', '0', '0'],
        ['0', '0', '0', '0', '0', '0'],
        ['1', '1', '1', '0', '0', '0'],
        ]
        self.assertEqual(estado['tablero_visible'],esperado)
        # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 6)
        self.assertEqual(estado['columnas'], 6)
        self.assertEqual(estado['minas'], 2)
        self.assertEqual(estado['tablero'], tab)
        self.assertTrue(estado['juego_terminado'])
    # Testeamos un gran efecto de cascada que se produce desde la parte de arriba del tablero hacia abajo
    def test_cascada_de_arriba_a_abajo(self):
        estado = {
            'filas': 7, 'columnas': 7, 'minas': 4,
            'tablero': [
                [-1, 1, 0, 0, 0, 1, -1],
                [1, 1, 0, 0, 0, 1, 1],
                [0, 0, 0, 1, 1, 2, 1],
                [0, 0, 0, 1, -1, 2, -1],
                [0, 1, 1, 2, 2, 3, 2],
                [0, 1, -1, 2, -1, 2, 1],
                [0, 1, 1, 2, 2, 1, 0]
            ],
            'tablero_visible': [[VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO],
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO],
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO],
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO]],
            'juego_terminado': False
        }
        tab = estado['tablero']
        descubrir_celda(estado, 3, 2)
        # Tablero visible esperado luego de aplicar descubrir celda en el medio
        esperado = [[VACIO, '1', '0', '0', '0', '1', VACIO], 
                    ['1', '1', '0', '0', '0', '1', VACIO], 
                    ['0', '0', '0', '1', '1', '2', VACIO], 
                    ['0', '0', '0', '1', VACIO, VACIO,VACIO], 
                    ['0', '1', '1', '2', VACIO,VACIO,VACIO], 
                    ['0', '1', VACIO,VACIO,VACIO,VACIO,VACIO], 
                    ['0', '1', VACIO,VACIO,VACIO,VACIO,VACIO]]

        self.assertEqual(estado['tablero_visible'], esperado)
        # Testeamos que nada haya cambiado
        self.assertEqual(estado['filas'], 7)
        self.assertEqual(estado['columnas'], 7)
        self.assertEqual(estado['minas'], 4)
        self.assertEqual(estado['tablero'],tab)
        self.assertFalse(estado['juego_terminado'])



    # Testeo que gano un juego gracias al efecto cascada y a utilizar marcar_celda
    def test_victoria_con_super_cascada(self):
        estado = {
            'filas': 7, 'columnas': 7, 'minas': 2,
            'tablero': [
                [0, 0, 0, 0, 0, 1, -1],
                [0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0, 0],
                [-1, 1, 0, 0, 0, 0, 0]
            ],
            'tablero_visible': [[VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,BANDERA], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO],
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO],
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO], 
                                [VACIO, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO],
                                [BANDERA, VACIO ,VACIO ,VACIO ,VACIO,VACIO,VACIO]],
            'juego_terminado': False
        }   
        tab = estado['tablero']
        descubrir_celda(estado, 0, 0)
        esperado = [
            ['0', '0', '0', '0', '0', '1', BANDERA],
            ['0', '0', '0', '0', '0', '1', '1'],
            ['0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0'],
            ['1', '1', '1', '0', '0', '0', '0'],
            [BANDERA, '1', '0', '0', '0', '0', '0']
        ]

        self.assertEqual(estado['tablero_visible'], esperado)
        # Chequeamos que se termino el juego
        self.assertTrue(estado['juego_terminado'])        
        #Testeamos que nada haya cambiado
        self.assertEqual(estado['tablero'], tab)        
        self.assertEqual(estado['filas'], 7)
        self.assertEqual(estado['columnas'], 7)
        self.assertEqual(estado['minas'], 2)


    #Los de caminos descubiertos son de la aux 
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
        ####    

""" -------------------------------- EJERCICIO 7 --------------------------------
    * BIEN
"""
class TestVerificarVictoria(unittest.TestCase):
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
"""
class TestReiniciarJuego(unittest.TestCase): 
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

    # mira que al reiniciar el juego se cree un nuevo tablero distinto 
    def test_reiniciar_juego_resetea_estado(self):
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], 
                              [1, 1]],
                  'tablero_visible': [
                      [VACIO, '1'], 
                      [VACIO, '1']],
                  'juego_terminado': False}
        
        filas_antes = estado["filas"]
        columnas_antes = estado["columnas"]
        minas_antes = estado["minas"]
        viejo_tablero = estado['tablero']

        reiniciar_juego(estado)
        # Testeo que el tablero cambia, que las dimensiones y minas se mantienen
        # Y que el juego pase a False
        self.assertEqual(estado['juego_terminado'], False)
        self.assertEqual(filas_antes,estado["filas"])
        self.assertEqual(columnas_antes,estado["columnas"])
        self.assertEqual(minas_antes,estado["minas"])
        self.assertNotEqual(viejo_tablero, estado['tablero'])

        for i in range (len(estado["tablero_visible"])):
            for j in range (len(estado["tablero_visible"])):
                self.assertEqual(VACIO, estado["tablero_visible"][i][j])

    def test_reinciar_juego_perdido(self):
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], 
                              [1, 1]],
                  'tablero_visible': [
                      [BOMBA, '1'], 
                      [VACIO, '1']],
                  'juego_terminado': True}
        
        filas_antes = estado["filas"]
        columnas_antes = estado["columnas"]
        minas_antes = estado["minas"]
        viejo_tablero = estado['tablero']

        reiniciar_juego(estado)
        # Testeo que el tablero cambia, que las dimensiones y minas se mantienen
        # Y que el juego pase a False
        self.assertEqual(estado['juego_terminado'], False)
        self.assertEqual(filas_antes,estado["filas"])
        self.assertEqual(columnas_antes,estado["columnas"])
        self.assertEqual(minas_antes,estado["minas"])
        self.assertNotEqual(viejo_tablero, estado['tablero'])
        # Chequeo que todas las celdas de tablero_visible pasen a ser VACIO
        for i in range (len(estado["tablero_visible"])):
            for j in range (len(estado["tablero_visible"])):
                self.assertEqual(VACIO, estado["tablero_visible"][i][j])

    def test_reinciar_juego_ganado(self):
        estado = {'filas': 2, 'columnas': 2, 'minas': 1,
                  'tablero': [[-1, 1], 
                              [1, 1]],
                  'tablero_visible': [
                      [BANDERA, '1'], 
                      ["1", '1']],
                  'juego_terminado': True}
        
        filas_antes = estado["filas"]
        columnas_antes = estado["columnas"]
        minas_antes = estado["minas"]
        viejo_tablero = estado['tablero']

        reiniciar_juego(estado)
        # Testeo que el tablero cambia, que las dimensiones y minas se mantienen
        # Y que el juego pase a False
        self.assertEqual(estado['juego_terminado'], False)
        self.assertEqual(filas_antes,estado["filas"])
        self.assertEqual(columnas_antes,estado["columnas"])
        self.assertEqual(minas_antes,estado["minas"])
        self.assertNotEqual(viejo_tablero, estado['tablero'])
        # Chequeo que todas las celdas de tablero_visible pasen a ser VACIO
        for i in range (len(estado["tablero_visible"])):
            for j in range (len(estado["tablero_visible"])):
                self.assertEqual(VACIO, estado["tablero_visible"][i][j])

    def test_reinciar_juego_tableros_grandes(self):
        estado = crear_juego(8,8,50)
        filas_antes = estado["filas"]
        columnas_antes = estado["columnas"]
        minas_antes = estado["minas"]
        viejo_tablero = estado['tablero']
        reiniciar_juego(estado)
        # Testeo que el tablero cambia, que las dimensiones y minas se mantienen
        # Y que el juego pase a False
        self.assertEqual(estado['juego_terminado'], False)
        self.assertEqual(filas_antes,estado["filas"])
        self.assertEqual(columnas_antes,estado["columnas"])
        self.assertEqual(minas_antes,estado["minas"])
        self.assertNotEqual(viejo_tablero, estado['tablero'])
        # Chequeo que todas las celdas de tablero_visible pasen a ser VACIO
        for i in range (len(estado["tablero_visible"])):
            for j in range (len(estado["tablero_visible"])):
                self.assertEqual(VACIO, estado["tablero_visible"][i][j])





        #! Falta chequear el resto de los atributos del estado.

""" -------------------------------- EJERCICIO 9 --------------------------------
    - Faltan algunos tests: - Tableros de tamaño minimo y máximo, con muchas minas o con solo una, tablero con todos los símbolos...
"""

#TEST EJ 9



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
    
    #Hago la misma prueba pero con ambos tableros ENORMES

    def test_archivos_enormes_creados(self):
        ruta = "./data"
        estado = {'filas': 8, 
          'columnas': 8, 
          'minas': 60, 
          'tablero': [
            [-1, -1, -1, 5, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, 8, -1, -1, -1, -1, 8, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, 5, -1, -1]], 
           'tablero_visible': [
               [BANDERA, BANDERA, BANDERA, "5", BANDERA, BANDERA, ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', "8", BANDERA, ' ', ' ', ' ', "8", ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', BANDERA]], 
            'juego_terminado': False}
        
        guardar_estado(estado, ruta) 

        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta, 'tablero_visible.txt')

        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_tablero_visible))

    #Hago la misma prueba pero con ambos tableros en sus MINIMOS TAMAÑOS
    def test_archivos_creados_minimo_tamaño(self):
        ruta = "./data"  
        estado = {
            'filas': 2,
            'columnas': 1,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [
                [-1],
                [1]],
            'tablero_visible': [
                [BANDERA],
                [VACIO]]}

        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        ruta_tablero_visible = os.path.join(ruta, 'tablero_visible.txt')
        self.assertTrue(os.path.exists(ruta_tablero))
        self.assertTrue(os.path.exists(ruta_tablero_visible))
        #Mismo test que antes, pero ahora el minimo tamaño es (2x1)
        estado = {
            'filas': 1,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [
                [-1,1]
                        ],
            'tablero_visible': [
                [BANDERA,VACIO]
                                ]}

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
    # Parecido al anterior, pero el tablero_visible tiene el tamaño max,y contiene bastantes simbolos
    def test_tablero_visible_grande_todos_simbolos_contenido_correcto(self):
        ruta = "./data"
        estado = {'filas': 8, 'columnas': 8, 'minas': 20,
                  'tablero': [[2, -1, 2, 3, -1, 4, -1, -1], 
                              [-1, 3, 3, -1, -1, 4, -1, 4], 
                              [1, 2, -1, 5, 5, 4, 3, -1], 
                              [0, 2, 3, -1, -1, -1, 2, 1], 
                              [0, 1, -1, 5, 5, 4, 2, 1], 
                              [0, 1, 2, -1, -1, 3, -1, 2], 
                              [1, 2, 2, 3, 2, 3, -1, 2], 
                              [-1, 2, -1, 1, 0, 1, 1, 1]],


                  'tablero_visible':[
                      [' ', BANDERA, ' ', ' ', BANDERA, ' ', BANDERA, BANDERA], 
                      [BANDERA, ' ', ' ', BANDERA, BANDERA, ' ', BANDERA, ' '], 
                      ['1', '2', BANDERA, ' ', ' ', ' ', ' ', BANDERA], 
                      ['0', '2', ' ', BANDERA, BANDERA, BANDERA, ' ', ' '], 
                      ['0', '1', BANDERA, ' ', ' ', ' ', ' ', ' '], 
                      ['0', '1', ' ', BANDERA, BANDERA, ' ', BANDERA, ' '],
                      ['1', '2', ' ', ' ', ' ', ' ', BANDERA, ' '], 
                      [BANDERA, ' ', BANDERA, ' ', ' ', ' ', ' ', ' ']],  
                  'juego_terminado': False}
        
        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero, "r")
        lineas = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas, 
                                ['?,*,?,?,*,?,*,*\n', 
                                '*,?,?,*,*,?,*,?\n', 
                                '1,2,*,?,?,?,?,*\n',
                                '0,2,?,*,*,*,?,?\n', 
                                '0,1,*,?,?,?,?,?\n', 
                                '0,1,?,*,*,?,*,?\n', 
                                '1,2,?,?,?,?,*,?\n', 
                                '*,?,*,?,?,?,?,?\n'])
    # Parecido al anterior, pero ahora tenemos demasiadas minas
    def test_tablero_visible_enorme_muchas_minas_contenido_correcto(self):
        ruta = "./data"
        estado = {'filas': 8, 
          'columnas': 8, 
          'minas': 60, 
          'tablero': [
            [-1, -1, -1, 5, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, 8, -1, -1, -1, -1, 8, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, 5, -1, -1]], 
           'tablero_visible': [
               [BANDERA, BANDERA, BANDERA, "5", BANDERA, BANDERA, ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', "8", BANDERA, ' ', ' ', ' ', "8", ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', BANDERA]], 
            'juego_terminado': False}
        
        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero, "r")
        lineas = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas, 
                                ['*,*,*,5,*,*,?,?\n', 
                                 '*,?,?,?,?,?,?,?\n', 
                                 '?,?,?,?,*,?,?,*\n', 
                                 '?,?,?,?,*,?,?,*\n', 
                                 '?,?,?,?,?,?,?,?\n', 
                                 '?,8,*,?,?,?,8,?\n', 
                                 '?,?,?,?,?,?,?,?\n', 
                                 '*,?,?,?,?,?,?,*\n'])
             
    # Misma idea de test que los anteriores, pero ahora con tablero txt
    def test_tablero_txt_grande_todos_simbolos_contenido_correcto(self):
        ruta = "./data"
        estado = {'filas': 8, 'columnas': 8, 'minas': 20,
                  'tablero': [[2, -1, 2, 3, -1, 4, -1, -1], 
                              [-1, 3, 3, -1, -1, 4, -1, 4], 
                              [1, 2, -1, 5, 5, 4, 3, -1], 
                              [0, 2, 3, -1, -1, -1, 2, 1], 
                              [0, 1, -1, 5, 5, 4, 2, 1], 
                              [0, 1, 2, -1, -1, 3, -1, 2], 
                              [1, 2, 2, 3, 2, 3, -1, 2], 
                              [-1, 2, -1, 1, 0, 1, 1, 1]],


                  'tablero_visible':[
                      [' ', BANDERA, ' ', ' ', BANDERA, ' ', BANDERA, BANDERA], 
                      [BANDERA, ' ', ' ', BANDERA, BANDERA, ' ', BANDERA, ' '], 
                      ['1', '2', BANDERA, ' ', ' ', ' ', ' ', BANDERA], 
                      ['0', '2', ' ', BANDERA, BANDERA, BANDERA, ' ', ' '], 
                      ['0', '1', BANDERA, ' ', ' ', ' ', ' ', ' '], 
                      ['0', '1', ' ', BANDERA, BANDERA, ' ', BANDERA, ' '],
                      ['1', '2', ' ', ' ', ' ', ' ', BANDERA, ' '], 
                      [BANDERA, ' ', BANDERA, ' ', ' ', ' ', ' ', ' ']],  
                  'juego_terminado': False}
        
        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero, "r")
        lineas = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas, 
                                ['2,-1,2,3,-1,4,-1,-1\n', 
                                 '-1,3,3,-1,-1,4,-1,4\n', 
                                 '1,2,-1,5,5,4,3,-1\n', 
                                 '0,2,3,-1,-1,-1,2,1\n', 
                                 '0,1,-1,5,5,4,2,1\n', 
                                 '0,1,2,-1,-1,3,-1,2\n', 
                                 '1,2,2,3,2,3,-1,2\n', 
                                 '-1,2,-1,1,0,1,1,1\n'])

    def test_tablero_txt_enorme_muchas_minas_contenido_correcto(self):
        ruta = "./data"
        estado = {'filas': 8, 
          'columnas': 8, 
          'minas': 60, 
          'tablero': [
            [-1, -1, -1, 5, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, 8, -1, -1, -1, -1, 8, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, 5, -1, -1]], 
           'tablero_visible': [
               [BANDERA, BANDERA, BANDERA, "5", BANDERA, BANDERA, ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', "8", BANDERA, ' ', ' ', ' ', "8", ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', BANDERA]], 
            'juego_terminado': False}
        
        guardar_estado(estado, ruta)
        ruta_tablero = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero, "r")
        lineas = archivo.readlines()
        archivo.close()
        self.assertEqual(lineas, 
                                ['-1,-1,-1,5,-1,-1,-1,-1\n', 
                                 '-1,-1,-1,-1,-1,-1,-1,-1\n', 
                                 '-1,-1,-1,-1,-1,-1,-1,-1\n', 
                                 '-1,-1,-1,-1,-1,-1,-1,-1\n', 
                                 '-1,-1,-1,-1,-1,-1,-1,-1\n', 
                                 '-1,8,-1,-1,-1,-1,8,-1\n', 
                                 '-1,-1,-1,-1,-1,-1,-1,-1\n', 
                                 '-1,-1,-1,-1,-1,5,-1,-1\n'])
        
    # Ideas parecidas a las anteriores, pero ahora probando los menores posibles tamaños de ambos tableros
    def test_tableros_tamaño_minimo_contenido_correcto(self):
        ruta = "./data" 
        estado = {
            'filas': 1,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [[-1,1]],
            'tablero_visible': [[BANDERA,VACIO]]}

        guardar_estado(estado, ruta)
        
        ruta_tablero_txt = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        ruta_tablero_vis = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_vis = archivo.readlines()
        archivo.close()

        self.assertEqual(lineas_txt,['-1,1\n'])
        self.assertEqual(lineas_vis,['*,?\n'])


        # Repito lo mismo que antes, pero teniendo en cuenta la otra
        # Posibilidad de tablero minimo (2x1)
        estado = {
            'filas': 2,
            'columnas': 1,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [[-1],
                        [1]
                        ],
            'tablero_visible': [
                [BANDERA],
                [VACIO]
                                ]}

        guardar_estado(estado, ruta)

        ruta_tablero_txt = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        ruta_tablero_vis = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_vis = archivo.readlines()
        archivo.close()

        self.assertEqual(lineas_txt,['-1\n', '1\n'])
        self.assertEqual(lineas_vis,['*\n', '?\n'])


# Testeo lo siguiente:
# asegura: {La cantidad de l´ıneas de cada archivo guardado es igual a estado[filas]
#considerando una linea cuando la cantidad de caracteres sea mayor a 0.}
    
    def test_tableros_cant_lineas_igual_cant_filas(self):
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

    #Ahora con tableros enormes y muchisimas minas

    def test_tableros_enormes_cant_lineas_igual_cant_filas(self):
        ruta = "./data"
        estado = {'filas': 8, 
          'columnas': 8, 
          'minas': 60, 
          'tablero': [
            [-1, -1, -1, 5, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, 8, -1, -1, -1, -1, 8, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, 5, -1, -1]], 
           'tablero_visible': [
               [BANDERA, BANDERA, BANDERA, "5", BANDERA, BANDERA, ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', "8", BANDERA, ' ', ' ', ' ', "8", ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', BANDERA]], 
            'juego_terminado': False}
        guardar_estado(estado,ruta)
        ruta_tablero_txt = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_visible = archivo.readlines()
        archivo.close()


        ruta_tablero_vis = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        self.assertEqual(len(lineas_visible), estado['filas'])
        self.assertEqual(len(lineas_txt), estado['filas'])

    #Ahora con las minimas dimensiones para ambos tableros, y una sola mina

    def test_tableros_minimo_tamaño_cant_lineas_igual_cant_filas(self):
        ruta = "./data"
        estado = {
            'filas': 1,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [[-1,1]],
            'tablero_visible': [[BANDERA,VACIO]]}
        
        guardar_estado(estado, ruta)

        ruta_tablero_txt = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_visible = archivo.readlines()
        archivo.close()

        ruta_tablero_vis = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        self.assertEqual(len(lineas_visible), estado['filas'])
        self.assertEqual(len(lineas_txt), estado['filas'])

        #Misma prueba pero ahora uso 2x1 de dim
        estado = {
            'filas': 2,
            'columnas': 1,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [[-1],
                        [1]
                        ],
            'tablero_visible': [
                [BANDERA],
                [VACIO]
                                ]}
        
        guardar_estado(estado, ruta)

        ruta_tablero_txt = os.path.join(ruta, 'tablero_visible.txt')
        archivo = open(ruta_tablero_txt, "r")
        lineas_visible = archivo.readlines()
        archivo.close()

        ruta_tablero_vis = os.path.join(ruta, 'tablero.txt')
        archivo = open(ruta_tablero_vis, "r")
        lineas_txt = archivo.readlines()
        archivo.close()

        self.assertEqual(len(lineas_visible), estado['filas'])
        self.assertEqual(len(lineas_txt), estado['filas'])

    #Test para chequear que la cant de comas sea la correcta
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

    #Ahora con tableros enormes y muchisimas minas

    def test_comas_correctas_tableros_enormes(self):
        ruta = "./data"
        estado = {'filas': 8, 
          'columnas': 8, 
          'minas': 60, 
          'tablero': [
            [-1, -1, -1, 5, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, 8, -1, -1, -1, -1, 8, -1], 
           [-1, -1, -1, -1, -1, -1, -1, -1], 
           [-1, -1, -1, -1, -1, 5, -1, -1]], 
           'tablero_visible': [
               [BANDERA, BANDERA, BANDERA, "5", BANDERA, BANDERA, ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA], 
                [' ', ' ', ' ', ' ',BANDERA, ' ', ' ', BANDERA],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [' ', "8", BANDERA, ' ', ' ', ' ', "8", ' '], 
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                [BANDERA, ' ', ' ', ' ', ' ', ' ', ' ', BANDERA]], 
            'juego_terminado': False}
        
        guardar_estado(estado, ruta)

        ruta_tablero_vis = os.path.join(ruta,'tablero_visible.txt')
        ruta_tablero_txt = os.path.join(ruta,'tablero.txt')

        self.assertEqual(contar_comas(ruta_tablero_vis), estado['filas'] * (estado['columnas'] - 1))
        self.assertEqual(contar_comas(ruta_tablero_txt), estado['filas'] * (estado['columnas'] - 1))

    #Ahora con tableros de minima dimension y una mina 
    def test_comas_correctas_tableros_minimos(self):
        ruta = "./data"
        estado = {
            'filas': 1,
            'columnas': 2,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [[-1,1]],
            'tablero_visible': [[BANDERA,VACIO]]}
        
        guardar_estado(estado, ruta)

        ruta_tablero_vis = os.path.join(ruta,'tablero_visible.txt')
        ruta_tablero_txt = os.path.join(ruta,'tablero.txt')

        self.assertEqual(contar_comas(ruta_tablero_vis), estado['filas'] * (estado['columnas'] - 1))
        self.assertEqual(contar_comas(ruta_tablero_txt), estado['filas'] * (estado['columnas'] - 1))


        estado = {
            'filas': 2,
            'columnas': 1,
            'minas' : 1,
            'juego_terminado': False,
            'tablero': [[-1],
                        [1]
                        ],
            'tablero_visible': [
                [BANDERA],
                [VACIO]
                                ]}
        
        guardar_estado(estado, ruta)

        ruta_tablero_vis = os.path.join(ruta,'tablero_visible.txt')
        ruta_tablero_txt = os.path.join(ruta,'tablero.txt')

        self.assertEqual(contar_comas(ruta_tablero_vis), estado['filas'] * (estado['columnas'] - 1))
        self.assertEqual(contar_comas(ruta_tablero_txt), estado['filas'] * (estado['columnas'] - 1))


""" -------------------------------- EJERCICIO 10 --------------------------------

"""

class cargar_estadoTest(unittest.TestCase):
    # Falla pues ambos archivos no existen
    def test_falla_sin_archivos(self):
        ruta = "./tests10/t1/"
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta)) 
        self.assertFalse(existe_archivo(ruta,'tablero.txt'))
        self.assertFalse(existe_archivo(ruta,'tablero_visible.txt'))
    # Falla pues tablero.txt no existe
    def test_falla_sin_archivo_tablero(self):
        ruta = "./tests10/t13/"
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta)) 
        self.assertFalse(existe_archivo(ruta,'tablero.txt'))
        self.assertTrue(existe_archivo(ruta,'tablero_visible.txt'))
    # Falla pues tablero_visible no existe
    def test_falla_sin_archivo_tablero_visible(self):
        ruta = "./tests10/t14/"
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta)) 
        self.assertTrue(existe_archivo(ruta,'tablero.txt'))
        self.assertFalse(existe_archivo(ruta,'tablero_visible.txt'))

    # Falla, la cantidad de sus lineas son distintas
    def test_falla_lineas_distintas(self):
        ruta = "./tests10/t2/"
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta)) 
    # Falla, la cantidad de sus comas son distintas
    def test_falla_comas_distintas(self):
        ruta = "./tests10/t3/"
        estado = {}
        self.assertFalse(cargar_estado(estado, ruta)) 
   
    #Res es True y me modifica mi estado@pre. 
    def test_tablero_ok(self):
        estado = {
            'filas': 500,
            'columnas': 1,
            'minas' : 777,
            'juego_terminado': True,
            'tablero': [[-100,1]],
            'tablero_visible': [[BANDERA,"boca"]]}
        
        ruta = "./tests10/t4/"
        self.assertTrue(cargar_estado(estado, ruta))
        self.assertEqual(estado['filas'],2)
        self.assertEqual(estado['columnas'],2)
        self.assertEqual(estado['minas'],1)
        self.assertEqual(estado['tablero'],[[-1,1],
                                          [1,1]])
        self.assertEqual(estado['tablero_visible'], [[BANDERA,VACIO],
                                                     ['1',VACIO]] )
        self.assertEqual(estado['juego_terminado'], False)
        

    # Res es False porque hay valores en tablero visible que no concuerdan con tablero
    def test_tableros_con_numeros_distintos(self):
        estado = {}
        ruta = "./tests10/t5/"
        self.assertFalse(cargar_estado(estado, ruta))
    
    # Res es False pues la cant de comas es igual pero tiene comas al principio y final
    def test_tablero_comas_al_principio_y_final(self):
        estado = {}
        ruta = "./tests10/t6/"
        self.assertFalse(cargar_estado(estado, ruta))
    # Res es False pues ambos archivos contienen valores no correspondidos
    def test_tableros_valores_erroneos(self):
        estado = {}
        ruta = "./tests10/t7/"
        self.assertFalse(cargar_estado(estado, ruta))
    # Res es False pues si bien ambos archivos existen, no tienen un solo valor
    def test_tableros_vacios(self):
        estado = {}
        ruta = "./tests10/t8/"
        self.assertFalse(cargar_estado(estado, ruta))
    # Res es False, pues tablero_visible contiene un -1
    def test_tablero_visible_con_menos_uno(self):
        estado = {}
        ruta = "./tests10/t9/"
        self.assertFalse(cargar_estado(estado, ruta))   
    # Res es False, pues la cantidad de columnas no es fija para ambos archivos
    def test_tableros_malas_dimensiones(self):
        estado = {}
        ruta = "./tests10/t10/"
        self.assertFalse(cargar_estado(estado, ruta))   
    # Res es False pues tablero no fue creado con calcular_numeros
    def test_tablero_numeros_mal_calculados(self):
        estado = {}
        ruta = "./tests10/t11/"
        self.assertFalse(cargar_estado(estado, ruta))   
    # Res es False pues los archivos estan mal separados, y tiene comas al principio y final
    def test_tableros_muchas_comas(self):
        estado = {}
        ruta = "./tests10/t12/"
        self.assertFalse(cargar_estado(estado, ruta))  
    # Res es False pues en el final de una linea en tablero hay un - sin ningun 1 que lo acompañe
    def test_tablero_menos_uno_al_final_de_linea(self):
        estado = {}
        ruta = "./tests10/t15/"
        self.assertFalse(cargar_estado(estado, ruta))  
    # Res es True pues aunque los archivos tengan un salto de linea "de más", los tableros siguen siendo
    # Validos y correspondidos entre sí, ese salto de linea segun la especificación no se considera como
    # Una linea valida
    def test_tableros_validos_espaciados(self):
        estado = {}
        ruta = "./tests10/t16/"
        self.assertTrue(cargar_estado(estado, ruta))  

    # Res es False, pues ambos tableros tienen sus valores mal espaciados 
    def test_tableros_validos_espaciados(self):
        estado = {}
        ruta = "./tests10/t17/"
        self.assertFalse(cargar_estado(estado, ruta))   
    # Res es True, testeo con un tablero con dimensiones muy grandes
    def test_tableros_enormes_ok(self):
        estado = {'filas': 500,
            'columnas': 1,
            'minas' : 777,
            'juego_terminado': True,
            'tablero': [[-100,1]],
            'tablero_visible': [[BANDERA,"boca"]]}
        ruta = "./tests10/t18/"
        self.assertTrue(cargar_estado(estado, ruta))

        self.assertTrue(estado['filas'],8)
        self.assertTrue(estado['columnas'],8)
        self.assertTrue(estado['minas'],20)
        self.assertTrue(estado['tablero'],[ 
                              [2, -1, 2, 3, -1, 4, -1, -1], 
                              [-1, 3, 3, -1, -1, 4, -1, 4], 
                              [1, 2, -1, 5, 5, 4, 3, -1], 
                              [0, 2, 3, -1, -1, -1, 2, 1], 
                              [0, 1, -1, 5, 5, 4, 2, 1], 
                              [0, 1, 2, -1, -1, 3, -1, 2], 
                              [1, 2, 2, 3, 2, 3, -1, 2], 
                              [-1, 2, -1, 1, 0, 1, 1, 1]],)
        self.assertTrue(estado['tablero_visible'], [
            ['2',BANDERA,VACIO,'3',VACIO,'4',VACIO,BANDERA],
            [VACIO,VACIO,VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
            ['1','2',VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
            ['0','2',VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
            ['0','1',VACIO,'5','5','4',VACIO,VACIO],
            ['0','0',VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
            ['1','2',VACIO,VACIO,VACIO,VACIO,VACIO,VACIO],
            [BANDERA,VACIO,VACIO,VACIO,VACIO,VACIO,VACIO,'1']])
        self.assertEqual(estado['juego_terminado'], False)

    # Res es True, testeo con un tablero con una posible dimension valida minima (1x2)
    def test_tableros_minimos_v1(self):
        estado = {
            'filas': 500,
            'columnas': 1,
            'minas' : 777,
            'juego_terminado': True,
            'tablero': [[-100,1]],
            'tablero_visible': [[BANDERA,"boca"]]}
        
        ruta = "./tests10/t19/"
        self.assertTrue(cargar_estado(estado, ruta))

        self.assertEqual(estado['filas'],1)
        self.assertEqual(estado['columnas'],2)
        self.assertEqual(estado['minas'],1)
        self.assertEqual(estado['tablero'],[[-1,1]])
        self.assertEqual(estado['tablero_visible'], [[BANDERA,VACIO]])
        self.assertEqual(estado['juego_terminado'], False)
    # Res es True, testeo con un tablero con la otra posible dimension valida minima (2x1)
    def test_tableros_minimos_v2(self):
        estado = {
            'filas': 500,
            'columnas': 1,
            'minas' : 777,
            'juego_terminado': True,
            'tablero': [[-100,1]],
            'tablero_visible': [[BANDERA,"boca"]]}
        
        ruta = "./tests10/t20/"
        self.assertTrue(cargar_estado(estado, ruta))

        self.assertEqual(estado['filas'],2)
        self.assertEqual(estado['columnas'],1)
        self.assertEqual(estado['minas'],1)
        self.assertEqual(estado['tablero'],[[-1],[1]])
        self.assertEqual(estado['tablero_visible'], [[BANDERA],[VACIO]])
        self.assertEqual(estado['juego_terminado'], False)
if __name__ == '__main__':
    unittest.main()