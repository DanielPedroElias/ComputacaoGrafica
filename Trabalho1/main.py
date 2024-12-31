# Bibliotecas
from OpenGL.GL import * # Importa a biblioteca OpenGL para operações gráficas
from OpenGL.GLU import * # Importa a biblioteca OpenGL Utility para operações de câmera
from OpenGL.GLUT import * # Importa a biblioteca OpenGL Utility Toolkit para janelas
import pywavefront # Importa a biblioteca pywavefront para carregar objetos 3D
from pywavefront import visualization # Importa a biblioteca visualization da pywavefront para visualização de objetos 3D
import pygame # Importa a biblioteca pygame para reprodução de áudio

# from PIL import Image  # Importa a biblioteca Pillow para exibir imagens

# Definição das variaveis de audio
pygame.mixer.init() # Inicializa o mixer do pygame
# inicializa canais de audio
pygame.mixer.set_num_channels(2) # Define o número de canais de áudio
# Carrega a música de fundo
background = pygame.mixer.Sound("Media/funk do arquivo x.mp3") # Carrega a música de fundo
# define o canal da musica de fundo
background_channel = pygame.mixer.Channel(0) # Define o canal 0 para a música de fundo

vitoria = pygame.mixer.Sound("Media/Win.mp3") 
vitoria_channel = pygame.mixer.Channel(1) 

mensagem = 0
# Constantes
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18 # Importa a constante GLUT_BITMAP_HELVETICA_18

# Variáveis globais
T = 0 # Variável de movimento do homem, setas esq e dir
T2 = 0 # Variável de altura do homem, setas cima e baixo
D = 0 # Variável de movimento do disco
D2 = 1.5 # Variável de altura do disco
C = -4.0 # Variável de movimento do carro

controle = 0 # Variável de controle do salto
controle2 = 0 # Variável de controle da mensagem

Disco_mov = 0.05  # Velocidade e direção do movimento do disco no eixo x
Disco_mov2 = 0.003  # Velocidade e direção do movimento do disco no eixo y

# Definições das caixas
caixas = [ # (x, y, escala)
    (1.0, 0.0, 0.01),
    (1.5, 0.0, 0.01),
    (2, 0.0, 0.01), 
    (1.6, 0.25, 0.01),
    (2.10, 0.25, 0.01),
    (2.20, 0.50, 0.01) 
]

# Função para desenhar texto na tela
def DesenhaTexto(text, x, y, font=GLUT_BITMAP_HELVETICA_18):
    glPushMatrix() # Salva a matriz de transformação atual
    glRasterPos2f(x, y)  # Define a posição do texto
    # para cada caractere no texto
    for ch in text:
        glutBitmapCharacter(font, ord(ch))  # Desenha cada caractere do texto
    glPopMatrix() # Restaura a matriz de transformação anterior

