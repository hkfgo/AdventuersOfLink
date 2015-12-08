#Link's Adventure pitch sheet- https://drive.google.com/file/d/0ByuCfHejbh1bSzVYWGdIREtIZkk/view?pli=1
#This is a 2D RPG game where Link combats different enemies with several of his own weapns
#right now he can only shoot arrows
#getting hit by enemies or their projectiles will reduce link's life by 1 
#two types of enemies: red octorok moves horizontally while blue octorok moves vertically and shoots projectiles
#WASD to move, space to shoot, new game button resets game. 
#kill all enemies in the third and final room to win

import simplegui
import math
import random

FRAME_WIDTH = 700
FRAME_HEIGHT = 700
stairs = set([])
trophies = set([])
walls = set([])
arrow_group= set([])
enemy_missile_group = set([])

#enemy attributes 
link_sprite_size= [24, 30]
enemy_sprite_size = [40,40]
orientations = {'Down': [14, 58], 'Left': [339, 58], 'Up': [13, 179], 'Right': [341, 179]};
red_octorok_orientations = {'Down': [20, 20], 'Left': [96, 21], 'Up': [171, 21], 'Right': [249, 21]}
blue_octorok_orientations = {'Down': [324, 20], 'Left': [402, 21], 'Up': [478, 21], 'Right': [554, 21]}
wizzrope_orientations ={'Down': [628, 172], 'Left': [628, 172], 'Up': [708, 172], 'Right': [787, 172]}
fireball_orientations = {'Down': [785, 25], 'Left': [785, 25], 'Up': [785, 25], 'Right': [785, 25]}
map_position = 1 
lives = 2
arrow_count = 30 
in_play= False
in_how_to = False
in_score = False
in_how_to = False
in_name = False
level = 1
hit_counter = 0
death_counter = 3
score = 0
scores= []
#sounds
soundtrack = simplegui.load_sound("https://dl.dropboxusercontent.com/s/o6wlmgph46rilyu/battle_song.mp3?dl=0")
title_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/s/hjzz69oybeef3wv/title_song.mp3?dl=0")
sword_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/s/eu68dwea7nrcqgn/sword.mp3?dl=0")
arrow_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/s/sy050ur4jpd5weg/arrow_launch.wav?dl=0")
grunt_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/s/xxvhq2zjpohnqhi/grunt.wav?dl=0")
arrow_impact_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/s/ofj70m97h95bazm/arrow%20%281%29.wav?dl=0")
arrow_impact_sound.set_volume(0.7)
arrow_sound.set_volume(0.5)
timer = 0
OCTOROK_DIM = 2
FIRE_DIM = 2
WIZZROPE_DIM = 2
LINK_DIM = 3
time = 0
direction_key_down = False
attack_key_down = False
name = ""
key_down= set([])
class ImageInfo:
    def __init__(self, center, size, radius = 0):
        self.center = center
        self.size = size
        self.radius = radius
       

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius


class Sprite:
    def __init__(self, pos, orientation, vel, image, info, lifespan=None, health=0):
        self.pos=pos
        self.orientation=orientation
        self.vel=vel
        self.pos=pos 
        self.image=image
        self.image_size=info.get_size()        
        self.image_center = info.get_center()
        self.radius=info.get_radius()
        self.lifespan=lifespan
        self.health=health
        self.angle=orientation
        self.missile = False
        self.draw_angle = False
        self.enemy_type = None
        self.age = 0
        
    def draw(self, canvas):
        if(self.draw_angle):
            X =(self.pos[0]-(self.image_size[0]*math.cos(self.angle)/2+self.image_size[1]*math.sin(self.angle)/2))
            Y = (self.pos[1] - (self.image_size[0]*math.cos(self.angle)/2+self.image_size[1]*math.sin(self.angle)/2))
            
            #canvas.draw_polygon([(self.pos[0]-self.image_size[0]*math.cos(self.angle)/2-self.image_size[1]*math.sin(self.angle)/2, self.pos[1]-self.image_size[0]*math.cos(self.angle)/2-self.image_size[1]*math.sin(self.angle)/2), 
            #                 (self.pos[0]+self.image_size[0]*math.cos(self.angle)/2+self.image_size[1]*math.sin(self.angle)/2, self.pos[1]-self.image_size[0]*math.cos(self.angle)/2-self.image_size[1]*math.sin(self.angle)/2), 
            #               (self.pos[0]+self.image_size[0]*math.cos(self.angle)/2+self.image_size[1]*math.sin(self.angle)/2, self.pos[1]+self.image_size[0]*math.cos(self.angle)/2+self.image_size[1]*math.sin(self.angle)/2),
            #                (self.pos[0]-self.image_size[0]*math.cos(self.angle)/2-self.image_size[1]*math.sin(self.angle)/2, self.pos[1]+self.image_size[0]*math.cos(self.angle)/2+self.image_size[1]*math.sin(self.angle)/2)], 1, 'Green')
        #canvas.draw_polygon([(self.pos[0]-self.image_size[0]/2, self.pos[1]-self.image_size[1]/2), 
        #                     (self.pos[0]+self.image_size[0]/2, self.pos[1]-self.image_size[1]/2), 
        #                    (self.pos[0]+self.image_size[0]/2, self.pos[1]+self.image_size[1]/2),
        #                    (self.pos[0]-self.image_size[0]/2, self.pos[1]+self.image_size[1]/2)], 1, 'Green')
        if(self.draw_angle):
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size)
    def update(self):
        self.age +=1
        self.pos[0] = (self.pos[0] + self.vel[0]) % FRAME_WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % FRAME_HEIGHT
        
    def set_lifespan(self, lifespan):
        self.lifespan = lifespan
        
    def set_orientations(self, orientations):
        self.orientations = orientations
        
    def set_orientation(self, orientation):
        self.orientation= orientation
        self.image_center = self.orientations[orientation]
        magnitude = abs(self.vel[0] + self.vel[1])
        if(orientation == "Up"):
            self.angle = 1.57
            self.vel = [0, -1*magnitude]
        elif(orientation == "Down"):
            self.angle = 4.71
            self.vel = [0, magnitude]

        elif(orientation == "Left"):
            self.angle = 3.14
            self.vel = [-1*magnitude, 0]

        elif(orientation == "Right"):
            self.angle = 0
            self.vel = [magnitude, 0]

    
    def set_missile_image(self, image, image_info):
        self.missile = True
        self.missile_image = image
        self.missile_info = image_info
        
    def set_enemy_type(self, enemy_type):
        self.enemy_type=enemy_type
        
    def collide(self, sprite):  

        X =(self.pos[0]-self.image_size[0]/2)
        Y = (self.pos[1] - self.image_size[0]/2)
        spriteX = sprite.pos[0]-sprite.image_size[0]/2
        spriteY = sprite.pos[1]-sprite.image_size[1]/2
        if (spriteX<X+self.image_size[0] and X<spriteX+sprite.image_size[0]
           and spriteY<Y+self.image_size[1] and Y<spriteY+sprite.image_size[1]):
            return True
        else:
            return False
    def shoot(self):
        missile = Sprite( [int(25*math.cos((self.angle)))+self.pos[0], int(-25*math.sin((self.angle)))+self.pos[1]], self.angle, [0,0], self.missile_image, self.missile_info)

        missile.vel = [int(5*math.cos((self.angle)))+self.vel[0], int(-5*math.sin((self.angle)))+self.vel[1]]
        missile.set_lifespan(200)
        enemy_missile_group.add(missile) 
        level_grid.add_entity(missile)

