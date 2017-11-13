#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs, sys, re, subprocess, scipy.misc, numpy
import grafo

def main():
	meuGrafo = grafo.Grafo()

	saida = ""
	provincias = codecs.open("definition.csv", encoding="latin_1").readlines()
	provincias = [x.strip().split(";") for x in provincias[1:]]
	#simpleProvList = []
	for p in provincias:
		meuGrafo.adicionarVertice(p[4])
	meuGrafo.mostraVertices()

	saida += "graph \"grafo\" {\nnode [width=0.5,height=0.5];\n"

	subprocess.check_output(['convert', 'provinces.bmp', 'provinces-temp.png'])
	provMap = scipy.misc.imread('provinces-temp.png')
	colorMap = {}
	for line in range(1900, len(provMap)-1):
		print(line)
		#if line%50 == 0:
		#	print("line", line, "of", len(provMap))
		for col in range(1, len(provMap[0])-1):
			for n in twoNeighbors(line, col):
				if numpy.any(provMap[line, col] != provMap[n[0], n[1]]):
					#print ((provMap[line, col], provMap[n[0], n[1]])) not in edgeList
					#if ((provMap[line, col][:2], provMap[n[0], n[1]][:2])) not in edgeList:
					this = provMap[line, col]
					this = [int(x) for x in this[:3]]
					this = findProv(this, provincias)
					that = provMap[n[0], n[1]]
					that = [int(x) for x in that[:3]]
					that = findProv(that, provincias)
					wastes = ["686", "687","688","689","690","691","692","693","694"]
					if int(this) < 750 and int(that) < 750 and this not in wastes and that not in wastes and meuGrafo.matrizDeAdjacencias[this][that] == 0:
						meuGrafo.adicionarAresta('x', this, that)
						print(this,that)


	#i = 1
	for x in range(len(meuGrafo.vertices)):
		print(x)
		if meuGrafo.grau(x) > 0:
			saida += "N" + str(provincias[x][0]) + " [label=\""+provincias[x][4]+"\",fontsize=10];\n"
			print(provincias[x][4])
		else:
			print(provincias[x][0])

	for aresta in meuGrafo.arestas:
		#print(len(edge[0]), len(edge[1]))
		saida += "N"+str(aresta[1])+ " -- N"
		saida += str(aresta[2]) + " [weight=1,style=\"setlinewidth(1.0)\"];\n"
	#s.index([x for x in s if x[1:] == [2,3,2]][0])
	saida += "}\n"
	f = open('saida.dot', 'w')
	f.write(saida)
	f.close()

	subprocess.check_output(['rm', 'provinces-temp.png'])

def findProv(color, provList):
	for p in range(len(provList)):
		if color[0] == int(provList[p][1]) and color[1] == int(provList[p][2]) and \
		color[2] == int(provList[p][3]):
			return p

def distance(x, y):
	return((x[0]-y[0])**2 + (x[1]-y[1])**2)
	#no need to take the square root

def neighbors(x, y):
	return ((x-1, y),(x+1, y),(x,y-1),(x,y+1))

def twoNeighbors(x, y):
	#return only the preceding pixels to the left and up;
	#sufficient to find borders
	return((x-1, y),(x, y-1))

if __name__ == "__main__":
	main()
