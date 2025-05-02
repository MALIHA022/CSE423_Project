from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

camera_pos = (500, 1600, 0)

GRID_LENGTH = 100  
GRID_SIZE = 34

# Game stats
player_pos = [13 * GRID_LENGTH + (GRID_LENGTH // 2), 0, 12 * GRID_LENGTH + (GRID_LENGTH // 2)]
player_angle = 0
camera_mode = "third"  
game_over = False
paused = False


# Player stats
life = 5
collected = 0
rotate = False

#enemies
enemies = []
enemy_count = 10
last_hit_time = 0
cooldown_duration = 1.5  


#cheat mode
egg_visible = True
cheat_egg_positions = [(-550, 50, 265), (450, 50, 1350), (550, 50, -850), (1180, 50, 500)]
cheat_egg_pos = list(random.choice(cheat_egg_positions)) 
cheat_sequence = ['UP', 'UP', 'DOWN', 'DOWN', 'LEFT', 'RIGHT', 'LEFT', 'RIGHT']
sequence_index = 0
cheat_mode = False      # cheat mode on off
cheat_ready = False     # near cheat egg - ready to trigger cheat mode
egg_visible = True      # when cheat mode unlocked - egg disappears
cheat_unlocked = False  #unlocking cheatmode once
skip_wall_collision_player = False

# treasure
num_spheres = 10
treasure_positions = [(-850, 30, -700), (-50, 30, -150), (900, 30, 900), (1150, 30, 200), (250, 30, 1050),
                      (1400, 30, -300), (-650, 30, 1400), (-1400, 30, 550), (1150, 30, -1500), (-50, 30, -1200)]
remaining = len(treasure_positions)

#goal
goal_achieved = False

# on-screen texts
def draw_text(x, y, text, font):
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

# maze
maze = [  # --- Right wall
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
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
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] #---left wall
]

def draw_grid(GRID_SIZE):
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            glColor3f(0.8, 0.82, 0.76) # floor color

            x = (i - GRID_SIZE // 2) * GRID_LENGTH
            z = (j - GRID_SIZE // 2) * GRID_LENGTH

            glVertex3f(x, 0, z)
            glVertex3f(x + GRID_LENGTH, 0, z)
            glVertex3f(x + GRID_LENGTH, 0, z + GRID_LENGTH)
            glVertex3f(x, 0, z + GRID_LENGTH)
    glEnd()


def draw_cube(x, y, z, size=100): # maze walls drawn with cubes
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

def is_wall(x, z, skip_wall_collision_player): #maze walls collision detection
    player_radius = 25 

    maze_width = len(maze[0]) * GRID_LENGTH
    maze_height = len(maze) * GRID_LENGTH
    
    half_width = maze_width // 2
    half_height = maze_height // 2

    # boundary in cheat mode
    if not (-half_width <= x <= half_width and -half_height <= z <= half_height):
        return True  # Out of bounds

    # skiping inside maze walls
    if skip_wall_collision_player:
        return False
    
    # wall collision - normal state
    px_min = x - player_radius
    px_max = x + player_radius
    pz_min = z - player_radius
    pz_max = z + player_radius

    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                wall_x = (col - len(maze[0]) // 2) * GRID_LENGTH
                wall_z = (row - len(maze) // 2) * GRID_LENGTH
                wx_min = wall_x - 50
                wx_max = wall_x + 50
                wz_min = wall_z - 50
                wz_max = wall_z + 50

                if px_max > wx_min and px_min < wx_max and pz_max > wz_min and pz_min < wz_max:
                    return True

    return False

# player
def draw_player():
    if camera_mode == "first":
        return  
    glPushMatrix()

    if cheat_mode:
        glTranslatef(player_pos[0], 100, player_pos[2])
    else:
        glTranslatef(player_pos[0], 50, player_pos[2])
    glRotatef(-player_angle+90, 0, 1, 0)  

    if game_over: #player lies down when game over
        glRotatef(90, 1, 0, 0)

    # Legs
    # right leg
    glPushMatrix()
    glTranslatef(10, -30, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)  # blue
    gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 10)
    glPopMatrix()

    # left leg
    glPushMatrix()
    glTranslatef(-10, -30, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)  # blue
    gluCylinder(gluNewQuadric(), 8, 8, 60, 10, 10)
    glPopMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 50, 0) 
    glScalef(0.8, 1.6, 0.6)  
    glColor3f(0.2, 0.6, 1.0)  # Blueish
    glutSolidCube(40) 
    glPopMatrix()

    # Head 
    glPushMatrix()
    glTranslatef(0, 100, 0) 
    glColor3f(0.0, 0.0, 0.0)  # black
    gluSphere(gluNewQuadric(), 18, 20, 20)  
    glPopMatrix()

    # Arms
    # Right arm
    glPushMatrix()
    glTranslatef(20, 70, -5)  
    glRotatef(90, 1, 0, 0) 
    glColor3f(254 / 255, 223 / 255, 188 / 255) #skin tone
    gluCylinder(gluNewQuadric(), 4, 4, 45, 10, 10)
    glPopMatrix()

    # Left arm
    glPushMatrix()
    glTranslatef(-20, 70, -5) 
    glRotatef(90, 1, 0, 0)  
    glColor3f(254 / 255, 223 / 255, 188 / 255) #skin tone
    gluCylinder(gluNewQuadric(), 4, 4, 45, 10, 10)
    glPopMatrix()

    glPopMatrix() 

# enemy
def draw_enemy(e):
    glPushMatrix()
    glTranslatef(e["x"], e["y"], e["z"])
    glScalef(e["scale"], e["scale"], e["scale"])

    # Body 
    glColor3f(1, 0, 0)  # red
    gluSphere(gluNewQuadric(), 30, 20, 20)

    # Head 
    glTranslatef(0, 40, 0)  
    glColor3f(0, 0, 0)  # black
    gluSphere(gluNewQuadric(), 20, 20, 20)

    glPopMatrix()


def spawn_enemy():
    global enemies
    enemies = []

    enemy_positions = [
        (0, 50, -430, "x"),
        (-1120, 50, 1440, "z"), 
        (-1100, 50, -840, "z"), 
        (-730, 50, 550, "z"),
        (250, 45, 550, 'z'),
        (1350, 50, -1130, 'x'), 
        (900, 50, 1000, "z"),
        (1450, 50, -500, 'z'), 
    ]

    for x, y, z, go in enemy_positions:
        # maze coordinates
        col = int((x + (len(maze[0]) // 2) * GRID_LENGTH) // GRID_LENGTH)
        row = int((z + (len(maze) // 2) * GRID_LENGTH) // GRID_LENGTH)

        # Check if it's walkable maze path
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 0:
            enemy = {
                "x": x,
                "y": y,
                "z": z,
                "go": go,
                "dir": 1,
                "scale": 1.0
            }
            enemies.append(enemy)

def update_enemy_positions():
    if paused or game_over or goal_achieved:
        return 
    
    for enemy in enemies:
        speed = 3.0

        if enemy["go"] == "x":
            enemy["x"] += enemy["dir"] * speed
            if is_wall(enemy["x"]+20, enemy["z"]+20, False):
                enemy["dir"] *= -1  # reverse

        if enemy["go"] == "z":
            enemy["z"] += enemy["dir"] * speed
            if is_wall(enemy["x"]+20, enemy["z"]+20, False):
                enemy["dir"] *= -1  # reverse


def enemy_collision():
    global enemies, player_pos, life, game_over, last_hit_time, goal_achieved

    if game_over or goal_achieved or cheat_mode:
        return

    now = time.time()
    if now - last_hit_time < cooldown_duration:
        return 

    px, py, pz = player_pos[0], 50, player_pos[2]

    for enemy in enemies:
        ex, ey, ez = enemy["x"], enemy["y"], enemy["z"]

        dx = px - ex
        dy = py - ey
        dz = pz - ez

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        if distance < 60:
            life -= 1
            last_hit_time = now  # start cooldown
            print(f"Hit by enemy! Life remaining: {life}")

            if life <= 0:
                game_over = True
                print("Game Over!")
                print(f"Collected Treasure: {collected}" )
            break 

# cheat egg
def draw_cheat_egg():
    global cheat_egg_pos , egg_visible
    
    if not egg_visible:
        return  
    
    glPushMatrix()
    glTranslatef(*cheat_egg_pos)

    glColor3f(0.92, 0.32, 0)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 50, 20, 20)
    glPopMatrix()

    glPopMatrix()

def cheat_egg_collision():
    global cheat_ready, sequence_index, player_pos, cheat_egg_pos, cheat_unlocked
    px, py, pz = player_pos
    cex, cey, cez = cheat_egg_pos

    distance_x = abs(px - cex)
    distance_y = abs(py - cey)
    distance_z = abs(pz - cez)

    collision = distance_x < 60 and distance_y < 60 and distance_z < 60
    left_egg = distance_x > 100 or distance_y > 100 or distance_z > 100

    if collision:
        if not cheat_ready and not cheat_unlocked:
            cheat_ready = True
            print("You found a mysterious egg... A whisper echoes: ↑ ↑ ↓ ↓ ← → ← →")
    
    elif left_egg:  # moved far from cheat egg 
        if not cheat_unlocked and cheat_ready and not cheat_mode: 
            cheat_ready = False
            sequence_index = 0  
            print("Went too far from egg.")

# Treasure
def draw_treasure():
    global treasure_positions
    glColor3f(1.0, 0.5, 0.0)  # orange
    for x, y, z in treasure_positions:
        glPushMatrix()
        if cheat_mode:
            glTranslatef(x, 100, z)
        else:
            glTranslatef(x, y, z)

        gluSphere(gluNewQuadric(), 25, 20, 20)
        glPopMatrix()

def treasure_collision():
    global collected, remaining, treasure_positions, player_pos, goal_achieved

    if game_over:
        return

    px, _, pz = player_pos
    if cheat_mode:
        py = 100
    else:
        py = 50

    new_spheres = []

    for (tx, ty, tz) in treasure_positions:
        if cheat_mode:
            adjusted_ty = ty + 50 
        else:
            adjusted_ty = ty

        dx = px - tx
        dy = py - adjusted_ty
        dz = pz - tz

        distance = math.sqrt(dx * dx + dy * dy + dz * dz)

        if distance < 60:
            collected += 1
            remaining -= 1
            print(f"Treasure collected! Total: {collected}")
        else:
            new_spheres.append((tx, ty, tz))

    treasure_positions = new_spheres

    if collected == 10 and not goal_achieved:
        goal_achieved = True
        print("Goal Achieved! All treasures collected.")

# win condition
def check_win_condition():
    global collected, life, player_pos, game_over, goal_achieved

    if game_over or goal_achieved:
        return
    
    if collected == 10:
        goal_achieved == True
        print("All treasure collected!")
        print(f"Total treasure: {collected}")
        print(f"Enemy hit: {5 - life}")

# keyboard and mouse functions
def keyboardListener(key, x, y):
    global cheat_mode, cheat_unlocked
    global game_over, life, collected, remaining, treasure_positions, paused
    global player_pos, enemies, cheat_ready, sequence_index
    global player_angle, camera_mode, goal_achieved, last_hit_time
    global cheat_egg_pos, egg_visible
    
    if key == b'r':  # restart
        game_over = False
        treasure_positions = [(-950, 30, -700), (-50, 30, -150), (900, 30, 900), 
                              (1150, 30, 200), (250, 30, 1050), (1400, 30, -300), 
                              (-650, 30, 1400), (-1400, 30, 550), (1150, 30, -1500), 
                              (-50, 30, -1200)]
        
        life = 5
        collected = 0
        remaining = len(treasure_positions)
        
        player_pos = [13 * GRID_LENGTH + (GRID_LENGTH // 2), 0, 12 * GRID_LENGTH + (GRID_LENGTH // 2)]
        player_angle = 0
        camera_mode = "third"
        goal_achieved = False
        last_hit_time = 0
 
        cheat_mode = False
        cheat_ready = False
        sequence_index = 0
        cheat_unlocked = False
        cheat_egg_pos = list(random.choice(cheat_egg_positions))
        egg_visible = True

        print("Game restarted.")

    if key == b'\x1b': #close game window/ exit game
        glutLeaveMainLoop()
    
    if game_over or goal_achieved:
        return 
    
    if key == b'c':
        if cheat_unlocked:
            if cheat_mode:
                if not is_wall(player_pos[0], player_pos[2], skip_wall_collision_player=False): # cheatmode off when no maze wall beneath
                    cheat_mode = False
                    print("Cheat mode OFF")
                else:  
                    print("Cannot turn off cheat mode. You're over maze wall!")

            else:
                cheat_mode = True
                print("Cheat mode ON")


    if key == b'p': #pause
        if not game_over or not goal_achieved:
            paused = not paused
        if paused:
            print("Game paused!")
        else:
            print("Game Resumed")

def specialKeyListener(key, x, y):
    global player_pos, player_angle, rotate, camera_mode  
    global sequence_index, cheat_mode, cheat_ready, egg_visible, cheat_unlocked
    global game_over, goal_achieved

    if game_over or goal_achieved or paused:
        return

    speed = 20
    px, py, pz = player_pos

    # keys of cheat sequence
    key_map = {
        GLUT_KEY_UP: 'UP',
        GLUT_KEY_DOWN: 'DOWN',
        GLUT_KEY_LEFT: 'LEFT',
        GLUT_KEY_RIGHT: 'RIGHT'
    }

    # take cheat sequence input only if cheat mode is not active
    if not cheat_mode and key in key_map:
        pressed_key = key_map[key]
        
        # CHEAT MODE ACTIVATION 
        if cheat_ready and not cheat_mode:
            if sequence_index < len(cheat_sequence):
                expected_key = cheat_sequence[sequence_index]
                
                if pressed_key == expected_key:
                    sequence_index += 1
                    display_cheat_progress()
                    if sequence_index == len(cheat_sequence):
                        cheat_unlocked = True
                        cheat_mode = True
                        egg_visible = False
                        print("CHEAT MODE ACTIVATED!")
                else:
                    print(f"Wrong key! Restarting sequence.")
                    sequence_index = 0

    #normal player movement
    angle_step = 5
    if not game_over:
        angle = math.radians(player_angle)

        if key == GLUT_KEY_UP:  # Move player forward
            dx = -math.cos(angle) * speed
            dz = -math.sin(angle) * speed

            new_x = px + dx
            new_z = pz + dz

            if not is_wall(new_x, new_z, skip_wall_collision_player):
                player_pos = [new_x, py, new_z]  

        elif key == GLUT_KEY_DOWN:  # Move player backward
            dx = math.cos(angle) * speed
            dz = math.sin(angle) * speed

            new_x = px + dx
            new_z = pz + dz

            if not is_wall(new_x, new_z, skip_wall_collision_player):
                player_pos = [new_x, py, new_z]

        elif key == GLUT_KEY_RIGHT:  # Move player right
            if camera_mode == "third" and rotate == False:
                dx = math.sin(angle) * speed  
                dz = -math.cos(angle) * speed  

                new_x = px + dx
                new_z = pz + dz

                if not is_wall(new_x, new_z, skip_wall_collision_player):
                    player_pos = [new_x, py, new_z]
                player_angle = 0
            
            # if rotation on rotate in third person as well
            if camera_mode == 'first' or (camera_mode == "third" and rotate == True):
                player_angle += angle_step

        elif key == GLUT_KEY_LEFT:  # Move player left
            if camera_mode == "third" and rotate == False:
                dx = -math.sin(angle) * speed
                dz = math.cos(angle) * speed 

                new_x = px + dx
                new_z = pz + dz

                if not is_wall(new_x, new_z, skip_wall_collision_player):
                    player_pos = [new_x, py, new_z]
                player_angle = 0

            # if rotation on - rotate in third person as well
            if camera_mode == 'first' or (camera_mode == "third" and rotate == True):
                player_angle -= angle_step

    px, py, pz = player_pos

def mouseListener(button, state, x, y):
    global camera_mode, rotate, player_angle
    
    if game_over or goal_achieved or paused:
        return
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over: #camera toggle
        if camera_mode == "third":
            camera_mode = "first"
            rotate = True
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

def set_camera(): #remove before submission
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 
              0,0,0,   
              0, 1, 0)

# def set_camera(): #corrected set_camera() for first and third person mode
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
#         eye_y = py + 100  # Player's head is at y + 100 in draw_player()
#         eye_z = pz
    
#         look_x = eye_x - math.cos(angle_rad) * 60
#         look_z = eye_z - math.sin(angle_rad) * 60
    
#         gluLookAt(eye_x, eye_y, eye_z,   # Player's head position
#                   look_x, eye_y, look_z, # Look straight ahead
#                   0, 1, 0)


def display_cheat_progress(): # cheat sequence progress in terminal
    progress = ''
    
    for i, key in enumerate(cheat_sequence):
        if i < sequence_index:
            progress += f"[{key}] "
        else:
            progress += f"{key} "
    
    print(f"Cheat Code Progress: {progress}")
    return


def cheat():
    global player_pos, skip_wall_collision_player

    if cheat_mode:
        if player_pos[1] < 100:    
            player_pos[1] += 10    
        skip_wall_collision_player = True
    else:
        skip_wall_collision_player = False


def idle():
    if not game_over and not goal_achieved:
        cheat()
        update_enemy_positions()
    glutPostRedisplay()
    
    if paused:
        return

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    set_camera()
    draw_grid(GRID_SIZE)
    draw_maze()
    
    # game info text
    if not game_over:  # always showing game updates
        draw_text(10, 570, f"Player Life Remaining: {life}", GLUT_BITMAP_HELVETICA_18)      # type: ignore
        draw_text(10, 545, f"Collected Treasure: {collected}", GLUT_BITMAP_HELVETICA_18)    # type: ignore
        draw_text(10, 520, f"Remaining Treasure: {remaining}", GLUT_BITMAP_HELVETICA_18)    # type: ignore
    
    if cheat_unlocked and not game_over: # always showing after cheat mode activation
        draw_text(10, 495, f"Cheat Mode Activated!", GLUT_BITMAP_HELVETICA_12)      # type: ignore
    
    if game_over: # shows after game over
        draw_text(430, 550, f"Game Over.", GLUT_BITMAP_HELVETICA_18)    # type: ignore
        draw_text(300, 520, f"Total Treasure Collected: {collected}   |  Press 'R' to RESTART the Game.", GLUT_BITMAP_HELVETICA_12)     # type: ignore

    if cheat_ready and not cheat_mode and not paused and not cheat_unlocked: # shows only when player near egg
        draw_text(350, 550, f"You found a mysterious egg! A whisper echoes...", GLUT_BITMAP_HELVETICA_18)   # type: ignore
        draw_text(350, 525, f"'UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT'", GLUT_BITMAP_HELVETICA_18)           # type: ignore
    
    if not goal_achieved and paused: # shows when game paused
        draw_text(400, 520, "Game Paused   |   Press 'P' to Resume.", GLUT_BITMAP_HELVETICA_12)     # type: ignore
    
    if goal_achieved: # shows on game completion
        draw_text(430, 520, "You Win!!", GLUT_BITMAP_HELVETICA_18)      # type: ignore
        draw_text(400, 490, "Press 'R' to Play Again.", GLUT_BITMAP_HELVETICA_12)      # type: ignore


    draw_player()
    draw_cheat_egg()
    cheat_egg_collision()
    draw_treasure()
    treasure_collision()

    for enemy in enemies:
        draw_enemy(enemy)
    enemy_collision()
  
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
    glutInitWindowSize(1000, 570)
    glutInitWindowPosition(250, 0)
    glutCreateWindow(b"Treasure Hunt 3D")

    init()
    enemies = [spawn_enemy() for _ in range(enemy_count)]


    glutDisplayFunc(showScreen)
    glutSpecialFunc(specialKeyListener)   
    glutKeyboardFunc(keyboardListener)   
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()