#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#trabalho 1 - representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import random



def main():

    vertices = []

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

    criarVertices(vertices, qtVertices)

    listaDeArestas = novaListaDeArestas()
    listaDeAdjacencias = novaListaDeAdjacencias(qtVertices)
    matrizDeAdjacencias = novaMatrizDeAdjacencias(qtVertices)
    matrizDeIncidencias = novaMatrizDeIncidencias()

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
                adicionarAresta(vertices, strEntrada, strSaida, listaDeArestas,
                listaDeAdjacencias, matrizDeAdjacencias, matrizDeIncidencias,
                orientado, valorado, valor)
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
        for i in range(qtArestasAleatorias):
            if valorado:
                valor = random.choice(range(1,11))
            else:
                valor = 1
            adicionarAresta(vertices, random.choice(vertices), random.choice(vertices),
            listaDeArestas, listaDeAdjacencias,
            matrizDeAdjacencias, matrizDeIncidencias,
            orientado, valorado, valor)

    #mostrar as representações
    mostraVertices(vertices)
    mostraListaDeArestas(listaDeArestas, orientado)
    mostraListaDeAdjacencias(vertices, listaDeAdjacencias)
    mostraMatrizDeAdjacencias(vertices, matrizDeAdjacencias)
    mostraMatrizDeIncidencias(vertices, matrizDeIncidencias)
    saida = open('saida.dot', 'w')
    saida.write(paraGraphviz(vertices, listaDeArestas, orientado, valorado))
    saida.close()
    print("Uma representação do grafo para uso do programa")
    print("dot do pacote graphviz foi salva em saida.dot")

def criarVertices(vertices, quantidade: int):
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

def adicionarAresta(vertices, entrada: str, saida: str, listaAr, listaAd,
matrizA, matrizI, orientado: bool, valorado: bool, valor: int):
    nomeDaAresta = "E" + str(len(listaAr) + 1)

    #adicionar na lista de arestas
    if not valorado:
        listaAr.append((entrada.upper(), saida.upper()))
    else:
        listaAr.append((entrada.upper(), saida.upper(), valor))

    #encontrar os vértices digitados na lista de vértices,
    #agilizando as próximas representações
    i = vertices.index(entrada.upper())
    j = vertices.index(saida.upper())

    #adicionar na lista de adjacências
    if not valorado:
        listaAd[i].append([saida.upper()])
        if not orientado:
            listaAd[j].append([entrada.upper()])
    else:
        listaAd[i].append([saida.upper(), valor])
        if not orientado:
            listaAd[j].append([entrada.upper(), valor])

    #adicionar na matriz de adjacências
    matrizA[i][j] += 1 * valor
    if not orientado:
        matrizA[j][i] += 1 * valor

    #adicionar na lista de incidências
    colunaNova = [0] * len(vertices)
    colunaNova[i] += 1 * valor
    if not orientado:
        colunaNova[j] += 1 * valor
    else:
        #não está claro o que acontece com loops em dígrafos, mas como
        #a matriz de incidência se preocupa mais com caminhos, podemos deixar tudo 0
        #na coluna
        colunaNova[j] -= 1 * valor
    matrizI.append(colunaNova)

def mostraVertices(vertices):
    print()
    print("Vértices:", vertices)

def mostraListaDeArestas(lista, orientado: bool):
    print()
    print("Lista de arestas:")
    for aresta in lista:
        if orientado:
            print(aresta)
        else:
            print(str(aresta).replace('(','{').replace(')','}'))


def mostraListaDeAdjacencias(vertices, lista):
    print()
    print("Lista de adjacências:")
    for i in range(len(vertices)):
        print(vertices[i]+ ": " + str(lista[i]))

def mostraMatrizDeAdjacencias(vertices, matriz):
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

def mostraMatrizDeIncidencias(vertices, matriz):
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

def paraGraphviz(listaDeVertices, listaDeArestas, orientado, valorado):
    if orientado:
        saida = "digraph "
        seta = " -> "
    else:
        saida = "graph "
        seta = " -- "
    saida += "\"grafo\" {\nnode [width=1.0,height=1.0];\n"
    for v in range(len(listaDeVertices)):
        saida += "N" + str(v+1) + " [label=\"" + listaDeVertices[v]
        saida += "\",fontsize=24];\n"
    for a in range(len(listaDeArestas)):
        posVerticeA = listaDeVertices.index(listaDeArestas[a][0])
        posVerticeB = listaDeVertices.index(listaDeArestas[a][1])
        if valorado:
            valorAresta = listaDeArestas[a][2]
        saida += "N" + str(posVerticeA + 1) + seta
        saida += "N" + str(posVerticeB + 1) + " ["
        if valorado:
            saida += "label=" + str(valorAresta) + ","
        saida += "weight=1,style=\"setlinewidth(2.0)\",fontsize=20];\n"
    saida += "}"
    return saida

if __name__ == "__main__":
    main()
