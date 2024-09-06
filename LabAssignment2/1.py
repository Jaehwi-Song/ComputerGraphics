import glfw
from OpenGL.GL import *
import numpy as np
import math

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.5, -0.5, 0)
    glRotatef(-45,0,0,1)
    # draw triangle
    glBegin(GL_POLYGON)
    w = math.sqrt(2*(0.5*0.5))*0.5
    glVertex3f(-w, -w, 0)
    glVertex3f(-w,w,0)
    glVertex3f(w,w,0)
    glVertex3f(w,-w,0)
    glEnd()


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2020018958-2-2", None, None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's context current
    glfw.make_context_current(window)

    # set the number of screen refresh to wait before calling glfw.swap_buffer()
    glfw.swap_interval(1)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        t = glfw.get_time()

        # rotate 60 deg
        th = np.radians(60)
        R = np.array([[np.cos(th*t), -np.sin(th*t),0.],
                    [np.sin(th*t), np.cos(th*t),0.],
                    [0., 0., 1.]])
        
        # translate by (.5, .0)
        T = np.array([[1., 0., .5],
                      [0.,1.,.0],
                      [0.,0.,1.]])

        # Render here, e.g. using pyOpenGL
        render(R@T)

        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()