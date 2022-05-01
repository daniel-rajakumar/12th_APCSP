# click "PLAY" to play in the game menu. 
# made in cmu academy

app.background = 'grey'

app.player_size = 30
app.enemy_size = 30

app.gravity = 1
app.playing = False


platforms = []
app.enemies = []
app.mountains = []
app.pole = None 

# generate the map (all the platforms)
def createMap():
    for _ in range(len(platforms)):
        platforms.pop().visible = False
        
    platforms.append(createPlatform(0, 0, 40, 50))
    platforms.append(createPlatform(platforms[-1].right + 100,   0, 500, 40))
    platforms.append(createPlatform(platforms[-1].right -  20,   0, 300, 80))
    platforms.append(createPlatform(platforms[-1].right +  40, 250, 500, 20))
    platforms.append(createPlatform(platforms[-2].right +  40, 150, 400, 20))
    platforms.append(createPlatform(platforms[-2].right -  20,  85,  20, 340))
    platforms.append(createPlatform(platforms[-2].right - 100,  58, 200, 30))
    platforms.append(createPlatform(platforms[-1].left  - 100,   0,  20, 150))
    platforms.append(createPlatform(platforms[-1].right      ,   0, 700, 10))
    platforms.append(createPlatform(platforms[-1].right -  50,  58, 200, 30))
    platforms.append(createPlatform(platforms[-1].right +  25, 100, 250, 30))
    platforms.append(createPlatform(platforms[-1].right + 150,   0, 400, 50))
    
    if (app.pole != None): 
        app.pole.visible = False
        
    app.pole = Group(
            Polygon(0, 0, 100, 50, 0, 100, fill='red'),
            Rect(0, 0, 10, 250, fill='red')
        )
    app.pole.left   = platforms[-1].left + 20
    app.pole.bottom = platforms[-1].top
    
    app.mario.steps_to_travel = app.pole.left - app.mario.right


# generate all the enemies
def create_enemies():
    for enemy in app.enemies:
        enemy.visible = False
        

    app.enemies = [
            create_enemy(platforms[2].centerX, 0),
            create_enemy(platforms[4].centerX, 0),
            create_enemy(platforms[8].centerX, 0),
        ]
        
# generate all the mountains
def create_mountains():
    while (len(app.mountains) > 0):
        app.mountains.pop().visible = False
        
    app.mountains.append(create_mountain(100                            , 200, 400, 1, rgb(100, 100, 100)))
    app.mountains.append(create_mountain(app.mountains[-1].centerX - 100, 150, 400, 2, rgb(110, 110, 110)))
    app.mountains.append(create_mountain(app.mountains[-1].centerX + 400, 150, 400, 2, rgb(110, 110, 110)))
    app.mountains.append(create_mountain(app.mountains[-1].centerX + 900, 150, 400, 5, rgb(100, 100, 100)))
    app.mountains.append(create_mountain(app.mountains[-3].centerX + 200, 120, 400, 3, rgb(140, 140, 140)))
    app.mountains.append(create_mountain(app.mountains[-1].centerX + 700, 160, 400, 4, rgb(180, 180, 180)))
    app.mountains.append(create_mountain(app.mountains[-2].centerX + 150, 160, 400, 4, rgb(180, 180, 180)))
    app.mountains.append(create_mountain(app.mountains[-1].centerX + 700, 120, 400, 7, rgb(200, 200, 200)))
    app.mountains.append(create_mountain(app.mountains[-2].centerX + 700, 100, 400, 3, rgb( 80,  80,  80)))



# generate a single platform
def createPlatform(x_from_left, y_from_bottom, width, height):
    platform = Rect(0, 0, width, height, fill='black')
    platform.left = x_from_left
    platform.bottom = app.bottom - y_from_bottom
    return platform
    