class Link:
    def __init__(self, pos, orientation, vel, image, info, lifespan=None, health=10):
        self.pos=pos
        self.orientation=orientation
        self.vel=vel
        self.pos=pos 
        self.image=image
        self.image_size=info.get_size()
        self.radius=info.get_radius()
        self.lifespan=lifespan
        self.health=health
        self.image_center = info.get_center()
        self.set_orientation(orientation)
        self.collidable = True
        self.controllable = True
        self.drawable = True
        
    def draw(self, canvas):

        #canvas.draw_polygon([(self.pos[0]-self.image_size[0]/2, self.pos[1]-self.image_size[1]/2), 
         #                    (self.pos[0]+self.image_size[0]/2, self.pos[1]-self.image_size[1]/2), 
        #                   (self.pos[0]+self.image_size[0]/2, self.pos[1]+self.image_size[1]/2),
        #                    (self.pos[0]-self.image_size[0]/2, self.pos[1]+self.image_size[1]/2)], 1, 'Green')
        canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size)
        

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % FRAME_WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % FRAME_HEIGHT
    
    def set_orientation(self, orientation):
        self.orientation= orientation
        self.image_center = orientations[orientation]
        if(orientation == "Up"):
            self.angle = 1.57    
        if(orientation == "Down"):
            self.angle = 4.71
        if(orientation == "Left"):
            self.angle = 3.14
        if(orientation == "Right"):
            self.angle = 0
    
    def shoot(self):
        global arrow_count
        if(self.controllable):
            arrow_sound.play()
            if(self.orientation == "Down"):
                self.image_center = [94, 99]
            elif(self.orientation == "Up"):
                self.image_center = [98, 222]
            elif(self.orientation == "Right"):
                self.image_center = [422, 221]
            elif(self.orientation == "Left"):
                self.image_center = [422,99]
            if(self.orientation == "Left" or self.orientation =="Right"):
                angle = self.angle+1.57
            if(self.orientation == "Up" or self.orientation =="Down"):
                angle = self.angle-1.57
            if(arrow_count>0):    
                arrow = Sprite( [int(25*math.cos((self.angle)))+self.pos[0], int(-25*math.sin((self.angle)))+self.pos[1]], angle, [int(5*math.cos((self.angle)))+self.vel[0], int(-5*math.sin((self.angle)))+self.vel[1]], missile_image, missile_info)
                arrow.draw_angle = True
                arrow_group.add(arrow)
                level_grid.add_entity(arrow)
                arrow_count -= 1 
            
            
            
    def sword_attack(self):
        global score
        if(self.controllable):
            sword_sound.play()
            if(self.orientation == "Down"):
                self.image_size = [30,45]
                self.image_center = [138, 142]
            elif(self.orientation == "Up"):
                self.image_size = [30,45]

                self.image_center = [93,260]
            elif(self.orientation == "Right"):
                self.image_size = [45, 30]
                self.image_center = [422, 262]
            elif(self.orientation == "Left"):
                self.image_size = [45,30]
                self.image_center = [424, 141]
            
        for obj in level_grid.get_collidables(link):
            v_difference = obj.pos[1]-self.pos[1]
            h_difference = obj.pos[0]-self.pos[0]

            if(self.orientation == "Down" and v_difference>0 and v_difference<120 or obj.collide(link)):
                arrow_impact_sound.play()
                if(obj in enemies):
                    score +=50
                    enemies.remove(obj)
                    level_grid.remove_entity(obj)
            elif(self.orientation == "Up" and v_difference<0 and v_difference>-120 or obj.collide(link)):
                arrow_impact_sound.play()
                print "hit!"
                if(obj in enemies):
                    score +=50

                    enemies.remove(obj)
                    level_grid.remove_entity(obj)
            elif(self.orientation == "Right" and h_difference>0 and h_difference<120 or obj.collide(link)):
                arrow_impact_sound.play()
                if(obj in enemies):
                    score +=50
                    enemies.remove(obj)
                    level_grid.remove_entity(obj)
            elif(self.orientation == "Left" and h_difference<0 and h_difference>-120 or obj.collide(link)):  
                arrow_impact_sound.play()
                if(obj in enemies):
                    score+=50
                    enemies.remove(obj)
                    level_grid.remove_entity(obj)
        
