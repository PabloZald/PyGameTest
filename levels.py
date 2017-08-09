import pygame

import constants
import platforms
import items
import enemy

from spritesheet_functions import SpriteSheet

class Level():

        def __init__(self, player):
                self.font = pygame.font.SysFont(None, 36)
                self.font_name = pygame.font.SysFont(None, 18)
                self.platform_list = None
                self.coin_sound = pygame.mixer.Sound("Coin.ogg")
                self.level_score = 0
                self.item_list = None
                self.background = None
                self.world_shift = 0
                self.level_limit = -1000
                self.platform_list = pygame.sprite.Group()
                self.item_list = pygame.sprite.Group()
                self.enem_list = pygame.sprite.Group()
                self.player = player
                self.salu_image = None
                self.x_salu_image = 1700


                """Items (en este caso solo bananas)"""
                sprite_sheet = SpriteSheet("banana.png")
                image = sprite_sheet.get_image(0, 0, 56, 86)
                image = pygame.transform.scale(image, (28, 43))
                self.score_image = image

        def update(self):
                self.platform_list.update()
                self.item_list.update()
                self.enem_list.update()

                """ Comprueba se el jugador ha colisionado con un item (banana), la elimina y aumenta el marcador"""
                item_hit_list = pygame.sprite.spritecollide(self.player, self.item_list, True)

                for item in item_hit_list:
                        self.item_list.remove(item)
                        self.level_score += 1
                        pygame.mixer.Sound.play(self.coin_sound)
                        self.coin_sound.set_volume(0.25)
                        print(self.level_score)

                """ Define la fuente del marcador y de mi nombre que está al lado derecho"""
                self.text = self.font.render(str(self.level_score), True, constants.WHITE)
                self.text_name = self.font_name.render("Don Pablo", True, constants.WHITE)


                """Mueve los enemigos según los límites establecidos en el nivel, su dirección, y desplazamiento del escenario"""

                for enem in self.enem_list:
                    enem.rect.x += enem.change_x

                    if enem.change_x > 0 and enem.rect.x < enem.boundary_right:
                            enem.direction == "R"
                            frame_r = (enem.rect.x // 20) % len(enem.walking_frames_r)
                            enem.image = enem.walking_frames_r[frame_r]
                    else:
                            enem.direction == "L"
                            frame = (enem.rect.x // 20) % len(enem.walking_frames_l)
                            enem.image = enem.walking_frames_l[frame]


                    cur_pos = enem.rect.x - self.world_shift
                    if cur_pos < enem.boundary_left or cur_pos > enem.boundary_right:
                            enem.change_x *= -1


        def draw(self, screen):

                screen.fill(constants.BLACK)
                screen.blit(self.background, (self.world_shift // 3, 0))
                screen.blit(self.salu_image, (self.x_salu_image, 100))

                self.platform_list.draw(screen)
                self.item_list.draw(screen)
                self.enem_list.draw(screen)


        def shift_world(self, shift_x):

                self.world_shift += shift_x

                self.x_salu_image += shift_x

                for platform in self.platform_list:
                        platform.rect.x += shift_x

                for item in self.item_list:
                        item.rect.x += shift_x

                for enemy in self.enem_list:
                        enemy.rect.x += shift_x


class Level_01(Level):

        def __init__(self, player):

                Level.__init__(self, player)

                #self.background = pygame.image.load("junglebackground.jpg").convert()
                #self.background.set_colorkey(constants.WHITE)
                """ Esta es la imagen final de bananas que forman la palabra Salú, pero le faltan bananas de la izquierda que son items"""
                self.salu_image = pygame.image.load("salu.png").convert()
                self.salu_image.set_colorkey(constants.BLACK)

                """Límite de desplazamiento de este nivel, Level_01"""
                self.level_limit = -1500


                """Lista con las posiciones x, y de las bananas en la pantalla"""
                level_item = [ [95, 75],
                                        [575, 300],
                                        [1035, 200],
                                        [1300, 50],
                                        [1300, 50],
                                        [ 1400, 400],
                                        [ 1665, 175],
                                        [ 1665, 215],
                                        [ 1650, 270],
                                        [ 1680, 295],
                                      ]
                """ Recorre la lista de posiciones, crea los objetos, les establece sus propiedades según cada posición de la lista y luego los añade a una nueva lista llamada item_list """
                for fruit in level_item:
                        item = items.Banana()
                        item.rect.x = fruit[0]
                        item.rect.y = fruit[1]
                        item.player = self.player
                        item.level_item = self
                        self.item_list.add(item)


                """ Lista de plataformas de que se dibujan en el nivel, la posición [0] de cada sublista la llama del módulo platforms, las otras dos son las posiciones X y Y  en donde se dibujarn en la pantalla"""
                level = [ [platforms.GRASS_LEFT, 500, 500],
                              [platforms.GRASS_MIDDLE, 570, 500],
                              [platforms.GRASS_RIGHT, 640, 500],

                              [platforms.GRASS_LEFT, 800, 350],
                              [platforms.GRASS_MIDDLE, 870, 350],
                              [platforms.GRASS_RIGHT, 940, 350],

                              [platforms.GRASS_LEFT, 1000, 500],
                              [platforms.GRASS_MIDDLE, 1070, 500],
                              [platforms.GRASS_RIGHT, 1140, 500],

                              [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                              [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                              [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                            ]

                for platform in level:
                        block = platforms.Platform(platform[0])
                        block.rect.x = platform[1]
                        block.rect.y = platform[2]
                        block.player = self.player
                        self.platform_list.add(block)

                """Plataforma inicial del juego ubicado en la parte inferior izquierda del nivel, luego hay un hueco"""
                base = platforms.Platform(platforms.GRASS_MIDDLE)
                base.rect.x = 0
                base.rect.y = constants.SCREEN_HEIGHT - base.rect.height
                base.player = self.player
                self.platform_list.add(base)

                """ Plataforma ubicada en medio del nivel"""
                base = platforms.Platform(platforms.GRASS_MIDDLE)
                base.rect.x = 210
                base.rect.y = constants.SCREEN_HEIGHT - base.rect.height
                base.player = self.player
                self.platform_list.add(base)

                """ Plataforma larga en donde el jugador corre"""
                for num in range(210, 1500, 70):
                        base = platforms.Platform(platforms.GRASS_MIDDLE)
                        base.rect.x = num
                        base.rect.y = constants.SCREEN_HEIGHT - base.rect.height
                        base.player = self.player
                        self.platform_list.add(base)


                """ Plataforma que se mueve sobre las coordenas X entre 1350 a 1600"""
                block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
                block.rect.x = 1350
                block.rect.y = 280
                block.boundary_left = 1350
                block.boundary_right = 1600
                block.change_x = 6
                block.player =self.player
                block.level = self
                self.platform_list.add(block)

                """ Plataforma que se mueve de arriba a abajo, sobre las coordenas Y"""
                block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
                block.rect.x = 300
                block.rect.y = 300
                block.boundary_top = 100
                block.boundary_bottom = 450
                block.change_y = 6
                block.player = self.player
                block.level = self
                self.platform_list.add(block)

                """ Primer enemigo """
                enem = enemy.Enemy()
                enem.rect.x = 550
                enem.rect.y = 445
                enem.boundary_left= 505
                enem.boundary_right = 690
                enem.level = self
                self.enem_list.add(enem)

                """ Segundo enemigo """
                enem = enemy.Enemy()
                enem.rect.x = 1230
                enem.rect.y = 480
                enem.boundary_left= 1220
                enem.boundary_right = 1510
                enem.level = self
                self.enem_list.add(enem)



""" Nivel 2, no está terminado solo lo escribí como muestra"""

class Level_02(Level):

        def __init__(self, player):
                Level.__init__(self, player)
                self.level_limit = -1000

                level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                              [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                              [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                              [platforms.GRASS_LEFT, 800, 400],
                              [platforms.GRASS_MIDDLE, 870, 400],
                              [platforms.GRASS_RIGHT, 940, 400],
                              [platforms.GRASS_LEFT, 1000, 500],
                              [platforms.GRASS_MIDDLE, 1070, 500],
                              [platforms.GRASS_RIGHT, 1140, 500],
                              [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                              [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                              [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                            ]

                for platform in level:
                        block = platforms.Platform(platform[0])
                        block.rect.x = platform[1]
                        block.rect.y = platform[2]
                        block.player = self.player
                        self.platform_list.add(block)

                block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
                block.rect.x = 1500
                block.rect.y = 300
                block.boundary_top = 100
                block.boundary_bottom = 550
                block.change_y = 6
                block.player = self.player
                block.level = self
                self.platform_list.add(block)