# generate a single mountain
def create_mountain(x, y_from_bottom, size, speed, color):
    mountain = Rect(0, 0, size, size, rotateAngle=45, fill=color)
    mountain.centerX = x
    mountain.top = app.bottom - y_from_bottom
    mountain.dx = speed
    return mountain
    
# generate a single enemy
def create_enemy(x, y):
    enemy = Rect(x, y, app.enemy_size, app.enemy_size, fill='black')
    enemy.dx = 5
    enemy.dy = 0
    enemy.canMoveLeft = True
    enemy.canMoveRight = True
    enemy.canMoveUp = True
    enemy.canMoveDown = True
    return enemy

# generate a single player
def create_player():
    if (app.mario != None):     
        app.mario.visible = False
        
    player = Rect(0, 0, app.player_size, app.player_size, fill='white')
    player.dx = 10
    player.dy = 0
    player.count = 0
    player.jump_height = 16
    player.canMoveLeft = True
    player.canMoveRight = True
    player.canMoveUp = True
    player.canMoveDown = True
    player.playing = True
    app.playing = True
    
    player.bottom = 100
    player.left = 10
    return player
    
  
  
  
    

app.mario = None
app.progress_bar = Rect(0, 0, 0.01, 50, fill="red")

# mario jump
def player_jump():
    if (app.mario.canMoveDown): return
    app.mario.canMoveDown = True
    app.mario.dy = -app.mario.jump_height
    app.mario.centerY += app.mario.dy
    
# mario movement
def move_mario(direction):
    change_direction = 0
    screen_offset = False
    can_move = app.mario.canMoveLeft
        
    if (direction == 'left'): 
        change_direction = -1
        screen_offset = app.mario.left > 400 * 0.1
        can_move = app.mario.canMoveLeft
        
    if (direction == 'right'):
        change_direction = 1
        screen_offset = app.mario.right < 400 * 0.5
        can_move = app.mario.canMoveRight
    
    if (can_move):
        if (screen_offset):
            app.mario.centerX += app.mario.dx * change_direction
            
        else:
            app.pole.centerX -= app.mario.dx * change_direction

            for platform in platforms:
                platform.centerX -= app.mario.dx * change_direction
        
            for enemy in app.enemies:
                enemy.centerX -= app.mario.dx * change_direction
         
            for mountain in app.mountains:
                mountain.centerX -= mountain.dx * change_direction 



# mario fall using gravity           
def drop(obj):
    if (not obj.canMoveUp):
        obj.dy *= -1

    if (obj.canMoveDown):
        obj.centerY += obj.dy
        obj.dy += app.gravity
        
        if (app.mario.top > 400):
            reset()
    
  
    
label_play = Label('PLAY', 200, 200, size=50, fill='black', font='orbitron')
button_play = Circle(200, 200, 150, fill='white', border='black', borderWidth=10,  dashes=True)


# menu bar
menu = Group(
        Rect(0, 0, 400, 400),
        button_play,
        label_play,
        Label("RIGHT_ARROW = Move front ", label_play.centerX, label_play.bottom + label_play.height, size=15),
        Label("LEFT_ARROW = Move back ",  label_play.centerX, label_play.bottom + label_play.height + 20, size=15),
        Label("UP_ARROW = Jump ",  label_play.centerX, label_play.bottom + label_play.height + 40, size=15),
        
        Label("Goal: ",  label_play.centerX, label_play.top - 100, size=20),
        Label("- Reach the flag ",  label_play.centerX, label_play.top - 80, size=15),
        Label("- Avoid hitting enemies ",  label_play.centerX, label_play.top - 60, size=15),
        Label("- Avoid falling off",  label_play.centerX, label_play.top - 40, size=15),
    )



# clear every object's value
def clear_map():
    app.pole.visible = False
    app.mario.visible = False

    app.mario = None
    while len(platforms) != 0:
        platforms.pop().visible = False
        
    while len(app.enemies) != 0:        
        app.enemies.pop().visible = False
 
    while len(app.mountains) != 0:        
        app.mountains.pop().visible = False
        
    app.pole = None
    app.progress_bar.width = 0.1
    app.label_win.value = ""

    
