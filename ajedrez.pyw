#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, pygame, sys, os
from pygame.locals import *
from copy import deepcopy

############################################### Clase Main ################################################
#        Maneja los eventos del mouse y coordina las representaciones logicas y graficas del juego        #
############################################### Clase Main ################################################

class Main:
	
	CONSTANTES = (594, 594, 11,
	(3,4,4,4,5,5,5,5,6,6,6,7),
	(5,4,5,6,3,4,6,7,4,5,6,5),
	(0,0,0,0,0,1,10,10,10,10,10,9,3,4,5,6,7,5,3,4,5,6,7,5),
	(3,4,5,6,7,5,3,4,5,6,7,5,0,0,0,0,0,1,10,10,10,10,10,9))
	LARGO_VENTANA = CONSTANTES[0]
	ANCHO_VENTANA = CONSTANTES[1]
	FPS = 24
	
	def iniciar(self):
		# iniciar el modulo pygame, el objeto FPS y la venatna
		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		SUPERFICIE = pygame.display.set_mode((self.LARGO_VENTANA, self.ANCHO_VENTANA))
		pygame.display.set_caption('Hnefatafl')
		
		logico = Logico(self.CONSTANTES)
		grafico = Grafico(logico, SUPERFICIE, self.CONSTANTES)
		
		# almacenan las coordenadas del mouse
		mousex = 0 
		mousey = 0 
		
		grafico.dibujarTablero()
		
		while True: # loop principal del juego
			mouseClic = False
			
			if not mouseClic:
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
				# el mouse esta sobre un cuadro
				if logico.hayFicha(cuadrox, cuadroy):
					grafico.dibujarCuadroIluminado(cuadrox, cuadroy)
			
			pygame.display.update()	
			FPSCLOCK.tick(self.FPS)	
	
	
#############################################  Clase Grafico ##############################################
#                  Pinta la ventana conforme los datos proporcionados por la clase Logico                 # 
############################################### Clase Main ################################################

class Grafico:

	LARGO_VENTANA = None
	ANCHO_VENTANA = None
	ANCHO_CUADRO = None
	LARGO_CUADRO = None
	TAMANO = None
	CENTRO = None
	
	DIRECCION = None
	CARPETA = None
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
		
		for i in range(3):
			self.IMAGENES[i] = pygame.image.load(os.path.join(self.CARPETA, self.DIRECCION[i]))	
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
		return (izquierda, arriba)
		

	""" Convierte las coordenadas del centro del cuadro a una coordenada de pixel. """
	def coordFichaEnCuadro(self, cuadrox, cuadroy, escalax, escalay):
		izquierda = (cuadrox * self.LARGO_CUADRO)
		arriba = (cuadroy * self.ANCHO_CUADRO)
		izquierda += int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * escalax)) / 2)
		arriba += int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * escalay)) / 2)
		return (izquierda, arriba)
		

	""" Recorre un tablero "imaginario" y devuelve una posicion si la coordenada
	en pixel esta dentro de algun cuadrado, en caso contrario devuelve la
	tupla (None, None).
	""" 	
	def getCuadroEnPixel(self, x, y):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				izquierda, arriba = self.coordEsquinaCuadro(cuadrox, cuadroy)
				dibCuadro = pygame.Rect(izquierda, arriba, self.LARGO_CUADRO, self.ANCHO_CUADRO)
				if dibCuadro.collidepoint(x, y):
					return (cuadrox, cuadroy)
		return (None, None)
		
		
	def dibujarCuadros(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				izquierda, arriba = self.coordEsquinaCuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self.logico.getColorCuadro(cuadrox, cuadroy), (izquierda, arriba, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
		
	def dibujarFichas(self):
		copiaTablero = self.logico.getCopiaTablero()
		
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				if copiaTablero[cuadrox][cuadroy] == "rey":
					iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[0], (int(self.LARGO_CUADRO * 0.80), int(self.ANCHO_CUADRO * 0.75)))
					self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.80, 0.75))
				
				elif copiaTablero[cuadrox][cuadroy] == "sueco":
					iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[1], (int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
					self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.50, 0.75))
		
				elif copiaTablero[cuadrox][cuadroy] == "moscovita":
					iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[2], (int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
					self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.50, 0.75))
					
		del copiaTablero

	
	""" Vuelve a dibujar el cuadro señalado por los parámetros pero de un color más claro. """
	def dibujarCuadroIluminado(self, cuadrox, cuadroy):
		self.dibujarCuadros()
		izquierda, arriba = self.coordEsquinaCuadro(cuadrox, cuadroy)
		pygame.draw.rect(self.SUPERFICIE, self.logico.getColorIluminado(cuadrox, cuadroy), (izquierda, arriba, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		self.dibujarFichas()	
		
		
	def dibujarTablero(self):
		self.SUPERFICIE.fill(self.logico.getColorFondo())
		self.dibujarCuadros()
		self.dibujarFichas()
		
	
	
########################################### Clase Logico ##################################################	
#             Maneja los datos del tablero, lo actualiza y mantiene la puntuacion del jugador             #
###########################################################################################################
	
class Logico:

	COLOR1 = (100, 68, 54)
	COLOR2 = (223, 193, 132)
	COLOR_CLARO1 = (120, 88, 74)
	COLOR_CLARO2 = (243, 213, 152)
	
	TAMANO = None
	CENTRO = None
	
	POSBX = None
	POSBY = None
	POSNX = None
	POSNY = None
	
	tablero = None
	
	def __init__(self, constantes):
		self.TAMANO = constantes[2]
		self.CENTRO = (self.TAMANO-1) / 2
		
		self.POSBX = constantes[3]
		self.POSBY = constantes[4]
		self.POSNX = constantes[5]
		self.POSNY = constantes[6]
		
		self.crearTablero()
		
		
	def crearTablero(self):
		self.tablero = []
		for x in range(self.TAMANO):
			columna = []
			for y in range(self.TAMANO):
				columna.append("")
			self.tablero.append(columna)
			
		self.tablero[self.CENTRO][self.CENTRO] = "rey"
		
		for i in range(len(self.POSBX)):
			self.tablero[self.POSBX[i]][self.POSBY[i]] = "sueco"
			
		for i in range(len(self.POSNX)):
			self.tablero[self.POSNX[i]][self.POSNY[i]] = "moscovita"

			
	""" Devuelve una copia de la matriz. """
	def getCopiaTablero(self):
		return deepcopy(self.tablero)
			
	
	def hayFicha(self, cuadrox, cuadroy):
		if self.tablero[cuadrox][cuadroy] == "rey" or self.tablero[cuadrox][cuadroy] == "sueco" or self.tablero[cuadrox][cuadroy] == "moscovita":
			return True
		else:
			return False
	
	
	def getColorFondo(self):
		return self.COLOR1
		
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

	
if __name__ == '__main__':
	main = Main()
	main.iniciar()