import pygame
import constants
import levels

from player import Player

pygame.init()


"""Música y sonidos. La música puede estar en .mp3 codificado a 128 kbp"""
background_music = pygame.mixer.music.load("8-punk-8-bit-music.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
"""Sonido de salto, desactivar si no se cuenta con el sonido. Siempre debe estar en .OGG"""
jump_sound = pygame.mixer.Sound("mario_jump.ogg")


"""Pantalla """
size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

"""Leyenda de la ventana """
pygame.display.set_caption("LCP - DonPablo")

clock = pygame.time.Clock()


"""Pantalla inicial donde están los créditos """
def game_intro():

        """ Carga la imagen de los créditos. La hice así para ahorrar trabajo pero se puede hacer con textos """
        background_image = pygame.image.load("LCPTile.png").convert()
        intro = True

        """ Ciclo del intro, si se presiona una tecla se termina"""
        while intro:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                if event.type == pygame.KEYDOWN:
                                intro = False

                """Dibuja el fondo previamente cargado"""
                screen.blit(background_image, (0,0))

                pygame.display.update()
                clock.tick(5)

"""Función del juego"""
def main():

        player = Player()
        level_list = []
        level_list.append(levels.Level_01(player))
        level_list.append(levels.Level_02(player))
        current_level_no = 0
        current_level =level_list[current_level_no]
        current_level.word_shift = -10

        active_sprite_list = pygame.sprite.Group()

        player.level = current_level

        player.rect.x = 20
        player.rect.y = 475
        active_sprite_list.add(player)

        done = False

        while not done:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                done = True

                        if player.rect.bottom >= constants.SCREEN_HEIGHT:
                                done = True

                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_LEFT:
                                        player.go_left()
                                if event.key == pygame.K_RIGHT:
                                        player.go_right()
                                if event.key == pygame.K_UP:
                                        player.jump()
                                        pygame.mixer.Sound.play(jump_sound)
                                        jump_sound.set_volume(0.10)

                        if event.type == pygame.KEYUP:
                                if event.key == pygame.K_LEFT and player.change_x < 0:
                                        player.stop()
                                if event.key == pygame.K_RIGHT and player.change_x > 0:
                                        player.stop()

                """Actualiza la lista donde se guarda la instancia del jugador y llama al método update() de la clase Player()"""
                active_sprite_list.update()
                """current_level es la variable donde se guardan los niveles se manda a llamar el método update() según el nivel actual"""
                current_level.update()

                """Establece un punto  sobre en la pantalla (500 px en horizontal) en donde se empezarán a desplazar todos los elementos hacia la izquierda si el lado derecho del jugador sobrepasa ese punto"""
                if player.rect.right > 500:
                        diff = player.rect.right - 500
                        player.rect.right = 500
                        current_level.shift_world(-diff)

                """Establece un punto  sobre en la pantalla (120 px en horizontal) en donde se empezarán a desplazar todos los elementos hacia la derecha si el lado izquierdo del jugador sobrepasa o es igual a ese punto"""
                if player.rect.left <= 120 and current_level.world_shift < 0:
                        diff = 120 - player.rect.left
                        player.rect.left = 120
                        current_level.shift_world(diff)

                """Si el jugador llega al punto 0 en horizontal de la pantalla se detiene y no puede continuar"""
                if player.rect.x <= 0:
                        player.rect.x = 0

                """Cambia de nivel si el jugador llega al límite definido de desplazamiento del nivel (esto se define en cada nivel)"""
                current_position = player.rect.x + current_level.world_shift
                if current_position < current_level.level_limit:
                        player.rect.x = 120
                        if current_level_no < len(level_list)-1:
                                current_level_no += 1
                                current_level = level_list[current_level_no]
                                player.level = current_level

                """Dibuja los elementos en la pantalla accediendo a los métodos draw del nivel y del active_sprite que es lo mismo que el jugador player"""
                current_level.draw(screen)
                active_sprite_list.draw(screen)

                """Dibuja el icono de las bananas y su contador de bananas recogidas"""
                screen.blit(current_level.score_image, [35, 30])
                screen.blit(current_level.text, [65, 30])
                """Dibuja mi nombre al lado derecho de la pantalla"""
                screen.blit(current_level.text_name, [constants.SCREEN_WIDTH - 100, 30])


                clock.tick(60)

                pygame.display.flip()

        pygame.quit()

"""Llama al la funciones llama a las funciones game_intro() donde se encuentran los créditos y main() donde se encuentra el ciclo del juego"""
if __name__ == "__main__":
        game_intro()
        main()

