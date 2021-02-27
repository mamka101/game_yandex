import os
import sys

import pygame
import random

pygame.init()
pygame.display.set_caption("РосКосмос")
size = width, height = 580, 435
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert(24)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["РОСКОСМОС", "",
                  "Симулятор",
                  "Управление - стрелки",
                  "Лазер - пробел",
                  "За уничтожение астероидов - новый корабль",
                  "Каждые 100 астероидов дается бомба",
                  "Использование бомбы - ",
                  "уничтожение всех астероидов",
                  "Бомба - q"]

    fon = pygame.transform.scale(load_image('ros3.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


tile_images = {
    'aster': load_image('as.jpg', -1),
    'laser': load_image('laser.png', -1),
    'alien': load_image('alien.png', -1),
    'laser_alien': load_image('laser_alien.png', -1),
    'elon': load_image('elon.jpg', -1),
    'trash': load_image('trash.jpg', -1),
    'nyan_cat': load_image('nyan_cat.png', -1)
}
player_image_ship1 = load_image('ship1.jpg', -1)
player_image_ship2 = load_image('ship2.png', -1)
player_image_ship3 = load_image('ship3.png', -1)
player_image_ship4 = load_image('ship4.png', -1)
player_image = player_image_ship1

tile_width = tile_height = 50
ast_size = 30


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(asteroid_group, all_sprites)
        self.image = pygame.transform.scale(tile_images['aster'], (ast_size, ast_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.image.get_width())
        while len(pygame.sprite.spritecollide(self, all_sprites, False)) <= 1:
            self.rect.x = random.randrange(width - self.image.get_width())
            self.rect.y = 0

        self.vx = random.randint(-5, 5)
        self.vy = 2

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.x <= 0 - ast_size or self.rect.x >= width or self.rect.y >= height:
            self.kill()


nyan_cat_size = 80, 50


class NyanCat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(nyan_cat_group, all_sprites)
        self.image = pygame.transform.scale(tile_images['nyan_cat'], nyan_cat_size)
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(0, height // 2)
        # while len(pygame.sprite.spritecollide(self, all_sprites, False)) <= 1:
        #     self.rect.x = random.randrange(width - self.image.get_width())
        #     self.rect.y = 0

        self.vx = 5
        # self.vy = random.randint(0, height // 2)

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        if self.rect.x <= 0 - ast_size or self.rect.x >= width or self.rect.y >= height:
            self.kill()


elon_size = 50


class Elon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(elon_group, all_sprites)
        self.image = pygame.transform.scale(tile_images['elon'], (elon_size, elon_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.image.get_width())
        while len(pygame.sprite.spritecollide(self, all_sprites, False)) <= 1:
            self.rect.x = random.randrange(width - self.image.get_width())
            self.rect.y = 0

        self.vx = random.randint(-5, 5)
        self.vy = 2

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.x <= 0 - ast_size or self.rect.x >= width or self.rect.y >= height:
            self.kill()


trash_size = 40


class Trash(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(trash_group, all_sprites)
        self.image = pygame.transform.scale(tile_images['trash'], (trash_size, trash_size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.image.get_width())
        while len(pygame.sprite.spritecollide(self, all_sprites, False)) <= 1:
            self.rect.x = random.randrange(width - self.image.get_width())
            self.rect.y = 0

        self.vx = random.randint(-5, 5)
        self.vy = 2

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.x <= 0 - ast_size or self.rect.x >= width or self.rect.y >= height:
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(alien_group, all_sprites)
        self.image = pygame.transform.scale(tile_images['alien'], (ast_size, ast_size))

        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.vy = 1
        LaserAlien(self.rect.x + self.image.get_width() // 2 - 3, self.rect.y + self.image.get_height() - 5)

    def update(self):
        global cnt_time_laser_alien, FPS
        if cnt_time_laser_alien / FPS >= 2.5:
            LaserAlien(self.rect.x + self.image.get_width() // 2 - 3, self.rect.y + self.image.get_height() - 5)
            cnt_time_laser_alien = 0
        self.rect = self.rect.move(0, self.vy)
        if self.rect.y >= height:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(laser_group, all_sprites)
        self.image = tile_images['laser']

        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.vy = 3

    def update(self):
        global cnt_aster
        self.rect.y -= self.vy
        if pygame.sprite.spritecollide(self, asteroid_group, True):
            cnt_aster += 1
            self.kill()


class LaserAlien(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(laser_alien_group, all_sprites)
        self.image = tile_images['laser_alien']

        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.vy = 2

    def update(self):
        self.rect.y += self.vy
        if self.rect.y >= height:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(player_image, (player_size, player_size))
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_x, self.pos_y = pos_x, pos_y

    def move(self, x, y):
        vert = pygame.sprite.spritecollide(self, vertical_borders, False)  # список касания вертикальных стен
        if x < 0:  # выбор на проверку вертикальной стены левой или правой
            n_v = 0
        else:
            n_v = 1
        if not (vert and vert[0].n == n_v):  # проверка касания верт стены
            self.rect.x += x
            self.pos_x = self.rect.x

        hor = pygame.sprite.spritecollide(self, horizontal_borders, False)  # список касания горизонтальных стен
        if y < 0:  # выбор на проверку гориз стены нижней или верхней
            n_h = 3
        else:
            n_h = 2
        if not (hor and hor[0].n == n_h):  # проверка касания гориз стены
            self.rect.y += y
            self.pos_y = self.rect.y


# основной персонаж
player = None
# группы спрайтов
all_sprites = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
nyan_cat_group = pygame.sprite.Group()
elon_group = pygame.sprite.Group()
trash_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
laser_alien_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_size = 50
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, n):
        super().__init__(all_sprites)
        self.n = n  # обозначение номера стены
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


back_list = [[0 for j in range(width)] for i in range(height)]
for i in range(height):
    for j in range(width // 200):
        back_list[i][random.randint(0, width - 1)] = 1


Border(0, 0, width - 5, 5, 3)  # верхняя стена
Border(5, height - 5, width - 5, height - 5, 2)  # нижняя стена
Border(0, 0, 0, height, 0)  # левая стена
Border(width - 1, 0, width - 1, height, 1)  # правая стена


def back_draw():
    help_l = [0 for i in range(width)]
    for i in range(width // 200):
        help_l[random.randint(0, width - 1)] = 1
    back_list.insert(0, help_l)
    for i in range(height):
        for j in range(width):
            if back_list[i][j] == 1:
                screen.fill(pygame.Color("white"),
                            (j, i,
                            1, 1))


speed = 5
cnt_aster = 0

boom = pygame.sprite.Sprite()
boom.image = load_image("boom.png")

boom.rect = boom.image.get_rect()
boom_group = pygame.sprite.Group()
boom_group.add(boom)

game_over = pygame.sprite.Sprite()
game_over.image = load_image("game_over.png", -1)
game_over.rect = game_over.image.get_rect()
game_over_group = pygame.sprite.Group()
game_over_group.add(game_over)

cnt_time_laser_alien = 0
FPS = 30


def main():
    global screen, player_image, player_size, cnt_aster, cnt_time_laser_alien
    running = True
    player = Player((width - player_size) // 2, height - player_size)
    clock = pygame.time.Clock()

    cnt_time_aster = 0
    cnt_time_alien = 0
    cnt_time_laser = 0
    cnt_time_elon = 0
    cnt_time_trash = 0
    cnt_time_nyan_cat = 0
    time_limit = 0.5
    not_game_over = True
    ship = 1
    cnt_bomb = 0
    give_bomb_aster = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                not_game_over = False
            if not_game_over and event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_SPACE] and cnt_time_laser / FPS >= 0.5:
                if ship == 1:
                    Laser(player.pos_x + player_size // 2 - 3, player.pos_y)
                elif ship == 2:
                    Laser(player.pos_x + player_size // 2 - 6, player.pos_y)
                    Laser(player.pos_x + player_size // 2, player.pos_y)
                elif ship == 3:
                    Laser(player.pos_x + player_size // 2 - 13, player.pos_y + 12)
                    Laser(player.pos_x + player_size // 2 - 3, player.pos_y + 4)
                    Laser(player.pos_x + player_size // 2 + 7, player.pos_y + 12)
                elif ship == 4:
                    Laser(player.pos_x + player_size // 2 - 24, player.pos_y + 20)
                    Laser(player.pos_x + player_size // 2 - 15, player.pos_y + 10)
                    Laser(player.pos_x + player_size // 2 + 9, player.pos_y + 10)
                    Laser(player.pos_x + player_size // 2 + 18, player.pos_y + 20)
                cnt_time_laser = 0
            if not_game_over and event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_q] and cnt_bomb >= 1:
                # cnt_aster += len(asteroid_group.sprites())
                asteroid_group.empty()
                elon_group.empty()
                alien_group.empty()
                laser_alien_group.empty()
                laser_group.empty()
                cnt_bomb -= 1
        if not_game_over:
            screen.fill((0, 0, 0))
            back_draw()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                player.move(-speed, 0)
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                player.move(speed, 0)
            if pygame.key.get_pressed()[pygame.K_UP]:
                player.move(0, -speed)
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                player.move(0, speed)

            if pygame.sprite.spritecollideany(player, asteroid_group) or \
                    pygame.sprite.spritecollideany(player, alien_group) or \
                    pygame.sprite.spritecollideany(player, laser_alien_group):
                boom.rect.x = player.pos_x - player_size // 2
                boom.rect.y = player.pos_y - player_size // 2
                boom_group.draw(screen)
                not_game_over = False

            intro_text = [f"Счет: {cnt_aster}", "",
                          f"Бомб: {cnt_bomb}"]
            font = pygame.font.Font(None, 30)
            text_coord = 5
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('green'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += 10
                screen.blit(string_rendered, intro_rect)

            if cnt_aster >= 5 and ship < 2:
                player_image = player_image_ship2
                player.__init__(player.pos_x, player.pos_y)
                ship = 2

            if cnt_aster >= 25 and ship < 3:
                player_image = player_image_ship3
                player.__init__(player.pos_x, player.pos_y)
                ship = 3

            if cnt_aster >= 50 and ship < 4:
                player_image = player_image_ship4
                player.__init__(player.pos_x, player.pos_y)
                ship = 4

            if cnt_aster != 0 and cnt_aster % 100 == 0 and cnt_aster != give_bomb_aster:
                cnt_bomb += 1
                give_bomb_aster = cnt_aster

            if cnt_time_aster / FPS >= time_limit:
                Asteroid()
                cnt_time_aster = 0
                time_limit -= 0.01
                if time_limit <= 0.05:
                    time_limit = 0.05

            if cnt_time_elon / FPS >= 3:
                Elon()
                cnt_time_elon = 0

            if cnt_time_trash / FPS >= 2:
                Trash()
                cnt_time_trash = 0

            if cnt_time_nyan_cat / FPS >= 5:
                NyanCat()
                cnt_time_nyan_cat = 0

            if cnt_time_alien / FPS >= 3:
                Alien(random.randint(50, width - 50), 0)
                cnt_time_alien = 0

            nyan_cat_group.draw(screen)
            asteroid_group.draw(screen)
            alien_group.draw(screen)
            elon_group.draw(screen)
            trash_group.draw(screen)
            laser_group.draw(screen)
            laser_alien_group.draw(screen)
            player_group.draw(screen)
            all_sprites.update()
            cnt_time_aster += 1
            cnt_time_alien += 1
            cnt_time_laser_alien += 1
            cnt_time_laser += 1
            cnt_time_elon += 1
            cnt_time_trash += 1
            cnt_time_nyan_cat += 1
        if not not_game_over:
            game_over_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    start_screen()
    main()
