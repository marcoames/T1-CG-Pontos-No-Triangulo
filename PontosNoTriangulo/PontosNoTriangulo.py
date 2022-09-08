# ***********************************************************************************
#   PontosNoTriangulo.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um conjunto de Pontos e um triangulo em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
import random

from Quadtree import *

# ***********************************************************************************
# Variaveis que controlam o triangulo do campo de visao
PontosDoCenario = Polygon()
CampoDeVisao = Polygon()
TrianguloBase = Polygon()
PosicaoDoCampoDeVisao = Ponto

AnguloDoCampoDeVisao = 0.0

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()
Tamanho = Ponto()
Meio = Ponto()

PontoClicado = Ponto()

flagDesenhaEixos = True

flagDesenhaVerticesColoridos = False
flagqtPontos = False

flagForcaBruta = False
flagEnvelope = False
flagQuadtree = False

# para aumentar e diminuir o campo de visão
n = 0.25
flagAumentaVisao = False
flagDiminuiVisao = False

vermelhos, amarelos, verdes = 0, 0, 0


# **********************************************************************
# GeraPontos(int qtd)
#      Metodo que gera pontos aleatorios no intervalo [Min..Max]
# **********************************************************************
def GeraPontos(qtd, Min: Ponto, Max: Ponto):
    global PontosDoCenario
    Escala = Ponto()
    Escala = (Max - Min) * (1.0/1000.0)

    for i in range(qtd):
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        x = x * Escala.x + Min.x
        y = y * Escala.y + Min.y
        P = Ponto(x, y)
        PontosDoCenario.insereVertice(P.x, P.y, P.z)
        # PontosDoCenario.insereVertice(P)


# **********************************************************************
#  CriaTrianguloDoCampoDeVisao()
#  Cria um triangulo a partir do vetor (1,0,0), girando este vetor
#  em 45 e -45 graus.
#  Este vetor fica armazenado nas variáveis "TrianguloBase" e
#  "CampoDeVisao"
# **********************************************************************
def CriaTrianguloDoCampoDeVisao():
    global TrianguloBase, CampoDeVisao, Envelope

    vetor = Ponto(1, 0, 0)

    TrianguloBase.insereVertice(0, 0, 0)
    CampoDeVisao.insereVertice(0, 0, 0)

    vetor.rotacionaZ(45)
    TrianguloBase.insereVertice(vetor.x, vetor.y, vetor.z)
    CampoDeVisao.insereVertice(vetor.x, vetor.y, vetor.z)

    vetor.rotacionaZ(-90)
    TrianguloBase.insereVertice(vetor.x, vetor.y, vetor.z)
    CampoDeVisao.insereVertice(vetor.x, vetor.y, vetor.z)


# ***********************************************************************************
# void PosicionaTrianguloDoCampoDeVisao()
#  Posiciona o campo de visão na posicao PosicaoDoCampoDeVisao,
#  com a orientacao "AnguloDoCampoDeVisao".
#  O tamanho do campo de visão eh de 25% da largura da janela.
# **********************************************************************
def PosicionaTrianguloDoCampoDeVisao():
    global Tamanho, CampoDeVisao, PosicaoDoCampoDeVisao, TrianguloBase
    global AnguloDoCampoDeVisao

    tam = Tamanho.x * 0.25
    temp = Ponto()
    for i in range(TrianguloBase.getNVertices()):
        temp = TrianguloBase.getVertice(i)
        temp.rotacionaZ(AnguloDoCampoDeVisao)
        CampoDeVisao.alteraVertice(i, PosicaoDoCampoDeVisao + temp*tam)


def AvancaCampoDeVisao(distancia):
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao
    vetor = Ponto(1, 0, 0)
    vetor.rotacionaZ(AnguloDoCampoDeVisao)
    PosicaoDoCampoDeVisao = PosicaoDoCampoDeVisao + vetor * distancia


# ***********************************************************************************
#
# ***********************************************************************************
def init():
    global PosicaoDoCampoDeVisao, AnguloDoCampoDeVisao

    # Define a cor do fundo da tela (AZUL)
    glClearColor(0, 0, 1, 1)
    global Min, Max, Meio, Tamanho

    GeraPontos(1000, Ponto(0, 0), Ponto(500, 500))
    Min, Max = PontosDoCenario.getLimits()
    #Min, Max = PontosDoCenario.LePontosDeArquivo("PoligonoDeTeste.txt")

    Meio = (Max+Min) * 0.5  # Ponto central da janela
    Tamanho = (Max - Min)  # Tamanho da janela em X,Y

    # Ajusta variaveis do triangulo que representa o campo de visao
    PosicaoDoCampoDeVisao = Meio
    AnguloDoCampoDeVisao = 0

    # Cria o triangulo que representa o campo de visao
    CriaTrianguloDoCampoDeVisao()
    PosicionaTrianguloDoCampoDeVisao()


