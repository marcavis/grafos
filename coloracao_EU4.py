#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import codecs, sys, re, subprocess, scipy.misc, numpy, random
import grafo

def main():
	meuGrafo = grafo.Grafo()

	saida = ""

	arqNomesDasProvincias = codecs.open("../localisation/prov_names_l_english.yml", encoding="utf-8").readlines()
	nomesDasProvincias = {}
	nomesDasProvincias[0] = "Corrigir-erro-de-off-by-one"
	for linha in arqNomesDasProvincias:
		if "PROV" in linha:
			linhaAtual = linha.replace(" PROV", "")
			linhaAtual = linhaAtual.split(":")
			nome = linhaAtual[1].strip().strip('"')
			nomesDasProvincias[int(linhaAtual[0])] = nome

	provincias = codecs.open("definition.csv", encoding="latin_1").readlines()
	provincias = [x.strip().split(";") for x in provincias[1:]]
	dicionarioDeCores = {(int(x[1]),int(x[2]),int(x[3])): int(x[0]) for x in provincias }
	#simpleProvList = []
	meuGrafo.adicionarVertice("Corrigir-erro-de-off-by-one")
	for p in range(len(provincias)):
		meuGrafo.adicionarVertice(nomesDasProvincias[p])

	saida += "graph \"grafo\" {\nnode [width=0.5,height=0.5];\n"

	subprocess.check_output(['convert', 'provinces.bmp', 'provinces-temp.png'])
	provMap = scipy.misc.imread('provinces-temp.png')

	colorMap = {}
	pixelsDeFronteira = [[False] * len(provMap[0]) for y in provMap]
	donoDoPixel = [[-1] * len(provMap[0]) for y in provMap]

	#ler vários arquivos que informam quais províncias não são terra ocupável
	tiposDeProvincias = lerGrupos('default.map')
	tiposDeProvincias.update(lerGrupos('climate.txt'))

	#print(tiposDeProvincias)
	#return



	for linha in range(1, len(provMap)-1):
		if linha%50 == 0:
			print("linha", linha, "de", len(provMap))
		for col in range(1, len(provMap[0])-1):
			pixel1 = provMap[linha][col]
			pixel1 = [int(x) for x in pixel1[:3]]
			pais1 = findProv(pixel1, dicionarioDeCores)
			#acho que... corrigir um erro off-by-one, já que as províncias começam de 1
			#pais1 = pais1 - 1
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
					#pais2 = pais2 - 1

					if (ehOcupavel(pais1, tiposDeProvincias) and \
					ehOcupavel(pais2, tiposDeProvincias) and \
					meuGrafo.matrizDeAdjacencias[pais1][pais2] == 0):
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
	cores = [[220,50,50],[50,220,50],[230,40,230],[230,230,40],[250,150,50],[40,40,130],
			[100,0,0],[0,100,0],[0,0,100],[100,100,0],[100,0,100],[0,100,100]]


	novoMapa = provMap[:]
	for linha in range(len(provMap)):
		if linha%50 == 0:
			print("pintando linha", linha, "de", len(provMap))
		for col in range(len(provMap[0])):
			if (linha == 0 or col == 0 or \
			linha == len(provMap) - 1 or col == len(provMap[0]) - 1):
				novoMapa[linha][col] = [0, 0, 0]
			elif pixelsDeFronteira[linha][col]:
				novoMapa[linha][col] = [0, 0, 0]
			elif donoDoPixel[linha][col] in tiposDeProvincias['lakes']:
				novoMapa[linha][col] = [160, 200, 250]
			elif donoDoPixel[linha][col] in tiposDeProvincias['sea_starts']:
				novoMapa[linha][col] = [160, 200, 250]
			elif donoDoPixel[linha][col] in tiposDeProvincias['impassable']:
				novoMapa[linha][col] = [143, 143, 143]
			else:
				cor = coloracoes[donoDoPixel[linha][col]][1]
				novoMapa[linha][col] = cores[cor]
	scipy.misc.imsave("provinces-novo.png", novoMapa)

	contagemDeCores=[0]*12
	for num_prov in range(1, len(coloracoes)):
		if ehOcupavel(num_prov, tiposDeProvincias):
			contagemDeCores[coloracoes[num_prov][1]] += 1
	for num_cor in range(len(contagemDeCores)):
		print("Cor", num_cor, ":", contagemDeCores[num_cor], "províncias")
#lê o conteúdo de uma tag dentro de um arquivo; por exemplo,
#lerGrupo(sea_starts, arquivo) onde arquivo tem sea_starts = { 1 2 3 }
#retorna [1, 2, 3]
def lerGrupos(arquivo):
	linhas = codecs.open(arquivo, encoding="latin_1").readlines()
	#ignorar comentários
	linhas = [linha.split("#")[0] for linha in linhas]
	linhas = "".join(linhas)
	linhas = linhas.split("\n")
	num_linha = 0
	grupos = {}
	while num_linha < len(linhas):
		if ('=' in linhas[num_linha] and 'canal_definition' not in linhas[num_linha]):
			if ('{' in linhas[num_linha] and '}' not in linhas[num_linha]):
				chave = linhas[num_linha].split('=')[0].strip()
				conteudo = []
				num_linha += 1
				while '}' not in linhas[num_linha]:
					if len([s for s in linhas[num_linha] if s.isdigit()]) > 0:
						conteudo += [int(x.strip()) for x in linhas[num_linha].split()]
					num_linha += 1
				grupos[chave] = conteudo
			else:
				novaEntrada = linhas[num_linha].split('=')
				grupos[novaEntrada[0].strip()] = novaEntrada[1].strip()
		num_linha += 1
	return grupos

#retorna True se a província não é mar, lago, desabilitada ou
#não-ocupável (por exemplo, o Saara)
def ehOcupavel(prov, dicionario):
	return (prov not in dicionario['sea_starts'] and \
		prov not in dicionario['only_used_for_random'] and \
		prov not in dicionario['lakes'] and \
		prov not in dicionario['impassable'])

def findProv(color, dicionario):
	tuplaDeCores = (color[0], color[1], color[2])
	return dicionario[tuplaDeCores]

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
