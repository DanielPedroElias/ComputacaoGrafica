from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
from PIL import Image
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18 # Importa a constante GLUT_BITMAP_HELVETICA_18
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

# Variáveis globais
T, T2, T3 = 1, 1, 1
direcao = 0
L, L2, L3 = -45, 30, -55
C, C2, C3 = 0, 25, 60
CRota, CRota2, CRota3 = 0, 25, 0
scale_x, scale_y, scale_z = 1.0, 1.0, 1.0
target_scale_x, target_scale_y, target_scale_z = 1.0, 1.0, 1.0
scale_speed = 0.1
controleText = 0

def display():
    global scale_x, scale_y, scale_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)

    # Desenha mario com o efeito de Espremer e Esticar
    desenhaMario()
    desenhaFundo()

    # Desenha o texto inicial
    global controleText
    if controleText == 0:
        glColor3f(0.0, 0.0, 0.0)
        DesenhaTexto("Pressione 'a' para mover para a esquerda", -40 , 40)
        DesenhaTexto("Pressione 'd' para mover para a direita", -40 , 38)
        DesenhaTexto("Pressione 'w' para mover para cima", -40 , 36)
        DesenhaTexto("Pressione 's' para mover para baixo", -40 , 34)
        DesenhaTexto("Animação Espreme e Estica implementada", -40 , 32)
        DesenhaTexto("Vá até o botão para testar a colisão", -40 , 30)
    else:
        glColor3f(0.0, 0.0, 0.0)
        DesenhaTexto("Parabéns, você encontrou o botão!", -40 , 45)

    desenhaBotao(botaoDes_ID)

    glUseProgram(0)

    # Desenha esfera de luz
    glPushMatrix()
    glTranslatef(L, L2, L3)
    glColor3f(1.0, 0.0, 0.0)
    glutSolidSphere(0.8, 8, 8)
    glPopMatrix()
    
    desenhaEixos()
    glutSwapBuffers()

def DesenhaTexto(text, x, y, font=GLUT_BITMAP_HELVETICA_18):
    glPushMatrix()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()

posBx, posBy, posBz = -2, 1, -20
def desenhaBotao(texture):
    global posBx, posBy, posBz
    glPushMatrix()
    glRotate(-90, 0, 1, 0)
    glTranslatef(posBx, posBy, posBz)
    glScalef(5, 5, 5)
    glUseProgram(main_shader)
    obj_draw_shaderTexture(botao, main_shader, texture)
    glPopMatrix()

def desenhaFundo():
    glPushMatrix()
    glTranslatef(0, 20, -20)
    glScalef(1, 1.3, 1)
    glUseProgram(main_shader)
    obj_draw_shaderTexture(fundo, main_shader, fundo_ID)
    glPopMatrix()

def desenhaMario():
    glPushMatrix()
    glTranslatef(T, T2, T3)
    glRotatef(direcao, 0, 1, 0)
    glScalef(scale_x, scale_y, scale_z)
    glColor3f(0.1, 0.0, 1.1)
    glUseProgram(main_shader)
    configuraLuz()
    configuraMaterial()
    obj_draw_shaderTexture(mario, main_shader, mario_ID)
    glPopMatrix()

def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao, 1)
    EspremeEstica()
    colisoes()
    gravidade()

def gravidade():
    global T2
    if T2 > 1:
        T2 -= 0.125

def colisoes():
    global T, T2, T3
    if T2 < 1:
        T2 = 1

def ease_in_out(t):
    return 3 * t**2 - 2 * t**3

def EspremeEstica():
    global scale_x, scale_y, scale_z, target_scale_x, target_scale_y, target_scale_z
    progress = scale_speed
    smooth_progress = ease_in_out(progress)
    scale_x += (target_scale_x - scale_x) * smooth_progress
    scale_y += (target_scale_y - scale_y) * smooth_progress
    scale_z += (target_scale_z - scale_z) * smooth_progress
    if abs(scale_x - 1.0) < 0.01:
        scale_x = 1.0
    if abs(scale_y - 1.0) < 0.01:
        scale_y = 1.0
    if abs(scale_z - 1.0) < 0.01:
        scale_z = 1.0
    target_scale_x, target_scale_y, target_scale_z = 1.0, 1.0, 1.0

def Keys(key, x, y):
    global T, T2, T3, target_scale_x, target_scale_y, target_scale_z
    global direcao
    if key == b'a':
        T -= .5
        direcao = -90
        target_scale_x, target_scale_y, target_scale_z = .6, 1.0, 2.0
    elif key == b'd':
        T += .5
        direcao = 90
        target_scale_x, target_scale_y, target_scale_z = .6, 1.0, 2.0