# ***********************************************************************************
#
# ***********************************************************************************
def DesenhaLinha(P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x, P1.y, P1.z)
    glVertex3f(P2.x, P2.y, P2.z)
    glEnd()


# ***********************************************************************************
#
# ***********************************************************************************
def DesenhaEixos():
    global Min, Max, Meio

    glBegin(GL_LINES)
    # eixo horizontal
    glVertex2f(Min.x, Meio.y)
    glVertex2f(Max.x, Meio.y)
    # eixo vertical
    glVertex2f(Meio.x, Min.y)
    glVertex2f(Meio.x, Max.y)
    glEnd()


# ***********************************************************************************
def reshape(w, h):
    global Min, Max

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# ***********************************************************************************
def display():
    global PontoClicado, flagDesenhaEixos, flagAumentaVisao, flagDiminuiVisao, n
    global flagDesenhaVerticesColoridos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 1.0, 0.0)

    if (flagDesenhaEixos):
        glLineWidth(1)
        glColor3f(1, 1, 1)  # R, G, B  [0..1]
        DesenhaEixos()

    glPointSize(2)
    glColor3f(1, 1, 0)  # R, G, B  [0..1]
    PontosDoCenario.desenhaVertices()

    if (flagAumentaVisao):
        aumentaCampoDeVisao(n)

    if (flagDiminuiVisao):
        diminuiCampoDeVisao(n)

    if (not flagAumentaVisao and not flagDiminuiVisao):
        glLineWidth(3)
        glColor3f(1, 0, 0)  # R, G, B  [0..1]
        CampoDeVisao.desenhaPoligono()

    if (flagEnvelope):
        desenhaEnvelope()

    if (flagDesenhaVerticesColoridos):
        desenhaVerticesColoridos(PontosDoCenario)

    if (flagqtPontos):
        qtPontos()

    glutSwapBuffers()


# ***********************************************************************************
# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'


def keyboard(*args):
    global flagDesenhaEixos, flagAumentaVisao, flagDiminuiVisao, n
    global flagForcaBruta, flagEnvelope, flagDesenhaVerticesColoridos, flagqtPontos, flagQuadtree

    #print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b'p':
        PontosDoCenario.imprimeVertices()
    if args[0] == b'1':
        P1, P2 = PontosDoCenario.getAresta(0)
        P1.imprime()
        P2.imprime()
    if args[0] == b' ':
        flagDesenhaEixos = not flagDesenhaEixos
    if args[0] == b'2':
        flagForcaBruta = not flagForcaBruta
    if args[0] == b'3':
        flagEnvelope = not flagEnvelope
    if args[0] == b'4':
        flagQuadtree = not flagQuadtree    
    if args[0] == b'5':
        flagDesenhaVerticesColoridos = not flagDesenhaVerticesColoridos
    if args[0] == b'6':
        flagqtPontos = not flagqtPontos
    if args[0] == b'f':
        flagAumentaVisao = True
        flagDiminuiVisao = False
        n = n + 0.05
    if args[0] == b'g':
        flagDiminuiVisao = True
        flagAumentaVisao = False
        n = n - 0.05
    if args[0] == b'c':
        os.system('clear')

    # Forca o redesenho da tela
    glutPostRedisplay()


# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global AnguloDoCampoDeVisao, TrianguloBase

    #print ("Tecla:", a_keys)
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        AvancaCampoDeVisao(2)
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        AvancaCampoDeVisao(-2)
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao + 2
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        AnguloDoCampoDeVisao = AnguloDoCampoDeVisao - 2

    PosicionaTrianguloDoCampoDeVisao()

    glutPostRedisplay()


# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN):
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do
    # universo definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto(
        worldCoordinate1[0], worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()


# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    # glutPostRedisplay()
    return


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************


def aumentaCampoDeVisao(n):
    global Tamanho, CampoDeVisao, PosicaoDoCampoDeVisao, TrianguloBase
    global AnguloDoCampoDeVisao

    tam = Tamanho.x * (n)
    temp = Ponto()
    for i in range(TrianguloBase.getNVertices()):
        temp = TrianguloBase.getVertice(i)
        temp.rotacionaZ(AnguloDoCampoDeVisao)
        CampoDeVisao.alteraVertice(i, PosicaoDoCampoDeVisao + temp * tam)

    #CampoDeVisao = CampoDeVisao
    # desenha o triangulo
    glLineWidth(3)
    glColor3f(1, 0, 0)  # R, G, B  [0..1]
    CampoDeVisao.desenhaPoligono()
    # glutPostRedisplay()


