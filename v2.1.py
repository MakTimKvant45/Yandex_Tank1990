import sys

import pygame
import level
from random import randint, randrange, choice
from pprint import pprint

pygame.init()
pygame.font.init()
pygame.mixer.init()

level_start = pygame.mixer.Sound('sounds/level_start.wav')
level_finish = pygame.mixer.Sound('sounds/level_finish.wav')
destroy = pygame.mixer.Sound('sounds/destroy.wav')
shot = pygame.mixer.Sound('sounds/shot.wav')
engine = pygame.mixer.Sound('sounds/engine.wav')
engine.set_volume(10)
dead = pygame.mixer.Sound('sounds/dead.wav')
star = pygame.mixer.Sound('sounds/star.wav')
move = pygame.mixer.Sound('sounds/move.wav')
move.set_volume(15)

WIDTH, HEIGHT = 512, 480
FPS = 60
TILE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)
my_font = pygame.font.SysFont('fonts/retro-land-mayhem.ttf', 30)

menu_img_BG = pygame.image.load('images/flow.png')
menu_img_Cursor = pygame.image.load('images/Cursor.png')

imgBrick = pygame.image.load('images/block_brick.png')
imgArmor = pygame.image.load('images/block_armor.png')
imgBushes = pygame.image.load('images/block_bushes.png')
imgEmblem = pygame.image.load('images/block_emblem.png')
imgWater = pygame.image.load('images/block_water.png')

img_EnemyTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),
]
img_TeemTanks = [
    pygame.image.load('images/Ttank1.png'),
    pygame.image.load('images/Ttank2.png'),
    pygame.image.load('images/Ttank3.png'),
    pygame.image.load('images/Ttank4.png'),
    pygame.image.load('images/Ttank5.png'),
    pygame.image.load('images/Ttank6.png'),
    pygame.image.load('images/Ttank7.png'),
    pygame.image.load('images/Ttank8.png'),
]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
]
imgBonuses = [
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'),
]
imgTanksHp = [
    pygame.image.load('images/hp_1_tank.png'),
    pygame.image.load('images/hp_2_tank.png')
]

game_over = pygame.image.load('images/game_over.jpg')
game_won = pygame.image.load('images/game_win.png')
ui_tank = pygame.image.load('images/ui_black_tank.png')
bullet_img = pygame.image.load('images/ammo.png')
level_flag = pygame.image.load('images/level_flag.png')

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


class GameActivUI:
    def __init__(self):
        self.enemy_count = 0
        self.enemy_count_pos_list = [462, 48]
        self.ui_black_tank = ui_tank
        # self.total_enemy_count = 0

    def update(self):
        ...

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                # pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))
                #
                # text = fontUI.render(str(obj.rank), 1, 'black')
                # rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                # window.blit(text, rect)
                #
                # text = fontUI.render(str(obj.hp), 1, obj.color)
                # rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(imgTanksHp[obj.num], (self.enemy_count_pos_list[0], 240 + 48 * i))
                hp = my_font.render(str(obj.hp), True, (0, 0, 0))
                window.blit(hp, (self.enemy_count_pos_list[0] + 18, 240 + 48 * i + 16))
                i += 1
        # print(self.enemy_count)
        window.blit(level_flag, (self.enemy_count_pos_list[0], 334))
        level = my_font.render(str(lev + 1), True, (0, 0, 0))
        window.blit(level, (self.enemy_count_pos_list[0] + 20, 334 + 20))
        # - Draw count of enemy
        y = self.enemy_count_pos_list[1]
        for black_tank in range(self.enemy_count):
            if black_tank % 2 == 0 and black_tank != 0:
                y += + self.ui_black_tank.get_height()
            x = self.enemy_count_pos_list[0] + self.ui_black_tank.get_width() * (black_tank % 2)
            window.blit(self.ui_black_tank, (x, y))


