#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#trabalho 1 - representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import random, sys


class Grafo():

    def __init__(self, orientado=False, valorado=False):
        self.orientado = orientado
        self.valorado = valorado
        self.vertices = []
        self.arestas = []
        self.listaDeAdjacencias = []
        self.matrizDeAdjacencias = [[0]]
        self.matrizDeIncidencias = []

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

    def reordenarArestas(self):
        self.arestas.sort(key=lambda x: int(x[0][1:]))

    def grau(self, vertice):
        return len(self.listaDeAdjacencias[vertice])

    def saoAdjacentes(self, v1, v2):
        for aresta in self.listaDeAdjacencias[v1]:
            if v2 == aresta[0]:
                return True
        for aresta in self.listaDeAdjacencias[v2]:
            if v1 == aresta[0]:
                return True
        return False

    #se existir alguma distância infinita entre quaisquer vértices, o
    #grafo não é conexo
    def ehConexo(self):
        for v in range(len(self.vertices)):
            for distancia in bellmanFord(self, v)[0]:
                if distancia == sys.maxsize:
                    return False
        return True

    def temArestasNegativas(self):
        for a in self.arestas:
            if a[3] < 0:
                return True
        return False

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
            cabecalho += " " + '{:>4}'.format(self.arestas[w][0])
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
            saida += "N" + str(self.arestas[a][1] + 1) + seta #origem
            saida += "N" + str(self.arestas[a][2] + 1) + " [" #destino
            if self.valorado:
                saida += "label=" + str(self.arestas[a][3]) + ","
            saida += "weight=1,style=\"setlinewidth(2.0)\",fontsize=20];\n"
        saida += "}"
        return saida

def criarVertices(grafo: Grafo, quantidade: int):
    ultimoVertice = len(grafo.vertices) + 1
    for i in range(quantidade):
        grafo.adicionarVertice("V" + str(ultimoVertice + i))

def criarArestas(grafo: Grafo, quantidade, valorMinimo = 1, valorMaximo = 10):
    ultimaAresta = len(grafo.arestas) + 1
    for i in range(quantidade):
        if grafo.valorado:
            valor = random.randint(valorMinimo, valorMaximo)
        else:
            valor = 1
        origem = random.randint(0, len(grafo.vertices) - 1)
        destino = random.randint(0, len(grafo.vertices) - 1)
        grafo.adicionarAresta("E" + str(ultimaAresta + i), origem, destino, valor)

#como a função anterior, mas não cria laços nem repete arestas
def criarArestasSimples(grafo: Grafo, quantidade, valorMinimo = 1, valorMaximo = 10):
    ultimaAresta = len(grafo.arestas) + 1
    ordem = range(len(grafo.vertices))
    if grafo.orientado:
        arestasPossiveis = [(x, y) for x in ordem for y in ordem if x != y]
    else:
        arestasPossiveis = [(x, y) for x in ordem for y in ordem if x > y]
    limiteDeArestas = len(arestasPossiveis)
    for i in range(min(quantidade, limiteDeArestas)):
        if grafo.valorado:
            valor = random.randint(valorMinimo, valorMaximo)
        else:
            valor = 1
        selecionada = arestasPossiveis.pop(random.randint(0, len(arestasPossiveis) - 1))
        origem = selecionada[0]
        destino = selecionada[1]
        grafo.adicionarAresta("E" + str(ultimaAresta + i), origem, destino, valor)

def dijkstra(grafo: Grafo, origem):
    if grafo.temArestasNegativas():
        raise Exception("ERRO: GRAFO TEM ARESTAS NEGATIVAS")

    distancias = []
    precursores = []
    for v in range(len(grafo.vertices)):
        if v == origem:
            distancias.append(0)
            precursores.append(None)
        else:
            distancias.append(sys.maxsize)
            precursores.append(None)
    fila = [origem]

    while len(fila) > 0:
        v = fila.pop(0)
        for w in grafo.listaDeAdjacencias[v]:

            if distancias[v] + w[1] < distancias[w[0]]:
                fila.append(w[0])
                distancias[w[0]] = distancias[v] + w[1]
                precursores[w[0]] = v
        #ordenar os vertices conforme as distancias da origem
        fila.sort(key=lambda x: distancias[x])

    return(distancias, precursores)

