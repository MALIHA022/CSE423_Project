from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

camera_pos = (500, 1600, 0)

GRID_LENGTH = 100  
GRID_SIZE = 32

# Game stats
player_pos = [13 * GRID_LENGTH + (GRID_LENGTH // 2), 0, 12 * GRID_LENGTH + (GRID_LENGTH // 2)]
player_angle = 0
camera_mode = "third"  
rotate = False
game_over = False

# Player stats
life = 5
collected = 0
min_bound = (-GRID_SIZE * GRID_LENGTH // 2) + 100
max_bound = (GRID_SIZE * GRID_LENGTH // 2) - 100

#enemies
enemies = []

#cheat mode
egg_visible = True
cheat_egg_positions = [(-550, 50, 265), (450, 50, 1350), (550, 50, -850), (1180, 50, 500)]
cheat_egg_pos = list(random.choice(cheat_egg_positions)) 
cheat_sequence = ['UP', 'UP', 'DOWN', 'DOWN', 'LEFT', 'RIGHT', 'LEFT', 'RIGHT']
sequence_index = 0
cheat_mode = False
cheat_ready = False
egg_visible = True
skip_wall_collision = False

# treasure
num_spheres=10
sphere_positions = [(-300, 30, -800), (-50, 30, -150) ,(900, 30, 900), (1150, 30, 200), (250, 30, 1050),
     (1400, 30, -300), (-650, 30, 1400), (-1400, 30, 550), (1150, 30, -1500), (-50, 30, -1200)]
    

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


maze = [  # --- Right wall
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
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], # |bottom wall
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
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
    
    if cheat_mode:
        glTranslatef(player_pos[0], 100, player_pos[2])
    else:
        glTranslatef(player_pos[0], 50, player_pos[2])
    glRotatef(player_angle+90, 0, 1, 0)  

    if game_over:
        glRotatef(90, 0, 1, 0)

    # Legs
    # right leg
    glPushMatrix()
    glTranslatef(10, -30, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 10)
    glPopMatrix()

    # left leg
    glPushMatrix()
    glTranslatef(-10, -30, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 10)
    glPopMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 50, 0) 
    glScalef(0.8, 1.6, 0.6)  
    glColor3f(85 / 255, 108 / 255, 47 / 255)
    glutSolidCube(40) 
    glPopMatrix()

    # Head 
    glPushMatrix()
    glTranslatef(0, 100, 0) 
    glColor3f(0.0, 0.0, 0.0)  
    gluSphere(gluNewQuadric(), 18, 20, 20)  
    glPopMatrix()

    # Arms
    # Right arm
    glPushMatrix()
    glTranslatef(20, 70, -5)  
    glRotatef(90, 1, 0, 0) 
    glColor3f(254 / 255, 223 / 255, 188 / 255)
    gluCylinder(gluNewQuadric(), 4, 4, 45, 10, 10)
    glPopMatrix()

    # Left arm
    glPushMatrix()
    glTranslatef(-20, 70, -5) 
    glRotatef(90, 1, 0, 0)  
    glColor3f(254 / 255, 223 / 255, 188 / 255)
    gluCylinder(gluNewQuadric(), 4, 4, 45, 10, 10)
    glPopMatrix()

    glPopMatrix() 

def draw_enemy(e):
    pass
def spawn_enemy():
    pass

 
def draw_all_spheres():
    global sphere_positions
    glColor3f(0.8, 0.2, 0.8)  # Purple spheres
    for x, y, z in sphere_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(gluNewQuadric(), 25, 20, 20)
        glPopMatrix()


def place_spheres_on_maze(num_spheres):
    global sphere_positions
    walkable_tiles = []

    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == 0:
                x = (col - cols // 2) * GRID_LENGTH
                z = (row - rows // 2) * GRID_LENGTH
                walkable_tiles.append((x, 20, z))

def check_sphere_collection():
    global player_pos, sphere_positions, collected, remaining
    px, py, pz = player_pos
    updated_spheres = []

    for x, y, z in sphere_positions:
        if abs(px - x) < 40 and abs(pz - z) < 40:
            collected += 1
            remaining -= 1
            print("Collected a treasure sphere!")
        else:
            updated_spheres.append((x, y, z))

    sphere_positions = updated_spheres


def draw_cheat_egg():
    global cheat_egg_pos , egg_visible
    
    if not egg_visible:
        return  # Skip drawing if not visible

    glPushMatrix()
    glTranslatef(*cheat_egg_pos)

    glColor3f(0.92, 0.32, 0)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 40, 20, 20)
    glPopMatrix()

    glPopMatrix()


def is_wall(x, z):
    if not cheat_mode:
        offsets = [(-10, 0), (10, 0), (0, -10), (0, 10)]
        for dx, dz in offsets:
            col = int((x + dx + (len(maze[0]) // 2) * GRID_LENGTH) // GRID_LENGTH)
            row = int((z + dz + (len(maze) // 2) * GRID_LENGTH) // GRID_LENGTH)
            if 1 <= row < len(maze) and 1 <= col < len(maze[0]):
                if maze[row][col] == 1:
                    return True
            else:
                return True 
        return False

def cheat_egg_collision():
    global cheat_ready, sequence_index, player_pos, cheat_egg_pos
    px, py, pz = player_pos
    cex, cey, cez = cheat_egg_pos

    distance_x = abs(px - cex)
    distance_y = abs(py - cey)
    distance_z = abs(pz - cez)

    collision = distance_x < 60 and distance_y < 60 and distance_z < 60
    left_egg = distance_x > 100 or distance_y > 100 or distance_z > 100

    if collision:
        if not cheat_ready:
            cheat_ready = True
            print("You found a mysterious egg... A whisper echoes: ↑ ↑ ↓ ↓ ← → ← →")
    
    elif left_egg:
        if cheat_ready and not cheat_mode:  
            cheat_ready = False
            sequence_index = 0  
            print("Went too far from egg.")

def keyboardListener(key, x, y):
    if key == b'r': #restart
        pass

    if key == b'p': #pause
        pass

    if key == b'\x1b': #close game window/ exit game
        pass


def specialKeyListener(key, x, y):
    global player_pos, sequence_index, cheat_mode, cheat_ready, egg_visible, camera_mode, player_angle, rotate
    speed = 10
    px, py, pz = player_pos

    # Map special keys (arrows) to your cheat sequence
    key_map = {
        GLUT_KEY_UP: 'UP',
        GLUT_KEY_DOWN: 'DOWN',
        GLUT_KEY_LEFT: 'LEFT',
        GLUT_KEY_RIGHT: 'RIGHT'
    }

    # Handle special keys (arrow keys)
    if key in key_map:
        pressed_key = key_map[key]
        
        # CHEAT MODE ACTIVATION PROCESS
        if cheat_ready and not cheat_mode:
            expected_key = cheat_sequence[sequence_index]
            
            if pressed_key == expected_key:
                sequence_index += 1
                display_cheat_progress()
                if sequence_index == len(cheat_sequence):
                    cheat_mode = True
                    egg_visible = False
                    print("CHEAT MODE ACTIVATED!")
            
            else:
                print(f"Wrong key! Restarting sequence.")
                sequence_index = 0
        
        glutPostRedisplay()

    # normal player movement
    angle_step = 5
    if not game_over:
        angle = math.radians(player_angle)

        if key == GLUT_KEY_UP:  # Move player forward
            dx = -math.cos(angle) * speed
            dz = -math.sin(angle) * speed

            new_x = px + dx
            new_z = pz + dz

            if not is_wall(new_x, new_z):
                player_pos = [new_x, py, new_z]  

        elif key == GLUT_KEY_DOWN:  # Move player backward
            dx = math.cos(angle) * speed
            dz = math.sin(angle) * speed

            new_x = px + dx
            new_z = pz + dz

            if not is_wall(new_x, new_z):
                player_pos = [new_x, py, new_z]

        elif key == GLUT_KEY_RIGHT:  # Move player right
            if camera_mode == "third" and rotate == False:
                dx = math.sin(angle) * speed  
                dz = -math.cos(angle) * speed  

                new_x = px + dx
                new_z = pz + dz

                if not is_wall(new_x, new_z):
                    player_pos = [new_x, py, new_z]
                player_angle = 0
            if camera_mode == 'first' or (camera_mode == "third" and rotate == True):
                player_angle += angle_step

        elif key == GLUT_KEY_LEFT:  # Move player left
            if camera_mode == "third" and rotate == False:
                dx = -math.sin(angle) * speed
                dz = math.cos(angle) * speed 

                new_x = px + dx
                new_z = pz + dz

                if not is_wall(new_x, new_z):
                    player_pos = [new_x, py, new_z]
                player_angle = 0
            if camera_mode == 'first' or (camera_mode == "third" and rotate == True):
                player_angle -= angle_step

    px, py, pz = player_pos

def mouseListener(button, state, x, y):
    global camera_mode, rotate, player_angle
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over: #camera toggle
        if camera_mode == "third":
            camera_mode = "first"
        else:
            camera_mode = "third"
        print(f"Switched to {camera_mode}-person mode")
        
        glutPostRedisplay()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        rotate = not rotate
        if rotate == False and camera_mode == 'third':
            player_angle = 0
            print("Rotate: Off")
        else:
            print("Rotate: On")

def set_camera():
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 
              0,0,0,   
              0, 1, 0)

# def set_camera():  #corrected set_camera() for first and third person mode
#     global player_pos, player_angle, camera_mode

#     px, py, pz = player_pos

#     if camera_mode == "third":
#         distance = 150
#         height = 200

#         angle_rad = math.radians(player_angle)

#         cam_x = px + math.cos(angle_rad) * distance
#         cam_y = py + height
#         cam_z = pz + math.sin(angle_rad) * distance

#         gluLookAt(cam_x, cam_y, cam_z,  
#                   px, py + 50, pz,      
#                   0, 1, 0)              

#     elif camera_mode == "first":
#         angle_rad = math.radians(player_angle)

#         eye_x = px
#         eye_y = py + 120 
#         eye_z = pz

#         look_x = eye_x - math.cos(angle_rad) * 100
#         look_z = eye_z - math.sin(angle_rad) * 100

#         gluLookAt(eye_x, eye_y, eye_z,   
#                   look_x, eye_y, look_z, 
#                   0, 1, 0)         
              
def display_cheat_progress():
    progress = ''
    for i, key in enumerate(cheat_sequence):
        if i < sequence_index:
            progress += f"[{key}] "
        else:
            progress += f"{key} "
    print(f"Cheat Code Progress: {progress}")
    return


def cheat():
    global player_pos, skip_wall_collision

    if cheat_mode:
        if player_pos[1] < 250:    
            player_pos[1] += 10    
        skip_wall_collision = True
    else:
        skip_wall_collision = False


def idle():
    cheat()
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    set_camera()
    draw_grid(GRID_SIZE)
    draw_maze()
    draw_border_walls()
    
    # game info text
    if not game_over and not cheat_ready:
        draw_text(10, 570, f"Player Life Remaining: {life} ")
        draw_text(10, 550, f"Collected Treasure: {collected}")
        draw_text(10, 530, f"Remaining Treasure: {num_spheres - collected}")
    if game_over:
        draw_text(10, 460, f"Game is Over.")
        draw_text(10, 440, f'Press "R" to RESTART the Game.')

    if cheat_ready and not cheat_mode:
        draw_text(300, 550, f"You found a mysterious egg! A whisper echoes...")
        draw_text(300, 525, f"'UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT'")

    draw_player()
    draw_cheat_egg()
    cheat_egg_collision()
    draw_all_spheres()
    glutSwapBuffers()

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(120, 1.25, 1, -1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 580)
    glutInitWindowPosition(250, 0)
    glutCreateWindow(b"Treasure Hunt 3D")

    init()
    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)   
    glutKeyboardFunc(keyboardListener)   
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
