from math      import sqrt, log
from itertools import permutations as permutaciones
from itertools import islice as rango
from random    import randrange as aleatorio
from random    import random

#Vector donde se guardan los tiempos de espera de los semaforos.
tiempo = {}

#Método que calcula el factorial de un número.
def fact(n): return 1 if n < 2 else n * fact(n-1)

#Método que crea las aristas a partir de un archivo
def parserAristas(archivo):
	fcd = open(archivo,"r")
	lineas = fcd.readlines()
	fcd.close()
	aristas = []
	for i, linea in enumerate (lineas):
		nums = linea.split(" ")
		aristas.append( arista(i, float(nums[0]), float(nums[1])) )
	return aristas


#clase cuyas instancias representan las aristas que forman parte de la ruta

class arista:
	#constructor de la clase
	def __init__(self, id, min, max):
		self.__id = id
		self.__min = min
		self.__max = max

	#representación de una arista como cadena de caracteres
	def __str__(self):
		return "%d" % (self.__id)

	#destructor de la clase
	def __del__(self):
		del self.__id
		del self.__min
		del self.__max

	#devuelve el numero de arista
	def getid(self):
		return self.__id

	#devuelve la capacidad minima de la arista
	def getx(self):
		return self.__min

	#devuelve la capacidad maxima de la arista
	def gety(self):
		return self.__max


#clase cuyas instancias representan posibles soluciones al problema

class cromosoma:
	#constructor de la clase
	def __init__(self, aristas = []):
		self.__aristas = list(aristas)


	#copia un cromosoma.
	def copy( self ):
		return cromosoma( self.getaristas())

	#destructor de la clase cromosoma
	def __del__(self):
		while self.__aristas:
			arista = self.__aristas.pop()
			del arista

	#devuelve el valor de una arista
	def getaristas(self):
		return self.__aristas

	#representación como cadena de caracteres del cromosoma
	def __str__(self):
		s  = "["
		for arista in self.getaristas() :
			s += " %s," % (str(arista))
		s +=" %2s ]" % (self.getaristas()[0])
		return s


	#Método que calcula el tiempo de espera de un nodo
	def tiempo(self, cd1, cd2):
		a,b = (cd1, cd2) if cd1.getid() < cd2.getid() else (cd2, cd1)
		key = "%d-%d" % (a.getid(),b.getid())
		if tiempos.has_key(key):
			dist= tiempos[key]
		else:
			min= b.getmin() - a.getmin()
			max= b.getmax() - a.getmax()
			tiem= sqrt(min**2 + max**2)
			tiempos[key]= tiem
		return tiem


	#Método que calcula la aptitud asociada a un cromosoma.
	#Método que calcula el tiempo total de espera de todos los nodos.
	def aptitud( self ):
		apt = 0
		orig= self.getaristas()
		dest= list(orig)
		tmp= dest.pop(0)
		dest.append(tmp)
		for a,b in zip(orig,dest):
			apt += self.tiempo(a,b)
		return apt

	#Método para comparar dos cromosomas.
	def __cmp__(self, otro):
		return int(self.aptitud() - otro.aptitud())


	#Método para encontrar la posición de una arista en la lista.
	def index( self, nodo ):
		return self.___aristas.index(nodo)


	#Método que implementa la cruza de dos cromosomas.
	#Cruzamiento por ciclos
	def cruzar(self, otro):
		p1, p2 = self.getaristas(), otro.getaristas()
		h1, h2 = list(p2), list(p1)
		idx = [0]
		i = 0
		cont = True
		while cont:
			arista = p2[i]
			i = p1.index(arista)
			idx.append(i)
			cont = not p1[0] is p2[i]

		for i in idx:
			h1[i], h2[i] = h2[i], h1[i]

		return cromosoma(h1), cromosoma(h2)



	#Método con el que un cromosoma muta.
	#Mutación por inversión.
	def mutar(self):
		lista = self.getaristas()
		mitad = len(lista)/2
		ini = aleatorio(0, mitad)
		fin = aleatorio(mitad, len(lista))
		a, b, c = lista[0:ini], lista[ini:fin], lista[fin:]
		b.reverse()
		del self.__aristas
		self.__aristas = a + b + c
		del a
		del b
		del c