#executa o algoritmo, e retorna informação de quais
#arestas foram ignoradas, visitadas mas obsoletas, e usadas definitivamente.
def dijkstraEmCores(grafo: Grafo, origem):
    if grafo.temArestasNegativas():
        raise Exception("ERRO: GRAFO TEM ARESTAS NEGATIVAS")

    distancias = []
    precursores = []
    usoDeArestas = [0] * len(grafo.arestas)
    for v in range(len(grafo.vertices)):
        if v == origem:
            distancias.append(0)
            precursores.append(None)
        else:
            distancias.append(sys.maxsize)
            precursores.append(None)
    fila = [origem]

    while len(fila) > 0:
        v = fila.pop(0)
        for w in grafo.listaDeAdjacencias[v]:

            if distancias[v] + w[1] < distancias[w[0]]:
                for e in range(len(grafo.matrizDeIncidencias)):
                    if (abs(grafo.matrizDeIncidencias[e][v]) == w[1]) and (abs(grafo.matrizDeIncidencias[e][w[0]]) == w[1]):
                        usoDeArestas[e] = 1
                        break
                fila.append(w[0])
                distancias[w[0]] = distancias[v] + w[1]
                precursores[w[0]] = v
        #ordenar os vertices conforme as distancias da origem
        fila.sort(key=lambda x: distancias[x])

    return(distancias, precursores, usoDeArestas)

def relatorioDijkstra(meuGrafo, origem):
    distancias, precursores = dijkstra(meuGrafo, origem)
    print()
    print("Dijkstra: Distâncias a partir do vértice " + meuGrafo.vertices[origem] + ":")
    print("***** Distância | Anterior | Caminho Completo")
    for v in range(len(meuGrafo.vertices)):
        print('{:>4}'.format(meuGrafo.vertices[v]) + "| ", end='')
        dist = "∞" if distancias[v] == sys.maxsize else distancias[v]
        print('{:>9}'.format(dist) + " | ", end='')
        prec = "--" if precursores[v] == None else meuGrafo.vertices[precursores[v]]
        print('{:>8}'.format(prec) + " | ", end='')
        print(backtrack(v, meuGrafo, precursores), end='')
        print()

def relatorioDijkstraEmCores(meuGrafo, origem):
    distancias, precursores, usoDeArestas = dijkstraEmCores(meuGrafo, origem)
    print()
    print("Dijkstra: Distâncias a partir do vértice " + meuGrafo.vertices[origem] + ":")
    print("***** Distância | Anterior | Caminho Completo")
    for v in range(len(meuGrafo.vertices)):
        print('{:>4}'.format(meuGrafo.vertices[v]) + "| ", end='')
        dist = "∞" if distancias[v] == sys.maxsize else distancias[v]
        print('{:>9}'.format(dist) + " | ", end='')
        prec = "--" if precursores[v] == None else meuGrafo.vertices[precursores[v]]
        print('{:>8}'.format(prec) + " | ", end='')
        print(backtrack(v, meuGrafo, precursores), end='')
        print()

    if meuGrafo.orientado:
        saida = "digraph "
        seta = " -> "
    else:
        saida = "graph "
        seta = " -- "
    saida += "\"grafo\" {\nnode [width=1.0,height=1.0];\n"
    saida += "label=\"Dijkstra a partir do vértice " + meuGrafo.vertices[origem] + "\";\n"
    saida += "fontsize=32;\n"
    for v in range(len(meuGrafo.vertices)):
        saida += "N" + str(v+1) + " [label=\"" + meuGrafo.vertices[v]
        if v == origem:
            saida += "\",color=\"blue\",fontcolor=\"blue\","
        else:
            dist = "∞" if distancias[v] == sys.maxsize else distancias[v]
            saida += "\n" + str(dist) + "\""
            if dist == "∞":
                saida += "color=\"red\",fontcolor=\"red\","
            else:
                saida += "color=\"darkgreen\",fontcolor=\"darkgreen\","
        saida += "fontsize=24];\n"
    for a in range(len(meuGrafo.arestas)):
        saida += "N" + str(meuGrafo.arestas[a][1] + 1) + seta #origem
        saida += "N" + str(meuGrafo.arestas[a][2] + 1) + " [" #destino
        if meuGrafo.valorado:
            saida += "label=" + str(meuGrafo.arestas[a][3]) + ","
        if usoDeArestas[a] == 1:
            saida += "color=\"darkgreen\",fontcolor=\"darkgreen\","
        else:
            saida += "color=\"red\",fontcolor=\"red\","
        saida += "weight=1,style=\"setlinewidth(2.0)\",fontsize=20];\n"
    saida += "}"
    return saida

