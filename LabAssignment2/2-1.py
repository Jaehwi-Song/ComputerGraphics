import glfw
from OpenGL.GL import *
import numpy as np

CURRENT_TYPE = 4
PRIMITIVE_TYPE = [GL_POLYGON, GL_POINTS, GL_LINES, GL_LINE_STRIP, 
                  GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP, 
                  GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP]

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw dodecagon
    dodecagon_idx = np.linspace(0, 11, 12)
    glBegin(PRIMITIVE_TYPE[CURRENT_TYPE])
    glColor3ub(255, 255, 255)
    for idx in dodecagon_idx:
        angle = idx*2*np.pi/len(dodecagon_idx)
        glVertex2fv([np.cos(angle), np.sin(angle)])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global CURRENT_TYPE
    if key==glfw.KEY_1:
        if action==glfw.PRESS: 
            CURRENT_TYPE=1
    elif key==glfw.KEY_2:
        if action==glfw.PRESS:
            CURRENT_TYPE=2
    elif key==glfw.KEY_3:
        if action==glfw.PRESS:
            CURRENT_TYPE=3
    elif key==glfw.KEY_4:
        if action==glfw.PRESS:
            CURRENT_TYPE=4
    elif key==glfw.KEY_5:
        if action==glfw.PRESS:
            CURRENT_TYPE=5
    elif key==glfw.KEY_6:
        if action==glfw.PRESS:
            CURRENT_TYPE=6
    elif key==glfw.KEY_7:
        if action==glfw.PRESS:
            CURRENT_TYPE=7
    elif key==glfw.KEY_8:
        if action==glfw.PRESS:
            CURRENT_TYPE=8
    elif key==glfw.KEY_9:
        if action==glfw.PRESS:
            CURRENT_TYPE=9
    elif key==glfw.KEY_0:
        if action==glfw.PRESS:
            CURRENT_TYPE=0

def main():
    # Initialize the library 
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2020081958-2-1", None, None) 
    if not window:
        glfw.terminate() 
        return
    
    # set the number of screen refresh to wait before calling glfw.swap_buffer()
    glfw.swap_interval(1)
    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)

    # Loop until the user closes the window
    while not glfw.window_should_close(window): 
        # Poll for and process events 
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL 
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()