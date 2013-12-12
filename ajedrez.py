#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, pygame, sys, os
from pygame.locals import *
from copy import deepcopy

############################################### Clase Main ################################################
#                       Maneja los eventos del mouse y el loop principal del juego                        #
###########################################################################################################
class Main:	
	
	LARGO_VENTANA = None
	ANCHO_VENTANA = None
	
	# almacenaran las instancias de los objetos.
	jugador = None
	tablero = None
	calculos = None
	grafico = None
	logico = None
	
	# velocidad promedio de cuadros por segundo.
	FPS = 114
	
	FPSCLOCK = None
	SUPERFICIE = None
	
	# boolean para controlar estas de juego.
	seleccion = False
	jaque = False
	jaqueMate = False
	peligro = False
	
	# sirve para almacenar la posicion de la ficha seleccionada por el clic
	fichaSeleccion = ""
	
	""" Constructor """
	def __init__(self, config):
		self.LARGO_VENTANA = config["LARGO_VENTANA"]
		self.ANCHO_VENTANA = config["ANCHO_VENTANA"]
		
		# iniciar el modulo pygame y el objeto FPS.
		pygame.init()
		self.FPSCLOCK = pygame.time.Clock()

		
		# instancia de clases 
		self.tablero = Tablero(config)
		self.grafico = Grafico(self.tablero, self.SUPERFICIE, config)
		
		
	def iniciar(self):
		# almacenan las coordenadas del mouse
		mousex = 0 
		mousey = 0 
	
		while True: # loop principal del juego
		
			mouseClic = False
			
			# TODO 
			# dibujar ventana.
			self.grafico.dibujarVentana(self.jugador.getJugador(), self.logico.getComidas1(), self.logico.getComidas2(), self.jaque, self.jaqueMate, self.peligro)
			if self.jaque or self.jaqueMate:
				self.grafico.dibujarAlerta(self.calculos.getEsquinas(), "verde")
			if self.peligro:
				self.grafico.dibujarAlerta(self.calculos.getPeligroRey(), "roja")
			if self.seleccion:
				self.grafico.dibujarCaminoIluminado(None, None)
				
			# manejo de eventos.
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
			cuadrox, cuadroy = self.grafico.getCuadroEnPixel(mousex, mousey)					
			
			# TODO modificar por cuadrox, cuadrox != None, None
			if cuadrox != None and cuadroy != None and not mouseClic:
				if self.logico.hayFichaJugador(cuadrox, cuadroy):
					# el mouse esta sobre un cuadro
					self.grafico.dibujarCuadroIluminado(cuadrox, cuadroy)
				elif self.logico.estaEnCamino(cuadrox, cuadroy) and self.seleccion:
					# el mouse esta sobre un cuadro del camino de la ficha
					self.grafico.dibujarCuadroIluminado(cuadrox, cuadroy, self.fichaSeleccion)
					# si esa posible jugada puede comer alguna ficha
					if self.logico.hayQueComer(cuadrox, cuadroy):
						self.grafico.dibujarAlerta(self.logico.getComer(), "roja")
					
			elif cuadrox != None and cuadroy != None and mouseClic:			
				if self.logico.hayFichaJugador(cuadrox, cuadroy):
					# mouse hizo clic sobre alguna ficha de turno
					self.logico.setCamino(cuadrox, cuadroy)
					self.grafico.dibujarCaminoIluminado(cuadrox, cuadroy)
					self.seleccion = True
					self.fichaSeleccion = (cuadrox, cuadroy)
					
				elif self.logico.estaEnCamino(cuadrox, cuadroy) and self.seleccion:
					# mouse hizo clic en una posicion del camino
					self.logico.mover(self.fichaSeleccion[0], self.fichaSeleccion[1], cuadrox, cuadroy)
					self.seleccion = False
					self.jugador.switchJugador()
			
					# estado del juego sin terminar
					copiaTablero = self.logico.getCopiaTablero()
					if self.calculos.verificarEsquinas(copiaTablero):
						# El rey ha llegado a una esquina
						self.finJuego("jugador2")
					else:
						encasillado = self.calculos.verificarLimites(copiaTablero)
						if encasillado == 4:
							# El rey ha sido encasillado, jaquemate
							self.finJuego("jugador1")
						else:
							if encasillado == 3:
								# El rey puede estar en peligro
								if self.calculos.verificarPeligro(copiaTablero):
									# el rey esta en peligro
									self.grafico.dibujarAlerta(self.calculos.getPeligroRey(), "roja")
									self.peligro = True
							else:
								self.peligro = False
							
							esquinas = self.calculos.buscarEsquinaRey(copiaTablero)
							if esquinas == 1:
								# hay una situacion de jaque 
								self.jaque = True
								self.jaqueMate = False
								self.grafico.dibujarAlerta(self.calculos.getEsquinas(), "verde")	
							elif esquinas == 2:
								# hay una situacion de jaquemate
								self.jaque = False
								self.jaqueMate = True
								self.grafico.dibujarAlerta(self.calculos.getEsquinas(), "verde")	
							else:
								self.jaque = False
								self.jaqueMate = False
			
			pygame.display.update()	
			self.FPSCLOCK.tick(self.FPS)	
	
	
	""" Animaciones para el fin del juego """
	def finJuego(self, ganador):
		self.grafico.dibujarVentana(self.jugador.getJugador(), self.logico.getComidas1(), self.logico.getComidas2(), self.jaque, self.jaqueMate, self.peligro, ganador)
		pygame.display.update()
		pygame.time.wait(5000)
		self.logico.resetearTablero()
		self.seleccion = False
		self.jaque = False
		self.jaqueMate = False
		self.peligro = False
		self.fichaSeleccion = ""
		self.jugador.nuevoJuego()	
	
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
	MARGEN_X = None
	MARGEN_Y = None
	
	# almacenas las direcciones de las imagenes
	CARPETA = None
	DIRECCION = None
	IMAGENES = [None, None, None]
	
	SUPERFICIE = None
	objFuente = None
	tablero = None
	config = None
	
	def __init__(self, tablero, superficie, config):
		self.config = config 
		self.tablero = tablero
		self.SUPERFICIE = superficie
		self.LARGO_VENTANA = config["LARGO_VENTANA"]
		self.ANCHO_VENTANA = config["ANCHO_VENTANA"]
		self.TAMANO = config["TAMANO"]
		self.CENTRO = (self.TAMANO-1) / 2
		self.LARGO_CUADRO =  self.LARGO_VENTANA / self.TAMANO
		self.ANCHO_CUADRO =  self.ANCHO_VENTANA / self.TAMANO
		self.MARGEN_X = int(self.ANCHO_CUADRO*0.33)
		self.MARGEN_Y = self.ANCHO_CUADRO + int(self.ANCHO_CUADRO*0.33) 
		
		self.DIRECCION = ("rey.png","blanca.png","negra.png")
		self.CARPETA = ("img")
		for i in range(3):
			self.IMAGENES[i] = pygame.image.load(os.path.join(self.CARPETA, self.DIRECCION[i]))	
		self.IMAGENES = tuple(self.IMAGENES)
		
		self.objFuente = pygame.font.Font('freesansbold.ttf', 32)
		
		self.SUPERFICIE = pygame.display.set_mode(((self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_Y) ))
		pygame.display.set_caption('Ajedrez Vikingo')
		
		
	""" Convierte las coordenadas de la esquina superior coordX del cuadro 
	a una coordenada de pixel.
	"""
	def coordEsquinaCuadro(self, cuadrox, cuadroy):
		coordX = self.MARGEN_X + (cuadroy * self.ANCHO_CUADRO)
		coordY = self.MARGEN_Y + (cuadrox * self.LARGO_CUADRO)
		return (coordX, coordY)
		

	""" Convierte las coordenadas del centro del cuadro a una coordenada de pixel. """
	def coordFichaEnCuadro(self, cuadrox, cuadroy, escalax, escalay):
		coordX, coordY = self.coordEsquinaCuadro(cuadrox, cuadroy)
		coordX += int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * escalax)) / 2)
		coordY += int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * escalay)) / 2)
		return (coordX, coordY)
		

	""" Recorre un tablero "imaginario" y devuelve una posicion si la coordenada
	en pixel esta dentro de algun cuadrado, en caso contrario devuelve la
	tupla (None, None).
	""" 	
	def getCuadroEnPixel(self, x, y):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordY, coordX = self.coordEsquinaCuadro(cuadrox, cuadroy)
				dibCuadro = pygame.Rect(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO)
				if dibCuadro.collidepoint(x, y):
					return (cuadrox, cuadroy)
		return (None, None)
		
		
	""" Dibuja los cuadros del tablero. """	
	def dibujarCuadros(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordX, coordY = self.coordEsquinaCuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self.logico.getColorCuadro(cuadrox, cuadroy), 
					(coordX, coordY, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
	
	""" Dibuja el icono de una ficha. """
	def dibujarFicha(self, cuadrox, cuadroy, fichaEncima=""):
		if self.logico.getPos(cuadrox, cuadroy) == "rey" or fichaEncima == "rey":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[0], 
				(int(self.LARGO_CUADRO * 0.8), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.8, 0.75))
				
		elif self.logico.getPos(cuadrox, cuadroy) == "sueco" or fichaEncima == "sueco":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[1], 
				(int(self.LARGO_CUADRO * 0.5), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.5, 0.75))
		
		elif self.logico.getPos(cuadrox, cuadroy) == "moscovita" or fichaEncima == "moscovita":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[2], 
				(int(self.LARGO_CUADRO * 0.5), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.5, 0.75))	
		
		
	""" Dibuja las fichas del tablero. """
	def dibujarFichas(self):		
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				self.dibujarFicha(cuadrox, cuadroy)
					

	""" Vuelve a dibujar el cuadro señalado por los parámetros pero de un color más claro. """
	def dibujarCuadroIluminado(self, cuadrox, cuadroy, fichaEncima=(), alerta=""):
		coordY, coordX = self.coordEsquinaCuadro(cuadrox, cuadroy)
		if alerta != "":
			pygame.draw.rect(self.SUPERFICIE, self.logico.getColorAlerta(alerta), 
				(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		else:
			pygame.draw.rect(self.SUPERFICIE, self.logico.getColorIluminado(cuadrox, cuadroy), 
				(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO))
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
	def dibujarAlerta(self, listaCuadros, alerta):
		for cuadro in listaCuadros:
			self.dibujarCuadroIluminado(cuadro[0], cuadro[1], (), alerta)
	
	""" Dibuja una ficha (sirve para las fichas del panel. """
	def dibujarFichaIndividual(self, i, coordX, coordY):
		iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[i], 
			(int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
		self.SUPERFICIE.blit(iconoParaDibujar, (coordX, coordY))
	
	
	""" Dibuja los iconos de los paneles superior e inferior del tablero de juego. """
	def dibujarPanel(self):
		coordX = self.MARGEN_X + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * 0.75)) / 2)
		
		self.dibujarFichaIndividual(2, coordX, coordY)
		
		coordX = self.MARGEN_X + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = (self.ANCHO_VENTANA + self.MARGEN_X + self.MARGEN_Y) + int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * 0.75)) / 2)
		
		self.dibujarFichaIndividual(1, coordX, coordY)
		
		coordX = self.LARGO_VENTANA - self.MARGEN_X + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * 0.75)) / 2)
		
		self.dibujarFichaIndividual(1, coordX, coordY)

		coordX = self.LARGO_VENTANA - self.MARGEN_X + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = (self.ANCHO_VENTANA + self.MARGEN_X + self.MARGEN_Y) + int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * 0.75)) / 2)
		
		self.dibujarFichaIndividual(2, coordX, coordY)
		
		
	""" Dibuja una hilera en la pantalla. """
	def dibujarTexto(self, texto, color, coordx, coordy):
		superfTexto = self.objFuente.render(texto, True, color)
		rectTexto = superfTexto.get_rect()
		rectTexto.left = coordx
		rectTexto.centery = coordy
		self.SUPERFICIE.blit(superfTexto, rectTexto)
	
	
	""" Dibuja todos los textos de la pantalla. """
	def dibujarTextos(self, jugAct, c1, c2, jaque, jaqueMate, peligro, gano=""):
		color1 = self.logico.getColorTexto()
		color2 = self.logico.getColorTexto()
		textoJ1 = 'Jugador 1, tu turno.' if jugAct == "jugador1" else ''
		textoJ2 = 'Jugador 2, tu turno.' if jugAct == "jugador2" else ''
		
		if jaque:
			textoJ1 = 'Jugador 1, Jaque'
			color1 = self.logico.getColorAlerta("roja")
		elif jaqueMate:
			textoJ1 = 'Jugador 1, JaqueMate'
			color1 = self.logico.getColorAlerta("roja")
			
		if peligro:
			textoJ2 = 'Jugador 2, vigila tu rey'
			color2 = self.logico.getColorAlerta("roja")

		if gano == "jugador1":
			textoJ1 = 'Jugador 1, ganaste.'
			textoJ2 = ""
			color1 = self.logico.getColorAlerta("verde")
		elif gano == "jugador2":
			textoJ2 = 'Jugador 2, ganaste.'
			textoJ1 = ""
			color2 = self.logico.getColorAlerta("verde")
			
		
		fichasC1 = 'x'+str(c1)
		fichasC2 = 'x'+str(c2)
		
		coordX = self.MARGEN_X + self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int(self.ANCHO_CUADRO / 2)
		self.dibujarTexto(textoJ1, color1, coordX, coordY)
		
		coordX = self.MARGEN_X + self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = self.ANCHO_VENTANA + self.MARGEN_Y + self.MARGEN_X + int(self.ANCHO_CUADRO / 2)
		
		self.dibujarTexto(textoJ2, color2, coordX, coordY)
		
		coordX = self.LARGO_VENTANA - self.MARGEN_X - self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int(self.ANCHO_CUADRO / 2)
		
		self.dibujarTexto(fichasC1, self.logico.getColorTexto(), coordX, coordY)	

		coordX = self.LARGO_VENTANA - self.MARGEN_X - self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = self.ANCHO_VENTANA + self.MARGEN_Y + self.MARGEN_X + int(self.ANCHO_CUADRO / 2)
		
		self.dibujarTexto(fichasC2, self.logico.getColorTexto(), coordX, coordY)
		
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def dibujarVentana(self, jugAct, c1, c2, jaque, jaqueMate, peligro, gano=""):
		self.SUPERFICIE.fill(self.logico.getColorFondo())
		pygame.draw.rect(self.SUPERFICIE, self.logico.getColorMargenes(), (0, self.ANCHO_CUADRO, (self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_X)), 0)
		
		self.dibujarPanel()
		self.dibujarTextos(jugAct, c1, c2, jaque, jaqueMate, peligro, gano)
		self.dibujarCuadros()
		self.dibujarFichas()

