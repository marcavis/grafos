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

    listaDeArestas = novaListaDeArestas() #não faz nada, mas é bom constar
    listaDeAdjacencias = novaListaDeAdjacencias(qtVertices)

    print(vertices)
    print(listaDeAdjacencias)

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
            adicionarAresta(strEntrada, strSaida, listaDeArestas, listaDeAdjacencias)

    #mostrar as representações
    mostraVertices()
    mostraListaDeArestas(listaDeArestas)
    mostraListaDeAdjacencias(listaDeAdjacencias)

def criarVertices(quantidade: int):
    for i in range(quantidade):
        vertices.append("V"+str(i+1))

def novaListaDeArestas():
    return []

def novaListaDeAdjacencias(quantidade: int):
    return [ [] for i in range(quantidade)]

def adicionarAresta(entrada: str, saida: str, listaAr, listaAd):
    nomeDaAresta = "E" + str(len(listaAr) + 1)

    #adicionar na lista de arestas
    listaAr.append((nomeDaAresta, entrada.upper(), saida.upper()))

    #adicionar na lista de adjacências
    listaAd[vertices.index(entrada.upper())].append(saida.upper())

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
    for i in range(len(vertices)):
        print(vertices[i]+ ": " + str(lista[i]))

if __name__ == "__main__":
    main()