#Método que ordena la población de mejor aptitud a peor aptitud.
def sort( self ):
	self.__aristas.sort()


#Método que calcula la desvión estándar.
def desvestandar(poblacion =[]):
	tam = len(poblacion)
	aptitudes = map(cromosoma.aptitud, poblacion)
	xprom = sum(aptitudes)/tam
	desvs = sqrt(sum(map(lambda x: (x-xprom)**2, aptitudes))/ (tam - 1))
	return desvs, xprom



#Invoca el método de mutación para algunos individuos de la población con
#cierta probabilidad.
def mutarpop( pop, pmuta ):
	for p in pop:
		if pmuta > random():
			p.mutar()


#Cruza los individuos de la población para obtener cromosomas nuevos que
#posteriormente se integrarán a la población en la siguiente generación.
def cruzarpob( pob, pcruza ):
	padres = list( pob )
	hijos = list()

	if len(padres) % 2:
		if random() > 0.5:
			padres.pop( aleatorio(0, len(padres)))
		else:
			padres.append( padres[aleatorio(0, len(padres))] )

	while padres:
		a = padres.pop(aleatorio(0,len(padres)))
		b = padres.pop(aleatorio(0,len(padres)))

		if pcruza > random() :
			hijos.extend( a.cruzar(b) )

	return hijos


#Genera la población inicial.
#Seleccionando fin-ini permutaciones aleatorias del espacio de soluciones.
def generapob( aristas, pob):
	s     = list()
	perms = permutaciones(aristas)
	fin   = aleatorio( pob, fact( len(aristas) ) )
	ini   = fin - pob

	Sigma = list(rango(perms, pob))

	for sigma in Sigma:
		k = list(sigma)
		s.append(cromosoma(k))

	for k in range(2):
		mutarpop(s,1.0)

	return s


#Genera una representación como cadena de caracteres de un conjunto de
#soluciones.
def imprimepob( pob ):
	n      = int( log( len(pob),10) + 1 )
	s      = " | %" + str(n) + "d | %s | %f\n"
	edge= " +" + (n + 2) * "-" + "+" + (len(str(pob[0])) + 2) * "-" + "+\n"
	strpob = edge
	for i, p in enumerate(pob):
		strpob += s % (i+1,str(p), p.aptitud() )

	return strpob + edge



#selecciona
def selecciona(poblacion, pobtam):
	p = list(poblacion)
	p.sort()
	return p[:pobtam]



#selecciona una nueva población utilizando el método de ordenamiento exponencial.
def seleccionOE(poblacion = []):
    poblacion.sort()
    s, prom = desvestandar(poblacion)
    n = len(poblacion)
    prob = lambda r: (1-s)/(1-s**n)*(s**(r-1))
    probabilidades = map(prob, range(n))
    probacumulada  = 0
    pacumuladas    = []
    elegidos       = []
    pobtam = 20

    for probabilidad in probabilidades:
        probacumulada += probabilidad
    pacumuladas.append(probacumulada)
    print "*" *50 ,probacumulada

    for k in range(len(poblacion)):
        cota = random()
        i = 0
        while i < len(pacumuladas) and pacumuladas[i] < cota :
            i += 1
        elegidos.append( poblacion[i] )

    return elegidos[:pobtam]


#Método de selección por torneo.
def selecciont(poblacion, tampob):
	selec = list()
	for k in [1,2]:
		participantes = list(poblacion)
		if len(participantes)%2 ==1:
			if k==1:
				participantes.pop(aleatorio(0, len(participantes)))
			else:
				participantes.append(participantes[aleatorio(0, len(participantes))])
		while participantes:
			a= participantes.pop(aleatorio(0, len(participantes)))
			b= participantes.pop(aleatorio(0, len(participantes)))
			ganador= a if a<b else b
			selec.append(ganador)
	selec.sort()
	return selec[:tampob]



