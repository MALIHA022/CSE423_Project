from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

camera_pos = (1000, 2500, 0)

GRID_LENGTH = 100  
GRID_SIZE = 32

# Game stats
player_pos = [13 * GRID_LENGTH + (GRID_LENGTH // 2), 0, 12 * GRID_LENGTH + (GRID_LENGTH // 2)]
player_angle = 0
camera_mode = "third"  
game_over = False

# Player stats
life = 5
collected = 0
remaining = 5
min_bound = (-GRID_SIZE * GRID_LENGTH // 2) + 150
max_bound = (GRID_SIZE * GRID_LENGTH // 2) - 150

def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_18): # type: ignore
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 600)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text 
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2],
    [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 2],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #---left wall

]

def draw_grid(GRID_SIZE):
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            glColor3f(0.85, 0.80, 0.73)

            x = (i - GRID_SIZE // 2) * GRID_LENGTH
            z = (j - GRID_SIZE // 2) * GRID_LENGTH

            glVertex3f(x, 0, z)
            glVertex3f(x + GRID_LENGTH, 0, z)
            glVertex3f(x + GRID_LENGTH, 0, z + GRID_LENGTH)
            glVertex3f(x, 0, z + GRID_LENGTH)
    glEnd()

def draw_border_walls():
    wall_height = 100
    offset = GRID_LENGTH * GRID_SIZE // 2

    glBegin(GL_QUADS)

    # Back wall (+z)
    glColor3f(0.03, 0.46, 0.05)
    glVertex3f(-offset, 0, offset)
    glVertex3f(offset, 0, offset)
    glVertex3f(offset, wall_height, offset)
    glVertex3f(-offset, wall_height, offset)

    # Front wall (-z)
    glVertex3f(-offset, 0, -offset)
    glVertex3f(offset, 0, -offset)
    glVertex3f(offset, wall_height, -offset)
    glVertex3f(-offset, wall_height, -offset)

    # Left wall (-X)
    glVertex3f(-offset, 0, -offset)
    glVertex3f(-offset, 0, offset)
    glVertex3f(-offset, wall_height, offset)
    glVertex3f(-offset, wall_height, -offset)

    # Right wall (+X)
    glVertex3f(offset, 0, -offset)
    glVertex3f(offset, 0, offset)
    glVertex3f(offset, wall_height, offset)
    glVertex3f(offset, wall_height, -offset)

    glEnd()


def draw_cube(x, y, z, size=100):
    half = size / 2
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.03, 0.46, 0.05)
    glutSolidCube(size)
    glPopMatrix()

def draw_maze():
    global player_pos
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 1:
                x = (col - len(maze[0]) // 2) * GRID_LENGTH
                z = (row - len(maze) // 2) * GRID_LENGTH
                draw_cube(x, 25, z)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 150, player_pos[2])
    glRotatef(player_angle, 0, 0, 1)  

    if game_over:
        glRotatef(90,0,1,0)

    # Head
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 30, 10, 10)

    glPopMatrix()

def draw_enemy():
    pass

def mouseListener(button, state, x, y):
    pass

def keyboardListener(key, x, y):
    pass

def specialKeyListener(key, x, y):
    global player_pos, min_bound, max_bound, GRID_SIZE
    speed = 10
    # Unpack player position from global
    px, py, pz = player_pos

    if not game_over:
        angle = math.radians(player_angle)

        if key == GLUT_KEY_UP:  # Move player up (forward)
            dx = -math.cos(angle) * speed
            dz = -math.sin(angle) * speed

            new_x = px + dx
            new_z = pz + dz

            # Clamp within bounds
            if min_bound <= new_x <= max_bound and min_bound <= new_z <= max_bound:
                player_pos = [new_x, py, new_z]  # Update player position

        elif key == GLUT_KEY_DOWN:  # Move player down (backward)
            dx = math.cos(angle) * speed
            dz = math.sin(angle) * speed

            new_x = px + dx
            new_z = pz + dz

            # Clamp within bounds
            if min_bound <= new_x <= max_bound and min_bound <= new_z <= max_bound:
                player_pos = [new_x, py, new_z]  # Update player position

        # LEFT key (strafe left, perpendicular to the forward direction)
        elif key == GLUT_KEY_RIGHT:  
            dx = math.sin(angle) * speed  # Move in the X direction perpendicular to the angle
            dz = -math.cos(angle) * speed  # Move in the Z direction perpendicular to the angle

            new_x = px + dx
            new_z = pz + dz

            # Clamp within bounds
            if min_bound <= new_x <= max_bound and min_bound <= new_z <= max_bound:
                player_pos = [new_x, py, new_z]  # Update player position

        # RIGHT key (strafe right, opposite of left)
        elif key == GLUT_KEY_LEFT:  
            dx = -math.sin(angle) * speed  # Move in the X direction perpendicular to the angle
            dz = math.cos(angle) * speed  # Move in the Z direction perpendicular to the angle

            new_x = px + dx
            new_z = pz + dz

            # Clamp within bounds
            if min_bound <= new_x <= max_bound and min_bound <= new_z <= max_bound:
                player_pos = [new_x, py, new_z]  # Update player position

    # Ensure player position is updated correctly
    px, py, pz = player_pos  # Update the local player position variables



def set_camera():
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 
              0,0,0,  # Looking towards center
              0, 1, 0)

def EnemyPLayerInteraction(): #collision detection
    pass

def cheat_mode():
    pass

def idle():
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    set_camera()
    draw_grid(GRID_SIZE)
    draw_maze()
    draw_border_walls()
    
    # game info text
    if not game_over:
        draw_text(10, 570, f"Player Life Remaining: {life} ")
        draw_text(10, 550, f"Collected Treasure: {collected}")
        draw_text(10, 530, f"Remaining Treasure: {remaining}")
    else:
        draw_text(10, 460, f"Game is Over.")
        draw_text(10, 440, f'Press "R" to RESTART the Game.')

    draw_player()

    glutSwapBuffers()

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, 1.25, 1, -1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 600)
    glutInitWindowPosition(250, 0)
    glutCreateWindow(b"Treasure Hunt 3D")

    init()
    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
