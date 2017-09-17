#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import grafo, random, sys

def criarVertices(grafo: grafo.Grafo, quantidade: int):
    ultimoVertice = len(grafo.vertices) + 1
    for i in range(quantidade):
        grafo.adicionarVertice("V" + str(ultimoVertice + i))

def criarArestas(grafo: grafo.Grafo, quantidade):
    ultimaAresta = len(grafo.arestas) + 1
    for i in range(quantidade):
        if grafo.valorado:
            valor = random.randint(1, 10)
        else:
            valor = 1
        origem = random.randint(0, len(grafo.vertices) - 1)
        destino = random.randint(0, len(grafo.vertices) - 1)
        grafo.adicionarAresta("E" + str(ultimaAresta + i), origem, destino, valor)

def relatorioDijkstra(meuGrafo, origem):
    distancias, precursores = grafo.dijkstra(meuGrafo, origem)
    print()
    print("Distâncias a partir do vértice " + meuGrafo.vertices[origem] + ":")
    print("***** Distância | Anterior | Caminho Completo")
    for v in range(len(meuGrafo.vertices)):
        print('{:>4}'.format(meuGrafo.vertices[v]) + "| ", end='')
        dist = "∞" if distancias[v] == sys.maxsize else distancias[v]
        print('{:>9}'.format(dist) + " | ", end='')
        prec = "--" if precursores[v] == None else meuGrafo.vertices[precursores[v]]
        print('{:>8}'.format(prec) + " | ", end='')
        print(backtrack(v, meuGrafo, precursores), end='')
        print()

def backtrack(vertice: int, meuGrafo, precursores):
    caminho = []
    atual = vertice
    while precursores[atual] != None:
        caminho = [meuGrafo.vertices[precursores[atual]]] + caminho
        atual = precursores[atual]
    saida = ''.join([x + " -> " for x in caminho])
    return saida + meuGrafo.vertices[vertice]

a = grafo.Grafo( orientado=True, valorado=True)
criarVertices(a, 20)
criarArestas(a, 35)
a.mostraVertices()
a.mostraListaDeArestas()
a.mostraListaDeAdjacencias()
a.mostraMatrizDeAdjacencias()
a.mostraMatrizDeIncidencias()


for i in range(len(a.vertices)):
    relatorioDijkstra(a, i)

saida = open('saida.dot', 'w')
saida.write(a.paraGraphviz())
saida.close()
