#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#trabalho 1 - representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import random


class Grafo():
    vertices = []
    arestas = []
    listaDeAdjacencias = []
    matrizDeAdjacencias = [[0]]
    matrizDeIncidencias = []

    orientado = False
    valorado = False

    def __init__(self, orientado, valorado):
        self.orientado = orientado
        self.valorado = valorado

    def adicionarVertice(self, nomeDoVertice):
        self.vertices.append(nomeDoVertice)
        self.listaDeAdjacencias.append([])

        if(len(self.vertices)) > 1:
            for i in self.matrizDeAdjacencias:
                i.append(0)
            self.matrizDeAdjacencias.append([0] * len(self.vertices))


    #arestas recebem nome, índice do vértice de origem, índice do vértice de
    #destino, e valor é opcional
    def adicionarAresta(self, nome: str, origem: int, destino: int, valor=1):
        self.arestas.append((nome.upper(), origem, destino, valor))
        self.listaDeAdjacencias[origem].append((destino, valor))
        if not self.orientado:
            self.listaDeAdjacencias[destino].append((origem, valor))

        #adicionar na matriz de adjacências
        self.matrizDeAdjacencias[origem][destino] += 1 * valor
        if not self.orientado:
            self.matrizDeAdjacencias[destino][origem] += 1 * valor

        #adicionar na lista de incidências
        colunaNova = [0] * len(self.vertices)
        colunaNova[origem] += 1 * valor
        if not self.orientado:
            colunaNova[destino] += 1 * valor
        else:
            #não está claro o que acontece com loops em dígrafos, mas como
            #a matriz de incidência se preocupa mais com caminhos, podemos deixar tudo 0
            #na coluna
            colunaNova[destino] -= 1 * valor
        self.matrizDeIncidencias.append(colunaNova)

    def mostraVertices(self):
        print()
        print("Vértices:", self.vertices)

    def mostraListaDeArestas(self):
        print()
        print("Lista de arestas:")
        for aresta in self.arestas:
            if self.orientado:
                print(aresta)
            else:
                print(str(aresta).replace('(','{').replace(')','}'))

    def mostraListaDeAdjacencias(self):
        print()
        print("Lista de adjacências:")
        for i in range(len(self.vertices)):
            resto = [(self.vertices[j[0]], j[1]) for j in self.listaDeAdjacencias[i]]
            print(self.vertices[i]+ ": " + str(resto))

    def mostraMatrizDeAdjacencias(self):
        print()
        print("Matriz de adjacências:")
        cabecalho = "*****"
        for w in range(len(self.vertices)):
            cabecalho += " " + '{:>4}'.format(self.vertices[w])
        print(cabecalho)
        for v in range(len(self.vertices)):
            print('{:>4}'.format(self.vertices[v]) + "|", end='')
            for w in range(len(self.vertices)):
                print (" " + '{:>4}'.format(self.matrizDeAdjacencias[v][w]), end='')
            print()

    def mostraMatrizDeIncidencias(self):
        print()
        print("Matriz de incidências:")
        cabecalho = "*****"
        for w in range(len(self.matrizDeIncidencias)):
            cabecalho += " " + '{:>4}'.format("E" + str(w+1))
        print(cabecalho)
        for v in range(len(self.vertices)):
            print('{:>4}'.format(self.vertices[v]) + "|", end='')
            for w in range(len(self.matrizDeIncidencias)):
                print (" " + '{:>4}'.format(self.matrizDeIncidencias[w][v]), end='')
            print()

    def paraGraphviz(self):
        if self.orientado:
            saida = "digraph "
            seta = " -> "
        else:
            saida = "graph "
            seta = " -- "
        saida += "\"grafo\" {\nnode [width=1.0,height=1.0];\n"
        for v in range(len(self.vertices)):
            saida += "N" + str(v+1) + " [label=\"" + self.vertices[v]
            saida += "\",fontsize=24];\n"
        for a in range(len(self.arestas)):
            posVerticeA = self.vertices.index(self.arestas[a][0])
            posVerticeB = self.vertices.index(self.arestas[a][1])
            if valorado:
                valorAresta = self.aArestas[a][2]
            saida += "N" + str(posVerticeA + 1) + seta
            saida += "N" + str(posVerticeB + 1) + " ["
            if valorado:
                saida += "label=" + str(valorAresta) + ","
            saida += "weight=1,style=\"setlinewidth(2.0)\",fontsize=20];\n"
        saida += "}"
        return saida
