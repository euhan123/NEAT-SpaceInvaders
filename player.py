import pygame

class Player:
    IMAGE = pygame.image.load("images/ship.PNG")

    def __init__(self, settings, screen, number):
        self.number = number
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('images/ship.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()/10, self.image.get_height()/10))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        #Update ship's position
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.settings.ship_speed_factor
    
    def draw(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx