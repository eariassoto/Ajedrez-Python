#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, pygame, os
from pygame.locals import *
from copy import deepcopy

################################################## Main ###################################################
#                       Maneja los eventos del mouse y el loop principal del juego                        #
###########################################################################################################
class Main:	

	""" Constructor """
	def __init__(self, config):
	
		# iniciar el modulo pygame y el objeto FPS.
		pygame.init()
		FPSCLOCK = pygame.time.Clock()
		
		# velocidad promedio de cuadros por segundo.
		FPS = 114
				
		# almacenaran las instancias de los objetos.
		jugador = Jugador()
		tablero = Tablero(jugador)
		grafico = Grafico(jugador, tablero)
		
		
		
		# boolean para controlar estado de ficha seleccionada.
		seleccion = False
		
		# eventos que puede disparar el usuario
		CAMBIO_TURNO = pygame.USEREVENT+1
		JAQUE = pygame.USEREVENT+2
		JAQUE_MATE = pygame.USEREVENT+3
		REY_PELIGRO = pygame.USEREVENT+4
		GAME_OVER = pygame.USEREVENT+5
		
		
		# sirve para almacenar la posicion de la ficha seleccionada por el clic
		fichaSeleccion = ""
		
		# almacenan las coordenadas del mouse
		mousex = 0 
		mousey = 0 
		
		
		gameOver = False
		while not gameOver: # loop principal del juego
		
			mouseClic = False
			
			# dibujar ventana.
			grafico.dibujarVentana()
			if seleccion:
				grafico.dibujarCaminoIluminado(None, None)
			"""# TODO
			if self.jaque or self.jaqueMate:
				self.grafico.dibujarAlerta(self.calculos.getEsquinas(), "verde")
			if self.peligro:
				self.grafico.dibujarAlerta(self.calculos.getPeligroRey(), "roja")
			if self.seleccion:
				self.grafico.dibujarCaminoIluminado(None, None)
			"""	
			# manejo de eventos.
			for evento in pygame.event.get():
				if evento.type == QUIT or (evento.type == KEYUP and evento.key == K_ESCAPE):
					pygame.quit()
					os._exit(0)
				elif evento.type == GAME_OVER:
					gameOver = True
				else:
					if not mouseClic and evento.type == MOUSEMOTION:
						mousex, mousey = evento.pos 
					elif not mouseClic and evento.type == MOUSEBUTTONUP:
						mousex, mousey = evento.pos
						mouseClic = True	
					elif evento.type == CAMBIO_TURNO:
						jugador.cambioTurno()
			
			if not gameOver:
				# comprobar si el mouse esta actualmente en un cuadro
				cuadrox, cuadroy = grafico.getCuadroPixel(mousex, mousey)					

				if (cuadrox, cuadroy) != (None, None) and not mouseClic:
					if tablero.hayFichaTurno(cuadrox, cuadroy):
						# el mouse esta sobre un cuadro seleccionable
						grafico.dibujarCuadroIluminado(cuadrox, cuadroy)
					elif tablero.sobreCaminoActual(cuadrox, cuadroy) and seleccion:
						# el mouse esta sobre un cuadro del camino de la ficha
						grafico.dibujarCuadroIluminado(cuadrox, cuadroy, fichaSeleccion)
						# si esa posible jugada puede comer alguna ficha
						if tablero.puedeComerFicha(fichaSeleccion[0], fichaSeleccion[1], cuadrox, cuadroy):
							grafico.dibujarAlerta(tablero.getListaComerFicha(cuadrox, cuadroy), "roja")
						
				elif cuadrox != None and cuadroy != None and mouseClic:			
					if tablero.hayFichaTurno(cuadrox, cuadroy):
						# mouse hizo clic sobre alguna ficha de turno
						tablero.setCamino(cuadrox, cuadroy)
						grafico.dibujarCaminoIluminado(cuadrox, cuadroy)
						seleccion = True
						fichaSeleccion = (cuadrox, cuadroy)
						
					elif tablero.estaEnCamino(cuadrox, cuadroy) and seleccion:
						# mouse hizo clic en una posicion del camino
						tablero.mover(fichaSeleccion[0], fichaSeleccion[1], cuadrox, cuadroy)
						seleccion = False			
						evento = pygame.event.Event(CAMBIO_TURNO)
						pygame.event.post(evento)
						
				tablero.comprobarEstado()
			
			pygame.display.update()	
			FPSCLOCK.tick(FPS)	
	
	
	""" Animaciones para el fin del juego 
	def finJuego(self, ganador):
		self.grafico.dibujarVentana()
		pygame.display.update()
		pygame.time.wait(5000)
		self.logico.resetearTablero()
		self.seleccion = False
		self.jaque = False
		self.jaqueMate = False
		self.peligro = False
		self.fichaSeleccion = ""
		self.jugador.nuevoJuego()"""
		
	
