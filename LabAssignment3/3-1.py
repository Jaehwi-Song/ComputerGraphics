import glfw
from OpenGL.GL import *
import numpy as np

T_MATRIX= np.identity(3)

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global T_MATRIX

    if action == glfw.PRESS:
        if key == glfw.KEY_Q:
            translation= np.array([[1.,0.,-.1],
                                   [0.,1.,0.],   
                                   [0.,0.,1.]])
            T_MATRIX = translation @ T_MATRIX

        elif key == glfw.KEY_E:
            translation=np.array([[1.,0.,.1],
                                   [0.,1.,0.],   
                                   [0.,0.,1.]])
            T_MATRIX= translation @ T_MATRIX

        elif key == glfw.KEY_A:
            th=np.radians(10)
            rotation=np.array([[np.cos(th),-np.sin(th),0.],
                                [np.sin(th),np.cos(th),0.],
                                [0.,0.,1.]])
            T_MATRIX = T_MATRIX @ rotation

        elif key == glfw.KEY_D:
            th=np.radians(-10)
            rotation=np.array([[np.cos(th),-np.sin(th),0.],
                                [np.sin(th),np.cos(th),0.],
                                [0.,0.,1.]])
            T_MATRIX = T_MATRIX @ rotation

        elif key == glfw.KEY_1:
            T_MATRIX = np.identity(3)
def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(480, 480, "2020081958-3-1", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(T_MATRIX)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
