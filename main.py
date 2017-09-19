#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import grafo, random, sys




a = grafo.Grafo(valorado=True)
grafo.criarVertices(a, 50)
grafo.criarArestas(a, 100)
a.mostraVertices()
a.mostraListaDeArestas()
a.mostraListaDeAdjacencias()
a.mostraMatrizDeAdjacencias()
a.mostraMatrizDeIncidencias()


for i in range(len(a.vertices)):
    grafo.relatorioDijkstraEmCores(a, i)

saida = open('saida.dot', 'w')
saida.write(a.paraGraphviz())
saida.close()
