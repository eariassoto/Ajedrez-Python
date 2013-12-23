class Main:	
""" Constructor """
def __init__(self, config):
	# almacenaran las instancias de los objetos.
	jugador = Jugador()
	tablero = Tablero(self.jugador)
	grafico = Grafico(self.jugador, self.tablero, self.SUPERFICIE)
	
	# velocidad promedio de cuadros por segundo.
	FPS = 114
	
	SUPERFICIE = None
	
	# boolean para controlar estado de ficha seleccionada.
	seleccion = False
	
	# eventos que puede disparar el usuario
	CAMBIO_TURNO = pygame.USEREVENT+1
	JAQUE = pygame.USEREVENT+2
	JAQUE_MATE = pygame.USEREVENT+3
	REY_PELIGRO = pygame.USEREVENT+4
	REY_GANO = pygame.USEREVENT+5
	
	# sirve para almacenar la posicion de la ficha seleccionada por el clic
	fichaSeleccion = ""
	
	# iniciar el modulo pygame y el objeto FPS.
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	
	# almacenan las coordenadas del mouse
	mousex = 0 
	mousey = 0 
	
	
	gameOver = False
	while not gameOver: # loop principal del juego
	
		mouseClic = False
		
		# dibujar ventana.
		self.grafico.dibujarVentana()
		if self.seleccion:
			self.grafico.dibujarCaminoIluminado(None, None)
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
			#elif evento.type == 
			elif not mouseClic and evento.type == MOUSEMOTION:
				mousex, mousey = evento.pos 
			elif not mouseClic and evento.type == MOUSEBUTTONUP:
				mousex, mousey = evento.pos
				mouseClic = True	
			elif evento.type == pygame.USEREVENT+4:
				print("dsfhrtjh")
				
		# comprobar si el mouse esta actualmente en un cuadro
		cuadrox, cuadroy = self.grafico.getCuadroPixel(mousex, mousey)					

		if (cuadrox, cuadroy) != (None, None) and not mouseClic:
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
				self.jugador.switchJugador()
				
		self.tablero.comprobarEstado()
		
		pygame.display.update()	
		self.FPSCLOCK.tick(self.FPS)	


""" Animaciones para el fin del juego """
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
	self.jugador.nuevoJuego()	
