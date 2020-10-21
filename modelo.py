"""
Hacemos los modelos
"""

import scene_graph2 as sg
import basic_shapes as bs
import transformations2 as tr2
import easy_shaders as es
import numpy as np
import csv
from typing import List


from OpenGL.GL import *

class Monkey(object):

    def __init__(self, texture1):
        self.monkey = es.toGPUShape(bs.createTextureQuad(texture1), GL_REPEAT, GL_LINEAR)
        self.transmonkey = np.matmul(tr2.translate(0, -0.74, 0), tr2.scale(0.4, 0.4, 1))
        self.pos = 0
        self.jump = False
        self.logic = False

    #ayuda a cambiar la expresión del monito cuando este salta
    def jumping(self):
        self.jump= not self.jump

    #dibuja el monito según su expresión
    def draw (self, pipeline, texture1, texture2):

        if self.jump: #cuando esta saltando
            self.monkey= es.toGPUShape(bs.createTextureQuad(texture2), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

        else: #cuando se encuentra en reposo
            self.monkey = es.toGPUShape(bs.createTextureQuad(texture1), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

#mueve el monito hacia la izquierda
    def move_left(self):
        if self.pos == 0:
            self.transmonkey = np.matmul(tr2.translate(-0.7, -0.74, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = -1
        elif self.pos == 1:
            self.transmonkey = np.matmul(tr2.translate(0, -0.74, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = 0

#mueve el monito hacia la derecha
    def move_right(self):
        if self.pos == 0:
            self.transmonkey = np.matmul(tr2.translate(0.7, -0.74, 0), tr2.scale(-0.4, 0.4, 1))
            self.pos = 1
        elif self.pos == -1:
            self.transmonkey = np.matmul(tr2.translate(0, -0.74, 0), tr2.scale(-0.4, 0.4, 1))
            self.pos= 0


    def activate(self):
        self.logic= not self.logic

    def collide(self, plataforms: 'Plataforms'):
        deleted_eggs = []
        n= len(plataforms.cont)

        #si salto y choco con la plataforma qu eestoy revisando, paso
        #si salto y no choco con la plataforma que estoy revisando: si son dos en esa fila, debo revisar la otra. y si es una, perdi. ¿ cp




class Banana():

    def __init__(self, texture):
        gpubanana = es.toGPUShape(bs.createTextureQuad(texture), GL_REPEAT, GL_LINEAR)

        banana = sg.SceneGraphNode('banana')
        banana.transform = tr2.scale(0.2)
        banana.childs += [gpubanana]

        banana_tr = sg.SceneGraphNode('bananaTR')
        banana_tr.childs += [banana]

        self.model= banana_tr
        self.last= False

    def appear(self):
        self.last= not self.last


    def draw (self, pipeline):
        if self.last:
            glUseProgram(pipeline.shaderProgram)
            self.model.transform= tr2.translate(0.7 * self.pos_x, 0.5 * self.pos_y, 0)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.model.transform)
            pipeline.drawShape(self.model)



class Plataform():

    def __init__(self):
        gpuBlackQuad = es.toGPUShape(bs.createColorQuad(0, 0, 0))

        plataform = sg.SceneGraphNode('plataform')
        plataform.transform = tr2.scale(0.5, 0.04, 1)
        plataform.childs += [gpuBlackQuad]

        plataform_tr = sg.SceneGraphNode('plataformTR')
        plataform_tr.childs += [plataform]

        self.model = plataform_tr
        self.pos_x = 0
        self.pos_y= -1

#dibuja una plataforma
    def draw (self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        self.model.transform = tr2.translate(0.7*self.pos_x, 0.47*self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

# ayudará a ubicar las plataformas según la columna en la que esten
    def move_left(self):
        self.pos_x=-1

#ayudará a ubicar la plataforma según la columna en la que este en el archivo csv
    def move_right(self):
        self.pos_x=1

#ayuda a ubicar la plataforma según en la fila que este en el archivo csv
    def height(self,dy):
        self.pos_y= dy

#bajará la plataforma cuando el monito avance
    def update(self):
        self.pos_y -= 1

#elevará la plataforma cuando el monito se caiga
    def caida(self):
        self.pos_y +=1

class Plataforms(object):
    plataforms: List['Plataform']

    def __init__(self):
        self.plataforms = []
        self.cont= []

#crea conjunto plataformas a partir de un archivo csv
    def create_plataforms(self):
        with open('structure .csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            dy= -1
            for row in csv_reader:
                cont = 0
                for i in range(3):
                    if row[i] == '1':
                        if i==0:
                            p= Plataform()
                            p.move_left()
                            p.height(dy)
                            self.plataforms.append(p)
                            cont+=1
                        elif i==2:
                            p= Plataform()
                            p.move_right()
                            p.height(dy)
                            self.plataforms.append(p)
                            cont += 1
                        elif i==1:
                            p= Plataform()
                            p.height(dy)
                            self.plataforms.append(p)
                            cont += 1
                dy+=1
                line_count += 1
                self.cont.append(cont)

#dibuja las plataformas
    def draw(self, pipeline):
        for k in self.plataforms:
            k.draw(pipeline)

#baja las plataformas cuando el monito avanza
    def update(self):
        for k in self.plataforms:
            k.update()

#sube las plataformas cuando el monito cae
    def updatecaida(self):
        for k in self.plataforms:
            k.caida()



class Background():

    def __init__(self, texture):
        self.background = es.toGPUShape(bs.createTextureQuad(texture), GL_REPEAT, GL_LINEAR)
        self.transbackground = np.matmul(tr2.translate(0, 0.2, 0), tr2.scale(2, 2.5, 1))
        self.nivel= 0 #indica en que nivel esta el monito, parte desde 0: suelo

    def draw (self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transbackground)
        pipeline.drawShape(self.background)

#mueve el fondo a medida que el monito avanza hacia arriba
    def moveup(self, c):
        self.transbackground = np.matmul(tr2.translate(0, 0.2 + c*-0.04, 0), tr2.scale(2, 2.5, 1))

#actualiza el fondo a medida que el monito avanza
    def updatebg(self):
        self.moveup(self.nivel)
        self.nivel += 1