class Grid:
    def __init__(self, map_width, map_height, cell_size):
        self.cell_size=cell_size
        self.rows=(map_height+cell_size-1)//cell_size
        self.columns=(map_width+cell_size-1)//cell_size
        self.grid = [[[] for x in range(self.columns)] for x in range(self.rows)] 
        
    
    def clear(self):
        self.grid = [[[] for x in range(self.rows)] for x in range(self.columns)] 
    
    def add_entity(self, entity):
        topLeftX = max(0, (entity.pos[0]-entity.image_size[0]/2) / self.cell_size);
        topLeftY = max(0, (entity.pos[1]-entity.image_size[1]/2) / self.cell_size);
        bottomRightX = min(self.columns-1, (entity.pos[0] + entity.image_size[0]/2 -1) / self.cell_size);
        bottomRightY = min(self.rows-1, (entity.pos[1] + entity.image_size[1]/2 -1) / self.cell_size);
    
        
        for r in range(topLeftX, bottomRightX+1):
            for c in range(topLeftY, bottomRightY+1):
                    self.grid[r][c].append(entity)
    #get all objects that share same cells with an entity  
    
    def remove_entity(self, entity):
        topLeftX = max(0, (entity.pos[0]-entity.image_size[0]/2) / self.cell_size);
        topLeftY = max(0, (entity.pos[1]-entity.image_size[1]/2) / self.cell_size);
        bottomRightX = min(self.columns-1, (entity.pos[0] + entity.image_size[0]/2 -1) / self.cell_size);
        bottomRightY = min(self.rows-1, (entity.pos[1] + entity.image_size[1]/2 -1) / self.cell_size);
    
        
        for r in range(topLeftX, bottomRightX+1):
            for c in range(topLeftY, bottomRightY+1):
                if(entity in self.grid[r][c]):
                    self.grid[r][c].remove(entity)
                    
    def get_collidables(self, entity):
        topLeftX = max(0, (entity.pos[0]-entity.image_size[0]/2) / self.cell_size);
        topLeftY = max(0, (entity.pos[1]-entity.image_size[1]/2) / self.cell_size);
        bottomRightX = min(self.columns-1, (entity.pos[0] + entity.image_size[0]/2 -1) / self.cell_size);
        bottomRightY = min(self.rows-1, (entity.pos[1] + entity.image_size[1]/2 -1) / self.cell_size);
    
        collidables_list=[]
        for r in range(topLeftX, bottomRightX+1):
            for c in range(topLeftY, bottomRightY+1):
                collidables_list=collidables_list+self.grid[r][c]
                
        return collidables_list

#images and sprites
splash_info = ImageInfo([347.5, 185.5], [695, 371], 20)
splash_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/99r0hcnjm3zc5oa/splash_screen.jpg?dl=0")
how_to_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/u383paxfpxcz5e5/how_to_play.png?dl=0")
enter_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/5tviq906srsec83/enter_name.png?dl=0")
score_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/a3ds6w5fh5sf44v/score.png?dl=0") 
how_to_image=simplegui.load_image("https://dl.dropboxusercontent.com/s/bfkq282rnlsuq4c/How-to-Play.png?dl=0")
background_info = ImageInfo([350, 350], [700,600], 350)
background_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/pqy68gijld06d45/background.png?dl=0")
desert_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/p5ocitce561rtx9/desert_background.png?dl=0")
forest_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/ng5jihmelfw7pi2/forest_background.png?dl=0")

stair_info = ImageInfo([22,22], [44,44], 22)
stair_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/aub6qne3tuwv36m/stairs.png?dl=0")

heart_info = ImageInfo([11.5, 10], [23,20], 12)
heart_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/c4hwsunt5poiall/heart.png?dl=0")

trophy_info = ImageInfo([24,24], [48,48], 24)
trophy_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/x6ntvz9jwgzxkij/trophy.png?dl=0")

level_grid = Grid(FRAME_WIDTH, FRAME_HEIGHT, 25)
link_info=ImageInfo([339, 58], link_sprite_size, 20)
link_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/ybfvpmvnlx38czf/thelegendofzeldalinktothepast_link_sheet.png?dl=0")

wall_info = ImageInfo([24,24], [48, 48], 22)
wall_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/jnpsjcchk2xkeqq/wall_sprite.gif?dl=0")
crate_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/2xlh9s57nq7xkub/crate_sprite.png?dl=0")
yellow_wall_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/dn2khvxjjupjd0p/wall_sprite_2.png?dl=0")

red_oct_info = ImageInfo([20,20], [40,40], 22)
blue_oct_info = ImageInfo([325, 20], enemy_sprite_size, 22)
wizzrope_info = ImageInfo([633, 174], enemy_sprite_size, 22)
fireball_info = ImageInfo([785, 25], enemy_sprite_size, 22)

blue_oct_missile_info = ImageInfo([938, 22], [24, 28], 3)
enemy_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/mlewy4hm4vkxww0/zelda-sprites-enemies.png?dl=0")

missile_info = ImageInfo([7.5, 24], [15, 48], 3)
missile_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/p8221a3pz2qfxi4/Arrow3.png?dl=0")

wall_coordinates= set([])


    
link = Link([70,70], 'Down', [0,0], link_image, link_info)
enemies = set([])


def enemy_wall_collide(enemy):
    for obj in level_grid.get_collidables(enemy):
                if(obj in walls):
                    
                    return True
    return False

#def wall_wall_collide():
#    for wall in walls:
#        if enemy_wall_collide(wall):
#            return True
#    return False

def spawn_random_walls(num):
    global wall_coordinates
    for x in range(num):
        pos_x = random.randrange(96, FRAME_WIDTH-96)
        pos_y = random.randrange(96, FRAME_HEIGHT-96)
        if( not (pos_x,pos_y) in wall_coordinates):
            wall_coordinates.add((pos_x,pos_y))