# Função de display
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa o buffer de cor e o buffer de profundidade
    glMatrixMode(GL_MODELVIEW) # Define a matriz de transformação atual como a matriz de visualização
    glPushMatrix() # Salva a matriz de transformação atual

    # Movimento do Homem
    global T
    global T2
    glTranslatef(T, T2, 0) # Translação do homem
    glScalef(0.1, 0.1, 0.1) # Escala do homem
    glPushMatrix() # Salva a matriz de transformação atual
    glTranslatef(0.0, 0.0, 0.0) # posição do homem inicial
    glColor3f(0.0 , 0.3, 0.0) # Cor do homem 
    visualization.draw(homem) # Desenha o homem
    glPopMatrix() # Restaura a matriz de transformação anterior
    glPopMatrix() # Restaura a matriz de transformação anterior

    # Desenha o disco
    global D
    global D2
    glPushMatrix() 
    glTranslatef(D, D2, 0) 
    glScalef(0.1, 0.1, 0.1)
    glColor3f(0.5, 0.0, 1.0) 
    visualization.draw(disco) 
    glPopMatrix()

    # Desenha as caixas
    global caixas
    for cx, cy, escala in caixas:
        glPushMatrix() 
        glTranslatef(cx, cy, 0.0) 
        glScalef(escala, escala, escala)
        glColor3f(139/255.0, 69/255.0, 19/255.0)
        visualization.draw(caixa)
        glPopMatrix()

    #Desenha as arvores
    glPushMatrix()
    glTranslatef(-1.75, 0.0, 0.0)
    glScalef(0.15, 0.15, 0.15)
    glColor3f(0.0, 1.0, 0.0)
    visualization.draw(arvores)
    glPopMatrix()

    #Desenha o carro 1
    global C
    glPushMatrix()
    glTranslatef(C, 0.0, -3.0)
    glScalef(0.05, 0.05, 0.05)
    glColor3f(1.0, 0.0, 0.0)
    visualization.draw(carro)
    glPopMatrix()

    #Desenha o carro 2
    glPushMatrix()
    glTranslatef((C-1), 0.0, -3.0)
    glScalef(0.05, 0.05, 0.05)
    glColor3f(0.0, 0.0, 1.0)
    visualization.draw(carro)
    glPopMatrix()

    # Desenha a mensagem na tela quando T for menor que -1.25
    global controle2
    global mensagem 
    if T <= -1.25:
        glColor3f(1.0, 1.0, 1.0)  # Cor do texto (branco)
        DesenhaTexto("Não se esconda, vá atrás do conhecimento", -1.0, 1.8)  # Posição e texto
    elif (T >= D - 0.65 and T <= D + 0.65) and (T2 >= D2 - 0.5 and T2 <= D2 + 0.25): #(T >= 1.85 or T2 >= 1.25):
        mensagem = 1
        DesenhaTexto("bateu no disco", 0.0, 1.0)
        if controle2 == 0:            
            vitoria_channel.play(vitoria)  # Toca o som de vitória
            
            #img = Image.open("cimento.jpeg")
            #img.show()
            
            # Inicia o pygame para exibir a imagem em full screen
            pygame.init()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Define o modo full screen
            
            img = pygame.image.load("Media/cimento.jpeg")  # Carrega a imagem usando pygame
            img = pygame.transform.scale(img, (screen.get_width(), screen.get_height()))  # Redimensiona para preencher a tela
            
            screen.blit(img, (0, 0))  # Desenha a imagem na tela
            pygame.display.flip()  # Atualiza a tela

            controle2 = 1
    if (mensagem == 1):
        glColor3f(1.0, 1.0, 1.0)
        DesenhaTexto("Parabéns, você encontrou o conhecimento, ET Bilu estah orgulhoso", 0.2, 1.8)
    # teste de uma colisao dinamica
    # if (T >= D - 0.5 and T <= D + 0.5) and (T2 >= D2 - 0.5 and T2 <= T2 + 0.5):
    #     glColor3f(1.0, 1.0, 1.0)
    #     DesenhaTexto("bateu no disco",0.0,1.0)


    # Eixos de referência
    # Eixo X
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0) # Cor vermelha
    glVertex3f(-3.0, 0.0, 0.0) # Ponto inicial
    glVertex3f(10.0, 0.0, 0.0) # Ponto final
    glEnd() # Finaliza o desenho

    # Eixo Y
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0) # Cor verde 
    glVertex3f(0.0, 0.0, 0.0) # Ponto inicial 
    glVertex3f(0.0, 10.0, 0.0) # Ponto final
    glEnd() 

    # Eixo Z
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0) # Cor azul
    glVertex3f(0.0, 0.0, 0.0) # Ponto inicial
    glVertex3f(0.0, 0.0, 10.0) # Ponto final
    glEnd()

    glutSwapBuffers() # Troca os buffers

# Função de teclas especiais
def keys(key, x, y):
    global T
    global T2    
    # teclas W, A, S, D
    if key == b'a':  # Tecla A
        T -= 0.125
    elif key == b'd':  # Tecla D
        T += 0.125
    elif key == b'w':  # Tecla W
        T2 += 0.5
    elif key == b's' and T2 >= 0.25:  # Tecla S
        T2 -= 0.25

# Função de animação
def animacao(value):
    glutPostRedisplay() # solicita uma atualização da tela
    glutTimerFunc(30, animacao, 1) # define o tempo de atualização da tela
    global T 
    global T2
    
    # Movimento do disco
    global D
    global D2
    global Disco_mov 
    global Disco_mov2
    
    # configura os mov horizontal do disco
    if D >= 1.6 or D <= -0.75:
        Disco_mov = -Disco_mov # inverte a direção do movimento
    D += Disco_mov
    # configura as alturas do disco
    if D2 >= 1.6 or D2 <= 1.2:
        Disco_mov2 = -Disco_mov2
    D2 += Disco_mov2

    # Movimento do carro
    global C
    if C < 6.0 :
        C += 0.125
    else:
        C = -4.0

    # configura as gravidades do homem
    global controle
    
    if  T2 > 0.05 and controle == 0: # algo estranho aq
        T2 -= 0.05
    elif T2 > 0.25 and controle == 1:
        T2 -= 0.05
    elif T2 > 0.50 and controle == 2:
        T2 -= 0.05
    elif T2 > 0.75 and controle == 3:
        T2 -= 0.05
        
    # Impede o movimento para fora da tela à esquerda
    elif T <= -2.0 :
        T = -2.0    
    # Impede o movimento para fora da tela à direita
    elif T >= 2.0 :
        T = 2.0

    # sobe nas caixas com base no eixo x do homem
    elif T >= 0.75 and T <= 1.25:
        T2 = 0.25
        controle = 1
    elif T > 1.25 and T <= 1.75:
        T2 = 0.50
        controle = 2
    elif T > 1.75:
        T2 = 0.75
        controle = 3
    elif T < 0.75:
        controle = 0
       
    else:# garante que a altura do homem seja 0 
        T2 = 0 # @bug por algum motivo o valor nao volta pra 0 sozinho