def backtrack(vertice: int, meuGrafo, precursores):
    caminho = []
    atual = vertice
    while precursores[atual] != None:
        caminho = [meuGrafo.vertices[precursores[atual]]] + caminho
        atual = precursores[atual]
    saida = ''.join([x + " -> " for x in caminho])
    return saida + meuGrafo.vertices[vertice]

#usado pelo Bellman-Ford em grafos não-orientados
def duplicarArestas(arestas):
    resultado = []
    for a in arestas:
        resultado.append(a)
        resultado.append((a[0], a[2], a[1], a[3]))
    return resultado

def bellmanFord(meuGrafo: Grafo, origem: int):
    if meuGrafo.orientado:
        arestasBF = meuGrafo.arestas
    else:
        arestasBF = duplicarArestas(meuGrafo.arestas)

    distancias = []
    precursores = []
    for v in range(len(meuGrafo.vertices)):
        if v == origem:
            distancias.append(0)
            precursores.append(None)
        else:
            distancias.append(sys.maxsize)
            precursores.append(None)

    for iteracao in range(len(meuGrafo.vertices) - 1):
        semMudancas = True
        for e in arestasBF:
            origem, destino, valor = e[1], e[2], e[3]
            if (distancias[origem] + valor < distancias[destino] and
            distancias[origem] != sys.maxsize):
                distancias[destino] = distancias[origem] + valor
                precursores[destino] = origem
                semMudancas = False
        if semMudancas == True:
            break

    for e in arestasBF:
        origem, destino, valor = e[1], e[2], e[3]
        if (distancias[origem] + valor < distancias[destino] and
        distancias[origem] != sys.maxsize):
            raise Exception("ERRO: GRAFO TEM CICLO NEGATIVO")
    return(distancias, precursores)

def relatorioBellmanFord(meuGrafo, origem):
    distancias, precursores = bellmanFord(meuGrafo, origem)
    print()
    print("Bellman-Ford: Distâncias a partir do vértice " + meuGrafo.vertices[origem] + ":")
    print("***** Distância | Anterior | Caminho Completo")
    for v in range(len(meuGrafo.vertices)):
        print('{:>4}'.format(meuGrafo.vertices[v]) + "| ", end='')
        dist = "∞" if distancias[v] == sys.maxsize else distancias[v]
        print('{:>9}'.format(dist) + " | ", end='')
        prec = "--" if precursores[v] == None else meuGrafo.vertices[precursores[v]]
        print('{:>8}'.format(prec) + " | ", end='')
        print(backtrack(v, meuGrafo, precursores), end='')
        print()

def simplificarGrafo(meuGrafo):
    novoGrafo = Grafo(meuGrafo.orientado, meuGrafo.valorado)
    for vertice in meuGrafo.vertices[:]:
        novoGrafo.adicionarVertice(vertice)
    incluirAresta = [True for aresta in meuGrafo.arestas]
    #excluir arestas que são loops
    for a in range(len(meuGrafo.arestas)):
        if meuGrafo.arestas[a][1] == meuGrafo.arestas[a][2]:
            incluirAresta[a] = False
        for b in range(len(meuGrafo.arestas)):
            if a != b:
                if (meuGrafo.arestas[a][1] == meuGrafo.arestas[b][1] and
                meuGrafo.arestas[a][2] == meuGrafo.arestas[b][2]):
                    if meuGrafo.arestas[a][3] > meuGrafo.arestas[b][3]:
                        incluirAresta[a] = False

    for a in range(len(meuGrafo.arestas)):
        if incluirAresta[a]:
            aresta = meuGrafo.arestas[a]
            novoGrafo.adicionarAresta(aresta[0], aresta[1], aresta[2], aresta[3])
    novoGrafo.reordenarArestas()
    return novoGrafo

