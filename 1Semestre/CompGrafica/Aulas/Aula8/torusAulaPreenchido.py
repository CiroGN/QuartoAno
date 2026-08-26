import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# --- FUNÃ‡ÃƒO MATEMÃTICA DO TÃ“RUS SÃ“LIDO ---
def desenhar_torus_solido(R, r, fatias_maiores=40, fatias_menores=30):
    """
    R: Raio maior (distÃ¢ncia do centro atÃ© ao meio do tubo)
    r: Raio menor (espessura do prÃ³prio tubo)
    """
    for i in range(fatias_maiores):
        phi1 = 2.0 * math.pi * i / fatias_maiores
        phi2 = 2.0 * math.pi * (i + 1) / fatias_maiores
        
        # GL_QUAD_STRIP desenha uma sequÃªncia contÃ­nua de retÃ¢ngulos unindas duas circunferÃªncias vizinhas
        glBegin(GL_QUAD_STRIP)
        for j in range(fatias_menores + 1):
            theta = 2.0 * math.pi * j / fatias_menores
            
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            
            # --- VÃ‰RTICE DO ARO ATUAL (phi1) ---
            x1 = (R + r * cos_theta) * math.cos(phi1)
            y1 = r * sin_theta
            z1 = (R + r * cos_theta) * math.sin(phi1)
            
            # CÃ¡lculo da 'Normal' (Vetor que diz ao OpenGL para onde a face aponta, essencial para a luz)
            nx1 = cos_theta * math.cos(phi1)
            ny1 = sin_theta
            nz1 = cos_theta * math.sin(phi1)
            
            glNormal3f(nx1, ny1, nz1) # Diz Ã  luz como bater nesta curva
            glVertex3f(x1, y1, z1)    # Desenha o ponto
            
            # --- VÃ‰RTICE DO ARO SEGUINTE (phi2) ---
            x2 = (R + r * cos_theta) * math.cos(phi2)
            y2 = r * sin_theta
            z2 = (R + r * cos_theta) * math.sin(phi2)
            
            nx2 = cos_theta * math.cos(phi2)
            ny2 = sin_theta
            nz2 = cos_theta * math.sin(phi2)
            
            glNormal3f(nx2, ny2, nz2)
            glVertex3f(x2, y2, z2)
        glEnd()

# --- CONFIGURAÃ‡ÃƒO DA LUZ ---
def configurar_iluminacao():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) # Liga a primeira lÃ¢mpada do OpenGL
    
    # Define a posiÃ§Ã£o da luz (vinda de cima e da direita)
    posicao_luz = [5.0, 5.0, 5.0, 0.0] 
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    
    # Define a cor da luz (Luz branca difusa)
    cor_luz = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, cor_luz)
    
    # Permite que o glColor3f funcione mesmo com as luzes ligadas
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def main():
    if not glfw.init():
        return
        
    window = glfw.create_window(800, 600, "TÃ³rus SÃ³lido com Volume 3D", None, None)
    glfw.make_context_current(window)
    
    # Ativa o Z-Buffer (para que a parte da frente esconda a parte de trÃ¡s)
    glEnable(GL_DEPTH_TEST)

    # ConfiguraÃ§Ã£o da cÃ¢mara
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    
    glClearColor(0.2, 0.2, 0.25, 1.0) # Fundo cinzento-azulado

    # Chama a funÃ§Ã£o que criÃ¡mos para acender a luz do cenÃ¡rio
    configurar_iluminacao()

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # CÃ¢mera ligeiramente inclinada para ver o volume
        gluLookAt(0.0, 6.0, 10.0,   0.0, 0.0, 0.0,   0.0, 1.0, 0.0)

        # Roda o TÃ³rus continuamente na tela
        tempo = glfw.get_time()
        glRotatef(tempo * 40.0, 1.0, 0.5, 0.0)

        # Cor do material (Laranja "Donut")
        glColor3f(1.0, 0.5, 0.2) 
        
        # Desenha o objeto sÃ³lido
        desenhar_torus_solido(R=2.5, r=1.0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()