# n inicial = 0.25
def diminuiCampoDeVisao(n):
    global Tamanho, CampoDeVisao, PosicaoDoCampoDeVisao, TrianguloBase
    global AnguloDoCampoDeVisao

    tam = Tamanho.x * (n)
    temp = Ponto()
    for i in range(TrianguloBase.getNVertices()):
        temp = TrianguloBase.getVertice(i)
        temp.rotacionaZ(AnguloDoCampoDeVisao)
        CampoDeVisao.alteraVertice(i, PosicaoDoCampoDeVisao + temp * tam)

    #CampoDeVisao = CampoDeVisao
    # desenha o triangulo
    glLineWidth(3)
    glColor3f(1, 0, 0)  # R, G, B  [0..1]
    CampoDeVisao.desenhaPoligono()


def forcaBruta(P):
    global CampoDeVisao

    # Vertices do Triangulo
    PA = CampoDeVisao.getVertice(0)
    PB = CampoDeVisao.getVertice(1)
    PC = CampoDeVisao.getVertice(2)

    # Vetores de vertices para vertices do triangulo
    VAB = PB - PA
    VBC = PC - PB
    VCA = PA - PC

    # Vetores de vertices para ponto P
    VAP = P - PA
    VBP = P - PB
    VCP = P - PC

    # Calcula produto vetorial do vetor de vertice para vertice com vetor de vertice para ponto P
    pva = produtoVetorial(VAB, VAP)
    pvb = produtoVetorial(VBC, VBP)
    pvc = produtoVetorial(VCA, VCP)

    if(pva < 0):
        if (pvb < 0):
            if (pvc < 0):
                # Se estiver dentro do triangulo pinta de verde
                P.setCor(0, 1, 0)  # verde
                return True

    return False


def produtoVetorial(v1, v2):
    pvt = v1.x * v2.y - v1.y * v2.x
    return pvt


def envelope(P):
    global CampoDeVisao

    ponto = CampoDeVisao.getLimits()

    # Verifica se o ponto esta dentro do envelope
    if (P.x < ponto[1].x):
        if(P.y < ponto[1].y):
            if(P.x > ponto[0].x):
                if(P.y > ponto[0].y):
                    if (forcaBruta(P)):
                        # Se estiver dentro do triangulo pinta de verde
                        P.setCor(0, 1, 0)  # verde
                    else:
                        # Se estiver dentro do envelope pinta de amarelo
                        P.setCor(1, 1, 0)  # amarelo
                    return True

    return False


def desenhaEnvelope():
    global CampoDeVisao

    # Cria o envelope
    Envelope = Polygon()

    ponto = CampoDeVisao.getLimits()

    # desenha o envelope
    Envelope.insereVertice(ponto[1].x, ponto[1].y, 0)
    Envelope.insereVertice(ponto[1].x, ponto[0].y, 0)
    Envelope.insereVertice(ponto[0].x, ponto[0].y, 0)
    Envelope.insereVertice(ponto[0].x, ponto[1].y, 0)

    glLineWidth(2)
    glColor3f(1, 1, 1)  # R, G, B  [0..1]
    Envelope.desenhaPoligono()


def quadTree():
    qt = Quadtree(10, PontosDoCenario)
    #qt.imprime()
    qt.desenha()


def desenhaVerticesColoridos(Poly):
    global flagForcaBruta, flagEnvelope
    global vermelhos, amarelos, verdes

    vermelhos, amarelos, verdes = 0, 0, 0

    glBegin(GL_POINTS)

    for i in range(Poly.getNVertices()):
        P = Poly.getVertice(i)

        # ponto em vermelho por padrão
        P.setCor(1, 0, 0)  # vermelho
        glColor3f(1, 0, 0)  # vermelho
        glVertex3f(P.x, P.y, P.z)

        if (flagEnvelope):
            if (envelope(P)):
                if (P.getCor() == (1, 1, 0)):
                    # ponto em amarelo se estiver dentro do envelope
                    glColor3f(1, 1, 0)  # amarelo
                    amarelos += 1
                    glVertex3f(P.x, P.y, P.z)
                elif (P.getCor() == (0, 1, 0)):
                    # ponto em verde se estiver dentro do triangulo
                    glColor3f(0, 1, 0)  # verde
                    verdes += 1
                    glVertex3f(P.x, P.y, P.z)

        if (flagForcaBruta):
            if (forcaBruta(P)):
                P.setCor(0, 1, 0)  # verde
                glColor3f(0, 1, 0)  # verde
                verdes += 1
                glVertex3f(P.x, P.y, P.z)

        if (flagQuadtree):
            quadTree()
            #Quadtree.desenha()        

    glEnd()

    vermelhos = Poly.getNVertices() - amarelos - verdes


def qtPontos():
    global vermelhos, amarelos, verdes

    os.system('clear')
    print("Pontos verdes: ", verdes)
    print("Pontos amarelos: ", amarelos)
    print("Pontos vermelhos: ", vermelhos)


glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
glutInitWindowPosition(700, 100)
wind = glutCreateWindow("Pontos no Triangulo")
glutDisplayFunc(display)
# glutIdleFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass
