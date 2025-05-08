# Sprite classes for platform game
import pygame as pg
import spritesheet
import random
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self._layer = PLAYER_LAYER
        self.game = game
        self.idle_img = []
        self.run_img_r=[]
        self.run_img_l=[]
        self.jump_img = []
        self.running = False
        self.jumping = False
        self.load_images()
        self.image= self.idle_img[0]
        # self.image = pg.Surface((30, 40))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_update = 0
        self.current_frame = 0

    def animated(self):
        now =pg.time.get_ticks()
        if int(self.vel.x) != 0:
            self.running = True
        else:
            self.running = False
        if not self.running and not self.jumping:
            if now - self.last_update>225:
                self.last_update=now
                self.current_frame = (self.current_frame+1)%len(self.idle_img)
                self.image = self.idle_img[self.current_frame]
                self.rect = self.image.get_rect()
        if self.jumping:
            if now - self.last_update > 225:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_img)
                self.image = self.jump_img[self.current_frame]
                self.rect = self.image.get_rect()
            # self.image = self.jump_img[self.current_frame]
            # self.rect = self.image.get_rect()

        if self.running:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_img_r)
                if self.vel.x >0:
                    self.image = self.run_img_r[self.current_frame]
                else:
                    self.image = self.run_img_l[self.current_frame]
                self.rect = self.image.get_rect()

    def load_images(self):
        sprite_sheet_image = pg.image.load('sprite_sheet.png')
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        # size = 1
        i = 1
        for x in range(6):
            for y in range(7):
                # 426X629
                if y==4 and x>2 and x <6:
                    self.idle_img.append(sprite_sheet.get_image(x, y, 457/6, 515/7, 1, BLACK))
                    image = sprite_sheet.get_image(x, y, 457/6, 546/7, 1, BLACK)
                    image.set_colorkey(BLACK)
                if y==2 and x <6:
                    img = sprite_sheet.get_image(x, y, 457 / 6, 475 / 7, 1, BLACK)
                    img = pg.transform.flip(img,True,False)
                    img.set_colorkey(BLACK)
                    self.run_img_r.append(img)
                    self.run_img_l.append(sprite_sheet.get_image(x, y, 457 / 6, 475 / 7, 1, BLACK))
                    # image = sprite_sheet.get_image(x, y, 457 / 6, 546 / 7, 1, BLACK)
                    # image.set_colorkey(BLACK)
                # if y == 3  and x <2:
                #     self.jump_img.append(sprite_sheet.get_image(x, y, 500 / 6, 530/ 7, 1, BLACK))
        for i in range(1, 3):

            filename = "jump{}.png".format(i)
            img = pg.image.load(filename)
            img.set_colorkey(BLACK)
            #img = pg.transform.scale(img,(self.width,self.height))
            self.jump_img.append(img)
            #
        # for frame in self.run_img_r:
        #     self.run_img_r.append(pg.transform.flip(frame,True,False))

    # def load_images(self):
    #     for i in range(1,4):
    #         filename = "hulk{}.png".format(i)
    #         img = pg.image.load(filename)
    #         img = pg.transform.scale(img,(80,90))
    #         self.idle_img.append(img)
    #     for i in range(1, 7):
    #             filename = "run{}.png".format(i)
    #             img = pg.image.load(filename)
    #             img = pg.transform.scale(img,(80,90))
    #             self.run_img_r.append(img)
    #     for frame in self.run_img_r:
    #         self.run_img_l.append(pg.transform.flip(frame,True,False))
    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.jumping = True
            self.vel.y = -20

    def update(self):
        self.animated()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):

    def __init__(self, x, y, w, h):
        self._layer = PLATFORM_LAYER
        pg.sprite.Sprite.__init__(self)
        # self.plat_img = []
        # self.load_images()

        # self.image = random.choice(self.plat_img)
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)

        self.image = pg.image.load("iced platform.png")
        self.image = pg.transform.scale(self.image, (w, h))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # def load_images(self):
    #     for i in range(1,5):
    #         filename = "platform{}.PNG".format(i)
    #         img = pg.image.load(filename)
    #         #img = pg.transform.scale(img.(self.width.self/.height))
    #         self.plat_img.append(img)

class Snow(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.w = random.randrange(1,4)
        self.h = random.randrange(1,4)


        self.image = pg.Surface((self.w, self.h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()


        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(-500,-50)
        self.speedy = random.randrange(1,5)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top> HEIGHT:
            self.rect.x = random.randrange(WIDTH)
            self.rect.y = random.randrange(-500, -50)


class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
                self.groups = game.all_sprites, game.powerups
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.plat = plat
                self.type = random.choice(['boost'])
                self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.centerx = self.plat.rect.centerx
                self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
                    self.kill()