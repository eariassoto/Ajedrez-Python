#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, pygame, sys, os
from pygame.locals import *
from copy import deepcopy

############################################### Clase Main ################################################
#        Maneja los eventos del mouse y coordina las representaciones logicas y graficas del juego        #
############################################### Clase Main ################################################

class Main:
	
	""" Lista de constantes respectivamente corresponden a largo y ancho de la ventana, cantidad de
	cuadros del tablero nxn, coordenadas de las fichas blancas (x,y) y negras (x, y)
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
		
		fichaSeleccion = ""
		
		# dibujar la pantalla
		grafico.dibujarTablero()
		
		while True: # loop principal del juego
		
			mouseClic = False
			segundoMouseClic = False
			
			# TODO vigile esta parte weon
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
############################################### Clase Main ################################################

class Grafico:

	# Asignacion de constantes
	LARGO_VENTANA = None
	ANCHO_VENTANA = None
	ANCHO_CUADRO = None
	LARGO_CUADRO = None
	TAMANO = None
	CENTRO = None
	
	RUTA = None
	CARPETA = None
	DIRECCION = None
	IMAGENES = [None, None, None]
	
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
		
		
	""" Dibuja los cuadros del tablero """	
	def dibujarCuadros(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				arriba, izquierda = self.coordEsquinaCuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self.logico.getColorCuadro(cuadrox, cuadroy), (arriba, izquierda, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
	
	""" Dibuja el icono de una ficha """
	def dibujarFicha(self, cuadrox, cuadroy, fichaEncima=""):
		if self.logico.getPos(cuadrox, cuadroy) == "rey" or fichaEncima == "rey":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[0], (int(self.LARGO_CUADRO * 0.80), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.75, 0.80))
				
		elif self.logico.getPos(cuadrox, cuadroy) == "sueco" or fichaEncima == "sueco":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[1], (int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.75, 0.50))
		
		elif self.logico.getPos(cuadrox, cuadroy) == "moscovita" or fichaEncima == "moscovita":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[2], (int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.75, 0.50))	
		
		
	""" Dibuja las fichas del tablero """
	def dibujarFichas(self):		
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				self.dibujarFicha(cuadrox, cuadroy)
					

	""" Vuelve a dibujar el cuadro señalado por los parámetros pero de un color más claro. """
	def dibujarCuadroIluminado(self, cuadrox, cuadroy, fichaEncima=()):
		arriba, izquierda = self.coordEsquinaCuadro(cuadrox, cuadroy)
		pygame.draw.rect(self.SUPERFICIE, self.logico.getColorIluminado(cuadrox, cuadroy), (arriba, izquierda, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		if fichaEncima != ():
			self.dibujarFicha(cuadrox, cuadroy, self.logico.getPos(fichaEncima[0], fichaEncima[1]))
		else:
			self.dibujarFicha(cuadrox, cuadroy)
		
		
	""" Dibuja el camino iluminado de la ficha seleccionada """	
	def dibujarCaminoIluminado(self, cuadrox, cuadroy):
		camino = self.logico.getCamino()
		if cuadrox != None and cuadroy != None: 
			self.dibujarCuadroIluminado(cuadrox, cuadroy)
		for cuadro in camino:
			self.dibujarCuadroIluminado(cuadro[0], cuadro[1])
		
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def dibujarTablero(self):
		self.SUPERFICIE.fill(self.logico.getColorFondo())
		self.dibujarCuadros()
		self.dibujarFichas()
		
	
	
########################################### Clase Logico ##################################################	
#             Maneja los datos del tablero, lo actualiza y mantiene la puntuacion del jugador             #
###########################################################################################################
	
class Logico:
# TODO hacer modulos xq esta vara se esta agrandando
    #                R    G    B
	COLOR1 =       ( 80,  48,  34)
	COLOR2 =       (203, 173, 112)
	COLOR_CLARO1 = (140, 108,  94)
	COLOR_CLARO2 = (255, 233, 172)
	
	tablero = None
	camino = None
	comer = None
	
	def __init__(self, constantes):
		self.camino = Camino(constantes[2])
		self.tablero = Tablero(constantes)
		self.comer = Comer(constantes[2])
		self.crearTablero()
		
	""" Crea una matriz que representa la lógica del tablero """	
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
		

	def setCamino(self, cuadrox, cuadroy):
		self.camino.setCamino(self.getCopiaTablero(), cuadrox, cuadroy)
		
		
	def getCamino(self):
		return self.camino.getCamino()
		
		
	def estaEnCamino(self, cuadrox, cuadroy):
		return self.camino.estaEnCamino(cuadrox, cuadroy)	
	
	
	def mover(self, cx, cy, cnx, cny, jugAct):
		self.tablero.setPos(cx, cy, cnx, cny)
		print self.comer.comerFicha(self.getCopiaTablero(), cnx, cny, jugAct)
	
		
	""" Devuelve el color de fondo del tablero """
	def getColorFondo(self):
		return self.COLOR1	
		
		
	""" Devuelve un valor de color RGB. """
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
		
		
	""" Devuelve un valor de color RGB. """
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

		
	def setPos(self, cuadrox, cuadroy, cnx, cny):
		self.tablero[cnx][cny] = self.tablero[cuadrox][cuadroy]
		self.tablero[cuadrox][cuadroy] = ""
		
		
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
			
				
# modulo de logico
class Camino:

	TAMANO = None
	camino = None
	
	def __init__(self, tamano):
		self.camino = []
		self.TAMANO = tamano
	
	""" Devuelve True si no hay ficha en un cuadro """	
	def noHayFicha(self, tablero, cuadrox, cuadroy):
		if tablero[cuadrox][cuadroy] == "":
			return True
		else:
			return False
			
	
	""" Dada una posicion de ficha busca los posibles lugares donde esta se puede mover """
	# TODO recuerde modificar para restringir las esquinas	
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
	
				
class Comer:

	TAMANO = None
	JUGADOR1 = "jugador1"
	JUGADOR2 = "jugador2"	
	
	
	def __init__(self, tamano):
		self.TAMANO = tamano
		
		
	def comerFicha(self, copiaTablero, cuadrox, cuadroy, jugAct):
		
		if jugAct == self.JUGADOR1:
			oponente = ("rey", "sueco")
			aliado = ("moscovita", "moscovita")
		else:
			oponente = ("moscovita", "moscovita")
			aliado = ("moscovita", "moscovita")
		
		tablero = copiaTablero
		
		b = False
		
		# esquinas
		if cuadrox == 0 and cuadroy == 2 and (tablero[0][1] == oponente[0] or tablero[0][1] == oponente[1]):
			b = True
		elif cuadrox == 0 and cuadroy == self.TAMANO-3 and (tablero[0][self.TAMANO-2] == oponente[0] or tablero[0][self.TAMANO-2] == oponente[1]):
			b = True
		elif cuadrox == self.TAMANO-1 and cuadroy == 2 and (tablero[self.TAMANO-1][1] == oponente[0] or tablero[self.TAMANO-1][1] == oponente[1]):
			b = True
		elif cuadrox == self.TAMANO-1 and cuadroy == self.TAMANO-3 and (tablero[self.TAMANO-1][self.TAMANO-2] == oponente[0] or tablero[self.TAMANO-1][self.TAMANO-2] == oponente[1]):
			b = True
		elif cuadrox == 2 and cuadroy == 0 and (tablero[1][0] == oponente[0] or tablero[1][0] == oponente[1]):
			b = True
		elif cuadrox == self.TAMANO-3 and cuadroy == 0 and (tablero[self.TAMANO-2][0] == oponente[0] or tablero[self.TAMANO-2][0] == oponente[1]):
			b = True
		elif cuadrox == 2 and cuadroy == self.TAMANO-1 and (tablero[1][self.TAMANO-1] == oponente[0] or tablero[1][self.TAMANO-1] == oponente[1]):
			b = True	
		elif cuadrox == self.TAMANO-3 and cuadroy == self.TAMANO-1 and (tablero[self.TAMANO-2][self.TAMANO-1] == oponente[0] or tablero[self.TAMANO-2][self.TAMANO-1] == oponente[1]):
			b = True
			
		# limites
		if cuadrox >= 2: 
			if tablero[cuadrox-2][cuadroy] == (aliado[0] or aliado[1]) and (tablero[cuadrox-1][cuadroy] == oponente[0] or tablero[cuadrox-1][cuadroy] == oponente[1]):
				b = True
	
		if cuadrox <= self.TAMANO-3:
			if tablero[cuadrox+2][cuadroy] == (aliado[0] or aliado[1]) and (tablero[cuadrox+1][cuadroy] == oponente[0] or tablero[cuadrox+1][cuadroy] == oponente[1]):
				b = True
			
		if cuadroy >= 2:
			if tablero[cuadrox][cuadroy-2] == (aliado[0] or aliado[1]) and (tablero[cuadrox][cuadroy-1] == oponente[0] or tablero[cuadrox][cuadroy-1] == oponente[1]):
				b = True;
			
		if cuadroy <= self.TAMANO-3:
			if tablero[cuadrox][cuadroy+2] == (aliado[0] or aliado[1]) and (tablero[cuadrox][cuadroy+1] == oponente[0] or tablero[cuadrox][cuadroy+1] == oponente[1]):
				b = True;

		return b;

				
if __name__ == '__main__':
	main = Main()
	main.iniciar()