class Tank:
    def __init__(self, num, px, py, hp, rank, direct, keyList, team):
        objects.append(self)
        self.type = 'tank'
        self.start_pos = (px, py)

        self.num = num
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = hp
        self.shotTimer = 0
        self.team = team

        self.moveSpeed = 2
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = rank
        if self.team is False:
            self.image = pygame.transform.rotate(img_EnemyTanks[self.rank], -self.direct * 90)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = pygame.transform.rotate(img_TeemTanks[self.rank], -self.direct * 90)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.team is False:
            self.image = pygame.transform.rotate(img_EnemyTanks[self.rank], -self.direct * 90)
        else:
            self.image = pygame.transform.rotate(img_TeemTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]

        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            move.play()
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
            move.play()
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            move.play()
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
            move.play()

        for obj in objects:
            if obj != self and (
                    obj.type == 'brick' or obj.type == 'armor' or obj.type == 'emblem' or obj.type == 'water' or obj.type == 'wall') and \
                    self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        self.px, self.py = self.rect.topleft
        # for obj in objects:
        #     if obj.type == 'tank' and (self.px < 32 or self.px > 420 or self.py < 32 or self.py > 420):
        #         self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            shot.play()
            Bullet(self, self.type, self.rect.centerx, self.rect.centery, self.direct, self.bulletSpeed,
                   self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        dead.play()
        self.rect.topleft = self.start_pos
        if self.hp <= 0:
            objects.remove(self)

            print(self.num, 'dead')


class Enemy:
    def __init__(self, level, ex, ey):
        objects.append(self)
        self.type = 'enemy'
        self.direct = 2
        self.level = level
        # self.ex = ex
        # self.ey = ey
        self.old_ex = ex
        self.old_ey = ey
        self.rect = pygame.Rect(ex, ey, TILE, TILE)
        self.hp = 1
        self.rank = level
        self.direct_list = [-1, 0, 1, 2]
        self.direct_list_stop = self.direct_list.copy()
        self.direct_list_move = self.direct_list.copy()

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank] * 1.5
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]

        self.timer = self.shotDelay + randint(0, 50)
        self.direct_change_delay = 70
        self.direct_change_timer = self.direct_change_delay
        self.del_direct_list = [2, -1, 0, 1]

    def update(self):
        self.shoot()
        self.direct_list_stop = self.direct_list.copy()
        self.direct_list_move = self.direct_list.copy()

        self.old_ey = self.rect.y
        self.old_ex = self.rect.x

        # - Move up
        if self.direct == 0:
            if self.rect.y >= 32:
                self.rect.y -= self.moveSpeed
        # - Move down
        if self.direct == 2:
            if self.rect.y <= 448:
                self.rect.y += self.moveSpeed
        # - Move right
        if self.direct == 1:
            if self.rect.x <= 448:
                self.rect.x += self.moveSpeed
        # - Move left
        if self.direct == -1:
            if self.rect.x >= 32:
                self.rect.x -= self.moveSpeed

        self.image = pygame.transform.rotate(img_EnemyTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        if len(self.direct_list_move) > 0:
            self.random_direct_in_move()

        for obj in objects:
            if obj != self and obj.type != 'enemy' and (
                    obj.type == 'brick' or obj.type == 'armor' or obj.type == 'emblem' or obj.type == 'water' or obj.type == 'wall') and \
                    self.rect.colliderect(obj.rect):
                # or (self.rect.x < 32 or self.rect.x > 420 or self.rect.y < 32 or self.rect.y > 420):
                self.rect.x = self.old_ex
                self.rect.y = self.old_ey
                self.check_obj_rect = obj.rect
                if len(self.direct_list_stop) > 0:
                    self.direct = choice(self.direct_list_stop)
                self.direct_change_timer = self.direct_change_delay / 2

    def draw(self):
        window.blit(self.image, self.rect)

    def random_direct_in_move(self):
        if self.direct_change_timer == 0:
            for obj in objects:
                if obj != self and obj.type != 'enemy' and (
                        obj.type == 'brick' or obj.type == 'armor'):
                    self.check_obj_rect = obj.rect
                    self.get_available_direct()
                    if len(self.direct_list_move) > 0:
                        self.direct = choice(self.direct_list_move)
                        self.direct_change_timer = self.direct_change_delay
        else:
            self.direct_change_timer -= 1

    def shoot(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.timer = self.shotDelay
            Bullet(self, self.type, self.rect.centerx, self.rect.centery, self.direct, self.bulletSpeed,
                   self.bulletDamage)

    def get_available_direct(self):
        # - if enemy can't move to left
        if self.check_obj_rect.collidepoint(self.rect.x, self.rect.y):
            self.direct_list_stop.remove(-1)
            self.direct_list_move.remove(-1)
        # - if enemy can't move to right
        if self.check_obj_rect.collidepoint(self.rect.x + self.rect.width, self.rect.y):
            self.direct_list_stop.remove(1)
            self.direct_list_move.remove(1)
        # - if enemy can't move to up
        if self.check_obj_rect.collidepoint(self.rect.x, self.rect.y):
            self.direct_list_stop.remove(0)
            self.direct_list_move.remove(0)
        # - if enemy can't move to down
        if self.check_obj_rect.collidepoint(self.rect.x, self.rect.y + self.rect.height):
            self.direct_list_stop.remove(2)
            self.direct_list_move.remove(2)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            dead.play()


class Bullet:
    def __init__(self, parent, teem, px, py, direct, bulletSpeed, damage):
        bullets.append(self)
        self.parent = parent
        self.teem = teem
        self.px, self.py = px, py
        self.direct = direct
        self.dx = DIRECTS[self.direct][0] * bulletSpeed
        self.dy = DIRECTS[self.direct][1] * bulletSpeed
        self.damage = damage
        self.image = pygame.transform.rotate(bullet_img, -self.direct * 90)

    def update(self):
        self.px += self.dx
        self.py += self.dy

        # - Левая граница
        # 0, 0, 32, 448
        # - Верхняя граница
        # 0, 0, 480, 32
        # - Нижняя граница
        # 0, 448, 480, 32
        # - Правая граница
        # 448, 0, 64, 480

        # if self.px < 32 or self.px > 448 or self.py < 32 or self.py > 448:
        #     bullets.remove(self)
        # else:
        for obj in objects:
            if obj.type != self.teem and obj.type != 'bang' and obj.type != 'bonus' and obj.type != 'bushes' and obj.type != 'water':
                if obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break
        for bul in bullets:
            apx = range(bul.px - 10, bul.px + 10)
            apy = range(bul.py - 10, bul.py + 10)
            if self.px in apx and self.py in apy and bul != self:
                try:
                    bullets.remove(self)
                    bullets.remove(bul)
                except ValueError:
                    pass

    def draw(self):
        # pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)
        window.blit(self.image, (self.px - self.image.get_width() / 2 + 1, self.py - self.image.get_height() / 2 + 1))


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3: objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size, types):
        objects.append(self)
        self.type = types

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        if self.type == 'brick':
            window.blit(imgBrick, self.rect)
        elif self.type == 'armor':
            window.blit(imgArmor, self.rect)
        elif self.type == 'bushes':
            window.blit(imgBushes, self.rect)
        elif self.type == 'water':
            window.blit(imgWater, self.rect)
        elif self.type == 'emblem':
            window.blit(imgEmblem, self.rect)

    def damage(self, value):
        if self.type == 'brick' or self.type == 'emblem':
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)
                destroy.play()
        if self.type == 'armor':
            shot.play()


