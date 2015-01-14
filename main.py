#========================================================
# main.py
# 
# authors:  Johnathan Gould
# 
# date:     9 May 2012
# 
# description:
# This is our F29GR group project. It creates a bird of
# different colours using 3 initials of each group
# member.
#
# Initials used:  A, B, C, D, G, J, K, L, M
#========================================================

if __name__ == '__build__':
  raise Exception

# Import default libraries
import sys
from math import *

# Import PyOpenGL libraries
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print 'ERROR: PyOpenGL is not installed properly.'


#========================================================
# Global variables
#========================================================

# Animal default options
animal = {
  'wing_dir': 'up',\
  'wing_deg': -10.0,\
  'head_deg': 0.5,\
  'velocity': 3.0
}

# View control options
options = {}

options['G_walk'] = [0, 0, 0]
options['G_theta'] = [0, 0, 0]
options['G_zoom'] = 0.3
options['rotating'] = False

# Mouse and environment options
options['MousePressed'] = False
options['pitch0'] = 0
options['yaw0'] = 0
options['mouseX0'] = 0
options['mouseY0'] = 0


# Array of cube vertices
vertices = [
  [-0.5,-0.5,-0.5],\
  [0.5,-0.5,-0.5],\
  [0.5,0.5,-0.5],\
  [-0.5,0.5,-0.5],\
  [-0.5,-0.5,0.5],\
  [0.5,-0.5,0.5],\
  [0.5,0.5,0.5],\
  [-0.5,0.5,0.5]
];

# Define arrays of available colours
colors = [ [0.2,0.2,0.2], [0.5,0.5,0.5], [0.75,0.75,0.75], [0.5,0.5,0.5], [0.75,0.75,0.75], [0.3,0.3,0.3], [0.5,0.5,0.5], [0.9,0.9,0.9] ]
red = [ [0.8,0.2,0.2], [0.8,0.5,0.5], [0.9,0.5,0.5], [0.8,0.4,0.4], [0.9,0.5,0.5], [0.8,0.2,0.2], [0.8,0.3,0.3], [1.0,0.7,0.7] ]
blue = [ [0.2,0.8,0.8], [0.5,0.8,0.8], [0.5,0.9,0.9], [0.4,0.8,0.8], [0.5,0.9,0.9], [0.2,0.8,0.8], [0.3,0.8,0.8], [0.7,1.0,1.0] ]
yellow = [ [0.9,0.9,0.2], [0.9,0.9,0.5], [0.9,0.9,0.5], [0.9,0.9,0.4], [0.9,0.9,0.5], [0.9,0.9,0.2], [0.9,0.9,0.3], [1.0,1.0,0.7] ]


#========================================================
# REQUIRED FUNCTIONS
#========================================================

# Draws a polygon, using vertices array
def polygon(a, b, c, d, col = 'white'):
  # Draw a polygon using colour
  global vertices, colors, red, blue, yellow
  
  glBegin(GL_POLYGON)
  
  # Set the correct colour
  if col == 'red':
    glColor3fv(red[a])
  elif col == 'blue':
    glColor3fv(blue[a])
  elif col == 'yellow':
    glColor3fv(yellow[a])
  else:
    glColor3fv(colors[a])

  glVertex3fv(vertices[a])
  glVertex3fv(vertices[b])
  glVertex3fv(vertices[c])
  glVertex3fv(vertices[d])
  glEnd()


# Draw unit cube centred on the origin
def cube(col = 'white'):
  polygon(0,3,2,1, col)    # Back
  polygon(2,3,7,6, col)    # Top
  polygon(4,7,3,0, col)    # Left
  polygon(1,2,6,5, col)    # Right
  polygon(7,4,5,6, col)    # Front
  polygon(5,4,0,1, col)    # Bottom


