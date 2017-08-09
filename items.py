import pygame
import levels

from spritesheet_functions import SpriteSheet


class Banana(pygame.sprite.Sprite):

        def __init__(self):
                super().__init__()

                sprite_sheet = SpriteSheet("banana.png")
                self.image = sprite_sheet.get_image(0, 0, 56, 86)
                # self.image = sprite_sheet.get_image(0, 0, x, y)
                self.rect = self.image.get_rect()

                self.level_item = None
                self.player = None
                self.level_score = 0
