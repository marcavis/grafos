#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs, sys, re, subprocess, scipy.misc, numpy, random
import grafo

def main():
	meuGrafo = grafo.Grafo()

	saida = ""

	provincias = codecs.open("definition.csv", encoding="latin_1").readlines()
	provincias = [x.strip().split(";") for x in provincias[1:]]
	dicionarioDeCores = {(int(x[1]),int(x[2]),int(x[3])): int(x[0]) for x in provincias }
	#simpleProvList = []
	for p in provincias:
		meuGrafo.adicionarVertice(p[4])
	meuGrafo.mostraVertices()

	saida += "graph \"grafo\" {\nnode [width=0.5,height=0.5];\n"

	subprocess.check_output(['convert', 'provinces.bmp', 'provinces-temp.png'])
	provMap = scipy.misc.imread('provinces-temp.png')

	colorMap = {}
	pixelsDeFronteira = [[False] * len(provMap[0]) for y in provMap]
	donoDoPixel = [[-1] * len(provMap[0]) for y in provMap]
	for linha in range(1, len(provMap)-1):
		if linha%50 == 0:
			print("linha", linha, "de", len(provMap))
		for col in range(1, len(provMap[0])-1):
			pixel1 = provMap[linha][col]
			pixel1 = [int(x) for x in pixel1[:3]]
			pais1 = findProv(pixel1, dicionarioDeCores)
			#corrigir um erro off-by-one, já que as províncias começam de 1
			pais1 = pais1 - 1
			donoDoPixel[linha][col] = pais1
			for n in doisVizinhos(linha, col):
				if numpy.any(provMap[linha][col] != provMap[n[0], n[1]]):

					#no final, pinter o pixel e o vizinho de preto
					pixelsDeFronteira[linha][col] = True

					pixel2 = provMap[n[0]][n[1]]
					pixelsDeFronteira[n[0]][n[1]] = True
					pixel2 = [int(x) for x in pixel2[:3]]
					pais2 = findProv(pixel2, dicionarioDeCores)
					#corrigir um erro off-by-one, já que as províncias começam de 1
					pais2 = pais2 - 1
					#wastes = ["686", "687","688","689","690","691","692","693","694"]
					if meuGrafo.matrizDeAdjacencias[pais1][pais2] == 0:
						meuGrafo.adicionarAresta('x', pais1, pais2)
						print("encontrada fronteira de", meuGrafo.vertices[pais1], "para", meuGrafo.vertices[pais2])

	#funções para fazer um grafo; melhor não para esse caso, é muito grande
	if False:
		for x in range(len(meuGrafo.vertices)):
			if meuGrafo.grau(x) > 0:
				saida += "N" + str(provincias[x][0]) + " [label=\""+provincias[x][4]+"\",fontsize=10];\n"

		#graus = [(meuGrafo.vertices[x], meuGrafo.grau(x)) for x in range(len(meuGrafo.vertices))]
		#graus.sort(key=lambda x: x[1])
		#print(graus)
		#meuGrafo.mostraListaDeAdjacencias()

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
	coloracoes = grafo.coloracao(meuGrafo)
	coloracoes.sort(key=lambda x: x[0])
	cores = [[220,150,100],[100,220,150],[100,150,220],[130,130,40],[130,40,130],[40,130,130],
			[100,0,0],[0,100,0],[0,0,100],[100,100,0],[100,0,100],[0,100,100]]

	novoMapa = provMap[:]
	for linha in range(1, len(provMap)-1):
		for col in range(1, len(provMap[0])-1):
			if pixelsDeFronteira[linha][col]:
				novoMapa[linha][col] = [0, 0, 0]
			else:
				cor = coloracoes[donoDoPixel[linha][col]][1]
				novoMapa[linha][col] = cores[cor]
	scipy.misc.imsave("provinces-novo.png", novoMapa)

def findProv(color, dicionario):
	colorTuple = (color[0], color[1], color[2])
	return dicionario[colorTuple]

def distance(x, y):
	return((x[0]-y[0])**2 + (x[1]-y[1])**2)
	#no need to take the square root

def vizinhos(x, y):
	return ((x-1, y),(x+1, y),(x,y-1),(x,y+1))

def doisVizinhos(x, y):
	#retorna os pixels localizados acima e ao lado esquerdo;
	#são suficientes para encontrar vizinhos no mapa
	return((x-1, y),(x, y-1))

if __name__ == "__main__":
	main()
