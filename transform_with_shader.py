from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from ctypes import *
import sys
import math

ESCAPE = '\033'

window = 0

Triangle = []
Shader = None
u = 0.0

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
    global u
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    xx=0.0
    yy=0.0
    zz=0.0
    xx = 5+math.cos(u - 0.785)
    yy = 5+math.cos(2.0*u - 0.785)
    u=u+0.1
    zz = -3.0

    light_position = [xx, yy, zz, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glTranslatef(0.0, 0.0, -6.0)

    glUseProgram(Shader)

#    glutSolidTeapot(1.0, 32, 32);
    glBegin(GL_POLYGON)
    for row in Triangle:
        glVertex3f(row[0], row[1], row[2])
    
#    glVertex3f(0.0, 1.0, 0.0);
#    glVertex3f(1.0, -1.0, 0.0);
#     glVertex3f(-1.0, -1.0, 0.0);
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
    global Shader

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    Shader = compileProgram(
        compileShader('''
        // Vetex program
varying vec3 L;
varying vec3 N;
varying vec3 P;
 
void main(void) 
{
  P = vec3(gl_ModelViewMatrix * gl_Vertex); 
  L = normalize(gl_LightSource[0].position.xyz-P); 
  N = normalize(gl_NormalMatrix * gl_Normal); 
 
  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex; 
}
        ''', GL_VERTEX_SHADER),
        compileShader('''
        // Fragment program
varying vec3 L; 
varying vec3 N; 
varying vec3 P; 
 
void main (void) 
{  
  vec3 E = normalize(-P); 
  vec3 R = normalize(-reflect(L,N)); 
 
  vec4 Iamb = gl_FrontLightProduct[0].ambient;
  vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(N,L), 0.0); 
  vec4 Ispec = gl_FrontLightProduct[0].specular * pow(max(dot(R,E),0.0),0.3 * gl_FrontMaterial.shininess); 
 
  gl_FragColor =  gl_FrontLightModelProduct.sceneColor + Iamb + Idiff + Ispec; 
} 
        ''', GL_FRAGMENT_SHADER),
        )

    Triangle = load_rawfile("monkey.raw")

def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    
    window = glutCreateWindow("Shiny Eng-Math")
    
    light_ambient = [1.0, 0.0, 0.0, 1.0]
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_specular = [1.0, 1.0, 1.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()

main()
