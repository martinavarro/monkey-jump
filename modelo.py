"""
Hacemos los modelos
"""

import scene_graph2 as sg
import basic_shapes as bs
import transformations2 as tr2
import easy_shaders as es
import numpy as np

from OpenGL.GL import *

class Monkey(object):

    def __init__(self, texture1):
        self.monkey = es.toGPUShape(bs.createTextureQuad(texture1), GL_REPEAT, GL_LINEAR)
        self.transmonkey = np.matmul(tr2.translate(0, -0.8, 0), tr2.scale(0.4, 0.4, 1))
        self.pos = 0
        self.jump = False

    def jumping(self):
        self.jump= not self.jump


    def draw (self, pipeline, texture1, texture2):
        if self.jump:
            self.monkey= es.toGPUShape(bs.createTextureQuad(texture2), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

        else:
            self.monkey = es.toGPUShape(bs.createTextureQuad(texture1), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

    def move_left(self):
        if self.pos == 0:
            self.transmonkey = np.matmul(tr2.translate(-0.7, -0.8, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = -1
        elif self.pos == 1:
            self.transmonkey = np.matmul(tr2.translate(0, -0.8, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = 0

    def move_right(self):
        if self.pos == 0:
            self.transmonkey = np.matmul(tr2.translate(0.7, -0.8, 0), tr2.scale(-0.4, 0.4, 1))
            self.pos = 1
        elif self.pos == -1:
            self.transmonkey = np.matmul(tr2.translate(0, -0.8, 0), tr2.scale(-0.4, 0.4, 1))
            self.pos= 0

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


import csv
from typing import List

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

    def draw (self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        self.model.transform = tr2.translate(0.7*self.pos_x, 0.5*self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")


    def move_left(self):
        self.pos_x=-1

    def move_right(self):
        self.pos_x=1

    def height(self,cont):
        if cont==0:
            self.pos_y= -1
        if cont==1:
            self.pos_y= 0
        if cont==2:
            self.pos_y= 1


class Plataforms(object):
    plataforms: List['Plataform']

    def __init__(self):
        self.plataforms = []

    def create_plataforms(self):
        with open('structure .csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                for i in range(3):
                    if row[i] == '1' and line_count<=3:
                        if i==0:
                            p= Plataform()
                            p.move_left()
                            p.height(line_count)
                            self.plataforms.append(p)
                        elif i==2:
                            p= Plataform()
                            p.move_right()
                            p.height(line_count)
                            self.plataforms.append(p)
                        elif i==1:
                            p= Plataform()
                            p.height(line_count)
                            self.plataforms.append(p)

                line_count += 1


    def draw(self, pipeline):
        for k in self.plataforms:
            k.draw(pipeline)




class Background():

    def __init__(self, texture):
        self.background = es.toGPUShape(bs.createTextureQuad(texture), GL_REPEAT, GL_LINEAR)
        self.transbackground = np.matmul(tr2.translate(0, 0, 0), tr2.scale(2, 2, 1))

    def draw (self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transbackground)
        pipeline.drawShape(self.background)


