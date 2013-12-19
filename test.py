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
	
	def __init__(self, jugador, tablero, superficie):
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
	def dibujarTextos(self, jaque, jaqueMate, peligro, gano=""):
		color1 = config["COLOR_TEXTO"]
		color2 = config["COLOR_TEXTO"]
		textoJ1 = 'Jugador 1, tu turno.' if jugador.getJugadorActual() == Jugador.jugador1 else ''
		textoJ2 = 'Jugador 2, tu turno.' if jugador.getJugadorActual() == Jugador.jugador2 else ''
		
		if jaque:
			textoJ1 = 'Jugador 1, Jaque'
			color1 = self.logico.getColorAlerta("roja")
		elif jaqueMate:
			textoJ1 = 'Jugador 1, JaqueMate'
			color1 = self.logico.getColorAlerta("roja")
			
		if peligro:
			textoJ2 = 'Jugador 2, vigila tu rey'
			color2 = self.logico.getColorAlerta("roja")

		if gano == Jugador.jugador1:
			textoJ1 = 'Jugador 1, ganaste.'
			textoJ2 = ""
			color1 = self.logico.getColorAlerta("verde")
		elif gano == Jugador.jugador2:
			textoJ2 = 'Jugador 2, ganaste.'
			textoJ1 = ""
			color2 = self.logico.getColorAlerta("verde")
	
		coordX = self.MARGEN_X + self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = int(self.ANCHO_CUADRO / 2)
		self.dibujarTexto(textoJ1, color1, coordX, coordY)
		
		coordX = self.MARGEN_X + self.LARGO_CUADRO + int((self.ANCHO_CUADRO - int(self.ANCHO_CUADRO * 0.50)) / 2)
		coordY = self.ANCHO_VENTANA + self.MARGEN_Y + self.MARGEN_X + int(self.ANCHO_CUADRO / 2)
		
		self.dibujarTexto(textoJ2, color2, coordX, coordY)
		
		
	""" Dibuja los cuadros y las fichas del tablero. """	
	def dibujarVentana(self, jaque, jaqueMate, peligro, gano=""):
		self.SUPERFICIE.fill(config["COLOR_FONDO"])
		pygame.draw.rect(self.SUPERFICIE, config["COLOR_MARGEN"], (0, self.ANCHO_CUADRO, (self.LARGO_VENTANA + 2*self.MARGEN_X), (self.ANCHO_VENTANA + 2*self.MARGEN_X)), 0)
		
		self.dibujarPanel()
		self.dibujarTextos(jaque, jaqueMate, peligro, gano)
		self.dibujarCuadros()
		self.dibujarFichas()