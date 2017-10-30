#!/usr/bin/env python3
import grafo as lib_grafo
class Sudoku():
    def __init__(self, matriz=[]):
        if matriz == []:
            self.matriz = self.novaMatriz()
        else:
            self.matriz = matriz
        self.grafo = lib_grafo.Grafo()
        lib_grafo.criarVertices(self.grafo, 81)
        self.criarArestasNoGrafo()

    def novaMatriz(self):
        return [[None] * 9] * 9

    #def posicaoNaMatriz(self, vertice):
    #    return(vertice / 9, vertice % 9)

    def indiceDoVertice(self, linha, coluna):
        return linha * 9 + coluna

    def criarArestasNoGrafo(self):
        #conexões horizontais:
        for i in range(9):
            for j in range(9):
                for j2 in range(9):
                    vertice1 = self.indiceDoVertice(i, j)
                    vertice2 = self.indiceDoVertice(i, j2)
                    if (vertice1 != vertice2 and self.grafo.matrizDeAdjacencias[vertice1][vertice2] == 0):
                        self.grafo.adicionarAresta('', vertice1, vertice2)
        #conexões verticais:
        for i in range(9):
            for i2 in range(9):
                for j in range(9):
                    vertice1 = self.indiceDoVertice(i, j)
                    vertice2 = self.indiceDoVertice(i2, j)
                    if (vertice1 != vertice2 and self.grafo.matrizDeAdjacencias[vertice1][vertice2] == 0):
                        self.grafo.adicionarAresta('', vertice1, vertice2)
        #conexões dentro dos quadrados:
        for i in range(3):
            for j in range(3):
                quadrado = self.verticesDoQuadrado(i, j)
                for vertice1 in quadrado:
                    for vertice2 in quadrado:
                        if (vertice1 != vertice2 and self.grafo.matrizDeAdjacencias[vertice1][vertice2] == 0):
                            self.grafo.adicionarAresta('', vertice1, vertice2)


    def verticesDoQuadrado(self, i, j):
        return [self.indiceDoVertice(i*3+k, j*3+l) for k in [0,1,2] for l in [0,1,2]]


    def __str__(self):
        return "olá"

#s = Sudoku()
t = Sudoku([[None,   3,None,None,None,   5,   1,   7,None],
            [   5,None,None,None,   3,None,None,None,   2],
            [None,None,None,None,   2,None,None,None,   6],
            [None,None,None,None,   7,None,None,None,   9],
            [None,   1,   6,None,None,None,   2,   3,None],
            [   9,None,None,None,   8,None,None,None,None],
            [   6,None,None,None,   1,None,None,None,None],
            [   1,None,None,None,   9,None,None,None,   8],
            [None,   7,   8,   6,None,None,None,   4,None]])
print(t)
t.grafo.mostraVertices()
t.grafo.mostraListaDeArestas()
t.grafo.mostraListaDeAdjacencias()
#t.grafo.mostraMatrizDeAdjacencias()
#t.grafo.mostraMatrizDeIncidencias()

saida = open('saida.dot', 'w')
saida.write(t.grafo.paraGraphviz())
saida.close()

lib_grafo.coloracao(t.grafo)