def spawn_level(enemy_quantities, wall_img = wall_image):
    global walls, level_grid, enemies, arrow_group, enemy_missile_group
    enemies = set([])
    arrow_group = set([])
    enemy_missile_group = set([])
    n_red_oct = enemy_quantities["red_oct"] 
    n_blue_oct = enemy_quantities["blue_oct"]
    
    level_grid.clear()
    walls = set([])
    for wall_co in wall_coordinates: 
        wall = Sprite(wall_co, 0 , [0,0], wall_img, wall_info)  
        walls.add(wall)
        level_grid.add_entity(wall)
    #make sure walls don't touch each other    
  
    #make sure Link doesn't get stuck in walls
    if(link.pos[0]>=100 and link.pos[0]<=FRAME_WIDTH-100 and link.pos[1]<=FRAME_HEIGHT-100 and link.pos[1]>=100):

        while(True):
                    if(enemy_wall_collide(link)):
                            posx= random.randrange(100, FRAME_WIDTH-100)
                            posy= random.randrange(100, FRAME_HEIGHT-100)
                            link.pos = [posx, posy]
                    else:
                        break
    
    if("wizzrope" in enemy_quantities):
        
        n_wizzrope = enemy_quantities["wizzrope"]
        for x in range(n_wizzrope):
            posx= random.randrange(100, FRAME_WIDTH-100)
            posy= random.randrange(100, FRAME_HEIGHT-100)
            vely = random.randrange(1 , 2)
            enemy = Sprite([posx, posy], 0, [0, vely], enemy_image, wizzrope_info)
            enemy.set_enemy_type("wizzrope")
            enemy.set_orientations(wizzrope_orientations)
            enemy.set_orientation("Down")

            enemies.add(enemy) 
            level_grid.add_entity(enemy)
            while(True):
                if(enemy_wall_collide(enemy)):
                    posx= random.randrange(100, FRAME_WIDTH-100)
                    posy= random.randrange(100, FRAME_HEIGHT-100)
                    enemy.pos = [posx, posy]
                else:
                    break
    

    for x in range(n_red_oct):
        posx= random.randrange(100, FRAME_WIDTH-100)
        posy= random.randrange(100, FRAME_HEIGHT-100)
        velx = random.randrange(1 , 5)
        enemy = Sprite([posx, posy], 0, [velx, 0], enemy_image, red_oct_info)
        enemy.set_orientations(red_octorok_orientations)
        enemy.set_enemy_type("red_octorok")
        enemies.add(enemy) 
        enemy.set_orientation("Left")
        level_grid.add_entity(enemy)
        while(True):
            if(enemy_wall_collide(enemy)):
                posx= random.randrange(100, FRAME_WIDTH-100)
                posy= random.randrange(100, FRAME_HEIGHT-100)
                enemy.pos = [posx, posy]
            else:
                break
          
    for x in range(n_blue_oct) :
        posx= random.randrange(100, FRAME_WIDTH-100)
        posy= random.randrange(100, FRAME_HEIGHT-100)
        vely = random.randrange(1 , 5)
        enemy = Sprite([posx, posy], 0, [0, vely], enemy_image, blue_oct_info)
        enemy.set_orientations(blue_octorok_orientations)
        enemy.set_orientation("Down")
        enemy.set_missile_image(enemy_image, blue_oct_missile_info)
        enemy.set_enemy_type("blue_octorok")

        enemies.add(enemy) 
        level_grid.add_entity(enemy)
        while(True):
            if(enemy_wall_collide(enemy)):
                posx= random.randrange(100, FRAME_WIDTH-100)
                posy= random.randrange(100, FRAME_HEIGHT-100)
                enemy.pos = [posx, posy]
            else:
                break
   
def spawn_level_one():
    global wall_coordinates 
    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    
    spawn_random_walls(4)
    wall_coordinates.remove((FRAME_WIDTH-24, 24+5*48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+6*48))
    wall_coordinates.remove((24, 24+4*48))
    wall_coordinates.remove((24, 24+3*48))
    spawn_level({"red_oct": 3, "blue_oct": 1})

def spawn_level_two():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    
    wall_coordinates.remove((FRAME_WIDTH-24, 24+48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+2*48))
    spawn_random_walls(4)

    wall_coordinates.remove((24, 24+5*48))
    wall_coordinates.remove((24, 24+6*48))
    spawn_level({"red_oct": 1, "blue_oct": 3, "wizzrope": 1})
    
def spawn_level_three():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(3)
    wall_coordinates.remove((FRAME_WIDTH-24, 24+4*48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+3*48))
    spawn_level({"red_oct": 1, "blue_oct": 0, "wizzrope": 0})

def spawn_level_four():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(4)
    
    wall_coordinates.remove((24, 24+48))
    wall_coordinates.remove((24, 24+2*48))
    wall_coordinates.remove((24+10*48, 24))
    wall_coordinates.remove((24+9*48, 24))
    spawn_level({"red_oct": 2, "blue_oct": 4,"wizzrope": 0}, crate_image)

def spawn_level_five():
    global wall_coordinates 
    
    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    wall_coordinates.remove((24+10*48, FRAME_HEIGHT-24))
    wall_coordinates.remove((24+9*48, FRAME_HEIGHT-24))
    spawn_level({"red_oct": 2, "blue_oct": 4,"wizzrope": 1}, crate_image)    

def spawn_level_six():
    global wall_coordinates 
    
    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(5)
    
    wall_coordinates.remove((FRAME_WIDTH-24, 24+4*48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+5*48))
    spawn_level({"red_oct": 2, "blue_oct": 1, "wizzrope": 1}, crate_image)    

def spawn_level_seven():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(5)
    
    wall_coordinates.remove((24, 24+4*48))
    wall_coordinates.remove((24, 24+5*48))
    wall_coordinates.remove((24+7*48, 24))
    wall_coordinates.remove((24+8*48, 24))
    spawn_level({"red_oct": 3, "blue_oct": 3, "wizzrope": 0}, crate_image)    

def spawn_level_eight():
    global wall_coordinates 
    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(5)
     
    wall_coordinates.remove((24+7*48, FRAME_HEIGHT-24))
    wall_coordinates.remove((24+8*48, FRAME_HEIGHT-24))
    spawn_level({"red_oct": 3, "blue_oct": 3, "wizzrope": 1}, crate_image)  

def spawn_level_nine():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(3)
    wall_coordinates.remove((FRAME_WIDTH-24, 24+4*48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+3*48))
    spawn_level({"red_oct": 2, "blue_oct": 1, "wizzrope": 2}, yellow_wall_image) 

def spawn_level_ten():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(5)
    
    wall_coordinates.remove((24, 24+4*48))
    wall_coordinates.remove((24, 24+3*48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+2*48))
    wall_coordinates.remove((FRAME_WIDTH-24, 24+3*48))
    spawn_level({"red_oct": 3, "blue_oct": 3, "wizzrope": 0}, yellow_wall_image) 

def spawn_level_11():
    global wall_coordinates 

    wall_coordinates = set([])
    for x in range(24, FRAME_WIDTH+24, 48):
        wall_coordinates.add((x,24))
    
    for x in range(24, FRAME_WIDTH+24, 48):

        wall_coordinates.add((x,FRAME_HEIGHT-24))

    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((24,y))


    for y in range(24, FRAME_HEIGHT+24, 48):

        wall_coordinates.add((FRAME_WIDTH-24,y))
    spawn_random_walls(5)
    
    wall_coordinates.remove((24, 24+2*48))
    wall_coordinates.remove((24, 24+3*48))
    spawn_level({"red_oct": 0, "blue_oct": 0, "wizzrope": 2}, yellow_wall_image) 
    