#Implementación de un algoritmo genético para resolver el problema
def genetico(aristas, pobtam, pcruza, pmuta, iteraciones ):
	poblacion = generapob(aristas, pobtam)
	print imprimepob(poblacion)
	mejores = list()
	poblacion.sort()
	print "Poblacion ordenada"
	print imprimepob(poblacion)
	mejor = poblacion[0]
	mejores.append(mejor.copy())
	selec = selecciont(poblacion, pobtam)
	continua = True
	i = 1
	while continua and i < iteraciones:
		print i, ") comenzando iteracion"
		i+=1
		print imprimepob(selec)
		hijos = cruzarpob(selec, pcruza)
		selec.extend(hijos)
		mutarpop(selec, pmuta)
		selec = selecciont(selec, pobtam)
		selec.sort()
		mejores.append(selec[0].copy())
		if(len(mejores)>1):
			aux=list(mejores)
			aux.sort()
			n=aux.count(aux[0])
			if(len(mejores)>=10 and n>len(aux)/2):
				continua= False
	mejores.sort()

	print "Los mejores individuos en todas las iteraciones:"
	print imprimepob(mejores)
	return mejores[0]


#Método que guarda las las capacidades de las aritas, en un archivo
#ordenadas de acuerdo al recorrido óptimo.
def guardaCapacidades( optimo, rutaArchivo ):
	archivo   = open( rutaArchivo, "w" )
	contenido = ""
	for arista in optimo.getaristas():
		contenido += "%f %f\n" % (arista.getmin(), arista.getmax())
	archivo.write(contenido)

	archivo.close()

#Aquí modificaremos los parametros que le pasaremos a el método genetico.
#Aristas es una lista que contiene todas las aristas obtenidas del archivo aristas.csv.
#pobtam es el tamaño de la población con la que iniciaremos.
#pcruza es la probabilidad de cruzamiento.
#pmuta es la probabilidad de mutación.
#iteraciones es el número de iteraciones para detener el programa.
def main():
	aristas = parserAristas("aristas.csv")
	pobtam = 40
	pcruza = 0.9
	pmuta = 0.5
	iteraciones = 200
	optimo = genetico(aristas, pobtam, pcruza, pmuta, iteraciones )
	print "Mejor solución encontrada:"
	print optimo, "-- Con un costo de", optimo.aptitud(), "unidades."

	guardaCapacidades( optimo, "recorrido-optimo.data" )



if __name__ == "__main__":
	main()


