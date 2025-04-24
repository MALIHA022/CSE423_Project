from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera
camera_pos = (0,500,500)

fovY = 120  
GRID_LENGTH = 100  
GRID_SIZE = 14

# Game state
player_pos = [0, 0, 0]
player_angle = 0
camera_mode = "third"  
game_over = False

# Enemies
enemies = []
num_enemies = 5

# Player stats
life = 5
collected = 0
min_bound = -GRID_SIZE * GRID_LENGTH // 2
max_bound = GRID_SIZE * GRID_LENGTH // 2

#cheat
cheat = False
cheat_cam_offset = [-100, 0, 60]

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

# grid (game floor)
def draw_grid(GRID_SIZE):
    glBegin(GL_QUADS)
    for i in range(GRID_SIZE ):
        for j in range(GRID_SIZE):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)

            x = (i - GRID_SIZE // 2) * GRID_LENGTH
            y = (j - GRID_SIZE // 2) * GRID_LENGTH

            glVertex3f(x, y, 0) #bottom left
            glVertex3f(x + GRID_LENGTH, y, 0) #bottom right
            glVertex3f(x + GRID_LENGTH, y + GRID_LENGTH, 0) #top right
            glVertex3f(x, y + GRID_LENGTH, 0) #top left
    glEnd()

def draw_border_walls():
    wall_height = 100
    offset = GRID_LENGTH * GRID_SIZE // 2

    glBegin(GL_QUADS)

    # Bottom wall
    glColor3f(0.01, 0.9, 1)
    glVertex3f(-offset, -offset, 0)
    glVertex3f(offset, -offset, 0)
    glVertex3f(offset, -offset, wall_height)
    glVertex3f(-offset, -offset, wall_height)

    # Top wall
    glColor3f(1, 1, 1)
    glVertex3f(-offset, offset, 0)
    glVertex3f(offset, offset, 0)
    glVertex3f(offset, offset, wall_height)
    glVertex3f(-offset, offset, wall_height)

    # Left wall
    glColor3f(0, 0, 1)
    glVertex3f(-offset, -offset, 0)
    glVertex3f(-offset, offset, 0)
    glVertex3f(-offset, offset, wall_height)
    glVertex3f(-offset, -offset, wall_height)

    # Right wall 
    glColor3f(0.01, 0.9, 0.01)
    glVertex3f(offset, -offset, 0)
    glVertex3f(offset, offset, 0)
    glVertex3f(offset, offset, wall_height)
    glVertex3f(offset, -offset, wall_height)

    glEnd()


def draw_player():
    pass
    # glPushMatrix()
    # glTranslatef(*player_pos)
    # glRotatef(player_angle, 0, 0, 1)  

    # if game_over:
    #     glRotatef(90,0,1,0)

    # # Left foot
    # glColor3f(0, 0, 1)
    # glTranslatef(0,-20,-100)
    # glRotatef(90, 0, 1, 0)
    # glRotatef(90, 0, 1, 0)
    # gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # # Right
    # glColor3f(0, 0, 1)
    # glTranslatef(0,-80,0)
    # gluCylinder(gluNewQuadric(), 16, 8, 100, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # # Body
    # glColor3f(0.4, 0.5, 0)
    # glTranslatef(0, 40, -30)
    # glutSolidCube(80)

    # # Gun
    # glColor3f(0.5, 0.5, 0.5)
    # glTranslatef(0, 0, 40)
    # glTranslatef(30, 0, -90) 
    # glRotatef(90, 0, 1, 0)
    # gluCylinder(gluNewQuadric(), 20, 5, 120, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # # Left Hand
    # glColor3f(1, 0.7, 0.6)
    # glTranslatef(0, -25, 0)
    # gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # # Right Hand
    # glColor3f(1, 0.7, 0.6)
    # glTranslatef(0, 50, 0)
    # gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10) #quadric, base radius, top radius, height, slices, stacks

    # # Head
    # glColor3f(0, 0, 0)
    # glTranslatef(40,-25, -25)
    # gluSphere(gluNewQuadric(), 30, 10, 10)

    # glPopMatrix()


def draw_enemy(e):
    pass
    # glPushMatrix()
    # glTranslatef(*e['enemy_pos'])
    # glScalef(e["scale"], e["scale"], e["scale"]) 

    # #body
    # glColor3f(1, 0, 0)
    # glPushMatrix()
    # glTranslatef(0, 0, 40)
    # gluSphere(gluNewQuadric(), 40, 20, 20) #quadric, radius, slices, stacks
    # glPopMatrix()

    # #head
    # glColor3f(0,0,0)
    # glPushMatrix()
    # glTranslatef(0, 0, 80)
    # gluSphere(gluNewQuadric(), 30, 20, 20)
    # glPopMatrix()

    # glPopMatrix()

def spawn_enemy():  #respawn in the same place if collides with player
    pass

#     while True: # avoiding center
#         x = random.randint(-600, 500)
#         y = random.randint(-600, 500)
        
#         if abs(x) > 200 or abs(y) > 200:
#             break

#     return {
#         'enemy_pos': [x, y, 0], #position
#         'scale': 1.0, #size
#         'scale_dir': 0.005 #pulse
#     }
    
# for n in range(num_enemies):
#     enemy = spawn_enemy()
#     enemy["collide"] = False 
#     enemies.append(enemy)

def mouseListener(button, state, x, y):
    global camera_mode

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:  #jump with mouse left button
        if not game_over:
            pass

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over: #cheat/ fly mode toggle
        if camera_mode == "third":
            camera_mode = "first"
        else:
            camera_mode = "third"
        print(f"Switched to {camera_mode}-person mode")
        
        glutPostRedisplay()
  

def keyboardListener(key, x, y): 
    """
    Handles keyboard inputs for player movement, camera updates and cheat mode toggles.
    """
    global player_pos, player_angle, camera_mode, min_bound, max_bound, cheat_cam_offset
    global life, collected, game_over

    speed = 50


    if not game_over:
        if key == b'w':  # move forward
            angle = math.radians(player_angle)
            dx = -math.cos(angle) * speed
            dy = -math.sin(angle) * speed

            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy

            if min_bound <= new_x <= max_bound and min_bound <= new_y <= max_bound:
                player_pos[0] = new_x
                player_pos[1] = new_y
                
                if camera_mode == "first" and cheat:
                    cheat_cam_offset[0] += dx
                    cheat_cam_offset[1] += dy

        elif key == b's':  # move backward
            angle = math.radians(player_angle)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed

            new_x = player_pos[0] + dx
            new_y = player_pos[1] + dy

            if min_bound <= new_x <= max_bound and min_bound <= new_y <= max_bound:
                player_pos[0] = new_x
                player_pos[1] = new_y

                if camera_mode == "first" and cheat and not gun:
                    cheat_cam_offset[0] += dx
                    cheat_cam_offset[1] += dy


        elif key == b'a' and not cheat:  #rotate left
            player_angle += angle_step

        elif key == b'd' and not cheat: #rotate right
            player_angle -= angle_step
        
        elif key == b"c": #cheat mode
            cheat = not cheat
            if cheat:
                cheat_mode()
            else:
                gun = False
        
        elif key == b"v": #toggle automatic gun cam
            if camera_mode == "first" and cheat:
                gun = not gun
            if not cheat:
                gun = False
                
    if key == b'r' and game_over: #restart
        bullets.clear()
        enemies.clear()
        cheat = False
        camera_mode = "third"
        for _ in range(num_enemies):
            enemy = spawn_enemy()
            enemy['collide'] = False
            enemies.append(enemy)
            
        score = 0
        missed_bullets = 0
        life = 5
        game_over = False
        player_pos[:] = [0, 0, 0]
        player_angle = 0
        print("Game restarted!")
            
        glutPostRedisplay()

def specialKeyListener(key, x, y): #player turns left and right with left and right arrow keys
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, player_pos
    if not game_over:
        if key == GLUT_KEY_LEFT: # player turn left
            pass

        if key == GLUT_KEY_RIGHT:  # player right 
            pass

    # camera_pos = (x, y, z)

lastx, lasty, lastz = 0,0,0
def setupCamera():
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(fovY, 1.25, 0.1, 1500)  #(field of view, aspect ratio, near clip, far clip)
    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()

    global lastx, lasty, lastz

    if camera_mode == "third":
        x, y, z = camera_pos
        gluLookAt(x,y,z, 0,0,0, 0,0,1)

    if camera_mode == "first": #need to fix
        angle = math.radians(player_angle)
        gun_length = 50
        gun_right = 30
        gun_up = 40

        # camera at gun tip position
        cam_x = player_pos[0] + gun_right * math.sin(angle) - math.cos(angle) * gun_length
        cam_y = player_pos[1] - gun_right * math.cos(angle) - math.sin(angle) * gun_length
        cam_z = player_pos[2] + gun_up

        if camera_mode == "first" and cheat:
            look_x = cam_x + (-math.cos(angle)) * 100
            look_y = cam_y + (-math.sin(angle)) * 100
            look_z = cam_z

            lastx = look_x
            lasty = look_y
            lastz = look_z

        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)  

def enemy_player_interaction():
    global collected, life, game_over
    
    # enemies move towards player
    for e in enemies:
        dx = player_pos[0] - e['enemy_pos'][0]
        dy = player_pos[1] - e['enemy_pos'][1]
        
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 1:
            e['enemy_pos'][0] += dx / dist * 0.05  # enemy move speed
            e['enemy_pos'][1] += dy / dist * 0.05

        # Pulse effect
        e['scale'] += e['scale_dir']
        if e['scale'] >= 1.2 or e['scale'] <= 0.8:
            e['scale_dir'] *= -1
    
    # enemy and player collision
    if not game_over:
        for e in enemies:
            ex, ey, ez = e["enemy_pos"]
            px, py, pz = player_pos
    
            # Collision detection
            collision = abs(px - ex) < 100 and abs(py - ey) < 100 and abs(pz - ez) < 100
    
            if collision:
                if life > 0:
                    life -= 1
                    print(f"Remaining Player life: {life}")
                    enemies.remove(e)     
                    enemies.append(spawn_enemy()) 
                else:
                    game_over = True
                    enemies.clear()  
                break  

def cheat_mode(): #camera will get fixed in first person mode and player can move at any direction and collect anything
    global player_angle, player_pos, enemies, cheat_rotation, can_fire, collected

    if cheat and not game_over:
        # Rotate player slowly 
        rotate_speed = 1
        player_angle = (player_angle + rotate_speed) % 360
        cheat_rotation += rotate_speed

        if cheat_rotation >= 30:
            cheat_rotation = 0
            can_fire = True

        rad = math.radians(player_angle)
        dir_x = -math.cos(rad)
        dir_y = -math.sin(rad)

    glutPostRedisplay()


def idle():
    enemy_player_interaction()
    cheat_mode()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  
    glViewport(0, 0, 1000, 700)  

    setupCamera()

    draw_grid(GRID_SIZE)
    draw_border_walls()

    # game info text
    if not game_over:
        draw_text(10, 460, f"Player Life Remaining: {life} ")
        draw_text(10, 440, f"Collected Treasure: {collected}")
        draw_text(10, 420, f"Remaining: {5-collected}")
    else:
        draw_text(10, 460, f"Game is Over.")
        draw_text(10, 440, f'Press "R" to RESTART the Game.')

    draw_player()
    for e in enemies:
        draw_enemy(e)

    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 600)  # Window size
    glutInitWindowPosition(250, 0)  # Window position
    glutCreateWindow(b"Treasure Hunt 3D")  #window
    
    glutDisplayFunc(showScreen)  #display function
    glutKeyboardFunc(keyboardListener)  #keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  #idle function to move the bullet automatically

    glutMainLoop()  #GLUT main loop

if __name__ == "__main__":
    main()