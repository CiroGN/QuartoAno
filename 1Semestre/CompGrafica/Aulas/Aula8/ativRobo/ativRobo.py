import os
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math

# --- ESTADO GLOBAL DO JOGADOR E VEÍCULO ---
pos_x, pos_y, pos_z = 0.0, 0.0, 0.0
velocidade = 0.06 
ang_ombro = 0.0
braco_levantado = False
tempo_caminhada = 0.0
offset_lava = 0.0

# --- CONFIGURAÃ‡ÃƒO DA FONTE DE LUZ FIXA (O POSTE) ---
# Definido globalmente para evitar o NameError
posicao_da_luz = [5.0, 15.0, 5.0]
altura_da_grama = -2.5

# CÃ¢mera e Mouse
yaw = -90.0         
pitch = -20.0       
last_x, last_y = 500.0, 400.0
first_mouse = True  
camera_primeira_pessoa = False

# Gatilhos de Teclas
v_pressionado = False
p_pressionado = False
c_pressionado = False
e_pressionado = False

# --- SISTEMA DE INVENTÁRIO E MUNDO ---
player_angle = 0.0
held_item = None  
dropped_items = [] 
car_built = False
is_driving = False
car_x, car_z = -5.0, 0.0

# AnimaÃ§Ãµes de Entidades
animal_jump_timer = 0.0
animal_y = -1.5

# IDs dos Blocos
PAREDE, PORTA_JANELA, TETO, PIRAMIDE_CARRO, CORPO_CARRO, RODA_TORUS = 0, 1, 2, 3, 4, 5

spawners = {
    PAREDE: (13.0, -1.5, -5.0),
    PORTA_JANELA: (13.0, -1.5, -3.0),
    TETO: (13.0, -1.5, -1.0),
    PIRAMIDE_CARRO: (13.0, -1.5, 1.0),
    CORPO_CARRO: (13.0, -1.5, 3.0),
    RODA_TORUS: (13.0, -1.5, 5.0)
}

# --- MATRIZ DE SOMBRA PROJETADA (LUZ DE POSTE / PONTO) ---
def construir_matriz_sombra_poste(luz_pos, chao_y):
    lx, ly, lz = luz_pos[0], luz_pos[1], luz_pos[2]
    # Matriz matemÃ¡tica que distorce os blocos radialmente a partir da lÃ¢mpada
    matriz_lista = [
        ly - chao_y, 0.0,         0.0,  0.0,
        -lx,         -chao_y,     -lz, -1.0,
        0.0,         0.0,         ly - chao_y,  0.0,
        lx * chao_y, chao_y * ly, lz * chao_y,  ly
    ]
    return (GLfloat * 16)(*matriz_lista)

# --- CALLBACK DO MOUSE ---
def mouse_callback(window, xpos, ypos):
    global yaw, pitch, last_x, last_y, first_mouse
    if first_mouse:
        last_x, last_y = xpos, ypos
        first_mouse = False
    xoffset = xpos - last_x
    yoffset = last_y - ypos
    last_x, last_y = xpos, ypos
    
    sensibilidade = 0.1
    yaw += xoffset * sensibilidade
    pitch += yoffset * sensibilidade
    if pitch > 89.0: pitch = 89.0
    if pitch < -89.0: pitch = -89.0

# --- CARREGAMENTO DE TEXTURAS ---
def carregar_textura(arquivo):
    try:
        caminho = os.path.join(os.path.dirname(__file__), arquivo)
        img = Image.open(caminho)
        img_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return tex_id
    except Exception as e:
        print(f"Erro ao carregar textura {arquivo}: {e}")
        return None