################################################ Grafico ##################################################
#                                 Maneja la parte gráfica del programa                                    # 
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
	
	def __init__(self, jugador, tablero):
		self.tablero = tablero
		self.jugador = jugador
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
		

	""" Convierte las coordenadas del centro del cuadro a una coordenada de pixel. 
	"""
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
		
		
	""" Devuelve el color respectivo de una posicion del tablero.
	"""	
	def getColorCuadro(self, x, y):
		if x % 2 == 0:
			if y % 2 == 0:
				return config["COLOR1"]
			else:
				return config["COLOR2"]
		else:
			if y % 2 == 0:
				return config["COLOR2"]
			else:
				return config["COLOR1"]
	
	
	""" Devuelve el respectivo color con el efecto de iluminacion
	de un cuadro del tablero.
	"""
	def getColorIluminado(self, x, y):
		if x % 2 == 0:
			if y % 2 == 0:
				return config["COLOR_CLARO1"]
			else:
				return config["COLOR_CLARO2"]
		else:
			if y % 2 == 0:
				return config["COLOR_CLARO2"]
			else:
				return config["COLOR_CLARO1"]
				
				
	def getColorAlerta(self, alerta):
		if alerta == "roja":
			return config["COLOR_ALERTA_ROJA"]
		elif alerta == "verde":
			return config["COLOR_ALERTA_VERDE"]
							
		
	""" Dibuja los cuadros del tablero. """	
	def dibujarCuadros(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordX, coordY = self.coordEsquinaCuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self.getColorCuadro(cuadrox, cuadroy), 
					(coordX, coordY, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
	
	""" Dibuja el icono de una ficha. """
	def dibujarFicha(self, cuadrox, cuadroy, fichaEncima=None):
		if self.tablero.getTipoFicha(cuadrox, cuadroy) == Rey or fichaEncima == Rey:
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[0], 
				(int(self.LARGO_CUADRO * 0.8), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.8, 0.75))
				
		elif self.tablero.getTipoFicha(cuadrox, cuadroy) == Blanca or fichaEncima == Blanca:
			iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[1], 
				(int(self.LARGO_CUADRO * 0.5), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(iconoParaDibujar, self.coordFichaEnCuadro(cuadrox, cuadroy, 0.5, 0.75))
		
		elif self.tablero.getTipoFicha(cuadrox, cuadroy) == Negra or fichaEncima == Negra:
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
			self.dibujarFicha(cuadrox, cuadroy, self.tablero.getTipoFicha(fichaEncima[0], fichaEncima[1]))
		else:
			self.dibujarFicha(cuadrox, cuadroy)
		
		
	""" Dibuja el camino iluminado de la ficha seleccionada. 
	"""	
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
	
	
	""" Dibuja una ficha (sirve para las fichas del panel. 
	"""
	def dibujarFichaIndividual(self, i, coordX, coordY):
		iconoParaDibujar = pygame.transform.smoothscale(self.IMAGENES[i], 
			(int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
		self.SUPERFICIE.blit(iconoParaDibujar, (coordX, coordY))
	
	
	""" Dibuja los iconos de los paneles superior e inferior del tablero de juego. 
	"""
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
		
		
	""" Dibuja una hilera en la pantalla. 
	"""
	def dibujarTexto(self, texto, color, coordx, coordy):
		superfTexto = self.objFuente.render(texto, True, color)
		rectTexto = superfTexto.get_rect()
		rectTexto.left = coordx
		rectTexto.centery = coordy
		self.SUPERFICIE.blit(superfTexto, rectTexto)
	
	
	""" Dibuja todos los textos de la pantalla. """
	def dibujarMensaje(self, t, j):
		color = config["COLOR_TEXTO"]
		texto = t
		
		coordX = self.MARGEN_X + self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int(self.ANCHO_CUADRO / 2) if j == Jugador.jugador1 else self.ANCHO_VENTANA + self.MARGEN_Y + self.MARGEN_X + int(self.ANCHO_CUADRO / 2)
		self.dibujarTexto(texto, color, coordX, coordY)

		
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def dibujarVentana(self):
		self.SUPERFICIE.fill(config["COLOR_FONDO"])
		pygame.draw.rect(self.SUPERFICIE, config["COLOR_MARGEN"], (0, self.ANCHO_CUADRO, (self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_X)), 0)
		
		self.dibujarPanel()
		j = self.jugador.getJugador()
		turno = "Jugador 1, tu turno." if j == Jugador.jugador1 else "Jugador 2, tu turno"
		self.dibujarMensaje(turno, j)
		self.dibujarCuadros()
		self.dibujarFichas()


################################################ Tablero ##################################################
#  Maneja la representacion del tablero, crea una cantidad de ficha y las asocia entre ellas, para        #
#  referenciarlas posteriormente mantiene una matriz de punteros a las fichas                             # 
###########################################################################################################
class Tablero(object):
	jugador = None
	tablero = []
	camino = []
	
	""" Crea las fichas del tablero de juego 
	"""
	def __init__(self, jugador):
		rey = None
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
					ficha = Rey(i, j)
					rey = ficha
				else:
					if len(blanca) > 0 and (i, j) == blanca[0]:
						ficha = Blanca(i, j)
						blanca.remove((i,j))
					elif len(negra) > 0 and (i, j) == negra[0]: 
						ficha = Negra(i, j)
						negra.remove((i,j))
					else:
						ficha = Ficha(i, j)
				# asociar punteros
				if len(self.tablero) > 0:
					ficha.arr = self.tablero[len(self.tablero)-1][j]
					self.tablero[len(self.tablero)-1][j].aba = ficha
				if len(fila) > 0:
					ficha.izq = fila[len(fila)-1]
					fila[len(fila)-1].der = ficha
				fila.append(ficha)
			self.tablero.append(fila)
		
	
	def getTipoFicha(self, x, y):
		return type(self.tablero[x][y])
		
		
	def hayFichaTurno(self, cuadrox, cuadroy):
		if self.jugador.getJugador() == Jugador.jugador1:
			return type(self.tablero[cuadrox][cuadroy]) == Negra 
		else:
			return (type(self.tablero[cuadrox][cuadroy]) == Blanca or type(self.tablero[cuadrox][cuadroy]) == Rey)
			
			
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
		
		
	def comerFichas(self, lista):
		for x, y in lista:
			self.tablero[x][y] = Ficha(x, y)
		
		
	""" Reacomoda los punteros de las fichas, lo hace de una forma ineficiente
	"""	
	def reacomodarPunteros(self):
		for i in range(len(self.tablero)):
			for j in range(len(self.tablero[i])):
				self.tablero[i][j].x, self.tablero[i][j].y = i, j
				self.tablero[i][j].arr = self.tablero[i-1][j] if i > 0 else None
				self.tablero[i][j].aba = self.tablero[i+1][j] if i < config["TAMANO"]-1 else None
				self.tablero[i][j].izq = self.tablero[i][j-1] if j > 0 else None
				self.tablero[i][j].der = self.tablero[i][j+1] if j < config["TAMANO"]-1 else None
				
				
	def mover(self, ox, oy, dx, dy):
		aux = deepcopy(self.tablero[ox][oy])
		self.tablero[ox][oy] = self.tablero[dx][dy]
		self.tablero[dx][dy] = aux
		self.reacomodarPunteros()
		if self.tablero[dx][dy].comer(self.tablero[dx][dy]) != []:
			self.comerFichas(self.tablero[dx][dy].getListaComer())
			self.reacomodarPunteros()		
		
		
	def comprobarEstado(self):
		# primero comprobar si el rey ya ha llegado a una esquina
		coord = rey.getCoord()
		fin = config["TAMANO"]-1
		if coord == (0,0) or coord == (0, fin) or coord == (fin, 0) or coord == (fin, fin):
			evento = pygame.event.Event(GAME_OVER)
			jugador.setGanador(Jugador.jugador2)
		else:
			# buscar cuantos lados del rey estan asediados por fichas enemigas
			limitesRey = rey.getLimites()
			if limitesRey == 4:
				evento = pygame.event.Event(GAME_OVER)
				jugador.setGanador(Jugador.jugador1)
			else:
				if limitesRey == 3:
					pass
				
	

		
		
	def reyEnPeligro(self):
		self.buscarRey().estaEnPeligro()
					
					
	def esquinasRey(self):
		self.buscarRey().buscarEsquinas()


################################################# Ficha ###################################################
#  Clase base para modelar el comportamiento de las fichas, en ejecución esta va a ser un espacio en      #
#  blanco.                                                                                                #
###########################################################################################################
class Ficha(object):
	
	# punteros a las fichas vecinas
	der = None
	izq = None
	arr = None
	aba = None
	
	# tipo de ficha aliada y enemiga (las clases hijas lo determinan)
	aliado = None
	enemigo = None
	
	#posicion de la ficha en el tablero (y matriz punteros)
	x, y = 0, 0
	
	TAMANO_TABLERO = None
	
	# lista con coordenadas de fichas a las cuales puede comer
	listaComer = []
	
	""" Construye una nueva ficha 
	"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.TAMANO_TABLERO = config["TAMANO"]
	
	""" Devuelve las coordenadas de la ficha
	"""
	def getCoord(self):
		return (self.x, self.y)
	
	""" Determina si una ficha puede formar parte del 
	camino de otra. El parametro ficha indica quien 
	hizo el llamado, esto para determinar si dejo pasar
	el centro o las esquinas
	"""
	def esCamino(self, ficha):
		if type(self) == Blanca or type(self) == Negra or type(self) == Rey:
			return False
		else:
			if type(ficha) == Rey:
				return True
			else:
				centro = (config["TAMANO"]-1)/2
				return not ((self.x, self.y) == (centro, centro) or (self.x, self.y) == (0, 0) or
				(self.x, self.y) == (0, config["TAMANO"]-1) or (self.x, self.y) == (config["TAMANO"]-1, 0) 
				or (self.x, self.y) == (config["TAMANO"]-1, config["TAMANO"]-1))

				
	""" Calcula el camino que puede recorrer la ficha
	"""	
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
		
		
	""" Modifica la lista de comer almacenando las posibilidades
	"""
	def comer(self, ficha):
		listaComer = []
		x, y = self.x, self.y
		aliado = ficha.aliado
		enemigo = ficha.enemigo
		
		# esquinas
		if (x, y) == (0, 2) and type(self.izq) == enemigo:
			listaComer.append((0,1))
		elif (x, y) == (0, self.TAMANO_TABLERO-3) and type(self.der) == enemigo:
			listaComer.append((0,self.TAMANO_TABLERO-2))
		elif (x, y) == (self.TAMANO_TABLERO-1, 2) and type(self.izq) == enemigo:
			listaComer.append((self.TAMANO_TABLERO-1,1))
		elif (x, y) == (self.TAMANO_TABLERO-1, self.TAMANO_TABLERO-3) and type(self.der) == enemigo:
			listaComer.append((self.TAMANO_TABLERO-1,self.TAMANO_TABLERO-2))
		elif (self.x, self.y) == (2, 0) and self.izq != None and type(self.arr) == enemigo:
			listaComer.append((1,0))
		elif (x, y) == (self.TAMANO_TABLERO-3, 0) and type(self.aba) == enemigo:
			listaComer.append((self.TAMANO_TABLERO-2,0))
		elif (x, y) == (2, self.TAMANO_TABLERO-1) and type(self.arr) == enemigo:
			listaComer.append((1,self.TAMANO_TABLERO-1))
		elif (x, y) == (self.TAMANO_TABLERO-3, self.TAMANO_TABLERO-1) and type(self.aba) == enemigo:
			listaComer.append((self.TAMANO_TABLERO-2,self.TAMANO_TABLERO-1))
		
		#limites
		# uso el isinstance() para que las blancas reconozcan al rey pero no a la inversa
		if type(self.arr) == enemigo and isinstance(self.arr.arr, aliado):
			listaComer.append(self.arr.getCoord())
		if type(self.aba) == enemigo and isinstance(self.aba.aba, aliado):
			listaComer.append(self.aba.getCoord())
		if type(self.izq) == enemigo and isinstance(self.izq.izq, aliado):
			listaComer.append(self.izq.getCoord())
		if type(self.der) == enemigo and isinstance(self.der.der, aliado):
			listaComer.append(self.der.getCoord())
		
		self.listaComer = listaComer
		return self.listaComer
		
		
	""" Devuelve la lista de fichas para comer
	"""	
	def getListaComer(self):
		return self.listaComer
	
	
################################################# Negra ###################################################
#  Clase que hereda de Ficha y representa las fichas del jugador 1                                        #
###########################################################################################################	
class Negra(Ficha):
	def __init__(self, i, j):
		self.aliado = Negra
		self.enemigo = Blanca
		Ficha.__init__(self, i, j)
	

################################################# Blanca ##################################################
#  Clase que hereda de Ficha y representa las fichas del jugador 2, a excepción del rey                   #
###########################################################################################################	
class Blanca(Ficha):
	def __init__(self, i, j):
		self.aliado = Blanca
		self.enemigo = Negra
		Ficha.__init__(self, i, j)
		

################################################## Rey ####################################################
#  Hereda de Ficha, agrega funcionalidades específica de la ficha del rey.                                # 
###########################################################################################################		
class Rey(Blanca):
	
	def __init__(self, i, j):
		self.aliado = Blanca
		self.enemigo = Negra
		Blanca.__init__(self, i, j)

	
	def getLimites(self):
		c = 0
		centro = (config["TAMANO"]-1) / 2
		fin = config["TAMANO"]-1
		restricciones = ((centro, centro), (0,0), (fin, 0), (0, fin), (fin, fin))
		
		if self.arr == None or type(self.arr) == self.enemigo:
			c += 1
		elif type(self.arr) == self.aliado:
			if type(self.arr.arr) == self.enemigo:
				c += 1
		elif restricciones.count(self.arr.getCoord()) == 1:
			c += 1
			
		if self.aba == None or type(self.aba) == self.enemigo:
			c += 1
		elif type(self.aba) == self.aliado:
			if type(self.aba.aba) == self.enemigo:
				c += 1
		elif restricciones.count(self.aba.getCoord()) == 1:
			c += 1

		if self.izq == None or type(self.izq) == self.enemigo:
			c += 1
		elif type(self.izq) == self.aliado:
			if type(self.izq.izq) == self.enemigo:
				c += 1
		elif restricciones.count(self.izq.getCoord()) == 1:
			c += 1
			
		if self.der == None or type(self.der) == self.enemigo:
			c += 1
		elif type(self.der) == self.aliado:
			if type(self.der.der) == self.enemigo:
				c += 1
		elif restricciones.count(self.der.getCoord()) == 1:
			c += 1
			
		print c
		return c

	def estaEnPeligro(self):
		limite = ()
		for l in ((self.arr, 1), (self.aba, 2), (self.izq, 3), (self.der, 4)):
			if type(l[0]) == self.enemigo:
				limite = l
		
		if limite[1] == 1:
			while(limite[0] != None):
				if type(limite[0]) == self.enemigo:
					return True
				else:
					limite[0] = limite[0].arr
		elif limite[1] == 2:
			while(limite[0] != None):
				if type(limite[0]) == self.enemigo:
					return True
				else:
					limite[0] = limite[0].aba
		elif limite[1] == 3:
			while(limite[0] != None):
				if type(limite[0]) == self.enemigo:
					return True
				else:
					limite[0] = limite[0].izq
		elif limite[1] == 4:
			while(limite[0] != None):
				if type(limite[0]) == self.enemigo:
					return True
				else:
					limite[0] = limite[0].der
		
		return False
		
		
	def buscarEsquinas(self):
		c = 0
		tmp = self.arr
		while tmp != None and type(tmp) == self.enemigo:
			tmp = tmp.arr
		c += 1 if tmp == None else 0
		tmp = self.aba
		while tmp != None and type(tmp) == self.enemigo:
			tmp = tmp.aba
		c += 1 if tmp == None else 0
		tmp = self.izq
		while tmp != None and type(tmp) == self.enemigo:
			tmp = tmp.izq
		c += 1 if tmp == None else 0
		tmp = self.der
		while tmp != None and type(tmp) == self.enemigo:
			tmp = tmp.der
		c += 1 if tmp == None else 0
		return c
		

################################################ Jugador ##################################################
#  Mantiene el estado de los turnos durante el juego                                                      # 
###########################################################################################################		
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
	def cambioTurno(self):
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
	
	
	
		
if __name__ == '__main__':
	config = {}
	execfile("settings.config", config) 
	main = Main(config)
	main.iniciar()
