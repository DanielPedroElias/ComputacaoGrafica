from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
from PIL import Image

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

# variaveis Globais
# pos do Mario
T,T2,T3 = 1,1,1
direcao = 0

# pos da luz
L,L2,L3 = -5,15,-30
# pos da camera
C, C2, C3 = 0, 25, 60
# Rotação da camera
CRota,CRota2,CRota3 = 0,25,0

# Variáveis globais de escala para o efeito de Espremer e Esticar
scale_x, scale_y, scale_z = 1.0, 1.0, 1.0
target_scale_x, target_scale_y, target_scale_z = 1.0, 1.0, 1.0  # Escala padrão
scale_speed = 0.1  # Velocidade de retorno à escala padrão


# Variáveis de shader e textura
def display():
    global scale_x, scale_y, scale_z
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    

    glPushMatrix()

    # Desenha Mario com o efeito de Espremer e Esticar
    glTranslatef(T, T2, T3)
    glRotatef(direcao, 0, 1, 0)
    glScalef(scale_x, scale_y, scale_z)  # Aplica a escala com o efeito

    glColor3f(0.1, 0.0, 1.1)
    glUseProgram(mario_shader)
    configuraLuz()
    confiuraMaterial()
    obj_draw_shaderTexture(mario, mario_shader, mario_ID)
    glUseProgram(0)

    glPopMatrix()

    # Desenha esfera de luz
    glPushMatrix()
    glTranslatef(L, L2, L3)
    glutSolidSphere(0.8, 8, 8)
    glPopMatrix()
    
    desenhaEixos()
    glutSwapBuffers()

# Função de animação para interpolação de escala
def animacao(value):
    # Requisição de redesenho da tela
    glutPostRedisplay()
    glutTimerFunc(30, animacao, 1)

    EspremeEstica()

    colisoes()

    gravidade()

def gravidade():
    global T2
    if T2 > 1:
        T2 -= 0.25
        
def colisoes():
    global T, T2, T3
    if T2 < 1:
        T2 = 1

# Função de easing para o "Slow in Slow out"
def ease_in_out(t):
    return 3 * t**2 - 2 * t**3

# Função para espremer e esticar o objeto com "Slow in Slow out"
def EspremeEstica():
    global scale_x, scale_y, scale_z, target_scale_x, target_scale_y, target_scale_z

    # Tempo de interpolação (valor entre 0 e 1 para calcular o progresso da interpolação)
    progress = scale_speed
    smooth_progress = ease_in_out(progress)  # Aplica a função de easing

    # Interpolação gradual com 'slow in slow out' para retornar à escala normal (1.0, 1.0, 1.0)
    scale_x += (target_scale_x - scale_x) * smooth_progress
    scale_y += (target_scale_y - scale_y) * smooth_progress
    scale_z += (target_scale_z - scale_z) * smooth_progress

    # Trava valores próximos de 1.0 para evitar flutuações
    if abs(scale_x - 1.0) < 0.01:
        scale_x = 1.0
    if abs(scale_y - 1.0) < 0.01:
        scale_y = 1.0
    if abs(scale_z - 1.0) < 0.01:
        scale_z = 1.0

    # Redefine a escala alvo para (1.0, 1.0, 1.0) após cada movimento
    target_scale_x, target_scale_y, target_scale_z = 1.0, 1.0, 1.0

    # Redefine a escala alvo para (1.0, 1.0, 1.0) após cada movimento
    target_scale_x, target_scale_y, target_scale_z = 1.0, 1.0, 1.0

# Função para lidar com as teclas de movimento do objeto  
teclaW = False
def Keys(key, x, y):
    global T, T2, T3, target_scale_x, target_scale_y, target_scale_z
    global direcao

    # Controle de escala para efeito de Espremer e Esticar
    if key == b'a':  # Movimento para a esquerda
        T -= .5
        direcao = -90
        target_scale_x, target_scale_y, target_scale_z = .6, 1.0, 1.8  # Achatado no X, alongado no Y
    elif key == b'd':  # Movimento para a direita
        T += .5
        direcao = 90
        target_scale_x, target_scale_y, target_scale_z = .6, 1.0, 1.8
    elif key == b'w':  # Movimento para cima
        T2 += .5
        teclaW = True
        target_scale_x, target_scale_y, target_scale_z = 1.4, .6, 1.0  # Alongado no X, achatado no Y
    elif key == b's':  # Movimento para baixo
        T2 -= .5
        target_scale_x, target_scale_y, target_scale_z = 1.4, .6, 1.0
    elif key == b'q': 
        T3 -= 1
    elif key == b'e': 
        T3 += 1
    
