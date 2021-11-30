import pygame
import os
from settings import Settings
from player import Player
from enemy import Enemy
from game import Game
from scoreboard import Scoreboard
from pygame.sprite import Group
import game_functions as gf


pygame.init()
settings = Settings()
SCREEN = pygame.display.set_mode((settings.screen_width, settings.screen_height))
FONT = pygame.font.Font("freesansbold.ttf", 72)
pygame.display.set_caption("Space Invaders")

#add shooting sound
#add point sound (a.k.a. enemies being destroyed)

def main():
    run = True
    clock = pygame.time.Clock()

    game = Game(settings)

    #bg = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
    #bg_color = (230, 230, 230)

    #Initialize player
    player = Player(settings, SCREEN, 0)

    #Store bullets in a group
    bullets = Group()

    #Store enemies in a group
    enemies = Group()

    #Initialize score
    score = Scoreboard(settings, SCREEN, game)

    gf.create_enemies(settings, SCREEN, player, enemies)

    while run:
        
        gf.check_events(settings, SCREEN, player, bullets)

        if game.game_active:
            player.update()
            gf.update_bullets(settings, SCREEN, game, score, player, enemies, bullets)
            gf.update_aliens(settings, game, SCREEN, player, enemies, bullets)
            
        else:
            run = False
            
        gf.update_screen(settings, SCREEN, player, score, enemies, bullets)
            

if __name__ == "__main__":
    main()