def spawn_level_by_position(position):
    if(position == 1):
        spawn_level_one()
    elif(position == 2):
        spawn_level_two()
    elif(position == 0):
        spawn_level_three()
    elif(position == 3):
        spawn_level_four()
    elif(position == 4):
        spawn_level_five()
    elif(position == 5):
        spawn_level_six()
    elif(position ==6):
        spawn_level_seven()
    elif(position ==7):
        spawn_level_eight()
    elif(position == 8):
        spawn_level_nine()
    elif(position == 9):
        spawn_level_ten()
    elif(position ==10):
        spawn_level_11()
    elif(position ==11):
        spawn_level_11()
        
def new_game():
    global stairs, trophies, lives, in_play, map_position, arrow_count, death_counter, hit_counter, score
    lives = 10
    arrow_count = 30
    map_position = 0
    in_play = True
    link.pos=[70,70]
    link.image_size[0] =24
    link.set_orientation("Down")
    spawn_level_by_position(0)
    link.controllable = True
    link.drawable = True
    link.collidable = True
    death_counter =3 
    hit_counter = 0
    title_sound.rewind()
    title_sound_timer.stop()
    soundtrack.play()
    battle_sound_timer.start()
    score = 0
    stairs = set([])
    trophies = set([])
def click():
    global message
    message = "Good job!"
    
def keydown(key):
    global direction_key_down, attack_key_down, name, keydown
    if(in_name== False):
        if key == simplegui.KEY_MAP['w']:
                key_down.add("w")
                
        if key == simplegui.KEY_MAP['s']:
                key_down.add("s")
               
        elif key == simplegui.KEY_MAP['a']:
                key_down.add("a")
               
        elif key == simplegui.KEY_MAP['d']:
                key_down.add("d")
                
        elif key == simplegui.KEY_MAP['space']:
                key_down.add("space")
                
        elif key == simplegui.KEY_MAP['j']:
                key_down.add("j")
                
        if(link.controllable):
            if key == simplegui.KEY_MAP['w']:
                key_down.add("w")
                print link.drawable
                link.vel[1]= -5 
                link.set_orientation("Up")
                direction_key_down = True
            elif key == simplegui.KEY_MAP['s']:
                print link.drawable
                key_down.add("s")
                link.vel[1]=5
                link.set_orientation("Down")
                direction_key_down = True
            elif key == simplegui.KEY_MAP['a']:
                key_down.add("a")
                link.vel[0]=-5
                link.set_orientation("Left")
                direction_key_down = True
            elif key == simplegui.KEY_MAP['d']:
                key_down.add("d")
                link.vel[0]=5
                link.set_orientation("Right")
                direction_key_down = True
            elif key == simplegui.KEY_MAP['space']:
                key_down.add("space")
                link.shoot()
                attack_key_down = True
            elif key == simplegui.KEY_MAP['j']:
                key_down.add("j")
                attack_key_down = True
                link.sword_attack()
    else:
        #if key == simplegui.KEY_MAP['backspace']:
        #        name = ""
        if(len(name) <= 8):
            print name
            if key == simplegui.KEY_MAP['a']:
                name = name +"a"
            elif key == simplegui.KEY_MAP['b']:
                name = name +"b"
            elif key == simplegui.KEY_MAP['c']:
                name = name +"c"  
            elif key == simplegui.KEY_MAP['d']:
                name = name +"d"             

            elif key == simplegui.KEY_MAP['e']:
                name = name +"e"             
            elif key == simplegui.KEY_MAP['f']:
                name = name +"f"          
            elif key == simplegui.KEY_MAP['g']:
                name = name +"g"         
            elif key == simplegui.KEY_MAP['h']:
                name = name +"h"         
            elif key == simplegui.KEY_MAP['i']:
                name = name +"i" 
            elif key == simplegui.KEY_MAP['j']:
                name = name +"j" 
            elif key == simplegui.KEY_MAP['k']:
                name = name +"k" 
            elif key == simplegui.KEY_MAP['l']:
                name = name +"l"             

            elif key == simplegui.KEY_MAP['m']:
                name = name +"m"             

            elif key == simplegui.KEY_MAP['n']:
                name = name +"n"             
            elif key == simplegui.KEY_MAP['o']:
                name = name +"o"             

            elif key == simplegui.KEY_MAP['p']:
                name = name +"p" 

            elif key == simplegui.KEY_MAP['q']:
                name = name +"q"
    
            elif key == simplegui.KEY_MAP['r']:
                name = name +"r"            
            
            elif key == simplegui.KEY_MAP['s']:
                name = name +"s"            
            
            elif key == simplegui.KEY_MAP['t']:
                name = name +"t"
            elif key == simplegui.KEY_MAP['u']:
                name = name +"u"           
           
            elif key == simplegui.KEY_MAP['v']:
                name = name +"v"           
           
            elif key == simplegui.KEY_MAP['w']:
                name = name +"w"
           
            elif key == simplegui.KEY_MAP['x']:
                name = name +"x"
           
            elif key == simplegui.KEY_MAP['y']:
                name = name +"y"           
           
            elif key == simplegui.KEY_MAP['z']:
                name = name +"z"              
            elif key == simplegui.KEY_MAP['space']:
                name = ""
            
            
def keyup(key):
    global attack_key_down, direction_key_down, keydown
    if key == simplegui.KEY_MAP['w']:
        key_down.discard('w')
        link.vel[1]= 0 
        direction_key_down = False
    elif key == simplegui.KEY_MAP['s']:
        key_down.discard('s')
        link.vel[1]=0
        direction_key_down = False
    elif key == simplegui.KEY_MAP['a']:
        key_down.discard('a')
        link.vel[0]=0
        direction_key_down = False
    elif key == simplegui.KEY_MAP['d']:
        key_down.discard('d')
        link.vel[0]=0
        direction_key_down = False
    elif key == simplegui.KEY_MAP['j']:
        key_down.discard('j')
        link.image_center = orientations[link.orientation]
        link.image_size = link_sprite_size
        attack_key_down = False
    elif key == simplegui.KEY_MAP['space']:
        key_down.discard('space')
        link.set_orientation(link.orientation)
        attack_key_down = False
