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
        self.jump = False #indicará si el monito esta saltando para poder dibujarlo con otra textura
        self.logic = False #indica si la lógica del juego está activa o no
        self.winner = False #indica si el jugador ganó o no
        self.level = 0 #indica en que nivel con respecto al suelo se encuentra el monito
        self.started = False #indica que si el juego empezó o no. Empieza cuando el mono se sube a la primera plataforma.

    #ayuda a cambiar la expresión del monito cuando este salta
    def jumping(self):
        self.jump= not self.jump

    def win(self):
        self.winner = True

    def start(self):
        self.started= True

    #dibuja el monito según su expresión
    def draw (self, pipeline, texture1, texture2, texture3):

        if self.jump: #cuando esta saltando
            self.monkey= es.toGPUShape(bs.createTextureQuad(texture2), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

        elif self.winner:
            self.monkey = es.toGPUShape(bs.createTextureQuad(texture3), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

        else: #cuando se encuentra en reposo
            self.monkey = es.toGPUShape(bs.createTextureQuad(texture1), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transmonkey)
            pipeline.drawShape(self.monkey)

    #mueve el monito hacia la izquierda
    def jump_left(self):
        if self.pos == 0:
            self.transmonkey = np.matmul(tr2.translate(-0.7, -0.74, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = -1
        elif self.pos == 1:
            self.transmonkey = np.matmul(tr2.translate(0, -0.74, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = 0
        self.level +=1

    #mueve el monito hacia la derecha
    def jump_right(self):
        if self.pos == 0:
            self.transmonkey = np.matmul(tr2.translate(0.7, -0.74, 0), tr2.scale(0.4, 0.4, 1))
            self.pos = 1
        elif self.pos == -1:
            self.transmonkey = np.matmul(tr2.translate(0, -0.74, 0), tr2.scale(0.4, 0.4, 1))
            self.pos= 0
        self.level +=1

    #mueve al monito hacia arriba cuando este salta
    def jump_up(self):
        self.level+=1

    #Define la logica del programa: Que pasa cuando el monito choca con las plataformas, que pasa cuando no lo hace.
    #                               Que pasa cuando el monito llega a la banana
    def gamelogic(self, plataforms: 'Plataforms', background: 'Background', banana: 'Banana', notice: 'Notice'):
        l= self.level
        quantlevels= len(plataforms.cont) #cantidad de niveles
        quantplataforms= len(plataforms.plataforms) #cantidad de plataformas

        indice = 0  # indicará el indice de la plataforma que nos interesa analizar
        for i in range(l - 1):
            indice += plataforms.cont[i]

        #Se indicarán los valores para la posición de la banana, según la ubicación de la última plataforma.
        if not banana.set:
            x= plataforms.plataforms[quantplataforms-1].pos_x
            blevel= quantlevels-2
            banana.setvalues(x,blevel)
            banana.move()
            banana.setted()

        if l==0: #si el monito esta en el nivel 1, no pasa nada aún
            if self.started:
                notice.lose()
            else:
                return

        elif l==quantlevels and self.pos == plataforms.plataforms[quantplataforms-1].pos_x:
            self.win()
            notice.win()

        elif plataforms.cont[l-1] ==1: #si el nivel en el que estamos tiene 1 plataforma solo basta analizar esa
            if self.pos!= plataforms.plataforms[indice].pos_x: #significa que no estan en la misma posción
                self.level-=1
                plataforms.updatecaida()
                background.updatedown()
                banana.updatedown()
            else:
                self.start()
        else: #como pueden haber hasta dos plataformas por nivel, este caso indica en el que hay dos plataformas
            if self.pos==plataforms.plataforms[indice].pos_x:
                self.start()
            else:
                if self.pos==plataforms.plataforms[indice+1].pos_x:
                    self.start()
                else:
                    self.level -= 1
                    plataforms.updatecaida()
                    background.updatedown()
                    banana.updatedown()


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

    #ayudará a ubicar las plataformas según la columna en la que esten
    def move_left(self):
        self.pos_x=-1

    #ayudará a ubicar la plataforma según la columna en la que este en el archivo csv
    def move_right(self):
        self.pos_x=1

    #ayuda a ubicar la plataforma según en la fila que este en el archivo csv
    def height(self,dy):
        self.pos_y= dy

    #baja la plataforma cuando el monito avance
    def moveup(self):
        self.pos_y -= 1

    #eleva la plataforma cuando el monito se caiga
    def movedown(self):
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
            dy= -1 #se utilizará para ubicar las plataformas a la altura correspondiente
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
    def updatesubida(self):
        for k in self.plataforms:
            k.moveup()

    #sube las plataformas cuando el monito cae
    def updatecaida(self):
        for k in self.plataforms:
            k.movedown()



class Background():

    def __init__(self, texture):
        self.background = es.toGPUShape(bs.createTextureQuad(texture), GL_REPEAT, GL_LINEAR)
        self.transbackground = np.matmul(tr2.translate(0, 0.2, 0), tr2.scale(2, 2.5, 1))
        self.level= 0 #indica en que nivel esta el monito, parte desde 0: suelo

    #dibuja el fondo
    def draw (self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transbackground)
        pipeline.drawShape(self.background)

    #mueve el fondo a medida que el monito avanza hacia arriba
    def move(self, c):
        self.transbackground = np.matmul(tr2.translate(0, 0.2 + c*-0.05, 0), tr2.scale(2, 2.5, 1))

    #actualiza el fondo a medida que el monito avanza
    def updateup(self):
        self.level += 1
        self.move(self.level)

    #actualiza el fondo si esque el monito retrocede
    def updatedown(self):
        self.level -= 1
        self.move(self.level)

class Banana():

    def __init__(self, texture):
        self.banana = es.toGPUShape(bs.createTextureQuad(texture), GL_REPEAT, GL_LINEAR)
        self.pos_x= 0 #será la posición lógica donde se ubicará la banana, se indicará con posterioridad
        self.level = 0 #indica en que nivel partira la banana, se indicará con posterioridad
        self.transbanana = np.matmul(tr2.translate(0.7*self.pos_x, 0.47*self.level, 0), tr2.scale(0.3, 0.3, 1))
        self.set = False

    #seteará los valores correctos para pos_x y level según como estan ubicadas las plataformas
    def setvalues(self, x, level):
        self.pos_x = x
        self.level = level

    def setted(self):
        self.set= True

    # dibuja la banana
    def draw(self, pipeline):
        if self.set:
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transbanana)
            pipeline.drawShape(self.banana)

    # mueve la banana a medida que el monito avanza hacia arriba

    def move(self):
        self.transbanana = np.matmul(tr2.translate(0.7* self.pos_x, 0.12 + 0.47*self.level, 0), tr2.scale(0.3, 0.3, 1))

    # actualiza el fondo a medida que el monito avanza
    def updateup(self):
        self.level -= 1
        self.move()

    # actualiza el fondo si esque el monito retrocede
    def updatedown(self):
        self.level += 1
        self.move()

class Notice(object):

    def __init__(self, texture):
        self.notice = es.toGPUShape(bs.createTextureQuad(texture), GL_REPEAT, GL_LINEAR)
        self.transnotice = np.matmul(tr2.translate(0, 0.4, 0), tr2.scale(-1, 1, 1))
        self.winner = False
        self.loser = False

    def draw (self, pipeline, texture1, texture2):

        if self.winner: #cuando esta saltando
            self.notice= es.toGPUShape(bs.createTextureQuad(texture1), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transnotice)
            pipeline.drawShape(self.notice)

        elif self.loser:
            self.notice = es.toGPUShape(bs.createTextureQuad(texture2), GL_REPEAT, GL_LINEAR)
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, self.transnotice)
            pipeline.drawShape(self.notice)

    def win(self):
        self.winner = True

    def lose(self):
        self.loser = True



