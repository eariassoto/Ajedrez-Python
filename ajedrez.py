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
	grafico = None
	
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
		self.jugador = Jugador()
		self.tablero = Tablero(config, self.jugador)
		self.grafico = Grafico(self.jugador, self.tablero, self.SUPERFICIE, config)
		
		
	def iniciar(self):
		# almacenan las coordenadas del mouse
		mousex = 0 
		mousey = 0 
	
		while True: # loop principal del juego
		
			mouseClic = False
			
			# dibujar ventana.
			self.grafico.dibujarVentana(self.jugador, self.jaque, self.jaqueMate, self.peligro)
			# TODO
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
			cuadrox, cuadroy = self.grafico.getCuadroPixel(mousex, mousey)					

			# TODO modificar por cuadrox, cuadrox != None, None
			if cuadrox != None and cuadroy != None and not mouseClic:
				if self.tablero.hayFichaTurno(cuadrox, cuadroy):
					# el mouse esta sobre un cuadro seleccionable
					self.grafico.dibujarCuadroIluminado(cuadrox, cuadroy)
				elif self.tablero.sobreCaminoActual(cuadrox, cuadroy) and self.seleccion:
					# el mouse esta sobre un cuadro del camino de la ficha
					self.grafico.dibujarCuadroIluminado(cuadrox, cuadroy, self.fichaSeleccion)
					# si esa posible jugada puede comer alguna ficha
					if self.tablero.puedeComerFicha(self.fichaSeleccion[0], self.fichaSeleccion[1], cuadrox, cuadroy):
						self.grafico.dibujarAlerta(self.tablero.getListaComerFicha(cuadrox, cuadroy), "roja")
					
			elif cuadrox != None and cuadroy != None and mouseClic:			
				if self.tablero.hayFichaTurno(cuadrox, cuadroy):
					# mouse hizo clic sobre alguna ficha de turno
					self.tablero.setCamino(cuadrox, cuadroy)
					self.grafico.dibujarCaminoIluminado(cuadrox, cuadroy)
					self.seleccion = True
					self.fichaSeleccion = (cuadrox, cuadroy)
					
				elif self.tablero.estaEnCamino(cuadrox, cuadroy) and self.seleccion:
					# mouse hizo clic en una posicion del camino
					self.tablero.mover(self.fichaSeleccion[0], self.fichaSeleccion[1], cuadrox, cuadroy)
					self.seleccion = False
			
					# comprobar el estado del juego
					if self.jugador.jugadorActualEs(Jugador.jugador1) and self.tablero.reyEnEsquina():
						# El rey ha llegado a una esquina
						# TODO
						self.finJuego("jugador2")
					else:
						encasillado = self.tablero.verificarLimitesRey()
						if encasillado == 4:
							# El rey ha sido encasillado, jaquemate
							self.finJuego("jugador1")
						else:
							if encasillado == 3:
								# El rey puede estar en peligro
								if self.tablero.reyEnPeligro():
									# el rey esta en peligro
									self.grafico.dibujarAlerta(self.calculos.getPeligroRey(), "roja")
									self.peligro = True
							else:
								self.peligro = False
							
							esquinas = self.tablero.esquinasRey()
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
								
					self.jugador.switchJugador()
			
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
	
	IMAGENES = [None, None, None]
	
	SUPERFICIE = None
	objFuente = None
	tablero = None
	jugador = None
	config = None
	
	def __init__(self, jugador, tablero, superficie, config):
		self.config = config 
		self.tablero = tablero
		self.jugador = jugador
		self.SUPERFICIE = superficie
		self.LARGO_VENTANA = config["LARGO_VENTANA"]
		self.ANCHO_VENTANA = config["ANCHO_VENTANA"]
		self.TAMANO = config["TAMANO"]
		self.CENTRO = (self.TAMANO-1) / 2
		self.LARGO_CUADRO =  self.LARGO_VENTANA / self.TAMANO
		self.ANCHO_CUADRO =  self.ANCHO_VENTANA / self.TAMANO
		self.MARGEN_X = int(self.ANCHO_CUADRO*0.33)
		self.MARGEN_Y = self.ANCHO_CUADRO + int(self.ANCHO_CUADRO*0.33) 
		
		for i in range(3):
			self.IMAGENES[i] = pygame.image.load(os.path.join(config["CARPETA"], config["IMG"+str(i)]))	
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
	def getCuadroPixel(self, x, y):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordY, coordX = self.coordEsquinaCuadro(cuadrox, cuadroy)
				dibCuadro = pygame.Rect(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO)
				if dibCuadro.collidepoint(x, y):
					return (cuadrox, cuadroy)
		return (None, None)
		
		
	def getColorCuadro(self, x, y):
		if x % 2 == 0:
			if y % 2 == 0:
				return self.config["COLOR1"]
			else:
				return self.config["COLOR2"]
		else:
			if y % 2 == 0:
				return self.config["COLOR2"]
			else:
				return self.config["COLOR1"]
	
	
	def getColorIluminado(self, x, y):
		if x % 2 == 0:
			if y % 2 == 0:
				return self.config["COLOR_CLARO1"]
			else:
				return self.config["COLOR_CLARO2"]
		else:
			if y % 2 == 0:
				return self.config["COLOR_CLARO2"]
			else:
				return self.config["COLOR_CLARO1"]
				
				
	def getColorAlerta(self, alerta):
		if alerta == "roja":
			return self.config["COLOR_ALERTA_ROJA"]
		elif alerta == "verde":
			return self.config["COLOR_ALERTA_VERDE"]
							
		
	""" Dibuja los cuadros del tablero. """	
	def dibujarCuadros(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordX, coordY = self.coordEsquinaCuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self.getColorCuadro(cuadrox, cuadroy), 
					(coordX, coordY, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
	
	""" Dibuja el icono de una ficha. """
	def dibujarFicha(self, cuadrox, cuadroy, fichaEncima=""):
		if self.tablero.getClaseFicha(cuadrox, cuadroy) == "rey" or fichaEncima == "rey":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[0], 
				(int(self.LARGO_CUADRO * 0.8), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.8, 0.75))
				
		elif self.tablero.getClaseFicha(cuadrox, cuadroy) == "sueco" or fichaEncima == "sueco":
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[1], 
				(int(self.LARGO_CUADRO * 0.5), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.5, 0.75))
		
		elif self.tablero.getClaseFicha(cuadrox, cuadroy) == "moscovita" or fichaEncima == "moscovita":
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
			pygame.draw.rect(self.SUPERFICIE, self.getColorAlerta(alerta), 
				(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		else:
			pygame.draw.rect(self.SUPERFICIE, self.getColorIluminado(cuadrox, cuadroy), 
				(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		if fichaEncima != ():
			self.dibujarFicha(cuadrox, cuadroy, self.tablero.getClaseFicha(fichaEncima[0], fichaEncima[1]))
		else:
			self.dibujarFicha(cuadrox, cuadroy)
		
		
	""" Dibuja el camino iluminado de la ficha seleccionada. """	
	def dibujarCaminoIluminado(self, cuadrox, cuadroy):
		camino = self.tablero.getCamino()
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
		color1 = self.config["COLOR_TEXTO"]
		color2 = self.config["COLOR_TEXTO"]
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
		
		self.dibujarTexto(fichasC1, self.config["COLOR_TEXTO"], coordX, coordY)	

		coordX = self.LARGO_VENTANA - self.MARGEN_X - self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = self.ANCHO_VENTANA + self.MARGEN_Y + self.MARGEN_X + int(self.ANCHO_CUADRO / 2)
		
		self.dibujarTexto(fichasC2, self.config["COLOR_TEXTO"], coordX, coordY)
		
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def dibujarVentana(self, jugador, jaque, jaqueMate, peligro, gano=""):
		self.SUPERFICIE.fill(self.config["COLOR_FONDO"])
		pygame.draw.rect(self.SUPERFICIE, self.config["COLOR_MARGEN"], (0, self.ANCHO_CUADRO, (self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_X)), 0)
		
		self.dibujarPanel()
		self.dibujarTextos(jugador.getJugador(), jugador.getFichasComidas(1), jugador.getFichasComidas(2), jaque, jaqueMate, peligro, gano)
		self.dibujarCuadros()
		self.dibujarFichas()




class Tablero(object):
	config = None
	jugador = None
	tablero = []
	camino = []
	
	def __init__(self, config, jugador):
		self.config = config
		self.jugador = jugador
		blanca = config["BLANCA"]
		negra = config["NEGRA"]
		centro = (config["TAMANO"]-1)/2
		for i in range(config["TAMANO"]):
			fila = []
			for j in range(config["TAMANO"]):
				clase = ()
				# asignar ficha
				if i == centro and j == centro:
					ficha = Rey(i, j, ("rey", "moscovita"), config["TAMANO"])
				else:
					if len(blanca) > 0 and (i, j) == blanca[0]:
						clase = ("sueco", "moscovita")
						blanca.remove((i,j))
					elif len(negra) > 0 and (i, j) == negra[0]: 
						clase = ("moscovita", "sueco")
						negra.remove((i,j))
					else:
						clase = ("", "")
					# instancia de variable
					ficha = Ficha(i,j, clase, config["TAMANO"])
				# asociar punteros
				if len(self.tablero) > 0:
					ficha.arr = self.tablero[len(self.tablero)-1][j]
					self.tablero[len(self.tablero)-1][j].aba = ficha
				if len(fila) > 0:
					ficha.izq = fila[len(fila)-1]
					fila[len(fila)-1].der = ficha
				fila.append(ficha)
			self.tablero.append(fila)
		

	def getClaseFicha(self, x, y):
		return self.tablero[x][y].getClase()
		
		
	def hayFichaTurno(self, cuadrox, cuadroy):
		if self.jugador.getJugador() == Jugador.jugador1:
			return self.getClaseFicha(cuadrox, cuadroy) == "moscovita" 
		else:
			return (self.getClaseFicha(cuadrox, cuadroy) == "rey" or self.getClaseFicha(cuadrox, cuadroy) == "sueco")
			
			
	def sobreCaminoActual(self, cuadrox, cuadroy):
		for cuadro in self.camino:
			if cuadro == (cuadrox, cuadroy):
				return True
		return False
		
		
	def puedeComerFicha(self, orx, ory, dx, dy):
		return self.tablero[dx][dy].comer(self.tablero[orx][ory]) != []
		
	
	def getListaComerFicha(self, cuadrox, cuadroy):
		return self.tablero[cuadrox][cuadroy].getListaComer()
	
		
	def setCamino(self, cuadrox, cuadroy):
		self.camino = self.tablero[cuadrox][cuadroy].getCamino()
		
		
	def getCamino(self):
		return self.camino
		
	
	def estaEnCamino(self, x, y):
		return self.camino.count((x, y)) == 1 
		
		
	def mover(self, ox, oy, dx, dy):
		aux = deepcopy(self.tablero[ox][oy])
		self.tablero[ox][oy] = self.tablero[dx][dy]
		self.tablero[dx][dy] = aux
		# solucion ineficiente pero fuc* it
		for i in range(len(self.tablero)):
			for j in range(len(self.tablero[i])):
				self.tablero[i][j].x, self.tablero[i][j].y = i, j
				self.tablero[i][j].arr = self.tablero[i-1][j] if i > 0 else None
				self.tablero[i][j].aba = self.tablero[i+1][j] if i < self.config["TAMANO"]-1 else None
				self.tablero[i][j].izq = self.tablero[i][j-1] if j > 0 else None
				self.tablero[i][j].der = self.tablero[i][j+1] if j < self.config["TAMANO"]-1 else None
		
		
	def reyEnEsquina(self):
		for (x, y) in ((0,0),(0,config["TAMANO"]-1),(config["TAMANO"]-1,0),(config["TAMANO"]-1,config["TAMANO"]-1)):
			if type(self.tablero[x][y]) == Rey:
				return True
		return False
		
	def buscarRey(self):
		for fila in self.tablero:
			for ficha in fila:
				if type(ficha) == Rey:
					return ficha
					
					
	def verificarLimitesRey(self):
		self.buscarRey().verificarLimites()
		
		
	def reyEnPeligro(self):
		self.buscarRey().estaEnPeligro()
					
					
	def esquinasRey(self):
		self.buscarRey().buscarEsquinas()



class Ficha(object):
	der = None
	izq = None
	arr = None
	aba = None
	
	clase = None
	enemigo = None
	
	TAMANO_TABLERO = None
	x = 0;
	y = 0;
	listaComer = []
	
	def __init__(self, i, j, clase, t):
		self.x = i
		self.y = j
		self.TAMANO_TABLERO = t
		self.clase = clase[0] 
		self.enemigo = clase[1]
		
		
	def getClase(self, bool = False):
		return self.clase
		
		
	def getEnemigo(self):
		return self.enemigo
		
		
	def getCoord(self):
		return (self.x, self.y)	
		
	
	def esCamino(self, ficha):
		if self.clase != "":
			return False
		else:
			if(type(ficha) == Rey):
				return True
			else:
				centro = (config["TAMANO"]-1)/2
				return not ((self.x, self.y) == (centro, centro) or (self.x, self.y) == (0, 0) or
				(self.x, self.y) == (0, config["TAMANO"]-1) or (self.x, self.y) == (config["TAMANO"]-1, 0) 
				or (self.x, self.y) == (config["TAMANO"]-1, config["TAMANO"]-1))
				
		
		
	def getCamino(self):
		camino = []
		tmp = self
		
		while tmp.izq != None and tmp.izq.esCamino(self):
			camino.append(tmp.izq.getCoord())
			tmp = tmp.izq
		tmp = self
		while tmp.der != None and tmp.der.esCamino(self):
			camino.append(tmp.der.getCoord())
			tmp = tmp.der
		tmp = self
		while tmp.arr != None and tmp.arr.esCamino(self):
			camino.append(tmp.arr.getCoord())
			tmp = tmp.arr
		tmp = self
		while tmp.aba != None and tmp.aba.esCamino(self):
			camino.append(tmp.aba.getCoord())
			tmp = tmp.aba
		return camino
		
		
	def comer(self, ficha):
		self.listaComer = []
		clase = ficha.getClase(True)
		enemigo = ficha.getEnemigo()
		b = False
		# esquinas
		if (self.x, self.y) == (0, 2) and self.izq.getClase() == enemigo:
			self.listaComer.append((0,1))
		elif (self.x, self.y) == (0, self.TAMANO_TABLERO-3) and self.der.getClase() == enemigo:
			self.listaComer.append((0,self.TAMANO_TABLERO-2))
		elif (self.x, self.y) == (self.TAMANO_TABLERO-1, 2) and self.izq.getClase() == enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-1,1))
		elif (self.x, self.y) == (self.TAMANO_TABLERO-1, self.TAMANO_TABLERO-3) and self.der.getClase() == enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-1,self.TAMANO_TABLERO-2))
		elif (self.x, self.y) == (2, 0) and self.izq != None and self.arr.getClase() == enemigo:
			self.listaComer.append((1,0))
		elif (self.x, self.y) == (self.TAMANO_TABLERO-3, 0) and self.aba.getClase() == enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-2,0))
		elif (self.x, self.y) == (2, self.TAMANO_TABLERO-1) and self.arr.getClase() == enemigo:
			self.listaComer.append((1,self.TAMANO_TABLERO-1))
		elif (self.x, self.y) == (self.TAMANO_TABLERO-3, self.TAMANO_TABLERO-1) and self.aba.getClase() == enemigo:
			self.listaComer.append((self.TAMANO_TABLERO-2,self.TAMANO_TABLERO-1))
			
		# limites
		if self.arr != None and self.arr.getClase() == enemigo and self.arr.arr != None and self.arr.arr.getClase(True) == clase:
			self.listaComer.append(self.arr.getCoord())
		if self.aba != None and self.aba.getClase() == enemigo and self.aba.aba != None and self.aba.aba.getClase(True) == clase:
			self.listaComer.append(self.aba.getCoord())
		if self.izq != None and self.izq.getClase() == enemigo and self.izq.izq != None and self.izq.izq.getClase(True) == clase:
			self.listaComer.append(self.izq.getCoord())
		if self.der != None and self.der.getClase() == enemigo and self.der.der != None and self.der.der.getClase(True) == clase:
			self.listaComer.append(self.der.getCoord())

		return self.listaComer
		
	
	def getListaComer(self):
		return self.listaComer
		
		
