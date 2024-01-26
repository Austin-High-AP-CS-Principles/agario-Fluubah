'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Enemy, self).__init__()
        self.x = random.randint(150,500)
        self.y = random.randint(150,400)
        self.radius = random.randint(20,150)

        self.color = color
        self.speed=100

        self.x_heading = (1/self.radius) * self.speed
        self.y_heading = (1/self.radius) * self.speed

        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y





    def move(self):
        if self.rect.left <= -0 or self.rect.right >= 800:
            self.x_heading *= -1
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.y_heading *= -1
                    

        self.rect.x += self.x_heading
        self.rect.y += self.y_heading



class Player(Enemy):
    def __init__(self,color):
        super().__init__(color)
        self.color=color
        self.image=self.image.convert_alpha()
        self.rect=self.image.get_rect(center=(100,100))
        self.pos = pygame.Vector2(100,100)

    def playerMove(self):
        dest_x,dest_y=pygame.mouse.get_pos()
        mouse_pos = pygame.math.Vector2(dest_x,dest_y)
        direction=mouse_pos-self.rect.center

        rise=self.rect.centerx-dest_x
        run=self.rect.centery-dest_y
        distance=int(math.sqrt(rise**2+run**2))
        try:
            velocity = direction.normalize()
        except:
            velocity = (0,0)

        self.pos+=velocity


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


        pygame.display.flip()

        self.rect=self.image.get_rect(center=(self.pos))




# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create clock to later control frame rate
clock = pygame.time.Clock()

enemies=pygame.sprite.Group()

for num in range(3):
    enemyColor = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
    enemies.add(Enemy(enemyColor))

players = pygame.sprite.Group()
players.add(Player("Black"))

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)
    enemies.draw(screen)
    players.draw(screen)

    for enemy in enemies:
        enemy.move()

    for player in players:
        player.playerMove()
    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
