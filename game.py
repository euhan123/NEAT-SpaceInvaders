import pygame

class Game:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats(settings)
        self.game_active = True
        self.score = 0

    def reset_stats(self, settings):
        self.player_left = self.settings.player_limit
        self.score = 0
        self.settings = settings