# Draw a 3D Curve
def Draw3DCurve(depth, r1, r2, theta_start, theta_stop, theta_inc, col = 'white'):
  global colors, red, blue, yellow

  # depth = z depth centred on axis
  # r1 = inner curve radius
  # r2 = outer curve radius
  # theta_start = Starting degree of curve
  # theta_stop = Ending degree of curve

  i=0
  radius=1.0
  c=3.14159/180.0
  z_front=depth/2
  z_back=-depth/2

  # Set the correct colour
  if col == 'red':
    colors = red
  elif col == 'blue':
    colors = blue
  elif col == 'yellow':
    colors = yellow

  # draw rear face (away from viewer)
  glColor3fv(colors[0])
  z=z_back
  glBegin(GL_QUAD_STRIP)
  for thet in xrange(int(theta_start), int(theta_stop)):
    x=cos(c*thet)*r2; y=sin(c*thet)*r2; glVertex3d(x,y,z)
    x=cos(c*thet)*r1; y=sin(c*thet)*r1; glVertex3d(x,y,z)
  glEnd()

  # draw front face (closer to viewer)
  glColor3fv(colors[7])
  z=z_front
  glBegin(GL_QUAD_STRIP)
  for thet in xrange(int(theta_start), int(theta_stop)):
    x=cos(c*thet)*r1; y=sin(c*thet)*r1; glVertex3d(x,y,z)
    x=cos(c*thet)*r2; y=sin(c*thet)*r2; glVertex3d(x,y,z)
  glEnd()

  # draw upper face
  glColor3fv(colors[2])
  glBegin(GL_QUAD_STRIP)
  for thet in xrange(int(theta_start), int(theta_stop)):
    x=cos(c*thet)*r2; y=sin(c*thet)*r2
    z=z_front; glVertex3d(x,y,z)
    z=z_back;  glVertex3d(x,y,z)
  glEnd()

  # draw lower face
  glColor3fv(colors[1])
  glBegin(GL_QUAD_STRIP)
  for thet in xrange(int(theta_start), int(theta_stop)):
    x=cos(c*thet)*r1; y=sin(c*thet)*r1
    z=z_back; glVertex3d(x,y,z)
    z=z_front; glVertex3d(x,y,z)
  glEnd()

  # draw bottom end
  glColor3fv(colors[2])
  glBegin(GL_POLYGON)
  glVertex3d(r1,0.0,z_front)
  glVertex3d(r1,0.0,z_back)
  glVertex3d(r2,0.0,z_back)
  glVertex3d(r2,0.0,z_front)
  glEnd()

  # draw top end
  glColor3fv(colors[2])
  glBegin(GL_POLYGON);
  x1=cos(c*theta_stop)*r1; y1=sin(c*theta_stop)*r1;
  x2=cos(c*theta_stop)*r2; y2=sin(c*theta_stop)*r2;
  glVertex3d(x1,y1,z_front)
  glVertex3d(x2,y2,z_front)
  glVertex3d(x2,y2,z_back)
  glVertex3d(x1,y1,z_back)
  glEnd()


# Draw a 3D quad
def Draw3DTriangle(w, h, d, col = 'white'):
  global colors, red, blue, yellow

  # Set the correct colour
  if col == 'red':
    colors = red
  elif col == 'blue':
    colors = blue
  elif col == 'yellow':
    colors = yellow


  #draws a cube from the center.
  glBegin(GL_QUADS)
  
  #front face (cream color)   
  glColor3fv(colors[7])
  glVertex3f(w/2, h/2, d/2)
  glVertex3f(-w/2, h/2, d/2)
  glVertex3f(-w/2, -h/2, d/2)
  glVertex3f(w/2, -h/2, d/2)

  #left face(pink)
  glColor3fv(colors[4])
  glVertex3f(-w/2, h/2, d/2)
  glVertex3f(-w/2, h/2, -d/2)
  glVertex3f(-w/2, -h/2, -d/2)
  glVertex3f(-w/2, -h/2, d/2)

  #back face (grey  color)
  glColor3fv(colors[0])
  glVertex3f(w/2, h/2, -d/2)
  glVertex3f(-w/2, h/2, -d/2)
  glVertex3f(-w/2, -h/2, -d/2)
  glVertex3f(w/2, -h/2, -d/2)

  #right face
  glColor3fv(colors[1])
  glVertex3f(w/2, h/2, -d/2)
  glVertex3f(w/2, h/2, d/2)
  glVertex3f(w/2, -h/2, d/2)
  glVertex3f(w/2, -h/2, -d/2)

  #top face
  glColor3fv(colors[2])
  glVertex3f(w/2, h/2, d/2)
  glVertex3f(-w/2, h/2, d/2)
  glVertex3f(-w/2, h/2, -d/2)
  glVertex3f(w/2, h/2, -d/2)

  #bottom face
  glColor3fv(colors[5])
  glVertex3f(w/2, -h/2, d/2)
  glVertex3f(-w/2, -h/2, d/2)
  glVertex3f(-w/2, -h/2, -d/2)
  glVertex3f(w/2, -h/2, -d/2)

  glEnd()