class Graficar(object):

    def __init__(self,n_generations,pop_size, graph=False):

        if csv_nodos:
            self.read_csv()

        self.n_generations = n_generations
        self.pop_size = pop_size

        # Declaramos las variables a graficar
        if graph:
            self.set_nodo_gcoords()
            
            self.window = Tk()
            self.window.wm_title("Generation 0")

            self.canvas_current = Canvas(self.window, height=300, width=300)
            self.canvas_best = Canvas(self.window, height=300, width=300)

            # Inicia barra de estado con cadena
            self.stat_tk_txt = StringVar()
            self.status_label = Label(self.window, textvariable=self.stat_tk_txt, relief=SUNKEN, anchor=W)

            # crea puntos para los nodos en ambos lienzos
            for nodo in list_of_nodos:
                self.canvas_current.create_oval(nodo.graph_x-2, nodo.graph_y-2, nodo.graph_x + 2, nodo.graph_y + 2, fill='blue')
                self.canvas_best.create_oval(nodo.graph_x-2, nodo.graph_y-2, nodo.graph_x + 2, nodo.graph_y + 2, fill='blue')

            self.canvas_current_title.pack()
            self.canvas_current.pack()
            self.canvas_best_title.pack()
            self.canvas_best.pack()
            self.status_label.pack(side=BOTTOM, fill=X)

            self.window_loop(graph)
        else:
            self.GA_loop(n_generations,pop_size, graph=graph)

    def set_nodo_gcoords(self):

        min_x = 100000
        max_x = -100000
        min_y = 100000
        max_y = -100000

        for nodo in list_of_nodos:

            if nodo.x < min_x:
                min_x = nodo.x
            if nodo.x > max_x:
                max_x = nodo.x

            if nodo.y < min_y:
                min_y = nodo.y
            if nodo.y > max_y:
                max_y = nodo.y

        # desplaza graph_x para que el nodo más a la izquierda comience en x = 0, lo mismo para y.
        for nodo in list_of_nodos:
            nodo.graph_x = (nodo.graph_x + (-1*min_x))
            nodo.graph_y = (nodo.graph_y + (-1*min_y))

        min_x = 100000
        max_x = -100000
        min_y = 100000
        max_y = -100000

        for nodo in list_of_nodos:

            if nodo.graph_x < min_x:
                min_x = nodo.graph_x
            if nodo.graph_x > max_x:
                max_x = nodo.graph_x

            if nodo.graph_y < min_y:
                min_y = nodo.graph_y
            if nodo.graph_y > max_y:
                max_y = nodo.graph_y

        if max_x > max_y:
            stretch = 300 / max_x
        else:
            stretch = 300 / max_y

        for nodo in list_of_nodos:
            nodo.graph_x *= stretch
            nodo.graph_y = 300 - (nodo.graph_y * stretch)


    def update_canvas(self,the_canvas,the_route,color):

        the_canvas.delete('path')

        for i in range(len(the_route.route)):

            next_i = i-len(the_route.route)+1

            the_canvas.create_line(the_route.route[i].graph_x,
                                the_route.route[i].graph_y,
                                the_route.route[next_i].graph_x,
                                the_route.route[next_i].graph_y,
                                tags=("path"),
                                fill=color)

            the_canvas.pack()
            the_canvas.update_idletasks()

    def read_csv(self):
        with open(csv_name, 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                new_nodo = nodo(row[0],float(row[1]),float(row[2]))

    def GA_loop(self,n_generations,pop_size, graph=False):

        start_time = time.time()
        the_population = RoutePop(pop_size, True)

        if the_population.fittest.is_valid_route() == False:
            raise NameError('Multiples nodos.')
            return

        initial_length = the_population.fittest.length

        best_route = Route()

        if graph:
            self.update_canvas(self.canvas_current,the_population.fittest,'red')
            self.update_canvas(self.canvas_best,best_route,'green')

        for x in range(1,n_generations):
            if x % 8 == 0 and graph:
                self.update_canvas(self.canvas_current,the_population.fittest,'red')

            the_population = GA().evolve_population(the_population)

            if the_population.fittest.length < best_route.length:

                best_route = copy.deepcopy(the_population.fittest)
                if graph:
                    self.update_canvas(self.canvas_best,best_route,'green')
                    self.stat_tk_txt.set('Initial length {0:.2f} Best length = {1:.2f}'.format(initial_length,best_route.length))
                    self.status_label.pack()
                    self.status_label.update_idletasks()

            if graph:
                self.window.wm_title("Generacion {0}".format(x))
        if graph:
            self.window.wm_title("Generacion {0}".format(n_generations))

            self.update_canvas(self.canvas_best,best_route,'green')
            
        end_time = time.time()

        self.clear_term()
        best_route.pr_cits_in_rt(print_route=True)

    def window_loop(self, graph):
        self.window.after(0,self.GA_loop(self.n_generations, self.pop_size, graph))
        self.window.mainloop()

    def clear_term(self):
        os.system('cls' if os.name=='nt' else 'clear')