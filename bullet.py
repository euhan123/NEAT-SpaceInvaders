<<<<<<< HEAD
import pygame
from pygame.sprite import Sprite

class Bullet (Sprite):

    def __init__(self, settings, screen, player):
        #Create the bullet
        super(Bullet, self).__init__()
        self.screen = screen

        #Create it at the correct place
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top

        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        #Move the bullet up
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
=======
import pygame
from pygame.sprite import Sprite

class Bullet (Sprite):

    def __init__(self, settings, screen, player):
        #Create the bullet
        super(Bullet, self).__init__()
        self.screen = screen

        #Create it at the correct place
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = player.rect.centerx
        self.rect.top = player.rect.top

        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        #Move the bullet up
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
>>>>>>> ec864d9e9c23be92f14208068a8f5402385db9d7
        pygame.draw.rect(self.screen, self.color, self.rect)