class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'
        self.image = imgBonuses[bonusNum]
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 800
        self.bonusNum = bonusNum

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                star.play()
                if self.bonusNum == 0:
                    if obj.rank < len(img_EnemyTanks) - 1:
                        obj.rank += 1
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.hp += 1
                    objects.remove(self)
                    break

    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


class Cursor:
    def __init__(self):
        self.index = 0

    def update(self):
        # if keys[pygame.K_UP] or keys[pygame.K_w]:
        #     self.index -= 1
        # if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        #     self.index += 1
        # if self.index > 2:
        #     self.index = 0
        # if self.index < 0:
        #     self.index = 2
        # print(pygame.event.get())
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.index -= 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.index += 1
        if self.index > 2:
            self.index = 0
        if self.index < 0:
            self.index = 2

    def draw(self):
        window.blit(menu_img_Cursor, (150, 208 + self.index * 27))


bullets = []
objects = []

ui = GameActivUI()
cur = Cursor()


def draw_map(levels, mode):
    Wall(0, 0, 32, 448, all_design_sprites)
    Wall(0, 0, 480, 32, all_design_sprites)
    Wall(0, 448, 480, 32, all_design_sprites)
    Wall(448, 0, 64, 480, all_design_sprites)
    if mode == 0:
        # Enemy(levels, 32, 32)
        Tank(0, 160, 416, first_tank_hp, first_tank_rank, 0,
             (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),
             True)
    if mode == 1:
        Tank(0, 160, 416, first_tank_hp, first_tank_rank, 0,
             (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),
             True)
        Tank(1, 288, 416, second_tank_hp, second_tank_rank, 0,
             (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_k), True)
    if mode != 2:
        y = 32
        for sr in level.lev[levels]:
            x = 32
            for el in sr:
                if el == 1:
                    Block(x, y, TILE, 'brick')
                elif el == 2:
                    Block(x, y, TILE, 'bushes')
                elif el == 3:
                    Block(x, y, TILE, 'armor')
                elif el == 4:
                    Block(x, y, TILE, 'water')
                elif el == 9:
                    Block(x, y, TILE, 'emblem')
                x += TILE
            y += TILE
    if mode == 2:

        new_level = []

        f = open('levels/level.txt', encoding='utf-8')
        for number, line in enumerate(f):
            sec_list = []
            for s in line:
                if s in '012349':
                    sec_list.append(int(s))
            new_level.append(sec_list)
            if number >= 13:
                break
        y = 32
        f.close()
        # pprint(new_level)
        player_spawn_list = get_player_spawn_list(new_level)
        Tank(0, 32 + 32 * new_level[-1][player_spawn_list[0]], 416, first_tank_hp, first_tank_rank, 0,
             (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE),
             True)
        for sr in new_level:
            x = 32
            for el in sr:
                if el == 1:
                    Block(x, y, TILE, 'brick')
                elif el == 2:
                    Block(x, y, TILE, 'bushes')
                elif el == 3:
                    Block(x, y, TILE, 'armor')
                elif el == 4:
                    Block(x, y, TILE, 'water')
                elif el == 9:
                    Block(x, y, TILE, 'emblem')
                x += TILE
            y += TILE

        # print(objects)


