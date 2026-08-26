##Código para as aulas comentado 
import glfw              #Graphics Library Framework 
#Gerencia a janela e eventos (teclado/mouse) 
# Mais atual que o GLUT  // O SDL é mais indicado para jogos / multimídia 
 
from OpenGL.GL import * # Funções principais de desenho e estados do OpenGL 
from OpenGL.GLU import * # Funções utilitárias para matrizes de câmera e projeção 
 
def desenhar_cubo(): 
    """ Define a geometria e as cores do cubo face por face """ 
    glBegin(GL_QUADS)    # Instrução para o OpenGL agrupar cada 4 vértices em um quadrado 
     
    # --- Face Frontal (Vermelha) --- 
    glColor3f(1, 0, 0)   # Define a cor do "pincel" (R, G, B) 
    glVertex3f(-1, -1,  1); glVertex3f( 1, -1,  1); glVertex3f( 1,  1,  1); glVertex3f(-1,  1,  1) 
     
    # --- Face Traseira (Verde) --- 
    glColor3f(0, 1, 0) 
    glVertex3f(-1, -1, -1); glVertex3f(-1,  1, -1); glVertex3f( 1,  1, -1); glVertex3f( 1, -1, -1) 
     
    # --- Face Superior (Azul) --- 
    glColor3f(0, 0, 1) 
    glVertex3f(-1,  1, -1); glVertex3f(-1,  1,  1); glVertex3f( 1,  1,  1); glVertex3f( 1,  1, -1) 
     
    # --- Face Inferior (Amarela) --- 
    glColor3f(1, 1, 0) 
    glVertex3f(-1, -1, -1); glVertex3f( 1, -1, -1); glVertex3f( 1, -1,  1); glVertex3f(-1, -1,  1) 
     
    # --- Face Direita (Magenta) --- 
    glColor3f(1, 0, 1) 
    glVertex3f( 1, -1, -1); glVertex3f( 1,  1, -1); glVertex3f( 1,  1,  1); glVertex3f( 1, -1,  1) 
     
    # --- Face Esquerda (Ciano) --- 
    glColor3f(0, 1, 1) 
    glVertex3f(-1, -1, -1); glVertex3f(-1, -1,  1); glVertex3f(-1,  1,  1); glVertex3f(-1,  1, -1) 
     
    glEnd() # Finaliza o envio de vértices para a placa de vídeo 
 
def main(): 
    # Inicializa o framework GLFW 
    if not glfw.init():  
        return 
     
    # Cria a janela onde o conteúdo será renderizado 
    janela = glfw.create_window(800, 600, "Aprendendo OpenGL 3D", None, None) 
    if not janela: 
        glfw.terminate() 
        return 
 
    # Ativa o contexto OpenGL nesta janela específica 
    glfw.make_context_current(janela) 
     
    # Ativa o Z-Buffer (Depth Test). Sem isso, as faces de trás seriam desenhadas  
    # por cima das da frente se fossem processadas por último no código. 
    glEnable(GL_DEPTH_TEST) 
 
    # --- Configuração da Lente (Projeção) --- 
    glMatrixMode(GL_PROJECTION) # Entra no modo de edição da "lente da câmera" 
    glLoadIdentity()            # Limpa qualquer configuração anterior 
    # Parâmetros: (Campo de visão em graus, Proporção da tela, Distância mínima, Distância máxima) 
    gluPerspective(45, 800/600, 0.1, 50.0) 
     
    # --- Configuração do Mundo (Modelview) --- 
    glMatrixMode(GL_MODELVIEW) # Entra no modo de posicionar objetos e a própria câmera 
 
    # Loop que mantém o programa rodando até fechar a janela 
    while not glfw.window_should_close(janela): 
        # Limpa a tela com a cor de fundo (preto por padrão) e limpa o buffer de profundidade 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
         
        # Reseta a matriz de transformação para o centro (0,0,0) 
        glLoadIdentity() 
         
        # Move o objeto 5 unidades para "dentro" da tela (afastando-o de nós) 
        # O OpenGL usa um sistema de mão direita, então -Z entra na tela. 
        glTranslatef(0, 0, -5)  # testar com -51 
         
        # Rotaciona o espaço. Parâmetros: (ângulo em graus, eixo_x, eixo_y, eixo_z) 
        # Aqui ele gira 50 graus por segundo nos eixos X e Y simultaneamente. 
        glRotatef(glfw.get_time() * 50, 1, 1, 0) 
 
        # Executa os comandos de desenho definidos na função lá em cima 
        desenhar_cubo() 
         
        # Inverte o buffer de desenho com o buffer de exibição (Double Buffering) 
        # Isso evita que vejamos a imagem sendo "escaneada" ou piscando. 
        glfw.swap_buffers(janela) 
         
        # Verifica se houve eventos (teclado, mouse, redimensionamento) 
        glfw.poll_events() 
 
    # Finaliza e limpa os recursos do sistema 
    glfw.terminate() 
 
# Execução do programa 
if __name__ == "__main__": 
    main()