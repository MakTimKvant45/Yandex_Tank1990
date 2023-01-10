import pygame
import level
from random import randint
pygame.init()

WIDTH, HEIGHT = 512, 480
FPS = 60
TILE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)

mimgFlow = pygame.image.load('images/flow.png')
mimgCursor = pygame.image.load('images/Cursor.png')

imgBrick = pygame.image.load('images/block_brick.png')
imgArmor = pygame.image.load('images/block_armor.png')
imgBushes = pygame.image.load('images/block_bushes.png')
imgEmblem = pygame.image.load('images/block_emblem.png')

imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),
    ]
imgTTanks = [
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

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

MOVE_SPEED =    [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED =  [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY =    [60, 50, 30, 40, 30, 25, 25, 30]

class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center = (5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center = (5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1
                

class Tank:
    def __init__(self, color, px, py, direct, keyList, team):
        objects.append(self)
        self.type = 'tank'
        self.start_pos = (px, py)

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = 5
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

        self.rank = 0
        if self.team is False:
            self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
            self.rect = self.image.get_rect(center = self.rect.center)
        else:
            self.image = pygame.transform.rotate(imgTTanks[self.rank], -self.direct * 90)
            self.rect = self.image.get_rect(center = self.rect.center)            

    def update(self):
        if self.team is False:
            self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        else:
            self.image = pygame.transform.rotate(imgTTanks[self.rank], -self.direct * 90)                    
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center = self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and (obj.type == 'brick' or obj.type == 'armor') and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
                
        self.px, self.py = self.rect.topleft   
        for obj in objects:
            if obj.type == 'tank' and (self.px < 32 or self.px > 420 or self.py < 32 or self.py > 420):
                self.rect.topleft = oldX, oldY       

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        self.rect.topleft = self.start_pos
        if  self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus' and obj.type != 'bushes':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


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
        rect = image.get_rect(center = (self.px, self.py))
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
        elif self.type == 'emblem':
            window.blit(imgEmblem, self.rect)                

    def damage(self, value):
        if self.type == 'brick':
            self.hp -= value
            if self.hp <= 0: objects.remove(self)

class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'
        self.image = imgBonuses[bonusNum]
        self.rect = self.image.get_rect(center = (px, py))

        self.timer = 800
        self.bonusNum = bonusNum

    def update(self):
        if self.timer > 0: 
            self.timer -= 1
        else: 
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(imgTanks) - 1:
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
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.index -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.index += 1
        if self.index > 2:
            self.index = 0
        if self.index < 0:
            self.index = 2
            
    
    def draw(self):
        window.blit(mimgCursor, (150, 208 + self.index * 27))
        
        
bullets = []
objects = []

ui = UI()
cur = Cursor()
def draw_map(levels, mode):
    if mode == 0:
        Tank('blue', 160, 416, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), True)
    if mode == 1:
        Tank('blue', 160, 416, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), True)
        Tank('red', 288, 416, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_k), True)      
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
                elif el == 9:
                    Block(x, y, TILE, 'emblem')            
                x += TILE
            y += TILE    
        
def draw_design():
    pygame.draw.rect(window, 'gray', (0, 0, 32, 448))
    pygame.draw.rect(window, 'gray', (0, 0, 480, 32))
    pygame.draw.rect(window, 'gray', (0, 448, 480, 32))
    pygame.draw.rect(window, 'gray', (448, 0, 64, 480))
    
def draw_menu():
    window.blit(mimgFlow, (0, 40))
    
bonusTimer = 1600
new_map = True
mainMenu = True
play = True
fpsm = 10
mode = 100

while play:
    if mainMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            mode = cur.index
            mainMenu = False
        cur.update()
        window.fill('black')
        draw_menu()
        cur.draw()
        pygame.display.update()
        clock.tick(fpsm)        
    else:
        if new_map:
            draw_map(0, mode)
            new_map = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
    
        keys = pygame.key.get_pressed()
    
        if bonusTimer > 0: bonusTimer -= 1
        else:
            Bonus(randint(50, 400), randint(50, 400), randint(0, len(imgBonuses) - 1))
            bonusTimer = 1600
        
        for bullet in bullets: bullet.update()
        for obj in objects: obj.update()
        ui.update()
    
        window.fill('black')
        draw_design()
        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()
        ui.draw()
        
        pygame.display.update()
        clock.tick(FPS)
    
pygame.quit()
