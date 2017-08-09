import pygame
import levels

from spritesheet_functions import SpriteSheet


class Enemy(pygame.sprite.Sprite):

        def __init__(self):
                super().__init__()

                self.boundary_top = 0
                self.boundary_bottom = 0
                self.boundary_left = 0
                self.boundary_right = 0

                self.change_x = 6
                self.change_y = 0


                self.walking_frames_l = []
                self.walking_frames_r = []

                self.direction = "R"

                self.level = None
                self.player = None

                """Carga la hoja del spritesheet  en el sprite"""
                sprite_sheet = SpriteSheet("enemy.png")

                """Posiciones caminando hacia la derecha"""
                image = sprite_sheet.get_image(0, 0, 35, 52)
                self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(45, 0, 38, 52)
                self.walking_frames_r.append(image)

                # image = sprite_sheet.get_image(0, 0, 35, 52)
                # self.walking_frames_r.append(image)

                image = sprite_sheet.get_image(136, 0, 51, 52)
                self.walking_frames_r.append(image)

                """Posiciones caminando hacia la izquierda"""
                image = sprite_sheet.get_image(0, 0, 35, 52)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(45, 0, 38, 52)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                # image = sprite_sheet.get_image(0, 0, 35, 52)
                # image = pygame.transform.flip(image, True, False)
                # self.walking_frames_l.append(image)

                image = sprite_sheet.get_image(136, 0, 51, 52)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_l.append(image)

                self.image = self.walking_frames_r[0]
                self.rect = self.image.get_rect()



                # def update(self):
                #         self.rect.x += self.change_x
                #         # range = self.rect.x + self.boundary_right - self.boundary_right

                #         if self.change_x >= 0:
                #                 self.direction == "R"
                #                 frame = (self.rect.x // 10) % len(self.walking_frames_l)
                #                 self.image = self.walking_frames_r[1]

                #         if self.change_x < 0:
                #                 self.direction == "L"
                #                 frame = (self.rect.x // 10) % len(self.walking_frames_l)
                #                 self.image = self.walking_frames_l[frame]


                #         cur_pos = self.rect.x - self.level.world_shift
                #         if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
                #                 self.change_x *= -1




        # # def loop(self):
        # #         for num in range(4):
        #                 frame= num

