#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" autor: Emmanuel Arias Soto
	emmanuel1412@gmail.com
	version 1.0 27/12/2013
"""
import random
import os
import pygame
from pygame.locals import *
from copy import deepcopy
from copy import copy

################################################## Main ###################################################
#                       Maneja los eventos del mouse y el loop principal del juego                        #
###########################################################################################################
class Main:	

	""" Constructor """
	def __init__(self, config):
	
		pygame.init() # inicia el modulo pygame
		FPSCLOCK = pygame.time.Clock()
				
		# instancias de clase
		jugador = Jugador()
		tablero = Tablero(jugador)
		grafico = Grafico(jugador, tablero)
		
		seleccion = False # indica si algun jugador ha selecconado una ficha
			
		fichaSeleccion = "" # almacena la posicion de la ficha seleccionada 
		
		mousex, mousey = 0, 0 # coordenadas del mouse 

		while True: # loop principal del juego
		
			mouseClic = False
			
			grafico._dibujar_ventana() # dibuja la ventana
			if seleccion:
				grafico._dibujar_camino() # pinta el camino que la ficha puede recorrer
			
			
			for evento in pygame.event.get(): # maneja los evento en cola
				if evento.type == QUIT or (evento.type == KEYUP and evento.key == K_ESCAPE):
					# jugador ha terminado el programa
					pygame.quit()
					os._exit(0)
				elif evento.type == pygame.USEREVENT+config["GAME_OVER"]:
					# termina el juego
					grafico._dibujar_ventana()
					pygame.display.update()	
					pygame.time.wait(5000)
					tablero._generar_tablero()
					jugador._set_nuevo_juego()
					seleccion = False
					grafico._dibujar_ventana()
					pygame.display.update()
									
				elif not mouseClic and evento.type == MOUSEMOTION:
					mousex, mousey = evento.pos # mouse se movio
				elif not mouseClic and evento.type == MOUSEBUTTONUP:
					mousex, mousey = evento.pos # mouse hizo clic
					mouseClic = True	
				elif evento.type == pygame.USEREVENT+config["CAMBIO_TURNO"]:
					jugador._cambiar_turno() # hay que cambiar turno
				elif evento.type == pygame.USEREVENT+config["REY_PELIGRO"]:
					grafico._dibujar_alerta(evento.dict["alerta"], "roja") # el rey esta en peligro
				elif evento.type == pygame.USEREVENT+config["JAQUE"]:
					grafico._dibujar_alerta(evento.dict["alerta"], "verde") # el rey hizo jaque
						
			cuadrox, cuadroy = grafico._hay_pixel_en_cuadro(mousex, mousey) # comprobar si el mouse esta en un cuadro					

			if (cuadrox, cuadroy) != (None, None) and not mouseClic:
				if tablero._hay_ficha_turno(cuadrox, cuadroy):
					# el mouse esta sobre un cuadro seleccionable
					grafico._dibujar_cuadro_iluminado(cuadrox, cuadroy)
				elif tablero._esta_sobre_camino(cuadrox, cuadroy) and seleccion:
					# el mouse esta sobre un cuadro del camino de la ficha
					grafico._dibujar_cuadro_iluminado(cuadrox, cuadroy, fichaSeleccion)
					# si esa posible jugada puede comer alguna ficha
					if tablero._puede_comer(fichaSeleccion[0], fichaSeleccion[1], cuadrox, cuadroy):
						grafico._dibujar_alerta(tablero._get_lista_comer(cuadrox, cuadroy), "roja")
					
			elif cuadrox != None and cuadroy != None and mouseClic:			
				if tablero._hay_ficha_turno(cuadrox, cuadroy):
					# mouse hizo clic sobre alguna ficha de turno
					tablero._set_camino(cuadrox, cuadroy)
					grafico._dibujar_camino(cuadrox, cuadroy)
					seleccion = True
					fichaSeleccion = (cuadrox, cuadroy)
					
				elif tablero._esta_sobre_camino(cuadrox, cuadroy) and seleccion:
					# mouse hizo clic en una posicion del camino
					tablero.mover(fichaSeleccion[0], fichaSeleccion[1], cuadrox, cuadroy)
					seleccion = False			
					evento = pygame.event.Event(pygame.USEREVENT+config["CAMBIO_TURNO"])
					pygame.event.post(evento)
			tablero._comprobar_estado_tablero()
			
			pygame.display.update()	
			FPSCLOCK.tick(114)	
	
		
		
	
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
	fuente = None
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
		
		self.fuente = pygame.font.Font('freesansbold.ttf', 32)
		
		self.SUPERFICIE = pygame.display.set_mode(((self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_Y)))
		pygame.display.set_caption('Ajedrez Vikingo')
		
		
	""" Indicado un cuadro (cuadrox, cuadroy) se devuelve
	la coordenada en px de la esquina superior izquierda del mismo.
	"""
	def _esquina_cuadro(self, cuadrox, cuadroy):
		coordX = self.MARGEN_X + (cuadroy * self.ANCHO_CUADRO)
		coordY = self.MARGEN_Y + (cuadrox * self.LARGO_CUADRO)
		return (coordX, coordY)
		

	""" Usando las coordenadas de la esquina superior de un cuadro
	calcula el centro del mismo y lo devuelve.
	"""
	def _centro_cuadro(self, cuadrox, cuadroy, escalax, escalay):
		coordX, coordY = self._esquina_cuadro(cuadrox, cuadroy)
		coordX += int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * escalax)) / 2)
		coordY += int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * escalay)) / 2)
		return (coordX, coordY)
		

	""" Recorre un tablero "imaginario" y devuelve una posicion si la coordenada
	en pixel esta dentro de algun cuadro, en caso contrario devuelve la
	tupla (None, None).
	""" 	
	def _hay_pixel_en_cuadro(self, x, y):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordY, coordX = self._esquina_cuadro(cuadrox, cuadroy)
				dibujo_cuadro = pygame.Rect(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO)
				if dibujo_cuadro.collidepoint(x, y):
					return (cuadrox, cuadroy)
		return (None, None)
		
		
	""" Devuelve el color respectivo de una posicion del tablero."""	
	def _get_color_cuadro(self, x, y):
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
	def _get_iluminado_cuadro(self, x, y):
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
				
	
	"""	Devuelve el color de alerta. """
	def _get_color_alerta(self, alerta):
		if alerta == "roja":
			return config["COLOR_ALERTA_ROJA"]
		elif alerta == "verde":
			return config["COLOR_ALERTA_VERDE"]
							
		
	""" Dibuja los cuadros del tablero. """	
	def _dibujar_cuadros_tablero(self):
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				coordX, coordY = self._esquina_cuadro(cuadrox, cuadroy)
				pygame.draw.rect(self.SUPERFICIE, self._get_color_cuadro(cuadrox, cuadroy), 
					(coordX, coordY, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		
	
	""" Dibuja el icono de una ficha. """
	def _dibujar_icono_ficha(self, cuadrox, cuadroy, fichaEncima=None):
		if self.tablero._get_tipo_ficha(cuadrox, cuadroy) == Rey or fichaEncima == Rey:
			icono_para_dibujar = pygame.transform.smoothscale(self.IMAGENES[0], 
				(int(self.LARGO_CUADRO * 0.8), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(icono_para_dibujar, self._centro_cuadro(cuadrox, cuadroy, 0.8, 0.75))
				
		elif self.tablero._get_tipo_ficha(cuadrox, cuadroy) == Blanca or fichaEncima == Blanca:
			icono_para_dibujar = pygame.transform.smoothscale(self.IMAGENES[1], 
				(int(self.LARGO_CUADRO * 0.5), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(icono_para_dibujar, self._centro_cuadro(cuadrox, cuadroy, 0.5, 0.75))
		
		elif self.tablero._get_tipo_ficha(cuadrox, cuadroy) == Negra or fichaEncima == Negra:
			icono_para_dibujar = pygame.transform.smoothscale(self.IMAGENES[2], 
				(int(self.LARGO_CUADRO * 0.5), int(self.ANCHO_CUADRO * 0.75)))
			self.SUPERFICIE.blit(icono_para_dibujar, self._centro_cuadro(cuadrox, cuadroy, 0.5, 0.75))	
		
		
	""" Dibuja las fichas del tablero. """
	def _dibujar_icono_fichas(self):		
		for cuadrox in range(self.TAMANO):
			for cuadroy in range(self.TAMANO):
				self._dibujar_icono_ficha(cuadrox, cuadroy)
					

	""" Vuelve a dibujar el cuadro señalado por los parámetros pero de un color más claro. """
	def _dibujar_cuadro_iluminado(self, cuadrox, cuadroy, fichaEncima=(), alerta=""):
		coordY, coordX = self._esquina_cuadro(cuadrox, cuadroy)
		if alerta != "":
			pygame.draw.rect(self.SUPERFICIE, self._get_color_alerta(alerta), 
				(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		else:
			pygame.draw.rect(self.SUPERFICIE, self._get_iluminado_cuadro(cuadrox, cuadroy), 
				(coordY, coordX, self.LARGO_CUADRO, self.ANCHO_CUADRO))
		if fichaEncima != ():
			self._dibujar_icono_ficha(cuadrox, cuadroy, self.tablero._get_tipo_ficha(fichaEncima[0], fichaEncima[1]))
		else:
			self._dibujar_icono_ficha(cuadrox, cuadroy)
		
		
	""" Dibuja el camino iluminado de la ficha seleccionada. """	
	def _dibujar_camino(self, cuadrox = None, cuadroy = None):
		camino = self.tablero._get_camino()
		if cuadrox != None and cuadroy != None: 
			self._dibujar_cuadro_iluminado(cuadrox, cuadroy)
		for cuadro in camino:
			self._dibujar_cuadro_iluminado(cuadro[0], cuadro[1])
		
		
	""" Dibuja un color de alerta en los cuadros indicados por 
	la lista retornada por logico.getComer().
	"""
	def _dibujar_alerta(self, listaCuadros, alerta):
		for cuadro in listaCuadros:
			self._dibujar_cuadro_iluminado(cuadro[0], cuadro[1], (), alerta)
	
	
	""" Dibuja una ficha (sirve para las fichas del panel. """
	def _dibujar_icono(self, i, coordX, coordY):
		icono_para_dibujar = pygame.transform.smoothscale(self.IMAGENES[i], 
			(int(self.LARGO_CUADRO * 0.50), int(self.ANCHO_CUADRO * 0.75)))
		self.SUPERFICIE.blit(icono_para_dibujar, (coordX, coordY))
	
	
	""" Dibuja los iconos de los paneles superior e inferior del tablero de juego. """
	def _dibujar_panel(self):
		coordX = self.MARGEN_X + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * 0.75)) / 2)
		
		self._dibujar_icono(2, coordX, coordY)
		
		coordX = self.MARGEN_X + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = (self.ANCHO_VENTANA + self.MARGEN_X + self.MARGEN_Y) + int((self.LARGO_CUADRO - int(self.LARGO_CUADRO * 0.75)) / 2)
		
		self._dibujar_icono(1, coordX, coordY)

		
	""" Dibuja una hilera en la pantalla. """
	def _dibujar_texto(self, texto, color, coordx, coordy):
		superficie_texto = self.fuente.render(texto, True, color)
		rectangulo_texto = superficie_texto.get_rect()
		rectangulo_texto.left = coordx
		rectangulo_texto.centery = coordy
		self.SUPERFICIE.blit(superficie_texto, rectangulo_texto)
	
	
	""" Dibuja todos los textos de la pantalla. """
	def _dibujar_mensaje(self, t, j, c):
		color = c
		texto = t
		
		coordX = self.MARGEN_X + self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int(self.ANCHO_CUADRO / 2) if j == Jugador.jugador1 else self.ANCHO_VENTANA + self.MARGEN_Y + self.MARGEN_X + int(self.ANCHO_CUADRO / 2)
		self._dibujar_texto(texto, color, coordX, coordY)

		
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def _dibujar_ventana(self):
		self.SUPERFICIE.fill(config["COLOR_FONDO"])
		pygame.draw.rect(self.SUPERFICIE, config["COLOR_MARGEN"], (0, self.ANCHO_CUADRO, (self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_X)), 0)
		
		self._dibujar_panel()
		
		if self.jugador._hay_ganador():
			j = self.jugador._get_ganador()
			texto = "Jugador 1, ganaste." if j == Jugador.jugador1 else "Jugador 2, ganaste."
			color = config["COLOR_ALERTA_VERDE"]
		else:
			j = self.jugador._get_jugador()
			texto = "Jugador 1, tu turno." if j == Jugador.jugador1 else "Jugador 2, tu turno"
			color = config["COLOR_TEXTO"]
		self._dibujar_mensaje(texto, j, color)
		self._dibujar_cuadros_tablero()
		self._dibujar_icono_fichas()

		
		

################################################ Tablero ##################################################
#  Maneja la representacion del tablero, crea una cantidad de ficha y las asocia entre ellas, para        #
#  referenciarlas posteriormente mantiene una matriz de punteros a las fichas                             # 
###########################################################################################################
class Tablero(object):
	rey = None
	jugador = None
	tablero = []
	camino = []
	
	""" Crea las fichas del tablero de juego """
	def __init__(self, jugador):
		self.jugador = jugador
		self._generar_tablero()
		
		
	""" Segun las posiciones de las fichas crea una serie
	de instancias de Ficha, Blanca, Negra y Rey y almacena sus
	direcciones en una matriz de punteros que corresponde al
	tablero de juego.
	"""	
	def _generar_tablero(self):
		blanca = copy(config["BLANCA"])
		negra = copy(config["NEGRA"])
		centro = (config["TAMANO"]-1)/2
		self.tablero = []
		for i in range(config["TAMANO"]):
			fila = []
			for j in range(config["TAMANO"]):
				clase = ()
				# asignar ficha
				if i == centro and j == centro:
					ficha = Rey(i, j)
					self.rey = ficha
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
			
	
	""" Devuelve el tipo de clase de una ficha. """	
	def _get_tipo_ficha(self, x, y):
		return type(self.tablero[x][y])
		
	
	""" Comprueba si la ficha indicada corresponde a una pieza del jugador actual. """	
	def _hay_ficha_turno(self, cuadrox, cuadroy):
		if self.jugador._get_jugador() == Jugador.jugador1:
			return type(self.tablero[cuadrox][cuadroy]) == Negra 
		else:
			return (type(self.tablero[cuadrox][cuadroy]) == Blanca or type(self.tablero[cuadrox][cuadroy]) == Rey)
			
	
	""" Comprueba si una posicion del tablero esta entre la lista de posiciones
	del camino actual del jugador.
	"""
	def _esta_sobre_camino(self, cuadrox, cuadroy):
		return self.camino.count((cuadrox, cuadroy)) == 1 
		
	
	""" Comprueba si la ficha indicada puede comer otras en la posicion
	donde se va a mover.
	"""
	def _puede_comer(self, orx, ory, dx, dy):
		return self.tablero[dx][dy].comer(self.tablero[orx][ory]) != []
		
		
	""" Devuelve la lista de fichas que se puede comer. """
	def _get_lista_comer(self, cuadrox, cuadroy):
		return self.tablero[cuadrox][cuadroy]._get_lista_comer()
	
	
	""" Actualiza la lista de camino actual. """	
	def _set_camino(self, cuadrox, cuadroy):
		self.camino = self.tablero[cuadrox][cuadroy]._get_camino()
	
	
	""" Devuelve la lista con las posiciones del tablero que estan en el
	camino actual del jugador.
	"""	
	def _get_camino(self):
		return self.camino
		
		
	""" Cambia las posiciones indicadas por la lista por espacios en blanco,
	osea, instancias de la clase Ficha.
	"""	
	def comerFichas(self, lista):
		for x, y in lista:
			self.tablero[x][y] = Ficha(x, y)
		
		
	""" Reacomoda los punteros de las fichas, lo hace de una forma ineficiente,
	mejorar después.
	"""	
	def reacomodarPunteros(self):
		for i in range(len(self.tablero)):
			for j in range(len(self.tablero[i])):
				self.tablero[i][j].x, self.tablero[i][j].y = i, j
				self.tablero[i][j].arr = self.tablero[i-1][j] if i > 0 else None
				self.tablero[i][j].aba = self.tablero[i+1][j] if i < config["TAMANO"]-1 else None
				self.tablero[i][j].izq = self.tablero[i][j-1] if j > 0 else None
				self.tablero[i][j].der = self.tablero[i][j+1] if j < config["TAMANO"]-1 else None
				
	
	""" Mueve una posicion del tablero """	
	def mover(self, ox, oy, dx, dy):
		self.tablero[ox][oy], self.tablero[dx][dy] = self.tablero[dx][dy], self.tablero[ox][oy]
		self.reacomodarPunteros()
		if self.tablero[dx][dy].comer(self.tablero[dx][dy]) != []:
			self.comerFichas(self.tablero[dx][dy]._get_lista_comer())
			self.reacomodarPunteros()		
					
	
	""" Comprueba si alguno de los dos jugadores ha ganado, o si hay que lanzar una alerta
	a cualquiera de estos.
	"""	
	def _comprobar_estado_tablero(self):
		# primero comprobar si el rey ya ha llegado a una esquina
		rey = self.rey
		fin = config["TAMANO"]-1
		restricciones = ((0,0), (fin, 0), (0, fin), (fin, fin))
		
		if restricciones.count(rey._get_coordenada()):
			evento = pygame.event.Event(pygame.USEREVENT+config["GAME_OVER"])
			pygame.event.post(evento)
			self.jugador._set_ganador(Jugador.jugador2)
		else:
			# buscar cuantos lados del rey estan asediados por fichas enemigas
			caminos_libres_rey = rey._get_caminos_libres()
			if len(caminos_libres_rey) == 0:
				evento = pygame.event.Event(pygame.USEREVENT+config["GAME_OVER"])
				pygame.event.post(evento)
				self.jugador._set_ganador(Jugador.jugador1)
			else:
				if len(caminos_libres_rey) == 1:
					# comprobar si el rey esta a punto de perder
					fichas_de_peligro = []
					if caminos_libres_rey[0] == 1:
						rey._buscar_peligro(fichas_de_peligro, rey.arr, rey.arr.izq, rey.arr.der, config["ARR"], config["DER"], config["IZQ"])
					elif caminos_libres_rey[0] == 2:
						rey._buscar_peligro(fichas_de_peligro, rey.aba, rey.aba.der, rey.aba.izq, config["ABA"], config["IZQ"], config["DER"])
					elif caminos_libres_rey[0] == 3:
						rey._buscar_peligro(fichas_de_peligro, rey.izq, rey.izq.aba, rey.izq.arr, config["IZQ"], config["ABA"], config["ARR"])
					elif caminos_libres_rey[0] == 4:
						rey._buscar_peligro(fichas_de_peligro, rey.der, rey.der.arr, rey.der.aba, config["DER"], config["ARR"], config["ABA"])
					
					if len(fichas_de_peligro) > 0:
						evento = pygame.event.Event(pygame.USEREVENT+config["REY_PELIGRO"], {"alerta":fichas_de_peligro})
						pygame.event.post(evento)
						
				esquinas_accesibles_rey = rey._buscar_esquinas(caminos_libres_rey)
				if esquinas_accesibles_rey > 0:
					evento = pygame.event.Event(pygame.USEREVENT+config["JAQUE"], {"alerta":esquinas_accesibles_rey})
					pygame.event.post(evento)
		



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
	
	
	""" Construye una nueva ficha """
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.TAMANO_TABLERO = config["TAMANO"]
	
	
	""" Devuelve las coordenadas de la ficha. """
	def _get_coordenada(self):
		return (self.x, self.y)
	
	
	""" Dada una constante predefinida devuelve un puntero
	correspondiente a una ficha vecina
	"""
	def _get_vecino(self, opcion):
		if opcion == 1:
			return self.arr
		elif opcion == 2: 
			return self.aba
		elif opcion == 3:
			return self.izq
		elif opcion == 4:
			return self.der	
	
	
	""" Determina si una ficha puede formar parte del 
	camino de otra. El parametro ficha indica quien 
	hizo el llamado, esto para determinar si dejo pasar
	el centro o las esquinas
	"""
	def _es_parte_camino(self, ficha):
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

				
	""" Calcula el camino que puede recorrer la ficha. """	
	def _get_camino(self):
		camino = []
		tmp = self
		
		while tmp.izq != None and tmp.izq._es_parte_camino(self):
			camino.append(tmp.izq._get_coordenada())
			tmp = tmp.izq
		tmp = self
		while tmp.der != None and tmp.der._es_parte_camino(self):
			camino.append(tmp.der._get_coordenada())
			tmp = tmp.der
		tmp = self
		while tmp.arr != None and tmp.arr._es_parte_camino(self):
			camino.append(tmp.arr._get_coordenada())
			tmp = tmp.arr
		tmp = self
		while tmp.aba != None and tmp.aba._es_parte_camino(self):
			camino.append(tmp.aba._get_coordenada())
			tmp = tmp.aba
		return camino
		
		
	""" Modifica la lista de comer almacenando las posibilidades. """
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
			listaComer.append(self.arr._get_coordenada())
		if type(self.aba) == enemigo and isinstance(self.aba.aba, aliado):
			listaComer.append(self.aba._get_coordenada())
		if type(self.izq) == enemigo and isinstance(self.izq.izq, aliado):
			listaComer.append(self.izq._get_coordenada())
		if type(self.der) == enemigo and isinstance(self.der.der, aliado):
			listaComer.append(self.der._get_coordenada())
		
		self.listaComer = listaComer
		return self.listaComer
		
		
	""" Devuelve la lista de fichas para comer. """	
	def _get_lista_comer(self):
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

		
	""" Busca los caminos libres de peligro para el rey. """
	def _get_caminos_libres(self):
		# para reducir comprobaciones es mejor buscar los caminos libres
		caminos_libres = []
		centro = (config["TAMANO"]-1) / 2
		fin = config["TAMANO"]-1
		restricciones = ((centro, centro), (0,0), (fin, 0), (0, fin), (fin, fin))
		if  type(self.arr) == Ficha:
			if restricciones.count(self.arr._get_coordenada()) == 0:
				caminos_libres.append(1)
		elif type(self.arr) == Blanca:
			if type(self.arr.arr) != Negra:
				caminos_libres.append(1)
		
		if type(self.aba) == Ficha:
			if restricciones.count(self.aba._get_coordenada()) == 0:
				caminos_libres.append(2)
		elif type(self.aba) == Blanca:
			if type(self.aba.aba) != Negra:
				caminos_libres.append(2)
				
		if type(self.izq) == Ficha:
			if restricciones.count(self.izq._get_coordenada()) == 0:
				caminos_libres.append(3)
		elif type(self.izq) == Blanca:
			if type(self.izq.izq) != Negra:
				caminos_libres.append(3)
				
		if type(self.der) == Ficha:
			if restricciones.count(self.der._get_coordenada()) == 0:
				caminos_libres.append(4)
		elif type(self.der) == Blanca:
			if type(self.der.der) != Negra:
				caminos_libres.append(4)
				
		return caminos_libres

	
	""" Dado el caso que el rey solo tiene un camino libre, comprueba si 
	hay alguna ficha que en el proximo movimiento pueda asediar al rey.
	(recursivo)
	"""
	def _buscar_peligro(self, fichas_de_peligro, fre, izq, der, pF, pI, pD):
		if fre != None or izq != None or der != None:
			if type(fre) == Negra:
				fichas_de_peligro.append(fre._get_coordenada())
			if type(izq) == Negra:
				fichas_de_peligro.append(izq._get_coordenada())
			if type(der) == Negra:
				fichas_de_peligro.append(der._get_coordenada())
			
			sig_fre = None if (fre == None or type(fre) != Ficha) else fre._get_vecino(pF)
			sig_izq = None if (izq == None or type(izq) != Ficha) else izq._get_vecino(pI)
			sig_der = None if (der == None or type(der) != Ficha) else der._get_vecino(pD)
			self._buscar_peligro(fichas_de_peligro, sig_fre, sig_izq, sig_der, pF,pI, pD)			
	
	
	""" Busca las esquinas por las cuales el rey puede escapar """
	def _buscar_esquinas(self, caminos_libres):
		esquinas_accesibles = []
		fin = config["TAMANO"]-1
		esquinas = ((0,0), (fin, 0), (0, fin), (fin, fin))
		for camino in caminos_libres:
			if camino == config["ARR"]:
				tmp = self.arr
				while tmp.arr != None and type(tmp) == Ficha:
					tmp = tmp.arr
				if esquinas.count(tmp._get_coordenada()) == 1:
					esquinas_accesibles.append(tmp._get_coordenada())
			elif camino == config["ABA"]:
				tmp = self.aba
				while tmp.aba != None and type(tmp) == Ficha:
					tmp = tmp.aba
				if esquinas.count(tmp._get_coordenada()) == 1:
					esquinas_accesibles.append(tmp._get_coordenada())
			elif camino == config["IZQ"]:
				tmp = self.izq
				while tmp.izq != None and type(tmp) == Ficha:
					tmp = tmp.izq
				if esquinas.count(tmp._get_coordenada()) == 1:
					esquinas_accesibles.append(tmp._get_coordenada())
			elif camino == config["DER"]:
				tmp = self.der
				while tmp.der != None and type(tmp) == Ficha:
					tmp = tmp.der
				if esquinas.count(tmp._get_coordenada()) == 1:
					esquinas_accesibles.append(tmp._get_coordenada())
		return esquinas_accesibles
	

	

################################################ Jugador ##################################################
#  Mantiene el estado de los turnos durante el juego                                                      # 
###########################################################################################################		
class Jugador(object):
	jugador1 = "jugador1"
	jugador2 = "jugador2"
	jugador_actual = None
	jugador_ganador = None
	
	
	""" Constructor de la clase. """
	def __init__(self):
		self.jugador_actual = self.jugador1
		
		
	""" Cambia el turno. """	
	def _cambiar_turno(self):
		if self.jugador_actual == self.jugador1:
			self.jugador_actual = self.jugador2
		else:
			self.jugador_actual = self.jugador1
	
	
	""" Devuelve el turno actual."""	
	def _get_jugador(self):
		return self.jugador_actual

		
	""" Indica si ya algun jugador gano el juego. """	
	def _hay_ganador(self):
		return self.jugador_ganador
		
		
	""" Indicado un jugador, lo coloca como el jugador ganador """	
	def	_set_ganador(self, ganador):
		self.jugador_ganador = ganador
		
		
	""" Devuelve el jugador que gano la partida. """	
	def _get_ganador(self):
		return self.jugador_ganador
	
	
	""" Pone el turno por defecto. """
	def _set_nuevo_juego(self):
		self.jugador_actual = self.jugador1
		self.jugador_ganador = None

		
		
	
if __name__ == '__main__':
	config = {}
	execfile("settings.config", config) 
	main = Main(config)
	main.iniciar()