#Como Floyd-Warshall trabalha com a matriz de adjacências, ele deve primeiro
#excluir as arestas múltiplas e loops
def floydWarshall(meuGrafo):
    novoGrafo = simplificarGrafo(meuGrafo)
    ordem = len(novoGrafo.vertices)

    dist = [[sys.maxsize for x in range(ordem)] for x in range(ordem)]
    for x in range(ordem):
        dist[x][x] = 0
    for a in range(len(novoGrafo.arestas)):
        origem = novoGrafo.arestas[a][1]
        destino = novoGrafo.arestas[a][2]
        dist[origem][destino] = novoGrafo.arestas[a][3]
        if not meuGrafo.orientado:
            dist[destino][origem] = novoGrafo.arestas[a][3]

    for k in range(ordem):
        for i in range(ordem):
            for j in range(ordem):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

def relatorioFloydWarshall(meuGrafo):
    distancias = floydWarshall(meuGrafo)
    print()
    print("Floyd-Warshall: Matriz de distâncias:")
    cabecalho = "*****"
    for w in range(len(meuGrafo.vertices)):
        cabecalho += " " + '{:>4}'.format(meuGrafo.vertices[w])
    print(cabecalho)
    for v in range(len(meuGrafo.vertices)):
        print('{:>4}'.format(meuGrafo.vertices[v]) + "|", end='')
        for w in range(len(meuGrafo.vertices)):
            dist = "∞" if distancias[v][w] == sys.maxsize else distancias[v][w]
            print (" " + '{:>4}'.format(dist), end='')
        print()

#funções de conjuntos usadas por Kruskal
def igualdade(conj1, conj2):
    return sorted(conj1) == sorted(conj2)

#testa se conj2 está contido em conj1
def contem(conj1, conj2):
    for conj in conj1:
        if igualdade(conj, conj2):
            return True
    return False

def uniao(conjunto, *conjuntos):
    resultado = conjunto[:]
    for conj in conjuntos:
        for elem in conj:
            if elem not in resultado:
                resultado.append(elem)
    return resultado

def interseccao(conjunto, *conjuntos):
    return [x for x in conjunto if all([x in conj for conj in conjuntos])]

#remove os *conjuntos de conjunto principal
def diferenca(principal, *conjuntos):
    resultado = []
    for conj in principal:
        if not contem(conjuntos, conj):
            resultado += [conj]
    return resultado

def achaConjunto(conjuntos, vertice):
    for conj in conjuntos:
        if vertice in conj:
            return conj
    return []

def kruskal(meuGrafo: Grafo):
    if meuGrafo.orientado:
        raise Exception("ERRO: GRAFO É ORIENTADO")
    if not meuGrafo.ehConexo():
        raise Exception("ERRO: GRAFO NÃO É CONEXO")
    filaDeArestas = meuGrafo.arestas[:]
    #ordenar a fila de arestas pelo valor
    filaDeArestas.sort(key= lambda x: x[3])
    arvore = []
    vertices = []
    conjuntos = [[v] for v in range(len(meuGrafo.vertices))]
    for aresta in filaDeArestas:
        #poderia testar se foram adicionadas v-1 arestas, mas testar
        #se existe apenas um conjunto de vértices interligados é equivalente
        if len(conjuntos) == 1:
            break
        conj1 = achaConjunto(conjuntos, aresta[1])
        conj2 = achaConjunto(conjuntos, aresta[2])
        if conj1 != conj2:
            vertices = uniao(vertices, [aresta[1]], [aresta[2]])
            arvore.append(aresta)
            conjuntos = diferenca(conjuntos, conj1, conj2)
            conjuntos.append(uniao(conj1, conj2))
    return arvore

def custoDaArvore(listaDeArestas):
    return sum([aresta[3] for aresta in listaDeArestas])

#executa kruskal, e mostra o custo e a matriz de incidências da árvore geradora
def relatorioKruskal(meuGrafo: Grafo, apenasGrafo = False):
    arvore = kruskal(meuGrafo)
    custo = custoDaArvore(arvore)
    novoGrafo = arvoreParaGrafo(meuGrafo, arvore)

    print()
    print("Algoritmo de Kruskal: Custo da árvore geradora:", custo)

    if not apenasGrafo:
        print("Representações da árvore geradora:", end='')
        novoGrafo.mostraVertices()
        novoGrafo.mostraListaDeArestas()
        novoGrafo.mostraListaDeAdjacencias()
        novoGrafo.mostraMatrizDeAdjacencias()
        novoGrafo.mostraMatrizDeIncidencias()

