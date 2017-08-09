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
                self.jumping = False

                self.level = None

                sprite_sheet = SpriteSheet("megaman_walk.png")\

                #Posiciones cuando esta parado
                self.standing_right = sprite_sheet.get_image(4, 0, 46, 47)
                image = sprite_sheet.get_image(4, 0, 46, 47)
                image = pygame.transform.flip(image, True, False)
                self.standing_left = image


                #Posiciones cuando salta

                self.jumping_right = sprite_sheet.get_image(287, 0,  53, 59)

                image = sprite_sheet.get_image(287, 0,  53, 59)
                image = pygame.transform.flip(image, True, False)
                self.jumping_left = image

                #Carga todas los sprites que van hacia la derecha en una lista

                #Primera imagen posicion parado
                # image = sprite_sheet.get_image(0, 0, 58, 47)
                # self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(0, 96, 48, 48)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(102, 96, 32, 48)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(190, 96, 42, 48)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(102, 96, 32, 48)
                self.walking_frames_r.append(image)

                # image = sprite_sheet.get_image(66, 93, 66, 90)
                # self.walking_frames_r.append(image)

                # image = sprite_sheet.get_image(132, 93, 72, 90)
                # self.walking_frames_r.append(image)

                # image = sprite_sheet.get_image(0, 186, 70, 90)
                # self.walking_frames_r.append(image)


                #Cargar todos los sprites que van a la izquierda

                #Imagen parado viendo izquierda
                # image = sprite_sheet.get_image(0, 0, 58, 47)
                # image = pygame.transform.flip(image, True, False)
                # self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(0, 96, 48, 48)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(102, 96, 32, 48)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(190, 96, 42, 48)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(102, 96, 42, 48)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                # image = sprite_sheet.get_image(66, 93, 66, 90)
                # image = pygame.transform.flip(image, True, False)
                # self.walking_frames_l.append(image)

                # image = sprite_sheet.get_image(132, 93, 72, 90)
                # image = pygame.transform.flip(image, True, False)
                # self.walking_frames_l.append(image)

                # image = sprite_sheet.get_image(0, 186, 70, 90)
                # image = pygame.transform.flip(image, True, False)
                # self.walking_frames_l.append(image)

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

                #         self.jumping = Fal



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
                                # frame = (pos // 20) % len(self.walking_frames_r)
                                # self.image = self.walking_frames_r[frame]

                        # if self.change_y > 0 and self.direction =="L":
                        #         self.rect.bottom = block.rect.top
                                # self.image = self.standing_left

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

                                self.rect.y += block.change_y
                                self.change_y = 0

        def calc_grav(self):
                if self.change_y == 0:
                        self.change_y = 1
                else:
                        self.change_y += .35

                if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y > 0:
                        self.change_y = 0
                        self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

        def jump(self):

                self.rect.y += 2
                platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                self.rect.y -=2

                # if not platform_hit_list or self.rect.bottom >= constants.SCREEN_HEIGHT:
                #         self.jumping = True

                if len (platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
                        self.change_y = -10

                        # self.jumping = True

                        # # while self.jumping:
                        # if self.direction == "R":
                        #         self.image = self.jumping_right

                        #         elif self.direction == "L":
                        #                 self.image = self.jumping_left

                        #         self.jumping = False

        # def stop_jump(self):
        #         self.change_y = 0

        def go_left(self):
                self.change_x = -16
                self.direction = "L"

        def go_right(self):
                self.change_x = 16
                self.direction = "R"

        def stop(self):
                self.change_x = 0