class Rey(Ficha):
	claseRey = None
	enemigo = None
	
	def __init__(self, i, j, clase, t):
		self.claseRey = clase[0]
		self.enemigo = clase[1]
		Ficha.__init__(self, i, j, ("sueco","moscovita"), t)
	
	
	def getClase(self, general = False):
		return self.clase if general else self.claseRey

	
	def verificarLimites(self):
		c = 0
		if self.arr != None and self.arr.getClase() == self.enemigo:
			c += 1
		if self.aba != None and self.aba.getClase() == self.enemigo:
			c += 1
		if self.izq != None and self.izq.getClase() == self.enemigo:
			c += 1
		if self.der != None and self.der.getClase() == self.enemigo:
			c += 1
		return c

	def estaEnPeligro(self):
		limite = ()
		for l in ((self.arr, 1), (self.aba, 2), (self.izq, 3), (self.der, 4)):
			if l[0].getClase() != self.enemigo:
				limite = l
		
		if limite[1] == 1:
			while(limite[0] != None):
				if limite[0].getClase() == self.enemigo:
					return True
				else:
					limite[0] = limite[0].arr
		elif limite[1] == 2:
			while(limite[0] != None):
				if limite[0].getClase() == self.enemigo:
					return True
				else:
					limite[0] = limite[0].aba
		elif limite[1] == 3:
			while(limite[0] != None):
				if limite[0].getClase() == self.enemigo:
					return True
				else:
					limite[0] = limite[0].izq
		elif limite[1] == 4:
			while(limite[0] != None):
				if limite[0].getClase() == self.enemigo:
					return True
				else:
					limite[0] = limite[0].der
		return False
		
		
	def buscarEsquinas(self):
		c = 0
		tmp = self.arr
		while tmp != None and tmp.getClase() == self.enemigo:
			tmp = tmp.arr
		c += 1 if tmp == None else 0
		tmp = self.aba
		while tmp != None and tmp.getClase() == self.enemigo:
			tmp = tmp.aba
		c += 1 if tmp == None else 0
		tmp = self.izq
		while tmp != None and tmp.getClase() == self.enemigo:
			tmp = tmp.izq
		c += 1 if tmp == None else 0
		tmp = self.der
		while tmp != None and tmp.getClase() == self.enemigo:
			tmp = tmp.der
		c += 1 if tmp == None else 0
		return c
		
		
class Jugador(object):
	jugador1 = "jugador1"
	jugador2 = "jugador2"
	fichasComidas1 = 0
	fichasComidas2 = 0
	jugadorActual = None
	
	""" Constructor de la clase. """
	def __init__(self):
		self.jugadorActual = self.jugador1
		
		
	""" Cambia el turno. """	
	def switchJugador(self):
		if self.jugadorActual == self.jugador1:
			self.jugadorActual = self.jugador2
		else:
			self.jugadorActual = self.jugador1
	
	
	""" Devuelve el turno actual."""	
	def getJugador(self):
		return self.jugadorActual

		
	def jugadorActualEs(self, jugador):
		return self.jugadorActual == jugador
		
		
	""" Pone el turno por defecto. """
	def nuevoJuego(self):
		self.jugadorActual = self.jugador1
		
		
	def getFichasComidas(self, j):
		return self.fichasComidas1 if j == 1 else self.fichasComidas2
	
	
	def getClaseTurno(self):
		return ("moscovita", "sueco") if self.jugadorActual == self.jugador1 else ("sueco", "moscovita")
		
		
		
if __name__ == '__main__':
	config = {}
	execfile("settings2.config", config) 
	main = Main(config)
	main.iniciar()
