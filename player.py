import pygame
import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet


class Player(pygame.sprite.Sprite):

        def __init__(self):
                super().__init__()

                self.change_x = 0
                self.change_y = 0

                self.walking_frames_l = []
                self.walking_frames_r = []


                self.direction = "R"

                self.level = None

                sprite_sheet = SpriteSheet("cipitio.png")

                """Posiciones cuando está parado"""
                self.standing_right = sprite_sheet.get_image(0, 0, 59, 69)
                image = sprite_sheet.get_image(0, 0, 59, 69)
                image = pygame.transform.flip(image, True, False)
                self.standing_left = image

                """Posiciones cuando salta"""

                self.jumping_right = sprite_sheet.get_image(250, 0,  58, 88)

                image = sprite_sheet.get_image(250, 0,  58, 88)
                image = pygame.transform.flip(image, True, False)
                self.jumping_left = image

                """Carga todas los sprites que van hacia la derecha en una lista"""

                image = sprite_sheet.get_image(64, 0, 57, 69)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(126, 0, 57, 69)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(188, 0, 57, 69)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(126, 0, 57, 69)
                self.walking_frames_r.append(image)

                #Cargar todos los sprites que van hacia la izquierda

                image = sprite_sheet.get_image(64, 0, 57, 69)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(126, 0, 57, 69)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(188, 0, 57, 69)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(126, 0, 57, 69)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                self.image = self.walking_frames_r[0]

                self.rect = self.image.get_rect()

        def update(self):

                self.calc_grav()

                self.rect.x += self.change_x
                pos = self.rect.x + self.level.world_shift

                if self.direction == "R" and self.change_x == 0:
                        self.image = self.standing_right

                if self.direction == "R" and self.change_x > 0:
                        frame = (pos // 20) % len(self.walking_frames_r)
                        self.image = self.walking_frames_r[frame]

                if self.direction == "L" and self.change_x == 0:
                        self.image = self.standing_left

                if self.direction == "L" and self.change_x < 0:
                        frame = (pos // 20) % len(self.walking_frames_l)
                        self.image = self.walking_frames_l[frame]

                if self.direction == "R" and self.change_y !=0:
                        self.image = self.jumping_right

                if self.direction == "L" and self.change_y !=0:
                        self.image = self.jumping_left


                block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                for block in block_hit_list:
                        if self.change_x > 0:
                                self.rect.right = block.rect.left
                        elif self.change_x < 0:
                                self.rect.left = block.rect.right


                self.rect.y += self.change_y

                block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                for block in block_hit_list:

                        if self.change_y > 0:
                                self.rect.bottom = block.rect.top

                        elif self.change_y < 0:
                                self.rect.top = block.rect.bottom

                        self.change_y = 0

                        if self.change_y == 0 and self.direction=="R":
                                if  self.change_x == 0:
                                        self.image = self.standing_right
                                else:
                                        frame = (pos // 20) % len(self.walking_frames_r)
                                        self.image = self.walking_frames_r[frame]

                        if self.change_y == 0 and self.direction=="L":
                                if  self.change_x == 0:
                                        self.image = self.standing_left
                                else:
                                        frame = (pos // 20) % len(self.walking_frames_r)
                                        self.image = self.walking_frames_l[frame]

                        if isinstance(block, MovingPlatform):
                                self.rect.x += block.change_x

                                self.change_y += 8

        def calc_grav(self):
                if self.change_y == 0:
                        self.change_y = 2
                else:
                        self.change_y += 3

        def jump(self):

                self.rect.y += 9
                platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                self.rect.y -= 9

                if len (platform_hit_list) > 0:
                        self.change_y = -35

        def go_left(self):
                self.change_x = -8
                self.direction = "L"

        def go_right(self):
                self.change_x = 8
                self.direction = "R"

        def stop(self):
                self.change_x = 0