class Tablero(object):
	tablero = None
	
	def __init__(self, config):
		blanca = config["BLANCA"]
		negra = config["NEGRA"]
		tablero = []
		for i in range(config["TAMANO"]):
			fila = []
			for j in range(config["TAMANO"]):
				clase = ()
				# asignar ficha
				if len(blanca) > 0 and (i, j) == blanca[0]:
					clase = ("sueco", "moscovita")
					blanca.remove((i,j))
				elif len(negra) > 0 and (i, j) == negra[0]: 
					clase = ("sueco", "moscovita")
					negra.remove((i,j))
				else:
					clase = (None, None)
				# instancia de variable
				nodo = Nodo(i,j, clase, config["TAMANO"])
				# asociar punteros
				if len(tablero) > 0:
					nodo.arr = tablero[len(tablero)-1][j]
					tablero[len(tablero)-1][j].aba = nodo
				if len(fila) > 0:
					nodo.izq = fila[len(fila)-1]
					fila[len(fila)-1].der = nodo
				fila.append(nodo)
			tablero.append(fila)
		
		self.tablero = tablero[0][0]
		del tablero		

class Nodo(object):
	der = None
	izq = None
	arr = None
	aba = None
	
	TAMANO_TABLERO = None
	clase = None
	enemigo = None
	listaComer = None
	
	x = 0;
	y = 0;
	
	def __init__(self, i, j, clase, t):
		self.x = i
		self.y = j
		self.TAMANO_TABLERO = t
		self.clase = clase[0]
		self.enemigo = clase[1]
		
	def getCoord(self):
		return (self.x, self.y)		
	
	def getFicha(self, x, y):
		tmp = self 
		while(tmp.getCoord() != (x, y)):
			coord = tmp.getCoord()
			if x > coord[0]:
				tmp = tmp.aba
			if y > coord[1]:
				tmp = tmp.der
		return tmp
		
	def getCamino(self):
		camino = []
		tmp = self
		while(tmp.izq != None and tmp.izq.clase == None):
			camino.append(tmp.izq.getCoord())
			tmp = tmp.izq
		tmp = self
		while(tmp.der != None and tmp.der.clase == None):
			camino.append(tmp.der.getCoord())
			tmp = tmp.der
		tmp = self
		while(tmp.arr != None and tmp.arr.clase == None):
			camino.append(tmp.arr.getCoord())
			tmp = tmp.arr
		tmp = self
		while(tmp.aba != None and tmp.aba.clase == None):
			camino.append(tmp.aba.getCoord())
			tmp = tmp.aba
		return camino
		
	def comerFicha(self):
		self.listaComer = []	
		b = False
		
		# esquinas
		if (self.x, self.y) == (0, 2) and self.arr.clase == self.enemigo:
			self.listaComer.append((0,1))
			b = True
		elif (self.x, self.y) == (0, self.TAMANO_TABLERO-3) and self.aba.clase == self.enemigo:
			self.listaComer.append((0,self.TAMANO_TABLERO-2))
			b = True
		elif (self.x, self.y) == (self.TAMANO_TABLERO-1, 2) and self.arr.clase == self.enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-1,1))
			b = True
		elif (self.x, self.y) == (self.TAMANO_TABLERO-1, self.TAMANO_TABLERO-3) and self.aba.clase == self.enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-1,self.TAMANO_TABLERO-2))
			b = True
		elif (self.x, self.y) == (2, 0) and self.izq.clase == self.enemigo:
			self.listaComer.append((1,0))
			b = True
		elif (self.x, self.y) == (self.TAMANO_TABLERO-3, 0) and self.der.clase == self.enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-2,0))
			b = True
		elif (self.x, self.y) == (2, self.TAMANO_TABLERO-1) and self.izq.clase == self.enemigo:
			self.listaComer.append((1,self.TAMANO_TABLERO-1))
			b = True	
		elif (self.x, self.y) == (self.TAMANO_TABLERO-3, self.TAMANO_TABLERO-1) and self.der.clase == self.enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-2,self.TAMANO_TABLERO-1))
			b = True
			
		# limites
		if self.arr != None and self.arr.clase == enemigo and self.arr.arr != None and self.arr.arr.clase == self.clase:
			self.listaComer.append(self.arr.getCoord())
		if self.aba != None and self.aba.clase == enemigo and self.aba.aba != None and self.aba.aba.clase == self.clase:
			self.listaComer.append(self.aba.getCoord())
		if self.izq != None and self.izq.clase == enemigo and self.izq.izq != None and self.izq.izq.clase == self.clase:
			self.listaComer.append(self.izq.getCoord())
		if self.der != None and self.der.clase == enemigo and self.der.der != None and self.der.der.clase == self.clase:
			self.listaComer.append(self.der.getCoord())
		
		return b
		
		
if __name__ == '__main__':
	config = {}
	execfile("settings2.config", config) 
	main = Main(config)
	main.iniciar()
