#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#trabalho 1 - representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro


vertices = []

def main():

    seOrientado = ""
    while(seOrientado not in ["1", "2"]):
        print("Qual o tipo de grafo? Não-orientado, ou Orientado?")
        print("1 - Não-orientado")
        print("2 - Orientado")
        seOrientado = input()

    if(seOrientado == "1"):
        orientado = False
    else:
        orientado = True

    seValorado = ""
    while(seValorado not in ["1", "2"]):
        print("O grafo é valorado ou não-valorado?")
        print("1 - Não-valorado")
        print("2 - Valorado")
        seValorado = input()

    if(seValorado == "1"):
        valorado = False
    else:
        valorado = True

    strQtVertices = ""
    qtVertices = 0
    while(qtVertices <= 0):
        print("Quantos vértices no grafo?")
        print("Escolha um valor maior que 0")
        strQtVertices = input()
        try:
            qtVertices = int(strQtVertices)
        except ValueError:
            qtVertices = 0

    criarVertices(qtVertices)

    listaDeArestas = novaListaDeArestas()
    listaDeAdjacencias = novaListaDeAdjacencias(qtVertices)
    matrizDeAdjacencias = novaMatrizDeAdjacencias(qtVertices)
    matrizDeIncidencias = novaMatrizDeIncidencias()

    print("*** Definição de arestas ***")
    cancelou = False
    while(cancelou == False):
        print()
        print("A qualquer ponto, para encerrar a criação de arestas, digite \"sair\"")
        strEntrada = ""
        while(cancelou == False and strEntrada.upper() not in vertices):
            print("Qual o vértice de entrada?")
            print("Vértices permitidos: do V1 ao V" + str(qtVertices))
            strEntrada = input()
            if(strEntrada.upper() == "SAIR"):
                cancelou = True
        strSaida = ""
        while(cancelou == False and strSaida.upper() not in vertices):
            print("Qual o vértice de saída?")
            print("Vértices permitidos: do V1 ao V" + str(qtVertices))
            strSaida = input()
            if(strSaida.upper() == "SAIR"):
                cancelou = True
        if(cancelou == False):
            adicionarAresta(strEntrada, strSaida, listaDeArestas,
            listaDeAdjacencias, matrizDeAdjacencias, matrizDeIncidencias)

    #mostrar as representações
    mostraVertices()
    mostraListaDeArestas(listaDeArestas)
    mostraListaDeAdjacencias(listaDeAdjacencias)
    mostraMatrizDeAdjacencias(matrizDeAdjacencias)
    mostraMatrizDeIncidencias(matrizDeIncidencias)

def criarVertices(quantidade: int):
    for i in range(quantidade):
        vertices.append("V"+str(i+1))

def novaListaDeArestas():
    return []

def novaListaDeAdjacencias(quantidade: int):
    return [ [] for i in range(quantidade)]

def novaMatrizDeAdjacencias(quantidade: int):
    #retorna uma matriz i x i onde i é a qtde. vértices
    return [ [0]*quantidade for i in range(quantidade) ]

def novaMatrizDeIncidencias():
    return []

def adicionarAresta(entrada: str, saida: str, listaAr, listaAd, matrizA, matrizI):
    nomeDaAresta = "E" + str(len(listaAr) + 1)

    #adicionar na lista de arestas
    listaAr.append((entrada.upper(), saida.upper()))

    #adicionar na lista de adjacências
    listaAd[vertices.index(entrada.upper())].append(saida.upper())

    i = vertices.index(entrada.upper())
    j = vertices.index(saida.upper())

    #adicionar na matriz de adjacências
    matrizA[i][j] += 1
    matrizA[j][i] += 1

    #adicionar na lista de incidências
    colunaNova = [0] * len(vertices)
    colunaNova[i] += 1
    colunaNova[j] += 1
    matrizI.append(colunaNova)

def mostraVertices():
    print()
    print("Vértices:", vertices)

def mostraListaDeArestas(lista):
    print()
    print("Lista de arestas:")
    for aresta in lista:
        print(aresta)

def mostraListaDeAdjacencias(lista):
    print()
    print("Lista de adjacências:")
    for i in range(len(vertices)):
        print(vertices[i]+ ": " + str(lista[i]))

def mostraMatrizDeAdjacencias(matriz):
    print()
    print("Matriz de adjacências:")
    cabecalho = "*****"
    for w in range(len(vertices)):
        cabecalho += " " + '{:>4}'.format(vertices[w])
    print(cabecalho)
    for v in range(len(vertices)):
        print('{:>4}'.format(vertices[v]) + "|", end='')
        for w in range(len(vertices)):
            print (" " + '{:>4}'.format(matriz[v][w]), end='')
        print()

def mostraMatrizDeIncidencias(matriz):
    print()
    print("Matriz de incidências:")
    cabecalho = "*****"
    for w in range(len(matriz)):
        cabecalho += " " + '{:>4}'.format("E" + str(w+1))
    print(cabecalho)
    for v in range(len(vertices)):
        print('{:>4}'.format(vertices[v]) + "|", end='')
        for w in range(len(matriz)):
            print (" " + '{:>4}'.format(matriz[w][v]), end='')
        print()

if __name__ == "__main__":
    main()
