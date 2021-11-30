import sys
import pygame
from bullet import Bullet
from enemy import Enemy
from time import sleep

def check_keydown_events(event, settings, SCREEN, player, bullets):
    #Move ship left and right
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(settings, SCREEN, player, bullets)

def check_keyup_events(event, player):
    #Stop moving the ship
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False

def check_events(settings, screen, player, bullets):
    #Respond to key presses and mouse activities
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, player, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)

def update_screen(settings, screen, player, score, alien, bullets):
    #Update images on the screen
    screen.fill(settings.bg_color)
    player.draw()
    alien.draw(screen)
    for bullet in bullets:
        bullet.draw()
    score.display()
    pygame.display.update()

def update_bullets(settings, screen, game, score, player, aliens, bullets):
    #Update and remove bullets
    bullets.update()
    for bullet in bullets.copy():
        if (bullet.rect.bottom <= 0):
            bullets.remove(bullet)
    check_bullet_alien_collision(settings, screen, game, score, player, aliens, bullets)
    
def check_bullet_alien_collision(settings, screen, game, score, player, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in collisions.values():
            game.score += settings.alien_points * len(alien)
            score.prep_score()

    if (len(aliens) == 0):
        bullets.empty()
        settings.increase_speed()
        create_enemies(settings, screen, player, aliens)
        player.center_ship()

def fire_bullets(settings, screen, player, bullets):
    #Fire bullets
    if (len(bullets) < settings.bullets_allowed):
        new_bullet = Bullet(settings, screen, player)
        bullets.add(new_bullet)

def get_num_aliens_x(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2*alien_width))
    return number_of_aliens_x

def create_alien(settings, screen, enemies, number, row_number):
    alien = Enemy(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2* alien_width * number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    enemies.add(alien)

def get_rows(settings, player_height, alien_height):
    available_space_y = (settings.screen_height - (3*alien_height) - player_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_enemies(settings, SCREEN, player, enemies):
    #Create a fleet of aliens
    alien = Enemy(settings, SCREEN)
    number_of_aliens_x = get_num_aliens_x (settings, alien.rect.width)
    number_rows = get_rows(settings, player.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for number in range(number_of_aliens_x):
            create_alien(settings, SCREEN, enemies, number, row_number)

def ship_hit(settings, game, screen, player, aliens, bullets):
    if (game.player_left > 1):
        #Ship being hit by alien
        game.player_left -= 1

        #Reset the aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create new fleet and ship
        create_enemies(settings, screen, player, aliens)
        player.center_ship()

        #Pause
        sleep(0.5)
    
    else:
        game.game_active = False

def check_aliens_bottom(settings, game, screen, player, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #ship_hit(settings, game, screen, player, aliens, bullets)
            return True

def update_aliens(settings, game, screen, player, aliens, bullets):
    #Make the aliens move
    check_fleet_edge(settings, aliens)
    aliens.update()

    #if pygame.sprite.spritecollideany(player, aliens):
    #    ship_hit(settings, game, screen, player, aliens, bullets)
    
    check_aliens_bottom(settings, game, screen, player, aliens, bullets)

def check_fleet_edge(settings, aliens):
    #Check if the aliens have hit the edge
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(settings, aliens)
            break
    
def change_fleet_direction(settings, aliens):
    #Change the fleet direction
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1
