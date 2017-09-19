#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#trabalho 1 - representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import random, grafo

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

    meuGrafo = grafo.Grafo(orientado, valorado)
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

    grafo.criarVertices(meuGrafo, qtVertices)

    print("*** Definição de arestas ***")

    seDefineArestas = ""
    while(seDefineArestas not in ["1", "2"]):
        print("Deseja escolher arestas, ou quer que o programa crie-as aleatoriamente?")
        print("1 - Definir manualmente")
        print("2 - Criar aleatoriamente")
        seDefineArestas = input()

    if(seDefineArestas == "1"):
        cancelou = False
        while(cancelou == False):
            print()
            print("A qualquer ponto, para encerrar a criação de arestas, digite \"sair\"")
            strEntrada = ""
            while(cancelou == False and strEntrada.upper() not in meuGrafo.vertices):
                print("Qual o vértice de entrada?")
                print("Vértices permitidos: " + ', '.join(meuGrafo.vertices))
                strEntrada = input().upper()
                if(strEntrada == "SAIR"):
                    cancelou = True
            strSaida = ""
            while(cancelou == False and strSaida.upper() not in meuGrafo.vertices):
                print("Qual o vértice de saída?")
                print("Vértices permitidos: " + ', '.join(meuGrafo.vertices))
                strSaida = input().upper()
                if(strSaida == "SAIR"):
                    cancelou = True
            strValor = ""
            if valorado:
                valor = 0 #será definido pelo usuário
            else:
                valor = 1
            while(cancelou == False and valor <= 0 and valorado):
                print("Qual o valor da aresta?")
                print("Valor deve ser um número inteiro, maior que zero")
                strValor = input()
                if(strValor.upper() == "SAIR"):
                    cancelou = True
                try:
                    valor = int(strValor)
                except ValueError:
                    valor = 0
            if(cancelou == False):
                meuGrafo.adicionarAresta("E"+str(len(meuGrafo.arestas) + 1),
                meuGrafo.vertices.index(strEntrada),
                meuGrafo.vertices.index(strSaida), valor)
    else:
        strQtArestasAleatorias = ""
        qtArestasAleatorias = 0
        while(qtArestasAleatorias <= 0):
            print("Quantas arestas serão criadas?")
            print("Escolha um valor maior que 0")
            strQtArestasAleatorias = input()
            try:
                qtArestasAleatorias = int(strQtArestasAleatorias)
            except ValueError:
                qtArestasAleatorias = 0
        grafo.criarArestas(meuGrafo, qtArestasAleatorias)

    #mostrar as representações
    meuGrafo.mostraVertices()
    meuGrafo.mostraListaDeArestas()
    meuGrafo.mostraListaDeAdjacencias()
    meuGrafo.mostraMatrizDeAdjacencias()
    meuGrafo.mostraMatrizDeIncidencias()
    saida = open('saida.dot', 'w')
    saida.write(meuGrafo.paraGraphviz())
    saida.close()
    print("Uma representação do grafo para uso do programa")
    print("dot do pacote graphviz foi salva em saida.dot")

    print("*** Algoritmo de Dijkstra ***")

    seDijkstra = ""
    while(seDijkstra not in ["1", "2", "3"]):
        print("Deseja executar o algoritmo de Dijkstra?")
        print("1 - Sim, escolhendo o vértice de origem")
        print("2 - Sim, para todos os vértices")
        print("3 - Não")
        seDijkstra = input()

    if seDijkstra == "1":
        cancelou = False
        while(cancelou == False):
            print()
            print("A qualquer ponto, para encerrar a execução de Dijkstra, digite \"sair\"")
            strVerticeDijkstra = ""
            while cancelou == False and strVerticeDijkstra.upper() not in meuGrafo.vertices:
                print("Qual o vértice de origem?")
                print("Vértices permitidos: " + ', '.join(meuGrafo.vertices))
                strVerticeDijkstra = input().upper()
                if strVerticeDijkstra == "SAIR":
                    cancelou = True
            if cancelou == False:
                grafo.relatorioDijkstra(meuGrafo, meuGrafo.vertices.index(strVerticeDijkstra))
    elif seDijkstra == "2":
        for v in range(len(meuGrafo.vertices)):
            grafo.relatorioDijkstra(meuGrafo, v)


if __name__ == "__main__":
    main()