#faz o mesmo que o acima, mas também retorna o código graphviz para visualizar
#a árvore geradora (arestas verdes) e
def relatorioKruskalEmCores(meuGrafo: Grafo, apenasGrafo = False):
    arvore = kruskal(meuGrafo)
    custo = custoDaArvore(arvore)
    novoGrafo = arvoreParaGrafo(meuGrafo, arvore)

    print()
    print("Algoritmo de Kruskal: Custo da árvore geradora:", custo)

    if not apenasGrafo:
        print("Representações da árvore geradora:", end='')
        novoGrafo.mostraVertices()
        novoGrafo.mostraListaDeArestas()
        novoGrafo.mostraListaDeAdjacencias()
        novoGrafo.mostraMatrizDeAdjacencias()
        novoGrafo.mostraMatrizDeIncidencias()

    saida = "graph "
    seta = " -- "
    saida += "\"grafo\" {\nnode [width=1.0,height=1.0];\n"
    saida += "label=\"Custo da árvore geradora: " + str(custo) + "\";\n"
    for v in range(len(meuGrafo.vertices)):
        saida += "N" + str(v+1) + " [label=\"" + meuGrafo.vertices[v]
        saida += "\",fontsize=24];\n"
    for a in range(len(meuGrafo.arestas)):
        saida += "N" + str(meuGrafo.arestas[a][1] + 1) + seta #origem
        saida += "N" + str(meuGrafo.arestas[a][2] + 1) + " [" #destino
        if meuGrafo.valorado:
            saida += "label=" + str(meuGrafo.arestas[a][3]) + ","
        if meuGrafo.arestas[a] in arvore:
            saida += "color=\"darkgreen\",fontcolor=\"darkgreen\","
        else:
            saida += "color=\"red\",fontcolor=\"red\","
        saida += "weight=1,style=\"setlinewidth(2.0)\",fontsize=20];\n"
    saida += "}"
    return saida

def arvoreParaGrafo(grafoModelo, arvore):
    novoGrafo = Grafo(grafoModelo.orientado, grafoModelo.valorado)
    for vertice in grafoModelo.vertices[:]:
        novoGrafo.adicionarVertice(vertice)
    for aresta in arvore:
        novoGrafo.adicionarAresta(aresta[0], aresta[1], aresta[2], aresta[3])
    novoGrafo.reordenarArestas()
    return novoGrafo

#versão que não recebe vértice de origem, pois o usuário não tem como ter uma decisão
#bem-informada de qual vértice pode trazer melhores resultados
def primJarnik(meuGrafo: Grafo, origem=0):
    if meuGrafo.orientado:
        raise Exception("ERRO: GRAFO É ORIENTADO")
    if not meuGrafo.ehConexo():
        raise Exception("ERRO: GRAFO NÃO É CONEXO")
    chave = [sys.maxsize for i in meuGrafo.vertices]
    #em vez de salvar o pai de cada vértice, salvar a aresta que contém
    #o pai e o próprio vértice
    arestasPai = [None for i in meuGrafo.vertices]
    chave[origem] = 0
    fila = [i for i in range(len(meuGrafo.vertices))]
    while len(fila) > 0:
        fila.sort(key=lambda x: chave[x])
        u = fila.pop(0)
        for v in meuGrafo.listaDeAdjacencias[u]:
            #arestas na lista de adjacências são uma tupla formada por:
            #(destino, valor)
            if v[0] in fila and v[1] < chave[v[0]]:
                #recria uma aresta como as usadas na lista de arestas, com, nessa ordem:
                #nome, origem, destino e valor
                arestasPai[v[0]] = ('E'+str(v[0]), u, v[0], v[1])
                chave[v[0]] = v[1]
    #como o vértice origem não tem pai, jogar fora a "aresta pai" dele
    arestasPai = [x for x in arestasPai if x != None]
    return arestasPai

#executa kruskal, e mostra o custo e a matriz de incidências da árvore geradora
def relatorioPrimJarnik(meuGrafo: Grafo, apenasGrafo = False):
    arvore = primJarnik(meuGrafo)
    custo = custoDaArvore(arvore)
    novoGrafo = arvoreParaGrafo(meuGrafo, arvore)

    print()
    print("Algoritmo de Prim-Jarnik: Custo da árvore geradora:", custo)

    if not apenasGrafo:
        print("Representações da árvore geradora:", end='')
        novoGrafo.mostraVertices()
        novoGrafo.mostraListaDeArestas()
        novoGrafo.mostraListaDeAdjacencias()
        novoGrafo.mostraMatrizDeAdjacencias()
        novoGrafo.mostraMatrizDeIncidencias()

