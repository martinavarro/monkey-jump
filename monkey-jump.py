from controller import *
from modelo import *

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Jumping Monkey", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    controller = Controller()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # A simple shader program with position and texture coordinates as inputs.
    texturepipeline = es.SimpleTextureTransformShaderProgram()
    colorpipeline = es.SimpleTransformShaderProgram()


    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory
    monkey = Monkey("img/mk1.png")
    background = Background("img/jungle.png")
    plataforms = Plataforms()
    banana = Banana("img/banana2.png")
    notice = Notice ("img/win.png")

    #setting the objects to the controller
    controller.set_model(monkey)
    controller.set_plataforms(plataforms)
    controller.set_background(background)
    controller.set_banana(banana)
    controller.set_notice(notice)

    # Creating the plataforms from the csv archive
    plataforms.create_plataforms()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fill_polygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        monkey.gamelogic(plataforms, background, banana, notice)

        # Drawing the shapes
        background.draw(texturepipeline)
        monkey.draw(texturepipeline, "img/mk1.png", "img/mk2.png", "img/mk4.png")
        plataforms.draw(colorpipeline)
        banana.draw(texturepipeline)
        notice.draw(texturepipeline, "img/win.png", "img/go.png")


        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
