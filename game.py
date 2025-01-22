import pygame as py
import sys
sys.path.append(".")
from vector import vec
#colors are 00BEC5 FF0BAC 54086B 050833
#they are blue, pink, purple, and black in order
py.init()
clock = py.time.Clock()
win = py.display.set_mode((1000, 1000))
running = True
arispritesheet = py.image.load("parsimonious-pistol-playoffs\\playerspritesheet.png").convert()
bulletspritesheet = py.image.load("parsimonious-pistol-playoffs\\bulletspritesheet.png").convert()
bulletspritesheet.set_colorkey((0, 255, 255))
bullettypedict = {"frag": vec(8, 0), "square": vec(16, 0), "player": vec(0, 16), "heavy": vec(0, 8)}
bulletlist = []
colors = [(0, 190, 197), (255, 11, 172), (84, 8, 107), (5, 8, 51)]
epoch = 0
gamestate = "playing"
class PhysicsObject:
    def __init__(self, pos: vec, vel: vec, acc: vec, size: vec):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.size = size
        self.rect = py.Rect(pos.x, pos.y, size.x, size.y)
    def updatePos(self):
        self.vel += self.acc
        self.pos += self.vel
        self.vel *= 0.9
        self.acc *= 0.8
        self.rect = py.Rect(self.pos.x - self.size.x/2, self.pos.y - self.size.y/2, self.size.x, self.size.y)
class Projectile(py.sprite.Sprite):
    def __init__(self, pos: vec, vel: vec, damage:int, type: str):
        self.pos = pos
        self.vel = vel
        self.type = type
        self.damage = damage
        self.age = 0
        self.exists = True
    def updatePos(self):
        self.pos += self.vel
        self.age += 1
        self.rect = (self.pos.x, self.pos.y, 8, 8)
        if self.age > 60 and "frag" in self.type:
            for i in range(8):
                bulletlist.append(Projectile(self.pos, (self.vel * 0.3).rot(45*i), self.damage//2, [x for x in self.type if x != "frag"]))
            bulletlist[:] = [x for x in bulletlist if x != self]
        if not py.Rect(8, 8, 984, 984).colliderect(self.rect):
            bulletlist[:] = [x for x in bulletlist if x != self]
        if ari.rect.colliderect(self.rect) and not "player" in self.type:
            ari.health -= 1
            bulletlist[:] = [x for x in bulletlist if x != self]
    def draw(self):
        dest = vec(0, 0)
        for i in self.type:
            dest += bullettypedict[i]
        win.blit(bulletspritesheet, tuple(self.pos), py.Rect(dest.x, dest.y, 8, 8))
class Player(PhysicsObject):
    def __init__(self, pos, vel, acc, direc: vec, size=vec(32, 32)):
        super().__init__(pos, vel, acc, size)
        self.direc = direc
        self.size = vec(32, 32)
        self.health = 10
        self.gun = None
        self.item1 = None
        self.item2 = None
    def update(self):
        self.direc = vec(0, 0)
        keys = py.key.get_pressed()
        if keys[py.K_w]:
            self.direc.y -= 1
            self.acc.y -= 0.1
        if keys[py.K_a]:
            self.direc.x -= 1
            self.acc.x -= 0.1
        if keys[py.K_s]:
            self.direc.y += 1
            self.acc.y += 0.1
        if keys[py.K_d]:
            self.direc.x += 1
            self.acc.x += 0.1
        self.vel += self.acc
        self.pos += self.vel
        self.vel *= 0.9
        self.acc *= 0.8
        if ari.pos.x > 1000 and ari.direc.x > 0:
            ari.pos.x -= 999
        if ari.pos.x < 0 and ari.direc.x < 0:
            ari.pos.x += 999
        if ari.pos.y > 1000 and ari.direc.y > 0:
            ari.pos.y -= 999
        if ari.pos.y < 0 and ari.direc.y < 0:
            ari.pos.y += 999
        self.rect = py.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
    def draw(self):
        if not self.rect.colliderect(32, 32, 936, 936):
            for i in range(9):
                win.blit(arispritesheet, tuple(self.pos + vec((i//3 - 1) * 1000, (i%3 - 1) * 1000)), (32 * (1 + self.direc.x), 32 * (1 + self.direc.y), 32, 32))
        else:
            win.blit(arispritesheet, tuple(self.pos), (32 * (1 + self.direc.x), 32 * (1 + self.direc.y), 32, 32))
ari = Player(vec(500, 500), vec(0, 0), vec(0, 0), vec(0, 0))
class Gun():
    def __init__(self, pos: vec, damage: int, rps: float, muzzlevel: float, cartridge: int, rarity: int, bullettype: list, tooltip: str):
        self.pos = pos
        self.damage = damage
        self.rps = rps
        self.muzzlevel = muzzlevel
        self.cartridge = cartridge
        self.rarity = rarity
        self.tooltip = tooltip
        self.bullettype = bullettype
        self.lastfiredepoch = 0
        #bulletnumber is the amount of bullets that come out when fired once, NOT THE CURRENT AMOUNT OF AMMO.
        #rps is Rounds Per Second, not rock paper scissors lmao
        #damage, rps and cartridge are turned into flat numbers
        #bulletnumber is apparent from the type of gun (shotgun vs anything else)
        #rarity is turned into a single capital letter, Common, Uncommon, Rare, Epic, and Legendary
        #idee is a single string that everything else can be extracted from.
    def fire(self):
        if epoch - self.lastfiredepoch > 60/self.rps:
            bulletlist.append(Projectile(self.pos, (vec(py.mouse.get_pos()[0], py.mouse.get_pos()[1]) - ari.pos).norm(self.muzzlevel), self.damage, self.bullettype))
            self.lastfiredepoch = epoch 
while running:
    clock.tick(60)
    epoch += 1
    keys = py.key.get_pressed()
    mouse = py.mouse.get_pressed()
    mousepos = vec(py.mouse.get_pos()[0], py.mouse.get_pos()[1])
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            running = False
    if keys[py.K_q]:
        running = False
    if gamestate == "menu":
        pass
    if gamestate == "playing":
        ari.update()
        if mouse[0]:
            bulletlist.append(Projectile(ari.pos, (mousepos-ari.pos).norm(2), 2, ["player", "frag"]))
        for bullet in bulletlist:
            bullet.updatePos()
        win.fill((245, 213, 240))
        for bullet in bulletlist:
            bullet.draw()
        ari.draw()
        py.display.update()