# --- PRIMITIVAS GRÃFICAS ---
def desenhar_bloco(sx, sy, sz, tex_id, rep_u=1.0, rep_v=1.0, off_v=0.0):
    if tex_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
    else:
        glDisable(GL_TEXTURE_2D)
        
    glPushMatrix()
    glScalef(sx, sy, sz)
    glBegin(GL_QUADS)
    # Face Superior
    glTexCoord2f(0, 0 + off_v);          glVertex3f(-0.5, 0.5, 0.5)
    glTexCoord2f(rep_u, 0 + off_v);      glVertex3f(0.5, 0.5, 0.5)
    glTexCoord2f(rep_u, rep_v + off_v);  glVertex3f(0.5, 0.5, -0.5)
    glTexCoord2f(0, rep_v + off_v);      glVertex3f(-0.5, 0.5, -0.5)
    # Face Inferior
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5); glTexCoord2f(rep_u, 0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(rep_u, rep_v); glVertex3f(0.5, -0.5, 0.5); glTexCoord2f(0, rep_v); glVertex3f(-0.5, -0.5, 0.5)
    # Face Frontal
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5); glTexCoord2f(rep_u, 0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(rep_u, rep_v); glVertex3f(0.5, 0.5, 0.5); glTexCoord2f(0, rep_v); glVertex3f(-0.5, 0.5, 0.5)
    # Face Traseira
    glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, -0.5); glTexCoord2f(rep_u, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(rep_u, rep_v); glVertex3f(-0.5, 0.5, -0.5); glTexCoord2f(0, rep_v); glVertex3f(0.5, 0.5, -0.5)
    # Face Direita
    glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, 0.5); glTexCoord2f(rep_u, 0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(rep_u, rep_v); glVertex3f(0.5, 0.5, -0.5); glTexCoord2f(0, rep_v); glVertex3f(0.5, 0.5, 0.5)
    # Face Esquerda
    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5); glTexCoord2f(rep_u, 0); glVertex3f(-0.5, -0.5, 0.5)
    glTexCoord2f(rep_u, rep_v); glVertex3f(-0.5, 0.5, 0.5); glTexCoord2f(0, rep_v); glVertex3f(-0.5, 0.5, -0.5)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

def desenhar_piramide(sx, sy, sz, tex_id):
    if tex_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
    else:
        glDisable(GL_TEXTURE_2D)
    glPushMatrix()
    glScalef(sx, sy, sz)
    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 1); glVertex3f(0, 0.5, 0);    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, 0.5);  glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, 0.5)
    glTexCoord2f(0.5, 1); glVertex3f(0, 0.5, 0);    glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, 0.5);   glTexCoord2f(1, 0); glVertex3f(0.5, -0.5, -0.5)
    glTexCoord2f(0.5, 1); glVertex3f(0, 0.5, 0);    glTexCoord2f(0, 0); glVertex3f(0.5, -0.5, -0.5);  glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, -0.5)
    glTexCoord2f(0.5, 1); glVertex3f(0, 0.5, 0);    glTexCoord2f(0, 0); glVertex3f(-0.5, -0.5, -0.5); glTexCoord2f(1, 0); glVertex3f(-0.5, -0.5, 0.5)
    glEnd()
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

def desenhar_torus(R, r, tex_id):
    if tex_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
    else:
        glDisable(GL_TEXTURE_2D)
    num_loops, num_fatias = 16, 8
    for i in range(num_loops):
        phi1 = 2.0 * math.pi * i / num_loops
        phi2 = 2.0 * math.pi * (i + 1) / num_loops
        glBegin(GL_QUAD_STRIP)
        for j in range(num_fatias + 1):
            theta = 2.0 * math.pi * j / num_fatias
            cos_t, sin_t = math.cos(theta), math.sin(theta)
            glVertex3f((R + r * cos_t) * math.cos(phi1), (R + r * cos_t) * math.sin(phi1), r * sin_t)
            glVertex3f((R + r * cos_t) * math.cos(phi2), (R + r * cos_t) * math.sin(phi2), r * sin_t)
        glEnd()
    glDisable(GL_TEXTURE_2D)

def renderizar_peca(tipo, tex_corpo):
    if tipo == PAREDE:              desenhar_bloco(1.2, 1.0, 0.2, tex_corpo)
    elif tipo == PORTA_JANELA:      desenhar_bloco(0.6, 1.2, 0.2, tex_corpo)
    elif tipo == TETO:              desenhar_bloco(1.5, 0.3, 1.5, tex_corpo)
    elif tipo == PIRAMIDE_CARRO:    desenhar_piramide(1.0, 1.0, 1.0, tex_corpo)
    elif tipo == CORPO_CARRO:       desenhar_bloco(1.8, 0.6, 1.2, tex_corpo)
    elif tipo == RODA_TORUS:        
        glPushMatrix(); glRotatef(90, 0, 1, 0)
        desenhar_torus(0.4, 0.15, tex_corpo); glPopMatrix()

def desenhar_membro(lado, ang, tex_id, eh_perna=False):
    glPushMatrix()
    tx = 0.75 * lado if not eh_perna else 0.35 * lado
    ty = 0.6 if not eh_perna else -0.8
    glTranslatef(tx, ty, 0)
    glRotatef(ang, 1, 0, 0)
    glTranslatef(0, -0.4, 0)
    desenhar_bloco(0.3, 0.8, 0.3, tex_id)
    glPopMatrix()

