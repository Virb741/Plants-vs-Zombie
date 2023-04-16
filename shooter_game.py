from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('ost.mp3')
mixer.music.play()
fire_sound = mixer.Sound('pew.ogg')
zombie_sound = mixer.Sound('mob1.ogg')
money = mixer.Sound('brawl.sound.ogg')
fail = mixer.Sound('fail.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 50)
win = font1.render("PLANTS WIN!", True, (0,255,0))
lose = font1.render('ZOMBIES WIN!', True, (180,0,0))
agn = font3.render('try again?', True, (255, 255, 255))



img_back = "back.png"
img_hero = "plant.png"
img_enemy = "zomb.png"
img_bullet = "pea.png"
img_ast = "opex.png"
img_bus = "buster.png"



life = 3
score = 0
goal =20
lost = 0
max_lost = 4
speed = 10


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite. __init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 20, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Buster(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0



win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Plants vz Zombies")
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 5, win_height - 100, 70, 80, speed)

monsters = sprite.Group()
for i in range(1,4):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -60, 90, 100, randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1):
    asteroid = Asteroid(img_ast, randint(80, win_width - 80), -60, 60,70, 5)
    asteroids.add(asteroid)

busters = sprite.Group()
for i in range(1):
    buster = Buster(img_bus, randint(80, win_width - 80), -60, 40,50, 4)
    busters.add(buster)


bullets = sprite.Group()


game = True
finish = False 
clock = time.Clock()
FPS = 60
rel_time = 0
num_fire = 0


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if not finish:
        window.blit(background,(0,0))
        text = font2.render("Счет:" + str(score), 1, (255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10,50))
        if life == 3:
            life_color = (0,200,0)
        elif life == 2:
            life_color = (200,200,0)
        elif life == 1:
            life_color = (200,0,0)
        lif = font1.render(''+str(life),1, life_color)
        window.blit(lif, (610,30))

        ship.update()
        monsters.update()
        asteroids.update()
        busters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        busters.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            zombie_sound.play()
            monster = Enemy(img_enemy, randint(80, win_width - 80), -60, 90, 100, randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(ship, busters, False):
            sprite.spritecollide(ship, busters, True)
            speed = speed + 2
            ship = Player(img_hero, ship.rect.centerx, ship.rect.top, 70, 80, speed)
            buster = Buster(img_bus, randint(80, win_width - 80), -60, 40,50, 3)
            busters.add(buster)

        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life -= 1

        if sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            life -= 1
            asteroid = Asteroid(img_ast, randint(80, win_width - 80), -60, 60,70, 5)
            asteroids.add(asteroid)

        if life == 0 or lost >= max_lost:
            finish = True
            mixer.music.pause()
            fail.play()
            window.blit(lose, (160, 210))
            window.blit(agn, (240, 380))

        if score >= goal:
            finish = True
            mixer.music.pause()
            money.play()
            window.blit(win, (160, 210))
            window.blit(agn, (240, 380))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        speed = 10
        mixer.music.unpause()
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1,4):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -60, 90, 100, randint(1,4))
            monsters.add(monster)
        for i in range(1):
            asteroid = Asteroid(img_ast, randint(80, win_width - 80), -60, 60,70, 5)
            asteroids.add(asteroid)
        for i in range(1):
            buster = Buster(img_bus, randint(80, win_width - 80), -60, 60,70, 5)
            busters.add(buster)


    time.delay(40)