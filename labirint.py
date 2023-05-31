from pygame import *
font.init()
speed = 10
fon = display.set_mode((1000, 700))
display.set_caption('Лабиринт')
fon.fill((221,160,221))

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, w, h, pic):
        super().__init__()
        self.image = transform.scale(image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        fon.blit(self.image, (self.rect.x, self.rect.y))
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    def load(self, pic):
        self.image = transform.scale(image.load(pic), (self.w, self.h))

class Player(GameSprite):
    def __init__(self, x, y, w, h, pic, speed_x, speed_y):
        GameSprite.__init__(self, x, y, w, h, pic)
        self.w = w
        self.h = h
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        if self.rect.x >= 5 or self.rect.x <=920 and self.rect.y >= 5 or self.rect.y <= 670:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x < 5 or self.rect.x > 920 and self.rect.y < 5 or self.rect.y > 670:
            player.rect.x = 90
            player.rect.y = 550
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x != 0:
            for p in platforms_touched:
                self.rect.x -= self.speed_x
                # self.rect.right = min(self.rect.right, p.rect.left)
        #elif self.speed_x < 0: 
            #for p in platforms_touched:
                #self.rect.x -= self.speed_x
                #self.rect.left = max(self.rect.left, p.rect.right) 
        if self.speed_y != 0:
            for p in platforms_touched:
                self.rect.y -= self.speed_y
                #self.rect.bottom = min(self.rect.bottom, p.rect.top)
        #elif self.speed_y < 0:
            #for p in platforms_touched:
                #self.rect.y -= self.speed_y
                #self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet(self.rect.right, self.rect.centery, 15, 20, 10, 'weapon.png')
        bullets.add(bullet)
    def fire_1(self):
        bullet = Bullet(self.rect.left, self.rect.centery, 15, 20, -10, 'weapon_2.png')
        bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self, x, y, w, h, speed, pic):
        GameSprite.__init__(self, x, y, w, h, pic)
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 1000 and self.rect.x <= 0:
            self.kill()

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, pic, speed, left, right, up, down):
        GameSprite.__init__(self, x, y, w, h, pic)       
        self.w = w
        self.h = h
        self.speed = speed
        self.direction_x = 'left'
        self.direction_y = 'down'
        self.left = left
        self.right = right
        self.up = up
        self.down = down
    def update(self):
        #по оси x
        if self.rect.x >= self.right:
            self.direction_x = 'left'
            self.load('enemy_2.png')
        elif self.rect.x <= self.left:
            self.direction_x = 'right'
            self.load('enemy.png')
        if self.direction_x == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        #по оси y
        if self.rect.y <= self.up:
            self.direction_y = 'down'
        elif self.rect.y >= self.down:
            self.direction_y = 'up'
        if self.direction_y == 'down':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        
game_over = GameSprite(50, 350, 466, 42, 'game_over.jpg')
next_lvl = GameSprite(50, 450, 400, 32, 'next_lvl.jpg')

wall_1 = GameSprite(250, 400, 50, 400, 'platform_h.png') #горизонтальная
wall_2 = GameSprite(250, 370, 300, 50, 'platform_v.png') #вертикальная
wall_3 = GameSprite(0, 160, 300, 50, 'platform_v.png')
wall_4 = GameSprite(500, 170, 50, 250, 'platform_v.png')
wall_5 = GameSprite(495, 170, 270, 50, 'platform_h.png')
wall_6 = GameSprite(750, 370, 330, 50, 'platform_h.png')

final = GameSprite(900, 600, 80, 80, 'door.png')
player = Player(100, 550, 80, 80, 'hero.png', 0, 0)
enemy = Enemy(700, 500, 80, 80, 'enemy.png', 3, 600, 800, 420, 600)
enemy_2 = Enemy(850, 150, 50, 50, 'enemy.png', 3, 780, 900, 100, 200)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)
barriers.add(wall_4)
barriers.add(wall_5)
barriers.add(wall_6)

bullets = sprite.Group()

enemies = sprite.Group()
enemies.add(enemy)
enemies.add(enemy_2)

finish = False
run = True
direc = 'right'
while run:
    time.delay(40)
    if finish == False:
        fon.fill((221,160,221))
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos #получаем координаты клика мыши
            if game_over.collidepoint(x, y):
                finish = False
                player.rect.x, player.rect.y = 90, 550
                enemies.add(enemy)
                enemies.add(enemy_2)
                
        elif e.type == KEYUP: #управление героем
            player.speed_x = 0
            player.speed_y = 0
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.speed_y -= speed
            elif e.key == K_a:
                player.speed_x -= speed
                direc = 'left'
                player.load('hero_2.png')
            elif e.key == K_s:
                player.speed_y += speed
            elif e.key == K_d:
                player.speed_x += speed
                direc = 'right'
                player.load('hero.png')
        
        if e.type == KEYDOWN: #стрельба
            if e.key == K_SPACE:
                if direc == 'right':
                    player.fire()
                elif direc == 'left':
                    player.fire_1()
    
    if not finish:

        barriers.draw(fon)
        enemies.draw(fon)
        bullets.draw(fon)
        final.reset()
        player.reset()
        player.update()
        enemies.update()
        bullets.update()
        #проверка столкновений спрайтов
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, enemies, True, True)
        
        if sprite.collide_rect(player, final):
            finish = True
            img = image.load('win.jpg')
            fon.fill((255, 255, 255))
            img = transform.scale(img, (1000, 700))
            fon.blit(img, (0,0))
            game_over.reset()
            next_lvl.reset()

        elif sprite.spritecollide(player, enemies, False):
            finish = True
            img = image.load('lose.jpg')
            fon.fill((255, 255, 255))
            img = transform.scale(img, (1000, 700))
            fon.blit(img, (0,0))
            game_over.reset()
            next_lvl.reset()
               

    display.update()