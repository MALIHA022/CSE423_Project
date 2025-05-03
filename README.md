# CSE423_Project

🌀 __Maze Explorer 3D__

Maze Explorer 3D is a 3D OpenGL-based game where players navigate through a maze, collect hidden treasures, and avoid patrolling enemies. The game features multiple camera modes, player rotation, and a hidden cheat mode that can be unlocked with a secret sequence.



🎮 __Gameplay Overview__

* Explore a 3D Maze constructed from a 2D array of wall blocks.
* Move using the arrow keys (↑ ↓ ← →).
* Toggle cameras between first-person and third-person views using the left mouse button.
* Toggle player rotation in third-person mode using the right mouse button.
* Collect 10 unique treasures scattered throughout the maze.
* Avoid enemies patrolling near treasures — colliding with them reduces lives.
* Unlock cheat mode by finding a hidden bonus sphere and entering a secret key combo.
* Win by collecting all 10 treasures.
* Lose when all lives are lost.



🧍 __Player__

* Built using primitive 3D shapes (cube, sphere, cylinder).
* Starts with 5 lives.
* Collision with enemies reduces 1 life.
* Player movement is smooth and wall-bounded (except in cheat mode).



💎 __Treasures__

* 10 small colored spheres scattered across the maze.
* 1 bonus sphere unlocks cheat mode when a secret key combo is entered.
* Each treasure is guarded by a patrolling enemy.
* Collected treasures are removed from the map and increase the score.




👾 __Enemies__

* Move back and forth along predefined short patrol paths.
* Cannot be killed or outrun.
* Collision with the player results in life loss.
* Do not chase the player, only patrol their paths.




🧪 __Cheat Mode__

* Unlocked after collecting the bonus treasure and entering the secret key combo:

`UP` `UP` `DOWN` `DOWN` `LEFT` `RIGHT` `LEFT` `RIGHT`
              
* Grants the ability to fly (ascend over walls) and pass through maze walls.
* Useful for quickly navigating the maze or escaping enemies.




🕹️ __Controls__

|       Action              |       Input          |           Description                         |
|---------------------------|----------------------|-----------------------------------------------|
| Move Player               | Arrow Keys           | Navigate through the 3D maze                  |
| Toggle Camera View        | Left Mouse Click     | Switch between first-person and third-person  |
| Toggle Player Rotation    | Right Mouse Click    | Toggle rotation (only in third-person)        |
| Activate Cheat Mode       | Secret Key Combo     | Unlock flying and no wall collision           |
| Toggle Cheat Mode         |       `C`            | Enable/disable cheat mode (once unlocked)     |
| Pause Game                |       `P`            | Pauses/resumes the game                       |
| Restart Game              |       `R`            | Restarts the game from the beginning          |
| Exit Game                 |       `Esc`          | Closes the game                               |




📊 __Game States__

* Win Condition: Collect all 10 treasures.
* Lose Condition: Lives drop to 0 (player can no longer move or collect).
* Scoreboard: Live updates on score, lives, and collected treasures.
* Console Feedback: Important game events are printed to the terminal (e.g. collisions, cheat status, game over).




🔧 __Dependencies__

- Python 3.x
- OpenGL (via PyOpenGL)
- GLUT (FreeGLUT or equivalent)

Ensure PyOpenGL is installed:
pip install PyOpenGL PyOpenGL_accelerate




📁 __Project Structure__

    maze_explorer_3d/
    ├── main.py                  # Game loop and rendering
    ├── assets/                  # Optional: models/textures
    ├── README.md
    └── requirements.txt         # PyOpenGL, etc.




🧠 __Inspiration & Notes__

This project was created as a Computer Graphics course assignment, focusing on transformation, camera logic, input handling, and game state management in OpenGL using Python. It showcases:

* 3D collision detection
* Multiple camera systems
* Object transformations
* Real-time feedback and UI rendering




📜 __License__

This project is for academic and learning purposes. Feel free to fork, learn from, and build upon it!
