import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math

# --- ESTADO GLOBAL ---
pos_x, pos_y, pos_z = 0.0, 0.0, 0.0
velocidade = 0.05 
ang_ombro = 0.0
braco_levantado = False
tempo_caminhada = 0.0
offset_lava = 0.0

# --- NOVAS VARIÃVEIS PARA A CÃ‚MERA E MOUSE ---
yaw = -90.0         # RotaÃ§Ã£o horizontal (olhar para os lados)
pitch = 0.0         # RotaÃ§Ã£o vertical (olhar para cima/baixo)
last_x = 500.0      # Ãšltima posiÃ§Ã£o X do mouse
last_y = 400.0      # Ãšltima posiÃ§Ã£o Y do mouse
first_mouse = True  # Evita pulos na cÃ¢mera ao iniciar o script
camera_primeira_pessoa = False
p_pressionado = False # Trava para o clique da tecla P

# --- CALLBACK DE MOVIMENTAÃ‡ÃƒO DO MOUSE ---
def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse
    
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False
        
    xoffset = xpos - last_x
    yoffset = last_y - ypos # Invertido: coordenadas Y vÃ£o de cima para baixo
    
    last_x = xpos
    last_y = ypos
    
    sensibilidade = 0.1
    xoffset *= sensibilidade
    yoffset *= sensibilidade
    
    yaw += xoffset
    pitch += yoffset
    
    # Limita o Ã¢ngulo vertical para a cÃ¢mera nÃ£o dar uma cambalhota
    if pitch > 89.0: pitch = 89.0
    if pitch < -89.0: pitch = -89.0

# --- CARREGAMENTO DE TEXTURAS ---
def carregar_textura(arquivo):
    # Resolve path relative to this script so the working directory doesn't matter
    try:
        base = os.path.dirname(__file__)
        caminho = os.path.join(base, arquivo)
        img = Image.open(caminho)
        img = img.convert("RGBA")
        img_data = img.tobytes("raw", "RGBA", 0, -1)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return tex_id
    except Exception as e:
        print(f"Warning: failed to load texture '{arquivo}' ({e}). Using fallback texture.")
        # Create a 1x1 white fallback texture so GL calls still receive a valid texture id
        white_pixel = bytes([255, 255, 255, 255])
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, white_pixel)
        return tex_id

def desenhar_bloco(sx, sy, sz, tex_id, rep_u=1.0, rep_v=1.0, off_v=0.0):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glPushMatrix()
    glScalef(sx, sy, sz)
    glBegin(GL_QUADS)
    # Face Superior (Y+)
    glTexCoord2f(0, 0 + off_v);          glVertex3f(-0.5, 0.5, 0.5)
    glTexCoord2f(rep_u, 0 + off_v);      glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(rep_u, rep_v + off_v);  glVertex3f(0.5, 0.5, -0.5)
    glTexCoord2f(0, rep_v + off_v);      glVertex3f(-0.5, 0.5, -0.5)
    # Outras faces (simplificadas)
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5);  glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(1, 1); glVertex3f(0.5, 0.5, 0.5);    glTexCoord2f(0, 1); glVertex3f(-0.5, 0.5, 0.5)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

def desenhar_membro(lado, ang, tex_id, eh_perna=False):
    glPushMatrix()
    tx = 0.75 * lado if not eh_perna else 0.35 * lado
    ty = 0.6 if not eh_perna else -0.8
    glTranslatef(tx, ty, 0)
    glRotatef(ang, 1, 0, 0)
    glTranslatef(0, -0.4, 0)
    desenhar_bloco(0.3, 0.8, 0.3, tex_id)
    glPopMatrix()

# --- FUNÃ‡ÃƒO PARA DESENHAR OS 4 CUBOS DE REFERÃŠNCIA ---
def desenhar_cubos_referencia(tex_id):
    # Define 4 posiÃ§Ãµes espalhadas pelo cenÃ¡rio ao redor do inÃ­cio
    posicoes = [
        (-6.0, -1.5, -6.0),
        (2.0, -1.5, -12.0),
        (-5.0, -1.5, 8.0),
        (12.0, -1.5, -4.0) # Perto da lava
    ]
    for pos in posicoes:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        desenhar_bloco(1.5, 1.5, 1.5, tex_id)
        glPopMatrix()

