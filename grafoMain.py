#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#trabalho 1 - representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro


vertices = []
listaDeArestas = []

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

    print("*** Definição de arestas ***")
    cancelou = False
    while(cancelou == False):
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
            adicionarAresta(strEntrada, strSaida)

    #mostrar as representações
    mostraVertices()
    mostraListaDeArestas()

def criarVertices(quantidade: int):
    for i in range(quantidade):
        vertices.append("V"+str(i+1))

def adicionarAresta(entrada: str, saida: str):
    nomeDaAresta = "E" + str(len(listaDeArestas) + 1)
    listaDeArestas.append((nomeDaAresta, entrada.upper(), saida.upper()))

def mostraVertices():
    print("Vértices:", vertices)

def mostraListaDeArestas():
    print("Arestas:")
    for aresta in listaDeArestas:
        print(aresta)

if __name__ == "__main__":
    main()
