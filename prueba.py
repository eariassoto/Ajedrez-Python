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
				nodo = Nodo(i,j, clase)
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
	
	clase = None
	enemigo = None
	
	x = 0;
	y = 0;
	
	def __init__(self, i, j, clase):
		self.x = i
		self.y = j
		self.clase = clase[0]
		self.enemigo = clase[1]
		
	def getFicha(self, x, y):
		tmp = self 
		for i in range(x):
			tmp = tmp.aba
		for j in range(y):
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
			
	def getCoord(self):
		return (self.x, self.y)
	
if __name__ == '__main__':
	config = {}
	execfile("settings2.config", config) 
	tablero = Tablero(config)