# DRAW AXES and GRIDLINES
def DrawAxesAndGridLines(x_y_display, x_z_display, y_z_display):
  
  glBegin(GL_LINES)
  
  # X Line
  glColor3f(1, 0, 0)
  glVertex3f(-50, 0, 0)
  glVertex3f(+50, 0, 0)          
  
  # Y Line
  glColor3f(0, 1, 0)
  glVertex3f( 0 ,-50, 0)             
  glVertex3f( 0, +50, 0)

  # Z Line
  glColor3f(0, 0, 1)
  glVertex3f( 0, 0,-50)              
  glVertex3f( 0, 0, +50)
  glEnd()
  
  glLineStipple(1, 0xAAAA) #line style = fine dots
  glEnable(GL_LINE_STIPPLE)

  glBegin(GL_LINES)

  if x_y_display:
    glColor3f(0.0,0.7,0.7)
    for offset in range(-10, 10):
      #draw lines in x-y plane
      glVertex3f(-10.0, offset, 0.0)          # Top Left
      glVertex3f(+10.0, offset, 0.0)          # Top Right
      glVertex3f( offset,-10, 0.0)            # Bottom Right
      glVertex3f( offset,+10.0, 0.0)          # Bottom Left

  if y_z_display:
    glColor3f(0.7,0.0,0.7)
    for offset in range (-10, 10):
      #draw lines in y-z plane
      glVertex3f( 0, offset, -10)      
      glVertex3f( 0, offset, 10.0)
      glVertex3f( 0, -10, offset)
      glVertex3f( 0, 10, offset)

  if x_z_display:
    glColor3f(0.7,0.7,0.0)
    for offset in range(-10, 10):
      #draw lines in x-z plane
      glVertex3f( offset, 0, -10)
      glVertex3f( offset, 0, 10.0)
      glVertex3f( -10, 0, offset)
      glVertex3f( 10, 0, offset)

  glEnd()

  glDisable(GL_LINE_STIPPLE)


#========================================================
# CODE
#========================================================

# The display callback
def DisplayCallback():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glLoadIdentity()

  # Draw the scene
  viewControl()
  DrawScene()

  #glFlush()
  glutSwapBuffers()

def viewControl():
  global options

  # Reset matrix
  glLoadIdentity()
  glTranslatef(options['G_walk'][0], options['G_walk'][1], options['G_walk'][2])
  
  # Rotate everything 
  glRotatef(options['G_theta'][0], 1.0, 0.0, 0.0)
  glRotatef(options['G_theta'][1], 0.0, 1.0, 0.0)
  glRotatef(options['G_theta'][2], 0.0, 0.0, 1.0)
  
  # zoom (NB glOrtho projection)
  glScalef(options['G_zoom'], options['G_zoom'], options['G_zoom'])

def DrawScene():
  global animal

  # Draw the Axes and/or gridlines
  DrawAxesAndGridLines(False, False, False)
  
  glPushMatrix()
  
  glRotatef(-35, 0, 1, 0)
  glScalef(0.6, 0.6, 0.6)

  # Draw the animal
  DrawAnimal(animal['wing_deg'], animal['head_deg'])
  
  glPopMatrix()

# BEGIN: Draw the animal (bird)

