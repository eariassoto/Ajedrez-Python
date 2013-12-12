#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tablero(object):
	cabezaTablero = None
	
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
		tablero = tablero[0][0]
		aa = tablero.getFicha(0,1)
		print(aa.getCoord())
		

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
	tablero = Tablero(config)