def main():
    global pos_x, pos_y, pos_z, ang_ombro, braco_levantado, tempo_caminhada, offset_lava
    global camera_primeira_pessoa, p_pressionado
    
    if not glfw.init(): return
    window = glfw.create_window(1000, 800, "Robo Interativo - Mouse Look & 1Pessoa", None, None)
    if not window:
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)

    # Captura o mouse e esconde o cursor padrÃ£o do sistema dentro da janela
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    tex_corpo = carregar_textura("roblox.png")
    tex_rosto = carregar_textura("rosto.png")
    tex_grama = carregar_textura("grama.png")
    tex_lava  = carregar_textura("lava.png")

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 1.25, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        # --- PROCESSAMENTO DE ENTRADA ---
        movendo = False
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS: pos_z -= velocidade; movendo = True
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS: pos_z += velocidade; movendo = True
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS: pos_x -= velocidade; movendo = True
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS: pos_x += velocidade; movendo = True

        # Toggle da cÃ¢mera (Tecla P) com trava de gatilho
        if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
            if not p_pressionado:
                camera_primeira_pessoa = not camera_primeira_pessoa
                p_pressionado = True
        if glfw.get_key(window, glfw.KEY_P) == glfw.RELEASE:
            p_pressionado = False

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)


        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            braco_levantado = True
            if ang_ombro > -150: ang_ombro -= 5
        else:
            braco_levantado = False
            if ang_ombro < 0: ang_ombro += 5

        offset_lava -= 0.005 
        if movendo: tempo_caminhada += 0.1
        balanco = math.sin(tempo_caminhada) * 30

        if 4.0 < pos_x < 10.0:
            if not braco_levantado: pos_y -= 0.03 
        elif pos_y < 0:
            pos_y += 0.03 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # --- CÃLCULO DO VETOR DIREÃ‡ÃƒO DA CÃ‚MERA (Trigonometria EsfÃ©rica) ---
        front_x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
        front_y = math.sin(math.radians(pitch))
        front_z = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))

        if camera_primeira_pessoa:
            # 1Âª Pessoa: Olhos posicionados na altura da cabeÃ§a do robÃ´ (pos_y + 1.1)
            cam_x, cam_y, cam_z = pos_x, pos_y + 1.1, pos_z
            gluLookAt(cam_x, cam_y, cam_z, 
                      cam_x + front_x, cam_y + front_y, cam_z + front_z, 
                      0, 1, 0)
        else:
            # 3Âª Pessoa: CÃ¢mera orbita a uma distÃ¢ncia fixa atrÃ¡s do vetor de olhar do mouse
            cam_x = pos_x - front_x * 12
            cam_y = pos_y + 5.0 - front_y * 5 # Levemente elevada para visÃ£o superior
            cam_z = pos_z - front_z * 12
            gluLookAt(cam_x, cam_y, cam_z, 
                      pos_x, pos_y, pos_z, 
                      0, 1, 0)

        # 1. CHÃƒO DE GRAMA
        glPushMatrix()
        glTranslatef(0, -2.5, 0) 
        desenhar_bloco(200, 0.1, 200, tex_grama, rep_u=40.0, rep_v=40.0)
        glPopMatrix()

        # 2. RIO DE LAVA
        glPushMatrix()
        glTranslatef(7.0, -2.48, 0) 
        desenhar_bloco(6, 0.2, 200, tex_lava, rep_u=1.0, rep_v=20.0, off_v=offset_lava)
        glPopMatrix()

        # 4 CUBOS DE REFERÃŠNCIA (Para perceber a cÃ¢mera girando)
        desenhar_cubos_referencia(tex_corpo)

        # 3. ROBÃ” 
        # Ocultamos o robÃ´ em 1Âª pessoa para que a cÃ¢mera nÃ£o veja o lado de dentro do prÃ³prio rosto
        if not camera_primeira_pessoa:
            glPushMatrix()
            glTranslatef(pos_x, pos_y, pos_z)
            
            # Tronco e CabeÃ§a
            desenhar_bloco(1.2, 1.6, 0.6, tex_corpo)
            glPushMatrix()
            glTranslatef(0, 1.1, 0); desenhar_bloco(0.7, 0.7, 0.7, tex_rosto)
            glPopMatrix()

            # BraÃ§os e Pernas
            desenhar_membro(1, ang_ombro if braco_levantado else -balanco, tex_corpo)
            desenhar_membro(-1, balanco, tex_corpo)
            desenhar_membro(1, balanco, tex_corpo, True)
            desenhar_membro(-1, -balanco, tex_corpo, True)

            glPopMatrix()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()