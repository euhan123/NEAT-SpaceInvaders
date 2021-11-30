import pygame, random
import os
import neat
import sys
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
FONT = pygame.font.Font('./flappy.ttf', 144)
pygame.display.set_caption("Space Invaders")


#add shooting sound
#add point sound (a.k.a. enemies being destroyed)

def fitness(i, genomes, player, nets, score):
    genomes[i].fitness += score
    #player.pop(i)
    #genomes.pop(i)
    #nets.pop(i)

def eval_genomes(genomes, config):
    player = []
    run = True
    clock = pygame.time.Clock()

    game = Game(settings)

    #bg = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
    #bg_color = (230, 230, 230)

    #Store bullets in a group
    bullets = Group()

    #Store enemies in a group
    enemies = Group()

    #Set up genomes and neural nets
    ge = []
    nets = []

    for genome_id, genome in genomes:
        ship = Player(settings, SCREEN, genome_id)
        player.append(ship)
        ge.append(genome)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

    for i, ship in enumerate(player):
        settings.__init__()
        game.__init__(settings)
        bullets = Group()
        enemies = Group()
        
        #Initialize score
        score = Scoreboard(settings, SCREEN, game)


        run = True
        game.game_active = True
        gf.create_enemies(settings, SCREEN, ship, enemies)
        
        while run:

            lowest = SCREEN.get_height()
            left = SCREEN.get_width()
            right = 0
            num_of_enemies = 0
            for alien in enemies.sprites():
                if alien.rect.bottom < lowest:
                    lowest = alien.rect.bottom
                if alien.rect.left < left:
                    left = alien.rect.left
                if alien.rect.right > right:
                    right = alien.rect.right
                num_of_enemies += 1
            
            #gf.check_events(settings, SCREEN, player, bullets)

            output = nets[i].activate((lowest - ship.rect.top, num_of_enemies, left, right)) 
            print(output)
            if (output[0] > 0.5):
                gf.fire_bullets(settings, SCREEN, ship, bullets)
            if (output[1] < 0.5):
                ship.moving_right = True
                ship.moving_left = False
            else:
                ship.moving_right = False
            if (output[2] > 0.5):
                ship.moving_left = True
                ship.moving_right = False
            else:
                ship.moving_left = False
            if (output[1] > 0.5 and output[2] > 0.5):
                ship.moving_right = False
                ship.moving_left = False

            if game.game_active:
                ship.update()
                gf.update_bullets(settings, SCREEN, game, score, ship, enemies, bullets)
                gf.update_aliens(settings, game, SCREEN, ship, enemies, bullets)
                if pygame.sprite.spritecollideany(ship, enemies) or gf.check_aliens_bottom(settings, game, SCREEN, ship, enemies, bullets):
                    print("HIT!")
                    fitness(i, ge, player, nets, game.score)
                    run = False
                    game.game_active = False
            
            gf.update_screen(settings, SCREEN, ship, score, enemies, bullets)

        i += 1
        bullets.empty()
        enemies.empty()


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    pop = neat.Population(config)
    pop.run(eval_genomes, 100)


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        local_dir = os.path.dirname(sys.executable)
    elif __file__:
        local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)