def desenhar_geometria_robo(tex_corpo, tex_rosto, balanco, braco_levantado, ang_ombro, primeira_pessoa=False):
    if primeira_pessoa: return 
    glPushMatrix()
    desenhar_bloco(1.2, 1.6, 0.6, tex_corpo) 
    glPushMatrix()
    glTranslatef(0, 1.1, 0); desenhar_bloco(0.7, 0.7, 0.7, tex_rosto) 
    glPopMatrix()
    desenhar_membro(1, ang_ombro if braco_levantado else -balanco, tex_corpo)
    desenhar_membro(-1, balanco, tex_corpo)
    desenhar_membro(1, balanco, tex_corpo, True)
    desenhar_membro(-1, -balanco, tex_corpo, True)
    glPopMatrix()

def desenhar_geometria_carro(tex_corpo):
    glPushMatrix()
    desenhar_bloco(1.8, 0.6, 1.2, tex_corpo) 
    glPushMatrix()
    glTranslatef(1.2, -0.1, 0); glRotatef(-90, 0, 0, 1)
    desenhar_piramide(0.6, 0.8, 1.2, tex_corpo) 
    glPopMatrix()
    pos_rodas = [(0.6, -0.3, 0.6), (0.6, -0.3, -0.6), (-0.6, -0.3, 0.6), (-0.6, -0.3, -0.6)]
    for r_pos in pos_rodas:
        glPushMatrix()
        glTranslatef(r_pos[0], r_pos[1], r_pos[2]); glRotatef(90, 0, 1, 0)
        desenhar_torus(0.3, 0.1, tex_corpo); glPopMatrix()
    glPopMatrix()

def checar_fabrica():
    global car_built, dropped_items
    itens_fabrica = [i for i in dropped_items if i['x'] < -2.0 and abs(i['z']) < 4.0]
    tori = [i for i in itens_fabrica if i['type'] == RODA_TORUS]
    piramides = [i for i in itens_fabrica if i['type'] == PIRAMIDE_CARRO]
    retangulos = [i for i in itens_fabrica if i['type'] == CORPO_CARRO]
    
    if len(tori) >= 4 and len(piramides) >= 1 and len(retangulos) >= 1:
        for _ in range(4): dropped_items.remove(tori[_])
        dropped_items.remove(piramides[0])
        dropped_items.remove(retangulos[0])
        car_built = True

