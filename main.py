#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import grafo, random, sys, os, subprocess
from timeit import default_timer as timer

def visualizacoesDijkstra(a: grafo.Grafo):
    #Apagar todas as visualizações anteriores de grafos de dijkstra
    for f in os.listdir("."):
        if 'dijkstra' in f:
            os.remove(f)
    for i in range(len(a.vertices)):
        saida = open('dijkstra' + a.vertices[i] + '.dot', 'w')
        saida.write(grafo.relatorioDijkstraEmCores(a, i))
        saida.close()
        subprocess.check_output(['dot', '-Tpng', '-Grankdir=LR', 'dijkstra' + a.vertices[i] + '.dot', '-o',
        'dijkstra' + a.vertices[i] + '.png'])
        print('Visualização do grafo do vértice ' + a.vertices[i] + ' completa')

#para testar dijkstra
# a = grafo.Grafo(orientado=True,valorado=True)
# grafo.criarVertices(a, 20)
# grafo.criarArestas(a, 45)
# a.mostraVertices()
# a.mostraListaDeArestas()
# a.mostraListaDeAdjacencias()
# a.mostraMatrizDeAdjacencias()
# a.mostraMatrizDeIncidencias()

#precisa do programa Dot do Graphviz instalado
# visualizacoesDijkstra(a)

# for i in range(len(a.vertices)):
#     grafo.relatorioDijkstra(a, i)

a = grafo.Grafo(orientado=False,valorado=True)
grafo.criarVertices(a, 20)
grafo.criarArestasSimples(a, 45)
a.mostraVertices()
a.mostraListaDeArestas()
a.mostraListaDeAdjacencias()
a.mostraMatrizDeAdjacencias()
a.mostraMatrizDeIncidencias()

saida = open('saida.dot', 'w')
saida.write(a.paraGraphviz())
saida.close()

saida = open('kruskal.dot', 'w')
saida.write(grafo.relatorioKruskalEmCores(a))
saida.close()

grafo.primJarnik(a)