# Função para desenhar um objeto com shader e textura (se fornecida)
def obj_draw_shaderTexture(objeto, shader_program, texture_ID=None):
    objs = list(objeto.materials.keys())    # Pega o primeiro material do objeto
    vertices = objeto.materials[objs[0]].vertices
    vertices = np.array(vertices, dtype=np.float32).reshape(-1, 8)  # Assumindo que temos tex_2, vn_3, v_3
    vbo_objeto = vbo.VBO(vertices)

    # Liga o VBO
    vbo_objeto.bind()

    # Ativa os estados necessários para usar os dados de vértices, normais e coordenadas de textura
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    # Define os ponteiros para os dados de vértices, normais e coordenadas de textura
    glVertexPointer(3, GL_FLOAT, 32, vbo_objeto + 20)  # 3 floats para os vértices (posição)
    glNormalPointer(GL_FLOAT, 32, vbo_objeto + 8)      # 3 floats para as normais
    glTexCoordPointer(2, GL_FLOAT, 32, vbo_objeto)     # 2 floats para coordenadas de textura

    # Se houver uma textura, ativa e aplica
    if texture_ID is not None:
        glActiveTexture(GL_TEXTURE0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_ID)
        glUniform1i(glGetUniformLocation(shader_program, 'tex'), 0)

    # Ativa o shader
    glUseProgram(shader_program)

    # Desenha o objeto
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])

    # Desativa o shader e estados
    glUseProgram(0)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    # Desvincula o VBO
    vbo_objeto.unbind()

# Função para configurar a luz
def configuraLuz():
    glUniform4f( LIGTH_LOCATIONS['Global_ambient'], 0.01, 0.01, 0.01, 1.0 )
    glUniform3f( LIGTH_LOCATIONS['Light_location'], L,L2,L3 )
    glUniform4f( LIGTH_LOCATIONS['Light_ambient'], 0.2, 0.2, 0.2, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_diffuse'], 0.9, 0.9, 0.9, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_specular'], 0.9,0.9,0.9, 1.0 )

# Função para configurar o material
def confiuraMaterial():
    glUniform4f( LIGTH_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], 0.1,0.1,0.9, 1 )
    glUniform4f( LIGTH_LOCATIONS['Material_specular'], 0.9,0.9,0.9, 1 )
    glUniform1f( LIGTH_LOCATIONS['Material_shininess'], 0.6*128.0 )

# Função para desenhar os eixos
def desenhaEixos():

    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()

# Função para configurar a câmera   
def camera(w, h):
   
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(C, C2, C3, 
    CRota, CRota2, CRota3, 
    0.0, 1.0, 0.0)
    
# Função para lidar com as teclas especiais para o movimento da luz
def KeysEspecial(key, x, y):
    global L
    global L2
    global L3
    
    if(key == GLUT_KEY_LEFT ): 
        L -= 1 
    elif(key == GLUT_KEY_RIGHT ): 
        L += 1 
    elif(key == GLUT_KEY_DOWN ): 
        L2 -= 1
    elif(key == GLUT_KEY_UP ): 
        L2 += 1 
    elif(key == GLUT_KEY_PAGE_UP ): 
        L3 -= 1 
        
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        L3 += 1         
    print(L3)
  
# Função para inicializar o programa
def init():
    glClearColor(0,0,0, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    vertexShader = shaders.compileShader(open('texture/mario.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('texture/mario.frag', 'r').read(), GL_FRAGMENT_SHADER)
    global mario_shader
    mario_shader = glCreateProgram()
    glAttachShader(mario_shader, vertexShader)
    glAttachShader(mario_shader, fragmentShader)
    glLinkProgram(mario_shader)

    # Define variáveis de iluminação no shader
    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation(mario_shader, 'Global_ambient'),
        'Light_ambient': glGetUniformLocation(mario_shader, 'Light_ambient'),
        'Light_diffuse': glGetUniformLocation(mario_shader, 'Light_diffuse'),
        'Light_location': glGetUniformLocation(mario_shader, 'Light_location'),
        'Light_specular': glGetUniformLocation(mario_shader, 'Light_specular'),
        'Material_ambient': glGetUniformLocation(mario_shader, 'Material_ambient'),
        'Material_diffuse': glGetUniformLocation(mario_shader, 'Material_diffuse'),
        'Material_shininess': glGetUniformLocation(mario_shader, 'Material_shininess'),
        'Material_specular': glGetUniformLocation(mario_shader, 'Material_specular'),
    }

    # Carregar textura do Mario
    global mario_ID
    mario_img = Image.open('texture/mario.png')
    w, h, mario_img = mario_img.size[0], mario_img.size[1], mario_img.tobytes("raw", "RGB", 0, -1)
    mario_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, mario_ID)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, mario_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Inicializa o GLUT e inicia o loop de eventos
glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")
init()
mario = pywavefront.Wavefront("texture/mario.obj")
glutDisplayFunc(display)
glutReshapeFunc(camera)
glutTimerFunc(30, animacao, 1)
glutSpecialFunc(KeysEspecial)
glutKeyboardFunc(Keys)
glutMainLoop()