# Handler to draw on canvas
def draw(canvas):
    global name, map_position, score, lives, in_play, enemies, stairs, level, arrow_count, trophies,link, time
    if(in_name == False and in_play ==False):
        canvas.draw_image(background_image, background_info.get_center(), background_info.get_size(), [FRAME_WIDTH/2, FRAME_HEIGHT/2], background_info.get_size())
    elif(map_position <5 and in_play):
        canvas.draw_image(desert_image, background_info.get_center(), background_info.get_size(), [FRAME_WIDTH/2, FRAME_HEIGHT/2], background_info.get_size())
    elif(map_position >= 5 and in_play):
        canvas.draw_image(forest_image, background_info.get_center(), background_info.get_size(), [FRAME_WIDTH/2, FRAME_HEIGHT/2], background_info.get_size())
    if(in_name):
        canvas.draw_text(name, (300, 250), 25, 'Black')
 
    if(in_play):
        if(link.drawable):
            link_index = time % LINK_DIM // 1
            if(len(key_down)>0):
                link.image_center[0] = link.image_center[0] + link_index*43

            link.draw(canvas)
            if(len(key_down)>0):
                link.image_center[0] = link.image_center[0] - link_index*43
            
            link.update()
        if(FRAME_WIDTH-link.pos[0] <= link.image_size[0] and link.orientation == "Right" and not map_position ==4 and not map_position ==7):
            for stair in stairs:
                level_grid.remove_entity(stair)
            stairs = set([])
            link.pos[0] = FRAME_WIDTH-link.pos[0]
            map_position += 1 
            spawn_level_by_position(map_position)
        elif(link.pos[1] <= link.image_size[1] and link.orientation == "Up" and not map_position ==4 and not map_position ==7):
            for stair in stairs:
                level_grid.remove_entity(stair)
            stairs = set([])
            link.pos[1] = FRAME_HEIGHT-link.pos[1]
            map_position += 1 

            spawn_level_by_position(map_position)
        elif(link.pos[0] <= link.image_size[0] and link.orientation == "Left"):
            
            for stair in stairs:
                level_grid.remove_entity(stair)
            stairs = set([])
            link.pos[0] = FRAME_WIDTH-link.pos[0]
            map_position -= 1 
     

            spawn_level_by_position(map_position)
        elif(FRAME_HEIGHT-link.pos[1] <= link.image_size[1] and link.orientation == "Down"):
          
            for stair in stairs:
                level_grid.remove_entity(stair)
            stairs = set([])
            link.pos[1] = FRAME_WIDTH-link.pos[1]
            map_position -= 1 
            spawn_level_by_position(map_position)
        for arrow in arrow_group:
            arrow.draw(canvas)
            level_grid.remove_entity(arrow)
            arrow.update()
            level_grid.add_entity(arrow)
            for obj in level_grid.get_collidables(arrow):
                if(obj.collide(arrow) and obj in walls):
                    if(arrow in arrow_group):
                        arrow_group.remove(arrow)
                    arrow_impact_sound.play()
                    level_grid.remove_entity(arrow)

    if(in_play):
        
        for stair in stairs:
            stair.draw(canvas)
        for trophy in trophies:
            trophy.draw(canvas)
        for wall in walls:

            wall.draw(canvas)

        for obj in level_grid.get_collidables(link):
            if (obj.collide(link)):
                if(obj in walls):
                 

                    link.pos[0] = (link.pos[0] - link.vel[0])
                    link.pos[1] = (link.pos[1] - link.vel[1])
                    link.vel=[0,0]

                elif(obj in enemies and link.collidable):
                    link.collidable = False
                    grunt_sound.play()
                    lives-=1
                    if(lives>0):

                        invincibility_timer.start()

                    #link.pos=[70,70]
                    link.vel= [0,0]
                    #map_position = 0

                    #spawn_level_three()
                elif(obj in enemy_missile_group and link.collidable):
                    original_pos = link.pos

                    if(obj.vel[0]>0 and link.orientation=="Left"):
                        obj.vel[0] = -1*obj.vel[0]
                        obj.vel[1] = -1*obj.vel[1]
                        enemy_missile_group.remove(obj)
                        arrow_group.add(obj)
                    elif(obj.vel[0]<0 and link.orientation=="Right"):
                        obj.vel[0] = -1*obj.vel[0]
                        obj.vel[1] = -1*obj.vel[1]
                        enemy_missile_group.remove(obj)
                        arrow_group.add(obj)   
                    elif(obj.vel[1]>0 and link.orientation=="Up"):
                        obj.vel[0] = -1*obj.vel[0]
                        obj.vel[1] = -1*obj.vel[1]
                        enemy_missile_group.remove(obj)
                        arrow_group.add(obj)
                    elif(obj.vel[1]<0 and link.orientation=="Down"):
                        obj.vel[0] = -1*obj.vel[0]
                        obj.vel[1] = -1*obj.vel[1]
                        enemy_missile_group.remove(obj)
                        arrow_group.add(obj)
                    else:
                        grunt_sound.play()
                        link.collidable = False
                        lives-=1
                        if(lives>0):

                            invincibility_timer.start()

                    if( obj in enemy_missile_group):

                        enemy_missile_group.remove(obj)

                    for obj in level_grid.get_collidables(link):
                        if(obj.collide(link) and obj in walls):
                            print "reset position"
                            link.pos = original_pos
                            break               
                    link.vel=[0,0]


                elif(obj in stairs):

                    for stair in stairs:
                         level_grid.remove_entity(stair)
                    stairs = set([])
                    arrow_count += 10
                    if(arrow_count>30):
                        arrow_count = 30
                    lives += 3
                    if(lives>10):
                        lives =10
                    map_position +=1 
                    level +=1 
                    spawn_level_by_position(map_position)
                elif(obj in trophies):
                    link.collidable = False
                    link.controllable = False
                    trophies = set([])
                    link.image_size = [37, 66]
                    link.image_center = [503, 322]
                    canvas.draw_text("YOU WIN!!!", (200, 200), 40, 'Red')
                    canvas.draw_text("Returning to main menu in "+ str(death_counter), (250, 250), 30, 'Red')
                    if(timer_death.is_running()==False):
                        timer_death.start()

        enemies_copy = enemies.copy() 
        octorok_index = time%OCTOROK_DIM//1

        for enemy in enemies_copy:
            if(enemy.enemy_type == "red_octorok" or enemy.enemy_type == "blue_octorok"):
                enemy.image_center[1] = enemy.image_center[1] + octorok_index*78
                if(octorok_index == 0):
                    enemy.image_size = [40, 40]
                elif(octorok_index == 1):
                    if(enemy.orientation =="Up" or enemy.orientation=="Down"):
                        enemy.image_size[1] = 47
                    else:
                        enemy.image_size[0] = 47
            else:
                enemy.image_center[1] = enemy.image_center[1] + octorok_index*78
            enemy.draw(canvas)
            enemy.image_center[1] = enemy.image_center[1] - octorok_index*78

            level_grid.remove_entity(enemy)
            for obj in level_grid.get_collidables(enemy):
                if (obj.collide(enemy) and obj in walls):
                    enemy.pos[0] = enemy.pos[0] -2*enemy.vel[0]
                    enemy.pos[1] = enemy.pos[1] -2*enemy.vel[1]

                    #enemy.vel[0]= -1* enemy.vel[0]
                    #enemy.vel[1]= -1* enemy.vel[1]
                    if(enemy.orientation == "Left"):
                        enemy.set_orientation("Right")  
                    elif(enemy.orientation == "Right"):
                        enemy.set_orientation("Left")
                    elif(enemy.orientation == "Down"):
                        enemy.set_orientation("Up")
                    elif(enemy.orientation == "Up"):
                        enemy.set_orientation("Down")
                    enemy.update()

                    break
            for obj in level_grid.get_collidables(enemy):
                if (obj.collide(enemy) and obj in arrow_group):
                    score += 50
                    arrow_impact_sound.play()

                    if(enemy in enemies):
                        enemies.remove(enemy)
                    arrow_group.remove(obj)
                    level_grid.remove_entity(enemy)
            if(enemy in enemies):
                enemy.update()
                level_grid.add_entity(enemy)
            if(enemy.lifespan != None and enemy.lifespan<=enemy.age):
                if(enemy in enemies):
                        enemies.remove(enemy)
                level_grid.remove_entity(enemy)    

        for enemy_missile in enemy_missile_group:
            enemy_missile.image_center[1] = enemy_missile.image_center[1] + octorok_index*78

            enemy_missile.draw(canvas)
            enemy_missile.image_center[1] = enemy_missile.image_center[1] - octorok_index*78


            level_grid.remove_entity(enemy_missile)
            enemy_missile.update()
            level_grid.add_entity(enemy_missile)
            for obj in level_grid.get_collidables(enemy_missile):
                if(obj.collide(enemy_missile) and obj in walls):
                    if(enemy_missile in enemy_missile_group):
                        enemy_missile_group.remove(enemy_missile)

                        level_grid.remove_entity(enemy_missile)
            if(enemy_missile.lifespan != None and enemy_missile.lifespan<=enemy_missile.age):
                if(enemy_missile in enemy_missile_group):
                        enemy_missile_group.remove(enemy_missile)
                level_grid.remove_entity(enemy_missile)                
        if(map_position ==4 or map_position == 7):
             if(len(enemies) ==0 ):
                stair = Sprite([FRAME_WIDTH/2, FRAME_HEIGHT/2], 0, [0, 0], stair_image, stair_info)
                while(True):
                    if(enemy_wall_collide(stair)):
                        posx= random.randrange(100, FRAME_WIDTH-100)
                        posy= random.randrange(100, FRAME_HEIGHT-100)
                        stair.pos = [posx, posy]
                    else:
                        break

                stairs.add(stair)
                level_grid.add_entity(stair)
    if(map_position == 10 and len(enemies)==0):
            trophy = Sprite([FRAME_WIDTH/2, FRAME_HEIGHT/2], 0, [0, 0], trophy_image, trophy_info)
            trophies.add(trophy)
            level_grid.add_entity(trophy)

    if(lives <= 0):
            canvas.draw_text("GAME OVER", (200, 200), 40, 'Red')
            canvas.draw_text("Returning to main menu in "+ str(death_counter), (250, 250), 30, 'Red')
            link.image_center = [137, 303]
            link.image_size[0]=36
            link.controllable = False
            link.collidable = False
            if(timer_death.is_running()==False):
                timer_death.start()
               
    if(in_play):
        time += 0.1
        canvas.draw_text("Health: ", (50, 100), 25, 'Red')  
        canvas.draw_image(heart_image, heart_info.get_center(), heart_info.get_size(), (150, 95), heart_info.get_size())
        canvas.draw_text("x"+str(lives), (175, 100), 25, 'Red')
        
        canvas.draw_text("Arrows: ", (250, 95), 25, 'Red')    
        canvas.draw_image(missile_image, missile_info.get_center(), missile_info.get_size(), (350, 90), missile_info.get_size())
        canvas.draw_text("x"+str(arrow_count), (370, 100), 25, 'Red')
        canvas.draw_text("Score: "+ str(score), (450, 100), 25, 'Red')
    if(in_play == False):
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [FRAME_WIDTH / 2, FRAME_HEIGHT / 2], 
                          splash_info.get_size())
    if(in_score):
        Y=300
        scores.sort()
        if(len(scores)==0):
            canvas.draw_text("No scores available", (200, 300), 35, 'Red')

        for x in range(0, 3):
            if(x<len(scores)):
                canvas.draw_text(str(scores[x][1])+":                  "+ str(scores[x][0]), (100, Y), 35, 'Red')
                Y+=60

                