def main():
    global pos_x, pos_y, pos_z, ang_ombro, braco_levantado, tempo_caminhada, offset_lava, player_angle
    global camera_primeira_pessoa, v_pressionado, p_pressionado, c_pressionado, e_pressionado
    global held_item, dropped_items, car_built, is_driving, car_x, car_z, animal_jump_timer, animal_y

    if not glfw.init(): return
    window = glfw.create_window(1000, 800, "Minecraft - RobÃ´ com sombra", None, None)
    if not window:
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, mouse_callback)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    tex_corpo = carregar_textura("roblox.png")
    tex_rosto = carregar_textura("rosto.png")
    tex_grama = carregar_textura("grama.png")
    tex_lava  = carregar_textura("lava.png")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.25, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    glClearColor(0.5, 0.7, 1.0, 1.0)

    while not glfw.window_should_close(window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        # --- PROCESSAMENTO DE INPUTS ---
        movendo = False
        forward_input = 0.0
        strafe_input = 0.0
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS: forward_input += 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS: forward_input -= 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS: strafe_input += 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS: strafe_input -= 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS: forward_input += 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS: forward_input -= 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS: strafe_input += 1.0; movendo = True
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS: strafe_input -= 1.0; movendo = True

        # Movimentação relativa à câmera no plano XZ
        forward_dir = [math.cos(math.radians(yaw)), 0.0, math.sin(math.radians(yaw))]
        right_dir = [-forward_dir[2], 0.0, forward_dir[0]]
        move_x = forward_dir[0] * forward_input + right_dir[0] * strafe_input
        move_z = forward_dir[2] * forward_input + right_dir[2] * strafe_input
        magnitude = math.hypot(move_x, move_z)
        if magnitude > 1e-6:
            move_x /= magnitude
            move_z /= magnitude
            dx = move_x * velocidade
            dz = move_z * velocidade
            if is_driving:
                car_x += dx; car_z += dz
                pos_x, pos_z = car_x, car_z
            else:
                pos_x += dx; pos_z += dz
            movendo = True
            player_angle = math.degrees(math.atan2(move_x, -move_z))
        else:
            if is_driving:
                # mantém o carro com a posição do jogador enquanto estiver dirigindo
                pos_x, pos_z = car_x, car_z

        if glfw.get_key(window, glfw.KEY_V) == glfw.PRESS and not v_pressionado:
            camera_primeira_pessoa = not camera_primeira_pessoa
            v_pressionado = True
        if glfw.get_key(window, glfw.KEY_V) == glfw.RELEASE: v_pressionado = False

        if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS and not p_pressionado:
            p_pressionado = True
            if held_item is None:
                for tipo, p_spawn in spawners.items():
                    if math.sqrt((pos_x - p_spawn[0])**2 + (pos_z - p_spawn[2])**2) < 2.0:
                        held_item = tipo; break
                if held_item is None:
                    for item in dropped_items:
                        if math.sqrt((pos_x - item['x'])**2 + (pos_z - item['z'])**2) < 2.0:
                            held_item = item['type']; dropped_items.remove(item); break
        if glfw.get_key(window, glfw.KEY_P) == glfw.RELEASE: p_pressionado = False

        if glfw.get_key(window, glfw.KEY_C) == glfw.PRESS and not c_pressionado:
            c_pressionado = True
            if held_item is not None:
                dropped_items.append({'type': held_item, 'x': pos_x, 'y': -1.8, 'z': pos_z})
                held_item = None; checar_fabrica()
        if glfw.get_key(window, glfw.KEY_C) == glfw.RELEASE: c_pressionado = False

        if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS and not e_pressionado:
            e_pressionado = True
            if car_built:
                if not is_driving and math.sqrt((pos_x - car_x)**2 + (pos_z - car_z)**2) < 2.5:
                    is_driving = True
                    pos_y = 0.5
                elif is_driving:
                    is_driving = False
                    pos_y = 0.0
        if glfw.get_key(window, glfw.KEY_E) == glfw.RELEASE: e_pressionado = False

        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            braco_levantado = True
            if ang_ombro > -150: ang_ombro -= 5
        else:
            braco_levantado = False
            if ang_ombro < 0: ang_ombro += 5

        offset_lava -= 0.005 
        if movendo: tempo_caminhada += 0.1
        balanco = math.sin(tempo_caminhada) * 30

        if 4.0 < pos_x < 10.0 and not is_driving:
            if not braco_levantado: pos_y -= 0.03
        elif pos_y < 0 and not is_driving:
            pos_y += 0.03

        dist_animal = math.sqrt((pos_x - (-3.0))**2 + (pos_z - (-5.0))**2)
        if dist_animal < 3.5:
            animal_jump_timer += 0.2
            animal_y = -1.5 + abs(math.sin(animal_jump_timer)) * 1.2
        else:
            animal_y = -1.5; animal_jump_timer = 0.0

        # --- SISTEMA DE CÃ‚MERA ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        front_x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
        front_y = math.sin(math.radians(pitch))
        front_z = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))

        if camera_primeira_pessoa:
            gluLookAt(pos_x, pos_y + 1.1, pos_z, pos_x + front_x, pos_y + 1.1 + front_y, pos_z + front_z, 0, 1, 0)
        else:
            gluLookAt(pos_x - front_x * 12, pos_y + 4.0 - front_y * 4, pos_z - front_z * 12, pos_x, pos_y, pos_z, 0, 1, 0)

        glColor4f(1.0, 1.0, 1.0, 1.0)

        # 1. CHÃO DE GRAMA
        glPushMatrix()
        glTranslatef(0.0, -2.5, 0.0)
        desenhar_bloco(400, 0.1, 400, tex_grama, rep_u=80.0, rep_v=80.0)
        glPopMatrix()

        # 2. RIO DE LAVA
        glColor4f(1.0, 0.4, 0.0, 1.0)
        glPushMatrix()
        glTranslatef(7.0, -2.48, 0.0)
        desenhar_bloco(6, 0.2, 400, tex_lava, rep_u=1.0, rep_v=40.0, off_v=offset_lava)
        glPopMatrix()
        glColor4f(1.0, 1.0, 1.0, 1.0)

        # 3. CRIAÃ‡Ã•ES E ENTIDADES NO CENÃRIO
        for tipo, p_spawn in spawners.items():
            glPushMatrix(); glTranslatef(p_spawn[0], p_spawn[1], p_spawn[2])
            glRotatef(glfw.get_time() * 25, 0, 1, 0); renderizar_peca(tipo, tex_corpo); glPopMatrix()

        for item in dropped_items:
            glPushMatrix(); glTranslatef(item['x'], item['y'], item['z']); renderizar_peca(item['type'], tex_corpo); glPopMatrix()

        # FÃ¡brica (Zona Verde)
        glPushMatrix(); glTranslatef(-5.0, -2.45, 0.0); glColor3f(0.2, 0.8, 0.2); desenhar_bloco(4.0, 0.01, 6.0, 0); glColor3f(1, 1, 1); glPopMatrix()

        # Ãrvore / Planta
        glColor3f(0.1, 0.8, 0.2)
        glPushMatrix(); glTranslatef(-4.0, -1.0, 6.0); desenhar_bloco(0.4, 1.5, 0.4, tex_corpo); glTranslatef(0, 1.0, 0); desenhar_bloco(1.5, 1.5, 1.5, tex_grama); glPopMatrix()
        glColor3f(1.0, 1.0, 1.0)
        
        # Animalzinho CÃºbico
        glPushMatrix(); glTranslatef(-3.0, animal_y, -5.0); desenhar_bloco(0.8, 0.6, 0.6, tex_corpo); glTranslatef(0.4, 0.3, 0); desenhar_bloco(0.4, 0.4, 0.4, tex_rosto); glPopMatrix()

        if car_built:
            glPushMatrix(); glTranslatef(car_x, -1.8, car_z); desenhar_geometria_carro(tex_corpo); glPopMatrix()

        if held_item is not None and not camera_primeira_pessoa:
            glPushMatrix(); glTranslatef(pos_x, pos_y + 1.8, pos_z); glRotatef(glfw.get_time() * 50, 0, 1, 0); renderizar_peca(held_item, tex_corpo); glPopMatrix()


        # =======================================================
        # 4. RENDERIZAÃ‡ÃƒO DAS SOMBRAS PROJETADAS DINÃ‚MICAS
        # =======================================================
        # Topo da grama = -2.45. Projetamos ligeiramente acima (-2.37) para evitar Z-fighting
        altura_segura_sombra = -2.37 
        matriz_sombra = construir_matriz_sombra_poste(posicao_da_luz, altura_segura_sombra)
        
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.45) 

        # Desliga a gravaÃ§Ã£o no Z-buffer temporariamente para a sombra nÃ£o piscar
        glDepthMask(GL_FALSE)

        #
        # --- Sombra do RobÃ´ ---
        glPushMatrix()
        # 1Âº: DÃ¡ o empurrÃ£ozinho final de 1 milÃ­metro para cima para nÃ£o piscar na grama
        glTranslatef(0.0, 0.01, 0.0) 
        
        # 2Âº: APLICA A MATRIZ DE LUZ (Achata tudo que vem depois)
        glMultMatrixf(matriz_sombra)      
        
        # 3Âº: Move o robÃ´ para o mundo real (Isso acontece ANTES da luz esmagar ele!)
        glTranslatef(pos_x, pos_y, pos_z) 
        
        desenhar_geometria_robo(0, 0, balanco, braco_levantado, ang_ombro, camera_primeira_pessoa)
        glPopMatrix()

        # --- Sombra do Carro (Se construÃ­do) ---
        if car_built:
            glPushMatrix()
            glTranslatef(0.0, 0.01, 0.0)
            glMultMatrixf(matriz_sombra) # A matriz vem primeiro!
            glTranslatef(car_x, -1.8, car_z) # O posicionamento vem depois!
            desenhar_geometria_carro(0)
            glPopMatrix()

        ######################
        '''
        # --- Sombra do RobÃ´ ---
        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z) # 1Âº: Move para o local correto
        glMultMatrixf(matriz_sombra)     # 2Âº: Achata radialmente a partir do poste
        desenhar_geometria_robo(0, 0, balanco, braco_levantado, ang_ombro, camera_primeira_pessoa)
        glPopMatrix()

        # --- Sombra do Carro (Se construÃ­do) ---
        if car_built:
            glPushMatrix()
            glTranslatef(car_x, -1.8, car_z)
            glMultMatrixf(matriz_sombra)
            desenhar_geometria_carro(0)
            glPopMatrix()
        '''
        # Restaura configuraÃ§Ãµes de desenho padrÃ£o
        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)

        # =======================================================
        # 5. ROBÃ” REAL (RENDER PASS FINAL)
        # =======================================================
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(pos_x, pos_y, pos_z)
        glRotatef(player_angle, 0, 1, 0)
        desenhar_geometria_robo(tex_corpo, tex_rosto, balanco, braco_levantado, ang_ombro, camera_primeira_pessoa)
        glPopMatrix()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()