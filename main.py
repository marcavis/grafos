#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#representação de grafos
#Caio Silveira Batista, Marcos Avila Isidoro

import grafo

a = grafo.Grafo(False, False)
a.adicionarVertice('V1')
a.adicionarVertice('V2')
a.adicionarVertice('V3')
a.adicionarAresta('E1', 0, 1)
a.adicionarAresta('E1', 1, 2)
a.adicionarAresta('E1', 0, 2)
a.mostraVertices()
a.mostraListaDeArestas()
a.mostraListaDeAdjacencias()
a.mostraMatrizDeAdjacencias()
a.mostraMatrizDeIncidencias()
