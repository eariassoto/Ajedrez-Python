#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, pygame, sys, os
from pygame.locals import *
from copy import deepcopy

############################################### Clase Main ################################################
#                       Maneja los eventos del mouse y el loop principal del juego                        #
###########################################################################################################
class Main:
	
	""" Lista de constantes respectivamente corresponden a largo y ancho de la ventana, cantidad de
	cuadros del tablero nxn, coordenadas de las fichas blancas (x,y) y negras (x, y).
	"""
	CONSTANTES = (594, 594, 11,
	(3,4,4,4,5,5,5,5,6,6,6,7),
	(5,4,5,6,3,4,6,7,4,5,6,5),
	(0,0,0,0,0,1,10,10,10,10,10,9,3,4,5,6,7,5,3,4,5,6,7,5),
	(3,4,5,6,7,5,3,4,5,6,7,5,0,0,0,0,0,1,10,10,10,10,10,9))
	LARGO_VENTANA = CONSTANTES[0]
	ANCHO_VENTANA = CONSTANTES[1]
	
	# velocidad promedio de cuadros por segundo
	FPS = 24
	
	# constantes para controlar los turnos de juego
	JUGADOR1 = "jugador1"
	JUGADOR2 = "jugador2"
	
	def switchJugador(self, jugAct):
		if jugAct == self.JUGADOR1:
			return self.JUGADOR2
		else:
			return self.JUGADOR1
	
	def iniciar(self):
		# iniciar el modulo pygame, el objeto FPS y la venatna
		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		SUPERFICIE = pygame.display.set_mode((self.LARGO_VENTANA, self.ANCHO_VENTANA))
		pygame.display.set_caption('Ajedrez Vikingo')
		
		# instancia de clases 
		logico = Logico(self.CONSTANTES)
		grafico = Grafico(logico, SUPERFICIE, self.CONSTANTES)
		
		# almacenan las coordenadas del mouse
		mousex = 0 
		mousey = 0 
		
		# controla el jugador de turno
		jugadorActual = self.JUGADOR1
		
		# boolean para saber si hay alguna ficha seleccionada
		seleccion = False
		
		# sirve para almacenar la posicion de la ficha seleccionada por el clic
		fichaSeleccion = ""
		
		while True: # loop principal del juego
		
			mouseClic = False
			
			if seleccion:
				grafico.dibujarTablero()
				grafico.dibujarCaminoIluminado(None, None)
			else:
				grafico.dibujarTablero()
			
			for evento in pygame.event.get():
				if evento.type == QUIT or (evento.type == KEYUP and evento.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				elif not mouseClic and evento.type == MOUSEMOTION:
					mousex, mousey = evento.pos 
				elif not mouseClic and evento.type == MOUSEBUTTONUP:
					mousex, mousey = evento.pos
					mouseClic = True	
					
			# comprobar si el mouse esta actualmente en un cuadro
			cuadrox, cuadroy = grafico.getCuadroEnPixel(mousex, mousey)					
			
			if cuadrox != None and cuadroy != None and not mouseClic:
				if logico.hayFichaJugador(cuadrox, cuadroy, jugadorActual):
					# el mouse esta sobre un cuadro
					grafico.dibujarCuadroIluminado(cuadrox, cuadroy)
				elif logico.estaEnCamino(cuadrox, cuadroy) and seleccion:
					# el mouse esta sobre un cuadro del camino de la ficha
					grafico.dibujarCuadroIluminado(cuadrox, cuadroy, fichaSeleccion)
					# si esa posible jugada puede comer alguna ficha
					if logico.hayQueComer(cuadrox, cuadroy, jugadorActual):
						grafico.dibujarAlertaComer()
					
			elif cuadrox != None and cuadroy != None and mouseClic:			
				if logico.hayFichaJugador(cuadrox, cuadroy, jugadorActual):
					# mouse hizo clic sobre alguna ficha de turno
					logico.setCamino(cuadrox, cuadroy)
					grafico.dibujarCaminoIluminado(cuadrox, cuadroy)
					seleccion = True
					fichaSeleccion = (cuadrox, cuadroy)
					
				elif logico.estaEnCamino(cuadrox, cuadroy) and seleccion:
					# mouse hizo clic en una posicion del camino
					logico.mover(fichaSeleccion[0], fichaSeleccion[1], cuadrox, cuadroy, jugadorActual)
					seleccion = False
					jugadorActual = self.switchJugador(jugadorActual)
			
			pygame.display.update()	
			FPSCLOCK.tick(self.FPS)	
	
	
#############################################  Clase Grafico ##############################################
#                  Pinta la ventana conforme los datos proporcionados por la clase Logico                 # 
###########################################################################################################
class Grafico:

	# Asignacion de constantes
	LARGO_VENTANA = None
	ANCHO_VENTANA = None
	ANCHO_CUADRO = None
	LARGO_CUADRO = None
	TAMANO = None
	CENTRO = None
	
	# almacenas las direcciones de las imagenes
	RUTA = None
	CARPETA = None
	DIRECCION = None
	IMAGENES = [None, None, None]
	
	# tuplas con las coordenadas de las posiciones de las fichas
	POSBX = None
	POSBY = None
	POSNX = None
	POSNY = None
	
	SUPERFICIE = None
	logico = None
	
	
	def __init__(self, logico, superficie, constantes):
		self.logico = logico
		self.SUPERFICIE = superficie
		self.LARGO_VENTANA = constantes[0]
		self.ANCHO_VENTANA = constantes[1]
		self.TAMANO = constantes[2]
		self.CENTRO = (self.TAMANO-1) / 2
		self.LARGO_CUADRO =  self.LARGO_VENTANA / self.TAMANO
		self.ANCHO_CUADRO =  self.ANCHO_VENTANA / self.TAMANO
		self.DIRECCION = ("rey.png","blanca.png","negra.png")
		self.CARPETA = ("img")
		self.RUTA = sys.argv[0][:len(sys.argv[0])-11]
		
		for i in range(3):
			self.IMAGENES[i] = pygame.image.load(os.path.join(self.RUTA, self.CARPETA, self.DIRECCION[i]))	
		self.IMAGENES = tuple(self.IMAGENES)
		
		self.POSBX = constantes[3]
		self.POSBY = constantes[4]
		self.POSNX = constantes[5]
		self.POSNY = constantes[6]
		
		
	""" Convierte las coordenadas de la esquina superior izquierda del cuadro 
	a una coordenada de pixel.
	"""
	def coordEsquinaCuadro(self, cuadrox, cuadroy):
		izquierda = (cuadrox * self.LARGO_CUADRO)
		arriba = (cuadroy * self.ANCHO_CUADRO)
		return (arriba, izquierda)
		

	""" Convierte las coordenadas del centro del cuadro a una coordenada de pixel. """
	def coordFichaEnCuadro(self, cuadrox, cuadroy, escalax, escalay):
		izquierda = (cuadrox * self.LARGO_CUADRO)
		arriba = (cuadroy * self.ANCHO_CUADRO)
		izquierda += int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * escalax)) / 2)
		arriba += int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * escalay)) / 2)
		return (arriba, izquierda)
		

	""" Recorre un tablero "imaginario" y devuelve una posicion si la coordenada
	en pixel esta dentro de algun cuadrado, en caso contrario devuelve la
	tupla (None, None).
	""" 	
	def getCuadroEnPixel(self, x, y):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				arriba, izquierda = self.coordEsquinaCuadro(cuadrox, cuadroy)
				dibCuadro = pygame.Rect(arriba, izquierda, self.LARGO_CUADRO, self.ANCHO_CUADRO)
				if dibCuadro.collidepoint(x, y):
					return (cuadrox, cuadroy)
		return (None, None)
		
		
	""" Dibuja los cuadros del tablero. """	
	def dibujarCuadros(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				arriba, izquierda = self.coordEsquinaCuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self.logico.getColorCuadro(cuadrox, cuadroy), 
					(arriba, izquierda, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
	
	""" Dibuja el icono de una ficha. """
	def dibujarFicha(self, cuadrox, cuadroy, fichaEncima=""):
		if self.logico.getPos(cuadrox, cuadroy) == "rey" or fichaEncima == "rey":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[0], 
				(int(self.LARGO_CUADRO * 0.80), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.75, 0.80))
				
		elif self.logico.getPos(cuadrox, cuadroy) == "sueco" or fichaEncima == "sueco":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[1], 
				(int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.75, 0.50))
		
		elif self.logico.getPos(cuadrox, cuadroy) == "moscovita" or fichaEncima == "moscovita":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[2], 
				(int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.75, 0.50))	
		
		
	""" Dibuja las fichas del tablero. """
	def dibujarFichas(self):		
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				self.dibujarFicha(cuadrox, cuadroy)
					

	""" Vuelve a dibujar el cuadro señalado por los parámetros pero de un color más claro. """
	def dibujarCuadroIluminado(self, cuadrox, cuadroy, fichaEncima=(), alerta=False):
		arriba, izquierda = self.coordEsquinaCuadro(cuadrox, cuadroy)
		if alerta:
			pygame.draw.rect(self.SUPERFICIE, self.logico.getColorAlerta(), 
				(arriba, izquierda, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		else:
			pygame.draw.rect(self.SUPERFICIE, self.logico.getColorIluminado(cuadrox, cuadroy), 
				(arriba, izquierda, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		if fichaEncima != ():
			self.dibujarFicha(cuadrox, cuadroy, self.logico.getPos(fichaEncima[0], fichaEncima[1]))
		else:
			self.dibujarFicha(cuadrox, cuadroy)
		
		
	""" Dibuja el camino iluminado de la ficha seleccionada. """	
	def dibujarCaminoIluminado(self, cuadrox, cuadroy):
		camino = self.logico.getCamino()
		if cuadrox != None and cuadroy != None: 
			self.dibujarCuadroIluminado(cuadrox, cuadroy)
		for cuadro in camino:
			self.dibujarCuadroIluminado(cuadro[0], cuadro[1])
		
		
	""" Dibuja un color de alerta en los cuadros indicados por 
	la lista retornada por logico.getComer().
	"""
	def dibujarAlertaComer(self):
		for cuadro in self.logico.getComer():
			self.dibujarCuadroIluminado(cuadro[0], cuadro[1], (), True)
	
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def dibujarTablero(self):
		self.SUPERFICIE.fill(self.logico.getColorFondo())
		self.dibujarCuadros()
		self.dibujarFichas()
			
########################################### Clase Logico ##################################################	
#         Maneja los datos y la lógica del juego, formada por las clases Tablero, Camino y Comer          #
###########################################################################################################	
class Logico:
    #                R    G    B
	COLOR1 =       ( 80,  48,  34)
	COLOR2 =       (203, 173, 112)
	COLOR_CLARO1 = (140, 108,  94)
	COLOR_CLARO2 = (255, 233, 172)
	COLOR_ALERTA = (248,  55,  47)
	
	# almacenaran las instancias de clase
	tablero = None
	camino = None
	comer = None
	
	def __init__(self, constantes):
		self.camino = Camino(constantes[2])
		self.tablero = Tablero(constantes)
		self.comer = Comer(constantes[2])
		self.crearTablero()
		
		
	# Operaciones que interactuan con la clase Tablero #
	
	""" Crea una matriz que representa la lógica del tablero. """	
	def crearTablero(self):
		self.tablero.crearTablero()

			
	""" Devuelve una copia de la matriz. """
	def getCopiaTablero(self):
		return self.tablero.getCopiaTablero()

		
	""" Devuelve una posición de la matriz. """
	def getPos(self, cuadrox, cuadroy):
		return self.tablero.getPos(cuadrox, cuadroy)

		
	""" Devuelve True si el cuadro indicado coresponde a una ficha de turno. """
	def hayFichaJugador(self, cuadrox, cuadroy, jugadorActual):
		return self.tablero.hayFichaJugador(cuadrox, cuadroy, jugadorActual)
		
	
	# Operaciones que interactúan con la clase Camino #
	
	""" Dada una posicion calcula el "camino" que esa ficha puede recorrer. """
	def setCamino(self, cuadrox, cuadroy):
		self.camino.setCamino(self.getCopiaTablero(), cuadrox, cuadroy)
		
	
	""" Retorna la lista con los cuadros del camino de la ficha. """	
	def getCamino(self):
		return self.camino.getCamino()
		
	
	""" Devuelve True si la posición indicada por los parametros forma parte de la lista
	actual del "camino". 
	"""	
	def estaEnCamino(self, cuadrox, cuadroy):
		return self.camino.estaEnCamino(cuadrox, cuadroy)	
	
	
	# Operaciones que interactúan con la clase Comer #
	
	""" Calcula si hay posibles fichas para comer dada una determinada posición
	devuelve True si hay al menos una.
	"""
	def hayQueComer(self, cuadrox, cuadroy, jugAct):
		return self.comer.comerFicha(self.getCopiaTablero(), cuadrox, cuadroy, jugAct)
	
	
	""" Devuelve la lista con las posiciones para comer. """
	def getComer(self):
		return self.comer.getComer()
		
	# Operaciones en conjunto #
	
	""" Mueve una ficha del tablero y busca si hay fichas para comer. """
	def mover(self, cx, cy, cnx, cny, jugAct):
		self.tablero.setFicha(cx, cy, cnx, cny)
		if self.comer.comerFicha(self.getCopiaTablero(), cnx, cny, jugAct):
			for cuadro in self.getComer():
				self.tablero.setFicha(cuadro[0], cuadro[1])
	

	""" Devuelve el color de fondo del tablero. """
	def getColorFondo(self):
		return self.COLOR1	
		
		
	""" Devuelve los colores del tablero por defecto. """
	def getColorCuadro(self, x, y):
		if x % 2 == 0:
			if y % 2 == 0:
				return self.COLOR1
			else:
				return self.COLOR2
		else:
			if y % 2 == 0:
				return self.COLOR2
			else:
				return self.COLOR1
		
		
	""" Devuelve los colores de los cuadros iluminados. """
	def getColorIluminado(self, x, y):
		if x % 2 == 0:
			if y % 2 == 0:
				return self.COLOR_CLARO1
			else:
				return self.COLOR_CLARO2
		else:
			if y % 2 == 0:
				return self.COLOR_CLARO2
			else:
				return self.COLOR_CLARO1
		
		
	""" Devuelve el color de alerta. """	
	def getColorAlerta(self):
		return self.COLOR_ALERTA

########################################### Clase Tablero #################################################	
#                        Maneja la representación y los cambios del tablero de juego.                     #
###########################################################################################################				
class Tablero:
	
	TAMANO = None
	CENTRO = None
	
	POSBX = None
	POSBY = None
	POSNX = None
	POSNY = None
	
	JUGADOR1 = "jugador1"
	JUGADOR2 = "jugador2"
	
	tablero = None
	
	def __init__(self, constantes):
		self.TAMANO = constantes[2]
		self.CENTRO = (self.TAMANO-1) / 2
		
		self.POSBX = constantes[3]
		self.POSBY = constantes[4]
		self.POSNX = constantes[5]
		self.POSNY = constantes[6]
	
	""" Crea una matriz que representa la lógica del tablero """	
	def crearTablero(self):
		self.tablero = []
		for x in range(self.TAMANO):
			columna = []
			for y in range(self.TAMANO):
				columna.append("")
			self.tablero.append(columna)
		
		# Coloca en los lugares correspondiente la representacion de las fichas.		
		self.tablero[self.CENTRO][self.CENTRO] = "rey"
		
		for i in range(len(self.POSBX)):
			self.tablero[self.POSBX[i]][self.POSBY[i]] = "sueco"
			
		for i in range(len(self.POSNX)):
			self.tablero[self.POSNX[i]][self.POSNY[i]] = "moscovita"
		
			
	""" Devuelve una copia de la matriz. """
	def getCopiaTablero(self):
		return deepcopy(self.tablero)

	""" Mueve una posicion del tablero a otra, dejando la primera en blanco. """	
	def setFicha(self, cuadrox, cuadroy, cnx=None, cny=None):
		if cnx == None:
			self.tablero[cuadrox][cuadroy] = ""
		else:
			self.tablero[cnx][cny] = self.tablero[cuadrox][cuadroy]
			self.tablero[cuadrox][cuadroy] = ""
		
		
	def sdfetPos(self):	
		print("a")
		
		
	""" Devuelve una posición de la matriz. """
	def getPos(self, cuadrox, cuadroy):
		return self.tablero[cuadrox][cuadroy]

		
	""" Devuelve True si el cuadro indicado coresponde a una ficha de turno. """
	def hayFichaJugador(self, cuadrox, cuadroy, jugadorActual):
		if jugadorActual == self.JUGADOR1:
			if self.tablero[cuadrox][cuadroy] == "moscovita":
				return True
			else:
				return False
		else:
			if self.tablero[cuadrox][cuadroy] == "rey" or self.tablero[cuadrox][cuadroy] == "sueco":
				return True
			else:
				return False
			
				
########################################### Clase Tablero #################################################	
#                  Calcula las posibles posiciones de movimento de una ficha del tablero.                 #
###########################################################################################################	
class Camino:

	TAMANO = None
	camino = None
	
	def __init__(self, tamano):
		self.camino = []
		self.TAMANO = tamano
	
	
	""" Devuelve True si no hay ficha en un cuadro. """	
	def noHayFicha(self, tablero, cuadrox, cuadroy):
		if tablero[cuadrox][cuadroy] == "":
			return True
		else:
			return False
			
	
	""" Dada una posicion de ficha busca los posibles lugares donde esta se puede mover. """
	def setCamino(self, tablero, cuadrox, cuadroy):
		copiaTablero = tablero
		self.camino = []
			
		# verifique a la derecha
		c = cuadrox + 1
		while c < self.TAMANO and self.noHayFicha(copiaTablero, c, cuadroy):
			self.camino.append( (c, cuadroy) )
			c+=1
		# verifique a la izquierda
		c = cuadrox - 1
		while c >= 0 and self.noHayFicha(copiaTablero, c, cuadroy):
			self.camino.append( (c, cuadroy) )
			c-=1
		# verifique abajo
		c = cuadroy + 1
		while c < self.TAMANO and self.noHayFicha(copiaTablero, cuadrox, c):
			self.camino.append( (cuadrox, c) )
			c+=1
		# verifique arriba
		c = cuadroy - 1
		while c >= 0 and self.noHayFicha(copiaTablero, cuadrox, c):
			self.camino.append( (cuadrox, c) )
			c-=1
			
		if copiaTablero[cuadrox][cuadroy] != "rey":
			if (0,0) in self.camino: self.camino.remove((0,0))	
			if (0, self.TAMANO-1) in self.camino: self.camino.remove((0, self.TAMANO-1))	
			if (self.TAMANO-1, 0) in self.camino: self.camino.remove((self.TAMANO-1, 0))	
			if (self.TAMANO-1, self.TAMANO-1) in self.camino: self.camino.remove((self.TAMANO-1, self.TAMANO-1))	
		
		return self.camino
	
	
	""" Devuelve la lista de camino actual """
	def getCamino(self):
		return self.camino
	
	
	""" Si el cuadro indicado esta dentro de la lista de camino, True """
	def estaEnCamino(self, cuadrox, cuadroy):
		for cuadro in self.camino:
			if cuadro == (cuadrox, cuadroy):
				return True
		return False
	
########################################### Clase Tablero #################################################	
#                      Calcula las posibles fichas que una ficha se pueda comer.                          #
###########################################################################################################					
class Comer:

	TAMANO = None
	JUGADOR1 = "jugador1"
	JUGADOR2 = "jugador2"	
	
	listaComer = None
	
	def __init__(self, tamano):
		self.TAMANO = tamano
		self.listaComer = []
		
		
	""" Calcula si hay posibles fichas para comer dada una determinada posición
	devuelve True si hay al menos una.
	"""		
	def comerFicha(self, copiaTablero, cuadrox, cuadroy, jugAct):
		self.listaComer = []
		if jugAct == self.JUGADOR1:
			oponente = ("sueco", "rey")
			aliado = ("moscovita", "moscovita")
		elif jugAct == self.JUGADOR2:
			oponente = ("moscovita", "moscovita")
			aliado = ("rey", "sueco")
		
		tablero = copiaTablero
		b = False
		
		# esquinas
		if cuadrox == 0 and cuadroy == 2 and (tablero[0][1] == oponente[0] or tablero[0][1] == oponente[1]):
			self.listaComer.append((0,1))
			b = True
		elif cuadrox == 0 and cuadroy == self.TAMANO-3 and (tablero[0][self.TAMANO-2] == oponente[0] or tablero[0][self.TAMANO-2] == oponente[1]):
			self.listaComer.append((0,self.TAMANO-2))
			b = True
		elif cuadrox == self.TAMANO-1 and cuadroy == 2 and (tablero[self.TAMANO-1][1] == oponente[0] or tablero[self.TAMANO-1][1] == oponente[1]):
			self.listaComer.append((self.TAMANO-1,1))
			b = True
		elif cuadrox == self.TAMANO-1 and cuadroy == self.TAMANO-3 and (tablero[self.TAMANO-1][self.TAMANO-2] == oponente[0] or tablero[self.TAMANO-1][self.TAMANO-2] == oponente[1]):
			self.listaComer.append((self.TAMANO-1,self.TAMANO-2))
			b = True
		elif cuadrox == 2 and cuadroy == 0 and (tablero[1][0] == oponente[0] or tablero[1][0] == oponente[1]):
			self.listaComer.append((1,0))
			b = True
		elif cuadrox == self.TAMANO-3 and cuadroy == 0 and (tablero[self.TAMANO-2][0] == oponente[0] or tablero[self.TAMANO-2][0] == oponente[1]):
			self.listaComer.append((self.TAMANO-2,0))
			b = True
		elif cuadrox == 2 and cuadroy == self.TAMANO-1 and (tablero[1][self.TAMANO-1] == oponente[0] or tablero[1][self.TAMANO-1] == oponente[1]):
			self.listaComer.append((1,self.TAMANO-1))
			b = True	
		elif cuadrox == self.TAMANO-3 and cuadroy == self.TAMANO-1 and (tablero[self.TAMANO-2][self.TAMANO-1] == oponente[0] or tablero[self.TAMANO-2][self.TAMANO-1] == oponente[1]):
			self.listaComer.append((self.TAMANO-2,self.TAMANO-1))
			b = True
			
		# limites
		if tablero[cuadrox-1][cuadroy] == oponente[0] or tablero[cuadrox-1][cuadroy] == oponente[1]:
			#busque arriba
			if tablero[cuadrox-2][cuadroy] == aliado[0] or tablero[cuadrox-2][cuadroy] == aliado[1]:
				self.listaComer.append((cuadrox-1, cuadroy))
				b = True
		# busque a la izquierda
		if tablero[cuadrox][cuadroy-1] == oponente[0] or tablero[cuadrox][cuadroy-1] == oponente[1]:
			if tablero[cuadrox][cuadroy-2] == aliado[0] or tablero[cuadrox][cuadroy-2] == aliado[1]:
				self.listaComer.append((cuadrox,cuadroy-1))
				b = True;
		# busque abajo
		if tablero[cuadrox+1][cuadroy] == oponente[0] or tablero[cuadrox+1][cuadroy] == oponente[1]:
			if tablero[cuadrox+2][cuadroy] == aliado[0] or tablero[cuadrox+2][cuadroy] == aliado[1]:
				self.listaComer.append((cuadrox+1,cuadroy))
				b = True
		# busque a la derecha
		if tablero[cuadrox][cuadroy+1] == oponente[0] or tablero[cuadrox][cuadroy+1] == oponente[1]:
			if tablero[cuadrox][cuadroy+2] == aliado[0] or tablero[cuadrox][cuadroy+2] == aliado[1]:
				self.listaComer.append((cuadrox,cuadroy+1))
				b = True;
		return b;
		
		
	""" Devuelve la lista con las posiciones para comer. """		
	def getComer(self):
		return self.listaComer

				
if __name__ == '__main__':
	main = Main()
	main.iniciar()
