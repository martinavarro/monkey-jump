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


    def on_key(self, window, key, scancode, action, mods):
        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

            # Controlador modifica al modelo

        elif key == glfw.KEY_A and action == glfw.PRESS:
            print('Move left')
            self.model.jumping()
            self.model.move_left()

        elif key == glfw.KEY_D and action == glfw.PRESS:
            print('Move right')
            self.model.jumping()
            self.model.move_right()

        elif key == glfw.KEY_W and action == glfw.PRESS:
            self.model.jumping()
            print('pyong')

        elif (key == glfw.KEY_A or key == glfw.KEY_D or key == glfw.KEY_W) and action == glfw.RELEASE:
            self.model.jumping()

        else:
            print('Unknown key')