def DrawAnimal(wing_deg, head_deg):
  # Draws the body
  DrawAnimalBody('red')
  
  # Draws the head
  glPushMatrix()
  glTranslatef(2.5, 2.5, 0)
  glRotatef(head_deg, 0, 0, 1)
  DrawAnimalHead('red')
  glPopMatrix()

  # Draws the wings
  glPushMatrix()
  glTranslatef(-0.1, 1.8, 2.05)
  glRotatef((-90 - wing_deg), 1, 0, 0)
  DrawAnimalWing('blue')
  glPopMatrix()

  glPushMatrix()
  glTranslatef(-0.1, 1.8, -2.05)
  glRotatef((-90 + wing_deg), 1, 0, 0)
  glScalef(1,-1,1)
  DrawAnimalWing('blue')
  glPopMatrix()

  # Draws the tail
  glPushMatrix()
  glTranslatef(-2.5, 2, 0)
  glRotatef(90, 0, 1, 0)
  glScalef(0.7, 0.7, 0.7)
  DrawAnimalTail(head_deg, 'red')
  glPopMatrix()

  # Draws the legs
  glPushMatrix()
  glTranslatef(-2, -0.3, -1)
  DrawAnimalLeg(head_deg, 'yellow')
  glPopMatrix()

  glPushMatrix()
  glTranslatef(-2, -0.3, 1)
  glScalef(1, 1, -1)
  DrawAnimalLeg(head_deg, 'yellow')
  glPopMatrix()

# Draw a body
def DrawAnimalBody(col = 'white'):
  # Specifically make ridge down the back blue if head is anything other than white
  if col == 'white':
    col2 = 'white';
  else:
    col2 = 'yellow';

  glPushMatrix()
  glTranslatef(0, 1.9, 0)
  glRotatef(90, 0, 1, 0)
  glRotatef(-90, 0, 0, 1)
  glScalef(1, 0.8, 5)
  DrawD(col)
  glPopMatrix()

  # Draw down the back
  glPushMatrix()
  glTranslatef(-2.2, 2.45, 0)
  glRotatef(-90, 0, 0, 1)
  glScalef(0.2, 0.1, 0.2)
  DrawC(col2)

  for place in xrange(1, 9):
    glTranslatef(0, 5, 0)
    DrawC(col2)

  glPopMatrix()

# Draw a head with beak
def DrawAnimalHead(col = 'white'):
  # Specifically make beak yellow if head is anything other than white
  if col == 'white':
    col2 = 'white';
  else:
    col2 = 'yellow';

  glPushMatrix()
  
  glRotatef(90, 0, 1, 0)
  glScalef(0.5, 0.5, 0.5)
  glRotatef(-30, 1, 0, 0)
  glTranslatef(0,0, 0.4)

  glPushMatrix()

  DrawM(col)

  glTranslatef(0, -3.5, 0)
  glRotatef(180, 0, 0, 1)
  DrawA(col2)

  glPopMatrix()

  glPopMatrix()