#faz o mesmo que o acima, mas também retorna o código graphviz para visualizar
#a árvore geradora (arestas verdes) e
def relatorioPrimJarnikEmCores(meuGrafo: Grafo, apenasGrafo = False):
    arvore = primJarnik(meuGrafo)
    custo = custoDaArvore(arvore)
    novoGrafo = arvoreParaGrafo(meuGrafo, arvore)

    print()
    print("Algoritmo de Prim-Jarnik: Custo da árvore geradora:", custo)

    if not apenasGrafo:
        print("Representações da árvore geradora:", end='')
        novoGrafo.mostraVertices()
        novoGrafo.mostraListaDeArestas()
        novoGrafo.mostraListaDeAdjacencias()
        novoGrafo.mostraMatrizDeAdjacencias()
        novoGrafo.mostraMatrizDeIncidencias()

    saida = "graph "
    seta = " -- "
    saida += "\"grafo\" {\nnode [width=1.0,height=1.0];\n"
    saida += "label=\"Custo da árvore geradora: " + str(custo) + "\";\n"
    for v in range(len(meuGrafo.vertices)):
        saida += "N" + str(v+1) + " [label=\"" + meuGrafo.vertices[v]
        saida += "\",fontsize=24];\n"
    for a in range(len(meuGrafo.arestas)):
        saida += "N" + str(meuGrafo.arestas[a][1] + 1) + seta #origem
        saida += "N" + str(meuGrafo.arestas[a][2] + 1) + " [" #destino
        if meuGrafo.valorado:
            saida += "label=" + str(meuGrafo.arestas[a][3]) + ","
        #como implementado, o prim-jarnik não recria arestas do mesmo jeito
        #que no grafo original, portanto, procurar também arestas onde os vértices
        #de origem e destino estejam em ordem oposta
        if (meuGrafo.arestas[a] in arvore or existeArestaSimilar(meuGrafo.arestas[a], arvore)):
            saida += "color=\"darkgreen\",fontcolor=\"darkgreen\","
        else:
            saida += "color=\"red\",fontcolor=\"red\","
        saida += "weight=1,style=\"setlinewidth(2.0)\",fontsize=20];\n"
    saida += "}"
    return saida

def existeArestaSimilar(aresta, arvore):
    for a in arvore:
        #as arestas têm o mesmo valor?
        if aresta[3] == a[3]:
            if (aresta[1] == a[1] and aresta[2] == a[2]):
                return True
            if (aresta[1] == a[2] and aresta[2] == a[1]):
                return True
    return False

def comparacaoArvoresGM(arvore1, arvore2):
    comparacao = 0
    for a1 in arvore1:
        for a2 in arvore2:
            if a1[3] == a2[3]:
                if a1[1] == a2[1] and a1[2] == a2[2]:
                    comparacao += 1
                if a1[1] == a2[2] and a1[2] == a2[1]:
                    comparacao += 1
    return comparacao, custoDaArvore(arvore1), custoDaArvore(arvore2)

def coloracao(meuGrafo, cores=range(1,15), verticesColoridos=[]):
    listaDeVertices = list(range(len(meuGrafo.vertices)))
    #começam todos sem cor, normalmente
    if verticesColoridos == []:
        verticesColoridos = [[v, None] for v in listaDeVertices]
    verticesColoridos.sort(key = lambda x: meuGrafo.grau(x[0]), reverse=True)
    for cor in cores:
        for vc in verticesColoridos:
            #se o vértice estiver sem cor e nenhum dos vértices da mesma cor for adjacente...
            if vc[1] == None:
                if not any([meuGrafo.saoAdjacentes(vc[0], vc2[0]) for vc2 in [v for v in verticesColoridos if v[1] == cor]]):
                    vc[1] = cor
    return verticesColoridos




def mostraSaidaColoracaoSudoku(verticesColoridos):
    for line in range(9):
        for col in range(9):
            cor = verticesColoridos[line*9+col][1]
            if cor == None:
                cor = '_'
            print('{:>2}'.format(cor),end=' ')
        print()