# show menu bar    
def main_menu():
    menu.visible = True
    app.playing = False
    clear_map()
    


# respawn every object. 
def reset():
    create_mountains()
    app.mario = create_player()
    createMap()
    create_enemies()



app.label_win = Label("", 200, app.progress_bar.centerY, size=20, font='orbitron')
# chck for win and celebrate if so. 
def checkWin():
    if (app.mario.hitsShape(app.pole)):
        app.label_win.value = "YOU WIN!"
        app.mario.playing = False
    
    if (not app.mario.playing and not app.mario.canMoveDown):
        app.mario.centerX += (app.mario.dx/2)
        
        if (app.mario.left > app.right):
            app.mario.dx = 0
            main_menu()

# check for lose and respawn if so. 
def checkLose():
    for enemy in app.enemies:
        if (enemy.hitsShape(app.mario)):
            reset()
 
# collision detection. 
def checkCanMove(entity):
    entity.canMoveLeft = True
    entity.canMoveRight = True   
    entity.canMoveUp = True
    entity.canMoveDown = True
    entity.stepped_out = False
    
    for platform in platforms:
        if (entity.bottom > platform.top and entity.top < platform.bottom):
            if (abs(entity.left - platform.right) < entity.dx):
                entity.canMoveLeft = False
                
            if (abs(entity.right - platform.left) < entity.dx):
                entity.canMoveRight = False
                
        if (entity.right > platform.left and entity.left < platform.right):
            if (abs(entity.top - platform.bottom) < 5):
                entity.canMoveUp = False
    
            if (entity.bottom >= platform.top and entity.top < platform.bottom):
                entity.bottom = platform.top 
                entity.canMoveDown = False

 
        if (entity.bottom >= platform.top and entity.top < platform.bottom):
            if (entity in app.enemies):
                if (abs(platform.right - entity.left) < entity.width
                or abs(platform.left - entity.right) < entity.width):
                    entity.stepped_out = True
         
         
# enemy movement  
def move_enemy(enemy):
    if (enemy.stepped_out and enemy in app.enemies):
        enemy.dx *= -1
        
    if (not enemy.canMoveDown):
        enemy.centerX += enemy.dx
        
 
# progress bar
def calc_progress():
    bar_width = ((app.mario.steps_to_travel - (app.pole.left - app.mario.right))/app.mario.steps_to_travel) * 400
    
    if (bar_width <= 0):
        app.progress_bar.width = 0.1
    else:
        app.progress_bar.width = bar_width
        
# button animation
def rotate_play_button():
    if (label_play.fill == "red"):
        button_play.rotateAngle += 0.25

# background thread 
def onStep():
    rotate_play_button()
    if (not app.playing): return
    checkWin()
    if (app.mario == None): return
    checkLose()
    checkCanMove(app.mario)
    drop(app.mario)
    calc_progress()
    
    for enemy in app.enemies:
        checkCanMove(enemy)
        drop(enemy)
        move_enemy(enemy)


# mouse input for game menu
def onMouseMove(x, y):
    if (label_play.hits(x, y)):
        label_play.fill = "red"
    else:
        label_play.fill = "black"
        

# mouse input for game menu
def onMousePress(x, y):
    if (label_play.hits(x, y)):
        menu.visible = False
        reset()

# key input for mario movement
def onKeyHold(keys):
    if (app.mario == None): return
    if (not app.mario.playing): return;
    
    if ('right' in keys):
        move_mario('right')
        
    if ('left' in keys):
        move_mario('left')

# key input for mario jump
def onKeyPress(key):
    if (app.mario == None): return
    if (not app.mario.playing): return;

    if ('up' in key):
        player_jump()
        
        
        
        
        
