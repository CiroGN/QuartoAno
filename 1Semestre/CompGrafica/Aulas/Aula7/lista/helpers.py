import numpy as np
from OpenGL.GL import *
import math


def criar_textura_checkerboard(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    check = size // 8
    for i in range(size):
        for j in range(size):
            if ((i // check) + (j // check)) % 2 == 0:
                data[i, j] = [255, 255, 255]
            else:
                data[i, j] = [50, 50, 50]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_atlas(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    cores = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255], [0, 255, 255]]
    tile = size // 3
    for i in range(2):
        for j in range(3):
            idx = i * 3 + j
            if idx < 6:
                x = j * tile
                y = i * tile
                data[y:y+tile, x:x+tile] = cores[idx]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_agua(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            val = int(100 + 50 * math.sin(i * 0.02) * math.cos(j * 0.02))
            data[i, j] = [val // 3, val, 200]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    return tex_id


def criar_textura_terra(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            val = math.sin(i * 0.01) * math.cos(j * 0.01)
            if val > 0.3:
                data[i, j] = [34, 139, 34]
            else:
                data[i, j] = [0, 100, 200]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_nuvens(size=256):
    data = np.zeros((size, size, 4), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            val = int(150 + 100 * math.sin(i * 0.02) * math.cos(j * 0.02))
            data[i, j] = [255, 255, 255, val // 2]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def criar_textura_skybox(size=256):
    data = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            ratio = i / size
            if ratio < 0.7:
                val = int(135 + 120 * ratio)
                data[i, j] = [val, val, 255]
            else:
                data[i, j] = [139, 90, 43]
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def desenhar_cubo_skybox():
    t = 100.0
    glDisable(GL_CULL_FACE)
    glBegin(GL_QUADS)
    faces = [
        ([(0,0,-t,-t,t), (1,0,t,-t,t), (1,1,t,t,t), (0,1,-t,t,t)], (0,0,1)),
        ([(1,0,-t,-t,-t), (1,1,-t,t,-t), (0,1,t,t,-t), (0,0,t,-t,-t)], (0,0,-1)),
        ([(0,1,-t,t,-t), (0,0,-t,t,t), (1,0,t,t,t), (1,1,t,t,-t)], (0,1,0)),
        ([(1,1,-t,-t,-t), (0,1,t,-t,-t), (0,0,t,-t,t), (1,0,-t,-t,t)], (0,-1,0)),
        ([(0,0,t,-t,-t), (0,1,t,t,-t), (1,1,t,t,t), (1,0,t,-t,t)], (1,0,0)),
        ([(1,0,-t,-t,-t), (1,0,-t,-t,t), (0,0,-t,t,t), (0,1,-t,t,-t)], (-1,0,0)),
    ]
    for verts, norm in faces:
        glNormal3f(*norm)
        for u, v, x, y, z in verts:
            glTexCoord2f(u, v)
            glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_CULL_FACE)
