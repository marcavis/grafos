#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import grafo, random

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

a = grafo.Grafo(False, False)
a.adicionarVertice('V1')
a.adicionarVertice('V2')
a.adicionarVertice('V3')
criarVertices(a, 15)
a.adicionarAresta('E1', 0, 1)
a.adicionarAresta('E2', 1, 2)
a.adicionarAresta('E3', 0, 2)
criarArestas(a, 35)
a.mostraVertices()
a.mostraListaDeArestas()
a.mostraListaDeAdjacencias()
a.mostraMatrizDeAdjacencias()
a.mostraMatrizDeIncidencias()