# Função de câmera
def camera(w, h):
    glViewport(0, 0, w, h) # Define a janela de visualização
    glMatrixMode(GL_PROJECTION) # Define a matriz de transformação atual como a matriz de projeção
    glLoadIdentity() # Carrega a matriz identidade
    gluPerspective(25.0, w/h, 1.0, 100.0) # Define a projeção perspectiva
    glMatrixMode(GL_MODELVIEW) # Define a matriz de transformação atual como a matriz de visualização
    glLoadIdentity() # Carrega a matriz identidade
    # Define a posição da câmera, o ponto de visão e o vetor Up
    gluLookAt(0.0, 2.0, 5.0, # Posição da câmera
                0.0, 1.0, 0.0, # Ponto de visão
                0.0, 1.0, 0.0) # Vetor Up
# Função de inicialização
def init():
    glClearColor (0.3, 0.3, 0.3, 0.0) # Cor de fundo
    glShadeModel( GL_SMOOTH ) # Tipo de sombreamento
    glClearColor( 0.0, 0.0, 0.0, 0.5 ) # Cor de fundo 
    glClearDepth( 1.0 ) # Profundidade do buffer de profundidade
    glEnable( GL_DEPTH_TEST ) # Ativa o teste de profundidade
    glDepthFunc( GL_LEQUAL ) # Função de profundidade
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST ) # Correção de perspectiva

    glLightModelfv( GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0] ) # Modelo de luz ambiente
    glLightfv( GL_LIGHT0, GL_AMBIENT, [ 0.2, 0.2, 0.2, 1.0] ) # Luz ambiente
    glLightfv( GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0] ) # Luz difusa
    glLightfv( GL_LIGHT0, GL_SPECULAR, [0.7, 0.7, 0.7, 1] ) # Luz especular
    glLightfv( GL_LIGHT0, GL_POSITION, [10.0, 10.0, 10.0, 0.0]) # Posição da luz
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01) # Atenuação da luz
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.01) # Atenuação da luz
    glEnable( GL_LIGHT0 ) # Ativa a luz 0
    glEnable( GL_COLOR_MATERIAL ) # Ativa o material de cor
    glShadeModel( GL_SMOOTH ) # Tipo de sombreamento
    glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE ) # Modelo de luz de um lado
    glDepthFunc(GL_LEQUAL) # Função de profundidade
    glEnable(GL_DEPTH_TEST) # Ativa o teste de profundidade
    glEnable(GL_LIGHTING) # Ativa a iluminação
    glEnable(GL_LIGHT0) # Ativa a luz 0

# Inicialização do GLUT
glutInit() 
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) # Modo de exibição
glutInitWindowSize(1920, 1080) # Tamanho da janela
glutInitWindowPosition(100, 100) # Posição da janela
wind = glutCreateWindow("Busque comer cimento") # Título da janela

# Inicialização do programa
init() 
# Carrega os objetos
homem = pywavefront.Wavefront("Objetos/homem.obj")
disco = pywavefront.Wavefront("Objetos/disco.obj")
caixa = pywavefront.Wavefront("Objetos/caixa.obj")
arvores = pywavefront.Wavefront("Objetos/arvores.obj")
carro = pywavefront.Wavefront("Objetos/bugatti.obj")

# toca a música de fundo
background_channel.play(background, loops=-1) 
# define o volume da música de fundo
background_channel.set_volume(0.4)

# Funções de callback
glutDisplayFunc(display)
glutReshapeFunc(camera)
glutTimerFunc(30, animacao, 1)
glutKeyboardFunc(keys) # Define a função de teclado
glutMainLoop()
