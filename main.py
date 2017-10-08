#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro
import grafo, random, sys, os, subprocess, timeit

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

def benchmarkAGM(vertices:int, arestas:int, testes:int):
    clock = timeit.Timer('grafo.kruskal(a)',
    'import grafo; a = grafo.Grafo(orientado=False,valorado=True);grafo.criarVertices(a, '+str(vertices)+');grafo.criarArestasSimples(a, '+str(arestas)+'); ',).timeit(100)
    print("Kruskal x", testes, ":", clock)

    clock = timeit.Timer('grafo.primJarnik(a)',
    'import grafo; a = grafo.Grafo(orientado=False,valorado=True);grafo.criarVertices(a, '+str(vertices)+');grafo.criarArestas(a, '+str(arestas)+'); ',).timeit(100)
    print("Prim-Jarnik x", testes, ":", clock)

def comparacaoArvores(meuGrafo):
    #verificar se Kruskal e Prim-Jarnik acharam a mesma árvore
    arestasIguais, custoK, custoPJ = grafo.comparacaoArvoresGM(grafo.kruskal(meuGrafo), grafo.primJarnik(meuGrafo))
    if arestasIguais == len(meuGrafo.vertices) - 1:
        print("As árvores Geradoras Mínimas são iguais")
    else:
        diferencas = len(meuGrafo.vertices) - 1 - arestasIguais
        print("Foram achadas", diferencas, "arestas diferentes nas árvores geradoras")
        print("encontradas pelos dois algoritmos.")
        print("A árvore geradora mínima de Kruskal teve custo", custoK)
        print("A árvore geradora mínima de Prim-Jarnik teve custo", custoPJ)

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
grafo.criarVertices(a, 18)
grafo.criarArestas(a, 45)
mostrarGrafo = True
if mostrarGrafo:
    a.mostraVertices()
    a.mostraListaDeArestas()
    a.mostraListaDeAdjacencias()
    a.mostraMatrizDeAdjacencias()
    a.mostraMatrizDeIncidencias()

saida = open('saida.dot', 'w')
saida.write(a.paraGraphviz())
saida.close()

#desenho das arestas usadas por Kruskal
saida = open('arvoreKruskal.dot', 'w')
saida.write(grafo.arvoreParaGrafo(a, grafo.kruskal(a)).paraGraphviz())
saida.close()

#arestas usadas por Kruskal, desenhadas no grafo original
saida = open('kruskal.dot', 'w')
saida.write(grafo.relatorioKruskalEmCores(a))
saida.close()

#desenho das arestas usadas por Prim-Jarnik
saida = open('arvorePrimJ.dot', 'w')
saida.write(grafo.arvoreParaGrafo(a, grafo.primJarnik(a)).paraGraphviz())
saida.close()

#arestas usadas por Prim-Jarnik, desenhadas no grafo original
saida = open('primj.dot', 'w')
saida.write(grafo.relatorioPrimJarnikEmCores(a))
saida.close()

#grafo.relatorioFloydWarshall(a)

#verifica se as árvores geradas por Kruskal e Prim-Jarnik são diferentes
comparacaoArvores(a)

#print(grafo.floydWarshall(a))
#teste de velocidade dos algoritmos de árvore geradora mínima
#benchmarkAGM(300, 1100, 100)

#comando para gerar todos os grafos graficamente (heh) no Linux
#dot -Tpng saida.dot > saida.png; dot -Tpng arvorePrimJ.dot > arvorePrimJ.png; dot -Tpng arvoreKruskal.dot > arvoreKruskal.png; dot -Tpng primj.dot >primj.png; dot -Tpng kruskal.dot >kruskal.png; compare kruskal.png primj.png diff.png; eog diff.png
