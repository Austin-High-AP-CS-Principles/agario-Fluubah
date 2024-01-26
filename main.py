'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''
global debug
debug=False
import math
import pygame
import sys
import random
# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agar.io")
font = pygame.font.Font('NimbusSanL-Reg.otf', 10)
Bfont = pygame.font.Font('NimbusSanL-Reg.otf', 50)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Enemy, self).__init__()
        self.x = random.randint(0,650)
        self.y = random.randint(0,500)
        self.radius = random.randint(20, 50)
        self.color = color
        self.speed = 100
        self.sizeSpeed = (1/self.radius) * self.speed

        self.x_heading = 1
        self.y_heading = 1

        self.image = pygame.Surface((self.radius*2, self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (self.x,self.y))
        #self.rect.x = self.x
        #self.rect.y = self.y

    def move(self):

        if self.rect.centerx <= -0 or self.rect.centerx >= 800:
            self.x_heading *= -1
        if self.rect.centery <= 0 or self.rect.centery >= 600:
            self.y_heading *= -1
       
        self.rect.x += self.x_heading * self.sizeSpeed
        print("im an enemy moving: ",self.x_heading*self.sizeSpeed)
        self.rect.y += self.y_heading * self.sizeSpeed

    def grow(self,amount):
        '''
        pwidth = self.rect.width
        pheight = self.rect.height
        self.image = pygame.transform.scale(self.image, (pwidth+amount, pheight+amount))
        self.rect.inflate_ip(amount,amount)
        '''
       
       
        self.rect.inflate(amount,amount)
        pos = self.rect.center
        self.radius += amount
        self.image = pygame.Surface((self.radius*2, self.radius*2),pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.sizeSpeed = (1/self.radius) * self.speed
       
        if(self.rect.x-self.radius <= -0):
            self.rect.x + self.radius*2
        #x_sign = (self.x_heading/abs(self.x_heading))
        #y_sign = (self.y_heading/abs(self.y_heading))
        #print(str(1/self.radius)+ " is multiplied by",self.speed," and then multiplied by",x_sign)
        #self.x_heading = (1/self.radius) * self.speed * x_sign
        #self.y_heading = (1/self.radius) * self.speed * y_sign
        #print(str(self.x_heading))
        #self.x_heading = 0.1 if self.x_heading < 0.1 else self.x_heading
        #self.y_heading = 0.1 if self.y_heading < 0.1 else self.y_heading

       
    def collision_detector(self):
        for collidable in edible:
            x,y = self.rect.center
            ex,ey = collidable.rect.center

            if(math.dist((x,y),(ex,ey)) < collidable.radius+self.radius and collidable != self and collidable.radius < self.radius):
                self.grow(collidable.radius)
                collidable.kill()
class Food(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, color):
        super(Food, self).__init__() #Calling the constructor
        self.color = color
        self.radius = 10
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (self.radius,self.radius), self.radius)
        self.rect = self.image.get_rect(center = (random.randint(10,790), random.randint(10,590)))



class Player(Enemy):
    def __init__(self,color):
        super().__init__(color)
        self.color=color
        self.image=self.image.convert_alpha()
        self.rect=self.image.get_rect(center=(100,100))
        self.pos = pygame.Vector2(100,100)

class Player(Enemy):
    def __init__(self, color):
        super(Player, self).__init__(color=color)
        self.color = (0,0,0)
        self.rect = self.image.get_rect(center = (100, 100))
        self.pos = pygame.Vector2(100,100)
   
    def playerMove(self):
        global debug
        dest_x,dest_y = pygame.mouse.get_pos()
        mouse_pos = pygame.math.Vector2(dest_x,dest_y)
        direction = mouse_pos - self.rect.center

        try:
            velocity = direction.normalize()
        except:
            velocity = (0,0)
        #movement_v = self.direction * velocity
        velocityf = (float(velocity[0])* float((1/self.radius) * self.speed),float(velocity[1])* float((1/self.radius) * self.speed))
       
        self.pos += velocityf

        rise=self.rect.centerx-dest_x
        run=self.rect.centery-dest_y
        distance=int(math.sqrt(rise**2+run**2))
        if debug:
            pygame.draw.line(screen, (255,0,0), (self.rect.center), (dest_x, dest_y))
            pygame.draw.line(screen, (0,255,0), (self.rect.center), (self.rect.centerx, dest_y))
            pygame.draw.line(screen, (0,0,255), (dest_x,dest_y), (self.rect.centerx, dest_y))

            text = str(distance)
            text = font.render(text, True, (255,0,0))
            screen.blit(text, ((self.rect.centerx+dest_x)/2, (self.rect.centery+dest_y)/2))

            text = str(run)
            text = font.render(text, True, (0,255,0))
            screen.blit(text, ((self.rect.centerx, (self.rect.centery+dest_y)/2)))

            text = str(rise)
            text = font.render(text, True, (0,0,255))
            screen.blit(text, ((self.rect.centerx+dest_x)/2, dest_y))
        else:
            pass

        pygame.display.flip()

        self.rect=self.image.get_rect(center=(self.pos))




# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create clock to later control frame rate
clock = pygame.time.Clock()

enemies=pygame.sprite.Group()
edible = pygame.sprite.Group()
players = pygame.sprite.Group()
players.add(Player("Black"))
foods = pygame.sprite.Group()

for num in range(3):
    enemyColor = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
    enemies.add(Enemy(enemyColor))

for num in range(0,20):
    mealColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    foods.add(Food(mealColor))

edible.add(foods)
edible.add(enemies)
edible.add(players)
playerinvince=60*2
e=0
# Main game loop
running = True
while running:
    if playerinvince>0:
        playerinvince-=1
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)

    foods.draw(screen)
    enemies.draw(screen)

    players.draw(screen)

    for enemy in enemies:
        enemy.move()
        if playerinvince<1:
            enemy.collision_detector()

    for player in players:
        player.playerMove()
        if playerinvince<1:
            player.collision_detector()

    if e>0:
        e-=1
    # Update the display
    keys=pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and e<1:
        if debug == False:
            e=20
            debug=True
        elif debug:
            e=20
            debug=False
    if len(enemies)==0:
        text = str("You win!")
        text = Bfont.render(text, True, (0,255,0))
        screen.blit(text, (250, 250))
    elif len(players)==0:
        text = str("You lost")
        text = Bfont.render(text, True, (255,0,0))
        screen.blit(text, (250, 250))
    pygame.display.flip()
    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