# Draw a wing
def DrawAnimalWing(col = 'white'):
  glPushMatrix()
  glTranslatef(0, -4, 0)

  glPushMatrix()
  glTranslatef(2, 0, 0)
  glRotatef(180, 0, 0, 1)
  glScalef(1.2, 1.2, 1.3)
  DrawB(col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(-1, 1, 0)
  glRotatef(10, 0, 0, 1)
  glScalef(0.9, 0.8, 1)
  DrawG(col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(-0.6, 3.8, 0)
  glRotatef(-90, 0, 0, 1)
  glScalef(0.5, 0.5, 1)
  DrawK(col)
  glPopMatrix()

  glPopMatrix()

# Draw a tail with feathers
def DrawAnimalTail(deg = 0, col = 'white'):
  glPushMatrix()
  glRotatef(deg, 1, 0, 0)

  glPushMatrix()
  glRotatef(30, 0, 0, 1)
  DrawAnimalTailFeather(col)

  glRotatef(-30, 0, 0, 1)
  DrawAnimalTailFeather(col)

  glScalef(-1,1,1)
  DrawAnimalTailFeather(col)

  glRotatef(30, 0, 0, 1)
  DrawAnimalTailFeather(col)
  glPopMatrix()

  glPopMatrix()

# Draw a single tail feather
def DrawAnimalTailFeather(col = 'white'):
  glPushMatrix()
  glRotatef(-40, 1, 0, 0)
  glTranslatef(-1, 2, 0)
  glRotatef(-150, 0, 0, 1)
  DrawJ(col)
  glPopMatrix()

# Draw a leg with feet and claws
def DrawAnimalLeg(deg = 0, col = 'white'):
  glPushMatrix()
  glRotatef(10+(deg/3), 1, 1, 0)
  glRotatef(deg, 0, 0, 1)
  glScalef(0.5, 0.5, 0.5)
  
  glPushMatrix()
  glTranslatef(1.6, -2.5, 0)
  glRotatef(-120, 0, 0, 1)
  glScalef(-1,1,1)
  DrawL(col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(4.3, -4.4, 0)
  DrawAnimalLegFoot(col)
  glPopMatrix()

  glPopMatrix()

# Draw a foot with claws
def DrawAnimalLegFoot(col = 'white'):
  glPushMatrix()
  glRotatef(-50, 0, 0, 1)
  glRotatef(-10, 0, 1, 0)
  glRotatef(-90, 0, 1, 0)
  glScalef(0.5, 0.5, 0.5)

  glPushMatrix()
  glRotatef(30, 0, 1, 1)
  DrawAnimalLegClaw(col)

  glRotatef(-30, 0, 0, 1)
  DrawAnimalLegClaw(col)

  glScalef(-1,1,1)
  DrawAnimalLegClaw(col)

  glRotatef(30, 0, 0, 1)
  DrawAnimalLegClaw(col)
  glPopMatrix()

  glPopMatrix()

# Draw a claw on a foot
def DrawAnimalLegClaw(col = 'white'):
  glPushMatrix()
  glRotatef(90, 0, 1, 0)

  glPushMatrix()
  glTranslatef(-1, 2, 0)
  glRotatef(-150, 0, 0, 1)
  DrawJ(col)
  glPopMatrix()

  glPopMatrix()

# END: Animal


# BEGIN: Jono Gould's code

# Draw all 3 initials
def DrawJAG():
  glPushMatrix()

  glTranslatef(-5.0, 0.0, 0.0)
  glColor3f(1.0,0.0,1.0)
  DrawJ()
  
  glTranslatef(5.0, 0.0, 0.0)
  DrawA()

  glTranslatef(7.0, 0.0, 0.0)
  DrawG()

  glPopMatrix()

# Draw the initial J
def DrawJ(col = 'white'):
  glPushMatrix()

  # TOP OF J
  glTranslatef(0.0, 3.0, 0.0)
  DrawJTop(col)

  # MIDDLE OF J
  glTranslatef(0.0, -3.0, 0.0)
  DrawJMiddle(col)

  # BOTTOM OF J
  glTranslatef(-1.0, -2.5, 0.0)
  DrawJBottom(col)

  glPopMatrix()

def DrawJTop(col = 'white'):
  glPushMatrix()

  glScalef(4.0, 1.0, 1.0)
  cube(col)

  glPopMatrix()

def DrawJMiddle(col = 'white'):
  glPushMatrix()

  glScalef(1.0, 5.0, 1.0)
  cube(col)

  glPopMatrix()

def DrawJBottom(col = 'white'):
  glPushMatrix()

  glRotatef(180, 0, 0, 1)
  Draw3DCurve(1.0, 1.5, 0.5, 0.0, 181.0, 1.0, col)

  glPopMatrix()

# Draw the initial A
def DrawA(col = 'white'):
  glPushMatrix()

  DrawALeft(col)
  DrawARight(col)
  DrawAMiddle(col)

  glPopMatrix()

def DrawALeft(col = 'white'):
  glPushMatrix()

  glTranslatef(-1.2, 0.0, 0.0)
  glRotatef(-18.0, 0, 0, 1)
  glScalef(1.0, 8.0, 1.0)
  cube(col)

  glPopMatrix()

def DrawARight(col = 'white'):
  glPushMatrix()

  glTranslatef(1.2, 0.0, 0.0)
  glRotatef(18.0, 0, 0, 1)
  glScalef(1.0, 8.0, 1.0)
  cube(col)

  glPopMatrix()

def DrawAMiddle(col = 'white'):
  glPushMatrix()

  glTranslatef(0.0, -1.5, 0.0)
  glScalef(3.0, 1.0, 1.0)
  cube(col)

  glPopMatrix()

# Draw the initial G
def DrawG(col = 'white'):
  glPushMatrix()

  DrawGCurve(col)

  glTranslatef(0.5, -2.5, 0.0)
  DrawGVertical(col)

  glTranslatef(-0.5, 2.0, 0.0)
  DrawGHorizontal(col)

  glPopMatrix()

def DrawGCurve(col = 'white'):
  glPushMatrix()

  glRotatef(90.0, 0, 0, 1)
  Draw3DCurve(1.0, 4.0, 3.0, 0.0, 181.0, 1.0, col)

  glPopMatrix()

def DrawGVertical(col = 'white'):
  glPushMatrix()

  glScalef(1.0, 3.0, 1.0)
  cube(col)

  glPopMatrix()

def DrawGHorizontal(col = 'white'):
  glPushMatrix()

  glScalef(2.0, 1.0, 1.0)
  cube(col)

  glPopMatrix()

# END: Jono Gould's code


# BEGIN: Kesireleditsoe Sepeng's code

# Draw the initial L
def DrawL(col = 'white'):
  glPushMatrix();  
  glTranslatef(-0.6, 0.5, 0.0);
  glScalef(5.0, 6.0, 1.0)
  Draw3DTriangle(0.2, 1.0, 1.0, col);
  glPopMatrix();

  glPushMatrix();
  glTranslatef(0.4, -2.5, 0.0);
  glScalef(5.0, 4.0, 1.0)
  Draw3DTriangle(0.6, 0.2, 1.0, col);
  glPopMatrix();

# Draw the initial K
def DrawK(col = 'white'):
  # First K horizontal
  glPushMatrix()
  glTranslatef(-0.1, 0, 0)
  glScalef(6.0,7.0,1.0)
  Draw3DTriangle(0.2,1.0, 1.0, col)
  glRotatef(105,0.0,0.0,1.0)
  glPopMatrix()


  # lower K acute DOWN
  glPushMatrix()
  glRotatef(33,-1.0,-1.0,2.0)
  glTranslatef(2.0,0.2, 0.0)
  glScalef(6.0,7.0,1.0)
  Draw3DTriangle(0.6, 0.2, 1.0, col)
  glPopMatrix()

  # top K acute UP
  glPushMatrix()
  glRotatef(33,-1.0,-1.2,2.0)
  glTranslatef(1.2,-2.2, 0.0)
  glScalef(6.0,5.0,1.0)
  Draw3DTriangle(0.2, -0.8, 1.0, col)
  glPopMatrix()

# Draw the initial M
def DrawM(col = 'white'):
  glPushMatrix()

  glTranslatef(-3.5, 0, 0)
  glRotatef(90, 0, 0, 1)
  glScalef(7.0, 7.0, 1.0)
  
  glPushMatrix()
  glTranslatef(0.2,-0.7, 0.0)
  Draw3DCurve(1.0, 0.1,0.3, -105,105, 1.0, col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(0.2, -0.3, 0.0)
  Draw3DCurve(1.0, 0.1,0.3, -105,105, 1.0, col)
  glPopMatrix()
  
  # top m square top
  glPushMatrix()
  glTranslatef(0.2,-0.1, 0.0)
  Draw3DTriangle(0.4, 0.2, 1.0, col)
  glPopMatrix()

  # middle m square
  glPushMatrix()
  glTranslatef(0.2, -0.5, 0.0)
  Draw3DTriangle(0.4, 0.2, 1.0, col)
  glPopMatrix()

  # bottom m square
  glPushMatrix()
  glTranslatef(0.2, -0.9, 0.0)
  Draw3DTriangle(0.4, 0.2, 1.0, col)
  glPopMatrix()
  
  # top m square
  glPushMatrix()
  glTranslatef(-0.1,-0.1, 0.0)
  Draw3DTriangle(0.4, 0.2, 1.0, col)
  glPopMatrix()
  
  # middle m square
  glPushMatrix()
  glTranslatef(0.1, -0.5, 0.0)
  Draw3DTriangle(0.4, 0.2, 1.0, col)
  glPopMatrix()

  # bottom m square
  glPushMatrix()
  glTranslatef(-0.1, -0.9, 0.0)
  Draw3DTriangle(0.4, 0.2, 1.0, col)
  glPopMatrix()

  glPopMatrix()

# END: Kesireleditsoe Sepeng's code


# BEGIN: Brandon Williams' code

# Draw the initial B
def DrawB(col = 'white'):
  glPushMatrix()
  glTranslatef(0.1, 0, 0.0)
  glScalef(6.0,7.0,1.0)
  Draw3DTriangle(0.2, 1.0, 1.0, col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(0.6, 1.4, 0.0)
  glScalef(6.0,7.0,1.0)
  Draw3DCurve(1.0, 0.1,0.3, -90,91, 1.0, col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(0.6, -1.4, 0.0)
  glScalef(6.0,7.0,1.0)
  Draw3DCurve(1.0, 0.1,0.3, -90,91, 1.0, col)
  glPopMatrix()

# Draw the initial C
def DrawC(col = 'white'):
  glPushMatrix()
  glRotatef(-90, 0.0, 0.0, 2.0)
  #glTranslatef(1.3, -0.95, 0.0)
  glScalef(9.0, 9.0, 1.0)
  glRotatef(-90, 0, 0, 1)
  Draw3DCurve(1.0, 0.1,0.3, -90, 90, 1.0, col)
  glPopMatrix()

# Draw the initial D
def DrawD(col = 'white'):
  glPushMatrix()
  glTranslatef(-0.1, 0, 0.0)
  glScalef(5.0,9.0,1.0)
  Draw3DTriangle(0.2, 0.6, 1.0, col)
  glPopMatrix()

  glPushMatrix()
  glTranslatef(0.4, 0, 0.0)
  glScalef(7.0,9.0,1.0)
  Draw3DCurve(1.0, 0.1,0.3, -90,91, 1.0, col)
  glPopMatrix()

# END: Brandon Williams' code


#========================================================
# DEFAULT GLUT FUNCTIONS
#========================================================

# Init the program
def Init(): 
  global vertices, colors

  # Clear the environment to black
  glClearColor (0.0, 0.0, 0.0, 0.0)
  glShadeModel (GL_SMOOTH)
  
  # Set the default polygon mode to fill
  glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
  glEnableClientState(GL_COLOR_ARRAY)
  glEnableClientState(GL_VERTEX_ARRAY)
  glVertexPointer(3, GL_FLOAT, 0, vertices)
  glColorPointer(3,GL_FLOAT, 0, colors)
  
  glClearDepth(1.0)
  glDepthFunc(GL_LESS)
  glEnable(GL_DEPTH_TEST)

  # Show the menu
  DisplayMenuOptions()


# Show the welcome screen with options
def DisplayMenuOptions():
  print '\n================================'
  print 'WELCOME'
  print '================================\n'
  print 'Please select an option below:'
  print 'a - Toggle animation of the bird'
  print 'l - View the bird as a wireframe model'
  print 'f - Show the bird filled-in\n'

  print 'Control speed of animation:'
  print '1 - Slow-motion'
  print '2 - Normal speed (default)'
  print '3 - Double speed'
  print '4 - 4X speed\n'

  print 'Control the environment:'
  print '+ - Zoom in on bird'
  print '- - Zoom out of bird'
  print 'ARROW KEYS - Move camera location'
  print 'CLICK AND DRAG MOUSE - Move camera direction\n'

  print 'r - Reset back to program defaults'
  print 'ESC - Quit program\n'

  print 'ENJOY OUR PROJECT!\n'
  print '================================'


# IdleCallback is called when the GLUT Idle function becomes active (on animation start)
def IdleCallback():
  global options, animal

  # Make the view swing around the animal
  options['G_theta'][1] -= 1

  # Animal stuff
  if animal['wing_deg'] <= -40:
    animal['wing_dir'] = 'up'
  elif animal['wing_deg'] >= 20:
    animal['wing_dir'] = 'dwn'

  if animal['wing_dir'] == 'up':
    animal['wing_deg'] += animal['velocity']
    animal['head_deg'] -= (animal['velocity'] / 3)
  else:
    animal['wing_deg'] -= animal['velocity']
    animal['head_deg'] += (animal['velocity'] / 3)

  glutPostRedisplay()


# Called by GLUTReshapeFunc
def ReshapeCallback(w, h):
  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)
  
  glLoadIdentity()

  if w == h:
    return

  if w <= h:
    glOrtho(-2.0, 2.0, -2.0 * float(h) / float(w), 2.0 * float(h) / float(w), -10.0, 10.0)
  else:
    glOrtho(-2.0 * float(w) / float(h), 2.0 * float(w) / float(h), -2.0, 2.0, -10.0, 10.0)
  
  glMatrixMode(GL_MODELVIEW)

# Handle the mouse events
def MouseCallback(btn, state, x, y):
  global options

  # Check that the mouse button is pressed down
  if state == GLUT_DOWN:
    options['MousePressed'] = True
    options['pitch0'] = options['G_theta'][0]
    options['yaw0'] = options['G_theta'][1]
    options['mouseX0'] = x
    options['mouseY0'] = y

  if state == GLUT_UP:
    MousePressed = False

# Handle any mouse motion
def MouseMotionCallback(x, y):
  global options

  # Change the view when the mouse is moved
  options['G_theta'][0] = options['pitch0'] + (y - options['mouseY0'])
  options['G_theta'][1] = options['yaw0'] + (x - options['mouseX0'])
  
  glutPostRedisplay()

# Handle keyboard events
def KeyboardCallback(key, x, y):
  global options

  if key == chr(27):
    sys.exit(0)
  elif key == '-':
    options['G_zoom'] /= 1.25
  elif key == '=' or key =='+':
    options['G_zoom'] *= 1.25
  elif key == 'f' or key == 'F':
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
  elif key == 'l' or key == 'L':
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);
  elif key == 'a' or key == 'A':
    if options['rotating']:
      options['rotating'] = False
      glutIdleFunc(None)
    else:
      options['rotating'] = True
      glutIdleFunc(IdleCallback)
  elif key == 'r' or key == 'R':
      # Reset the animal
      animal['wing_dir'] = 'up'
      animal['wing_deg'] = -10.0
      animal['head_deg'] = 0.5
      animal['velocity'] = 3.0

      # View control options
      options['G_walk'] = [0, 0, 0]
      options['G_theta'] = [0, 0, 0]
      options['G_zoom'] = 0.3
      options['rotating'] = False

      # Mouse and environment options
      options['MousePressed'] = False
      options['pitch0'] = 0
      options['yaw0'] = 0
      options['mouseX0'] = 0
      options['mouseY0'] = 0

      glutIdleFunc(None)
  elif key == '1':
    animal['velocity'] = 1.0
  elif key == '2':
    animal['velocity'] = 3.0
  elif key == '3':
    animal['velocity'] = 7.0
  elif key == '4':
    animal['velocity'] = 15.0
  else:
    DisplayMenuOptions()
    return

  glutPostRedisplay()


# Handle the special keyboard events (arrow keys)
def SpecialCallback(key, x, y):
    global options
    
    if key == GLUT_KEY_UP:
        options['G_walk'][1] -= 0.25
    elif key == GLUT_KEY_DOWN:
        options['G_walk'][1] += 0.25
    elif key == GLUT_KEY_LEFT:
        options['G_walk'][0] += 0.25
    elif key == GLUT_KEY_RIGHT:
        options['G_walk'][0] -= 0.25
    else:
        return

    glutPostRedisplay()


#========================================================
# MAIN
#========================================================

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(800, 600)
#glutFullScreen()
glutInitWindowPosition(100, 100)
glutCreateWindow('F29GR Project: A bird')

# Deal with the callback functions and initialize the program
Init()
glutDisplayFunc(DisplayCallback)
glutReshapeFunc(ReshapeCallback)
glutIdleFunc(None)
glutKeyboardFunc(KeyboardCallback)
glutSpecialFunc(SpecialCallback)
glutMouseFunc(MouseCallback)
glutMotionFunc(MouseMotionCallback)

# Start the main loop
glutMainLoop()