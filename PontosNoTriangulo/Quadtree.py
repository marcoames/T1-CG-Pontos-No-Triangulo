
from Ponto import *
from Poligonos import *
from PontosNoTriangulo.PontosNoTriangulo import Min, Max, Meio

class Node:

    def __init__(self, numPontos):
        self.filhos = [None, None, None, None]
        self.numPontos = numPontos

class Quadtree:     
    
    def __init__(self, capacidade, PontosDoCenario: Polygon):

        self.PontosDoCenario = PontosDoCenario

        self.capacidade = capacidade

        Envelope = Polygon()

        self.NW = Envelope (Ponto(Min.x, Meio.y), Ponto(Meio.x, Max.y), Ponto(Meio.x, Max.y), Ponto(Meio.x, Meio.y)) 
        self.NE = Envelope (Ponto(Meio.x, Meio.y), Ponto(Meio.x, Max.y), Ponto(Max.x, Max.y), Ponto(Max.x, Meio.y))
        self.SW = Envelope (Ponto(Min.x, Min.y), Ponto(Min.x, Ponto.y), Ponto(Meio.x, Meio.y), Ponto(Meio.x, Min.y))
        self.SE = Envelope (Ponto(Meio.x, Min.y), Ponto(Meio.x, Meio.y), Ponto(Max.x, Meio.y), Ponto(Max.x, Min.y))


    def desenha(self):
        pass

    def imprime(self):
        pass