def get_player_spawn_list(levels):
    player_spawn_list = []
    search_line = levels[-1]
    for chunk in range(len(search_line)):
        if search_line[chunk] == 0:
            player_spawn_list.append(chunk)

    return player_spawn_list


def get_enemy_spawn_list(levels):
    enemy_spawn_list = []
    search_line = level.lev[levels][0]
    zero_count = 0
    for chunk in range(len(search_line)):
        if len(enemy_spawn_list) < 4:
            if search_line[chunk] == 0:
                if zero_count % 2 == 0:
                    enemy_spawn_list.append(chunk)
                zero_count += 1
    if zero_count > 2:
        zero_count -= 2

    return enemy_spawn_list


def spawn_enemy(enemy_spawn_list, lev):
    y = 32
    x = 32
    spqwn_line = level.lev[lev][0]
    for chunk in enemy_spawn_list:
        x1 = x + x * chunk
        Enemy(lev, x1, y)


# def draw_design():
#     # # - Левая граница
#     # pygame.draw.rect(window, 'gray', (0, 0, 32, 448))
#     # # - Верхняя граница
#     # pygame.draw.rect(window, 'gray', (0, 0, 480, 32))
#     # # - Нижняя граница
#     # pygame.draw.rect(window, 'gray', (0, 448, 480, 32))
#     # # - Правая граница
#     # pygame.draw.rect(window, 'gray', (448, 0, 64, 480))
#     Wall(0, 0, 32, 448, all_design_sprites)
#     Wall(0, 0, 480, 32, all_design_sprites)
#     Wall(0, 448, 480, 32, all_design_sprites)
#     Wall(448, 0, 64, 480, all_design_sprites)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x1, y1, w, h, *group):
        super().__init__(*group)
        self.type = 'wall'
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h
        self.image = pygame.Surface([self.w, self.h])
        self.rect = self.image.get_rect()
        self.rect.x = self.x1
        self.rect.y = self.y1
        objects.append(self)

    def damage(self, value):
        ...

    def draw(self):
        self.image.fill('gray')
        window.blit(self.image, self.rect)
        # pygame.draw.rect(self.image, 'gray', (self.x1, self.y1, self.w, self.h))

    def update(self):
        ...


def draw_menu():
    window.blit(menu_img_BG, (0, 40))