# Create a frame and assign callbacks to event handlers
def projectile_timer():
    for enemy in enemies:
        if(enemy.missile):
            enemy.shoot()
    
def enemy_movement_timer():
    for enemy in enemies:
        if(enemy_wall_collide(enemy) == False):
            orientation = random.choice(["Up", "Down", "Left", "Right"])
            enemy.set_orientation(orientation)    
        
        
def invincibility_handler():
    global link, hit_counter, name
    hit_counter +=1
    link.collidable = False
    link.controllable = False
    if(hit_counter%2 == 0):
        link.drawable =False
    else:
        link.drawable = True
        
    if(hit_counter >= 6):
        link.collidable = True
        link.controllable = True
        link.drawable = True
        hit_counter = 0
 
        invincibility_timer.stop()
        if("a" in key_down):
            link.vel[0] -= 5
            link.set_orientation("Left")
        if("w" in key_down):
            link.vel[1] -= 5    
            link.set_orientation("Up")
        if("s" in key_down):
            link.vel[1] += 5
            link.set_orientation("Down")
        if("d" in key_down):
            link.vel[0] += 5    
            link.set_orientation("Right")
def death_timer():
    global link, death_counter, in_play, lives, name, scores
    death_counter -= 1
    if(death_counter ==0):
        timer_death.stop()
        soundtrack.rewind()
        battle_sound_timer.stop()
        title_sound.play()
        title_sound_timer.start()
        lives = 2
        scores.append((score, name))
        name = ""
        in_play = False

