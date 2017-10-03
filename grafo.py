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

    #testa apenas para grafos nao orientados
    def ehConexo(self):
        if self.orientado:
            raise Exception("ERRO: GRAFO ORIENTADO")
        #o teste espera que todos os vertices tenham ao menos uma aresta
        esperado = len(self.vertices)
        return sum([1 for x in range(esperado) if len(self.listaDeAdjacencias[x]) > 0]) == esperado

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

def bellmanFord(meuGrafo: Grafo, origem: int):
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
        for e in meuGrafo.arestas:
            origem, destino, valor = e[1], e[2], e[3]
            if (distancias[origem] + valor < distancias[destino] and
            distancias[origem] != sys.maxsize):
                distancias[destino] = distancias[origem] + valor
                precursores[destino] = origem
                semMudancas = False
        if semMudancas == True:
            break

    for e in meuGrafo.arestas:
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
def relatorioKruskal(meuGrafo: Grafo):
    arvore = kruskal(meuGrafo)
    custo = custoDaArvore(arvore)
    novoGrafo = arvoreParaGrafo(meuGrafo, arvore)

    print()
    print("Custo da árvore geradora:", custo)
    print("Representações da árvore geradora:", end='')
    novoGrafo.mostraVertices()
    novoGrafo.mostraListaDeArestas()
    novoGrafo.mostraListaDeAdjacencias()
    novoGrafo.mostraMatrizDeAdjacencias()
    novoGrafo.mostraMatrizDeIncidencias()

#faz o mesmo que o acima, mas também retorna o código graphviz para visualizar
#a árvore geradora (arestas verdes) e
def relatorioKruskalEmCores(meuGrafo: Grafo):
    arvore = kruskal(meuGrafo)
    custo = custoDaArvore(arvore)
    novoGrafo = arvoreParaGrafo(meuGrafo, arvore)

    print()
    print("Custo da árvore geradora:", custo)
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
