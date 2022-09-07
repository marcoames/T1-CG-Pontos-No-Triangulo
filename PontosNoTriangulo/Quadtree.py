from PontosNoTriangulo.Ponto import Ponto
from PontosNoTriangulo.Poligonos import Polygon
from PontosNoTriangulo.PontosNoTriangulo import PontosDoCenario

class Node:

    # lista de filhos
    #filhos = [null, null, null, null]

    def __init__(self, numPontos):
        self.filhos = [None, None, None, None]
        self.numPontos = numPontos
        self.max = Ponto()
        self.min = Ponto()

class Quadtree:     
    
    def __init__(self, pontos, Envelope: Polygon):
        # pontos do cenario
        numPontos = PontosDoCenario.getNVertices()

        # Nodo raiz
        raiz = Node()
        self.raiz = raiz
        raiz.filhos[0] = Node(10)
        raiz.filhos[1] = Node(10)
        raiz.filhos[2] = Node(10)
        raiz.filhos[3] = Node(10)

        self.pontos = pontos
        self.Envelope = Envelope
        
    def insereNodo():
        pass
    
    def deveDividir(self):
        if self.numPontos > 10:
            return True
        return False    

    def set():
        pass

    def getFilhos(node):
        return node.filhos