def get_tanks_hps_ranks():
    global first_tank_hp, first_tank_rank, second_tank_hp, second_tank_rank
    count_tank = 0
    for obj in objects:
        if obj.type == 'tank':
            count_tank += 1
            if count_tank == 1:
                first_tank_hp = obj.hp
                first_tank_rank = obj.rank
            if count_tank == 2:
                second_tank_hp = obj.hp
                second_tank_rank = obj.rank



bonusTimer = 1600
new_map = True
mainMenu = True
game_end = False
game_win = False
play = True
fpsm = 10
mode = 100
lev = 0
all_design_sprites = pygame.sprite.Group()
first_game = True
stage = 3
return_to_menu = 200
first_tank_hp = 2
second_tank_hp = 2
first_tank_rank = 0
second_tank_rank = 0

while play:
    engine.stop()
    move.stop()
    pygame.display.set_caption(str(clock.get_fps()))
    if mainMenu:
        if game_end is False and game_win is False:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    play = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                mode = cur.index
                mainMenu = False
            cur.update()
            # window.fill('black')
            draw_menu()

            cur.draw()
            pygame.display.update()
            clock.tick(FPS)

        elif game_end:
            if return_to_menu < 0:
                game_end = False
                new_map = True
                lev = 0
                stage = 3
            else:
                return_to_menu -= 1
            window.blit(game_over, (-40, 40))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    play = False
            pygame.display.update()
            clock.tick(FPS)
        elif game_win:
            if return_to_menu < 0:
                game_win = False
                new_map = True
                lev = 0
                stage = 3
            else:
                return_to_menu -= 1
            window.blit(game_won, (0, 40))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    play = False
            pygame.display.update()
            clock.tick(FPS)
    else:
        if lev < 3:
            engine.play()
            move.stop()
            if new_map:
                level_start.play()
                enemy_spawn_list = get_enemy_spawn_list(lev)
                spawn_enemy(enemy_spawn_list, lev)
                draw_map(lev, mode)
                new_map = False
                first_game = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False

            keys = pygame.key.get_pressed()

            if bonusTimer > 0:
                bonusTimer -= 1
            else:
                Bonus(randint(50, 400), randint(50, 400), randrange(len(imgBonuses) - 1))
                bonusTimer = 1600

            for bullet in bullets:
                bullet.update()
            for obj in objects:
                obj.update()
            ui.update()

            window.fill('black')
            # draw_design()
            # all_design_sprites.draw(window)
            for obj in objects:
                if obj.type == 'wall':
                    obj.draw()
            for obj in objects:
                if obj.type == 'tank' or obj.type == 'enemy':
                    obj.draw()

            for obj in objects:
                if obj.type != 'tank' and obj.type != 'enemy':
                    obj.draw()

            for bullet in bullets:
                bullet.draw()
            ui.draw()

            if stage > 0:
                tank_count = 0
                count_enemy = 0
                old_count_enemy = 0
                for obj in objects:
                    if obj.type == 'enemy':
                        count_enemy += 1
                    if obj.type == 'tank':
                        tank_count += 1
                get_tanks_hps_ranks()
                ui.enemy_count = len(get_enemy_spawn_list(lev)) * (stage - 1) + count_enemy
                if count_enemy == 0:
                    if stage > 1:
                        enemy_spawn_list = get_enemy_spawn_list(lev)
                        spawn_enemy(enemy_spawn_list, lev)
                        stage -= 1
                    elif stage == 1:
                        enemy_spawn_list = get_enemy_spawn_list(lev)
                        spawn_enemy(enemy_spawn_list, lev)
                        stage -= 1
            elif stage == 0:
                objects = []
                bullets = []
                lev += 1
                new_map = True
                stage = 3
            emblemc = 0
            for obj in objects:
                if obj.type == 'emblem':
                    emblemc += 1
            tankc = 0
            for obj in objects:
                if obj.type == 'tank':
                    tankc += 1

            if (emblemc == 0 or tankc == 0) and objects != []:
                objects = []
                return_to_menu = 300
                window.fill('black')
                mainMenu = True
                game_end = True
                engine.stop()
                level_start.stop()
                level_finish.play()
        else:
            objects = []
            return_to_menu = 300
            window.fill('black')
            game_win = True
            mainMenu = True

            first_tank_hp = 2
            second_tank_hp = 2
            first_tank_rank = 0
            second_tank_rank = 0

            level_finish.play()

        pygame.display.update()
        clock.tick(FPS)
pygame.quit()
