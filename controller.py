"""
Contralor de la aplicación.
"""

import glfw
import sys


class Controller(object):

    def __init__(self):
        self.model = None
        self.fill_polygon = True

    def set_model(self, m):
        self.model = m

    def set_plataforms(self, p):
        self.plataforms = p

    def set_background(self, b):
        self.background = b


    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

            # Controlador modifica al modelo

        elif key == glfw.KEY_A and action == glfw.PRESS:
            self.model.jumping()
            self.model.jump_left()
            self.plataforms.updatesubida()
            self.background.updateup()


        elif key == glfw.KEY_D and action == glfw.PRESS:
            self.model.jumping()
            self.model.jump_right()
            self.plataforms.updatesubida()
            self.background.updateup()

        elif key == glfw.KEY_W and action == glfw.PRESS:
            self.model.jumping()
            self.model.jump_up()
            self.plataforms.updatesubida()
            self.background.updateup()

            #self.model.activate()

        elif (key == glfw.KEY_A or key == glfw.KEY_D or key == glfw.KEY_W) and action == glfw.RELEASE:
            self.model.jumping()
            #self.model.activate()

        else:
            print('Unknown key')