def timer_wizz():
    global enemies
    for enemy in enemies:
        if(enemy.enemy_type == "wizzrope"):
            lx = link.pos[0]
            ly = link.pos[1]
            posx = random.choice([random.randrange(lx-80,lx-link.image_size[0]/2), 
                                 random.randrange(lx+link.image_size[0]/2, lx+80),
                                 ])
            posy = random.choice([random.randrange(ly-80, ly-link.image_size[1]/2),
                                 random.randrange(ly+link.image_size[1]/2, ly+80)])
            fire = Sprite([posx, posy], 0, [0, 0], enemy_image, fireball_info)
            while(True):
                if(enemy_wall_collide(fire)):
                    posx = random.choice([random.randrange(lx-80,lx-link.image_size[0]/2), 
                                 random.randrange(lx+link.image_size[0]/2, lx+80),
                                 ])
                    posy = random.choice([random.randrange(ly-80, ly-link.image_size[1]/2),
                                 random.randrange(ly+link.image_size[1]/2, ly+80)])
                    fire.pos = [posx, posy]
                else:
                    break
            fire.set_orientations(fireball_orientations)
            fire.set_orientation("Down")
            fire.set_lifespan(40)
            enemy_missile_group.add(fire)
            
def timer_battle_sound():
    soundtrack.rewind()
    soundtrack.play()

def timer_title_sound():
    title_sound.rewind()
    title_sound.play()
def mouse_handler(position):
    global in_name, in_play, in_score, in_how_to, splash_image
    pos = {}
    pos[0] = position[0]
    pos[1] = position[1]+splash_info.get_size()[1]/2-FRAME_HEIGHT/2
    start_size = [236, 70]
    how_to_size = [280, 50]
    score_size = [307,49]
    back_size = [120, 46]
    begin_size =[240, 59]
    name_size = [241, 48]
    
    start_center = [314, 144]
    how_to_center = [317, 220]
    score_center = [326, 286] 
    back_center = [60, 350]
    begin_center = [561, 365]
    name_center = [571, 350]
    
    instartwidth = (start_center[0] - start_size[0] / 2) < pos[0] < (start_center[0] + start_size[0] / 2)
    instartheight = (start_center[1] - start_size[1] / 2) < pos[1] < (start_center[1] + start_size[1] / 2)
  
    
    inhowtowidth = (how_to_center[0] - how_to_size[0] / 2) < pos[0] < (how_to_center[0] + how_to_size[0] / 2)
    inhowtoheight = (how_to_center[1] - how_to_size[1] / 2) < pos[1] < (how_to_center[1] + how_to_size[1] / 2)
    
    inscorewidth = (score_center[0] - score_size[0] / 2) < pos[0] < (score_center[0] + score_size[0] / 2)
    inscoreheight = (score_center[1] - score_size[1] / 2) < pos[1] < (score_center[1] + score_size[1] / 2)

    inbackwidth = (back_center[0] - back_size[0] / 2) < pos[0] < (back_center[0] + back_size[0] / 2)
    inbackheight = (back_center[1] - back_size[1] / 2) < pos[1] < (back_center[1] + back_size[1] / 2)
    
    innamewidth = (name_center[0] - name_size[0] / 2) < pos[0] < (name_center[0] + name_size[0] / 2)
    innameheight = (name_center[1] - name_size[1] / 2) < pos[1] < (name_center[1] + name_size[1] / 2)
    
    if(not in_play):
        if(instartwidth and instartheight and in_score==False and in_how_to==False):
            #print "start game"
            splash_image = enter_image
            in_name = True
            #in_play = True
            #new_game()
            
        elif(inhowtowidth and inhowtoheight and not in_score and not in_how_to and not in_name):
            splash_image = how_to_image
            in_how_to = True
        elif(inscorewidth and inscoreheight and not in_score and not in_how_to):
            splash_image = score_image
            in_score = True
        elif(innamewidth and innameheight and in_name):
            if(len(name)>0):
               
                splash_image=simplegui.load_image("https://dl.dropboxusercontent.com/s/99r0hcnjm3zc5oa/splash_screen.jpg?dl=0")
                in_name = False
                in_play = True
                new_game()
        elif(inbackwidth and inbackheight):
            splash_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/99r0hcnjm3zc5oa/splash_screen.jpg?dl=0")
            in_score = False
            in_how_to = False
            in_name = False
            
def button_click():
    global in_play
    in_play = False
invincibility_timer = simplegui.create_timer(300, invincibility_handler)
movement_timer = simplegui.create_timer(3000, enemy_movement_timer)
timer = simplegui.create_timer(2500, projectile_timer)
timer_death = simplegui.create_timer(1000, death_timer)
wizz_timer = simplegui.create_timer(2000, timer_wizz)
battle_sound_timer = simplegui.create_timer(50000, timer_battle_sound)
title_sound_timer = simplegui.create_timer(17000, timer_title_sound)
frame = simplegui.create_frame("Home", FRAME_WIDTH, FRAME_HEIGHT)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.add_button("New Game", button_click)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)
frame.set_canvas_background('Olive')
#new_game()
timer.start()
movement_timer.start()
wizz_timer.start()
#invincibility_timer.start()        

title_sound.play()
title_sound_timer.start()

# Start the frame animation
frame.start()
