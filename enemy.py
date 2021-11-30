import pygame
from pygame.sprite import Sprite

class Enemy (Sprite):
    def __init__(self, settings, screen):
        super(Enemy, self).__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load('images/enemy.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()/10, self.image.get_height()/10))
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        #Move the aliens left/right
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        #Check if an alien hit an edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False
