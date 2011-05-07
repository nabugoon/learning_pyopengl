from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

ESCAPE = '\033'

window = 0

Triangle = []

def load_rawfile(filename):
    points = []

    lines = open(filename).readlines()
    for line in lines:
        coord = line.strip().split(" ")
        coord = map(float, coord)
        points.append(coord[:3])
        points.append(coord[3:6])
        points.append(coord[6:])
        
    return points

def DrawGLScene():
    global Triangle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -6.0)

    glBegin(GL_POLYGON)
    for row in Triangle:
        glVertex3f(row[0], row[1], row[2])
    glEnd()
    
    glutSwapBuffers()

def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def matrixMultiply(matrix, target):
    results = []
    for row in matrix:
        result = 0.0
        for i, item in enumerate(row):
            result += item * target[i]
        results.append(result)

    return results

def translate(X, Y, Z):
    global Triangle

    translateMatrix = [
        [1.0, 0.0, 0.0, X],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, Z],
        [0.0, 0.0, 0.0, 1.0]
        ]

    results = []
    for row in Triangle:
        row.append(1)
        result = matrixMultiply(translateMatrix, row)
        results.append(result[:3])

    Triangle = results

def keyPressed(*args):
    if args[0] == 'w':
        translate(0.0, 0.0, -1)
    if args[0] == 's':
        translate(0.0, 0.0, 1)
    if args[0] == 'd':
        translate(0.1,0.0,0.0)
    if args[0] == 'a':
        translate(-0.1,0.0,0.0)
    if args[0] == ESCAPE:
        sys.exit()

def InitGL(Width, Height):
    global Triangle
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    Triangle = load_rawfile("cube.raw")

def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    
    window = glutCreateWindow("Shiny Eng-Math")
    
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

main()
