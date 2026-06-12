"""
╔══════════════════════════════════════════════════════════╗
║         DRAGON SIEGE: ARCANE SKIES                       ║
║         A Fantasy Space Shooter - Final Project          ║
║         Python 3.x + Pygame                              ║
╚══════════════════════════════════════════════════════════╝
"""

import pygame
import sys
import os
import json
import random
import math
import time

# ─── SETUP ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "savegame.json")

pygame.init()
pygame.mixer.init()

# ─── CONSTANTS ────────────────────────────────────────────
SW, SH = 900, 700
FPS = 60
TITLE = "DRAGON SIEGE: ARCANE SKIES"

# Colors
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GOLD    = (255, 215,   0)
DARK_GOLD=(180, 140,   0)
PURPLE  = (120,  40, 200)
DPURPLE = ( 60,  10, 120)
CYAN    = (  0, 220, 255)
RED     = (220,  30,  30)
ORANGE  = (255, 140,   0)
GREEN   = ( 50, 220,  80)
DGREEN  = ( 20, 140,  40)
BLUE    = ( 40, 100, 240)
LBLUE   = (100, 180, 255)
PINK    = (255,  80, 180)
GRAY    = (120, 120, 140)
DGRAY   = ( 40,  40,  60)
TEAL    = (  0, 200, 180)
FIRE1   = (255,  80,   0)
FIRE2   = (255, 200,   0)
ICE1    = (180, 230, 255)
BG_TOP  = (  5,   5,  25)
BG_BOT  = ( 20,   5,  50)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# ─── ASSET GENERATION (pure pygame drawing) ───────────────
def make_surface(w, h): return pygame.Surface((w, h), pygame.SRCALPHA)

class Assets:
    """All sprites drawn programmatically — no external files needed."""

    @staticmethod
    def wizard(frame=0):
        s = make_surface(48, 64)
        # Robe
        pygame.draw.polygon(s, DPURPLE, [(24,16),(6,60),(42,60)])
        pygame.draw.polygon(s, PURPLE,  [(24,16),(10,56),(38,56)])
        # Stars on robe
        for sx,sy in [(18,35),(30,40),(22,50)]:
            pygame.draw.circle(s, GOLD, (sx,sy), 2)
        # Arms
        pygame.draw.ellipse(s, PURPLE, (2,28,10,20))
        pygame.draw.ellipse(s, PURPLE, (36,28,10,20))
        # Head
        pygame.draw.circle(s, (230,190,140), (24,18), 12)
        # Hat
        pygame.draw.polygon(s, DPURPLE, [(24,0),(14,14),(34,14)])
        pygame.draw.rect(s, PURPLE, (10,13,28,5))
        # Hat star
        pygame.draw.circle(s, GOLD, (24,4), 2)
        # Eyes
        pygame.draw.circle(s, CYAN, (20,17), 2)
        pygame.draw.circle(s, CYAN, (28,17), 2)
        # Beard
        pygame.draw.polygon(s, WHITE, [(18,24),(30,24),(27,32),(24,28),(21,32)])
        # Staff (right hand)
        pygame.draw.line(s, (120,80,30), (38,32),(44,56), 3)
        # Orb on staff
        r = 2 + int(math.sin(frame*0.3)*1.5)
        pygame.draw.circle(s, CYAN, (44,30), r+2)
        pygame.draw.circle(s, WHITE, (44,30), r)
        # Thrust animation
        if frame % 10 < 5:
            pygame.draw.polygon(s, FIRE2, [(20,60),(28,60),(24,68)])
            pygame.draw.polygon(s, FIRE1, [(22,60),(26,60),(24,65)])
        return s

    @staticmethod
    def dragon_small(color=RED, frame=0):
        s = make_surface(56, 40)
        # Body
        pygame.draw.ellipse(s, color, (16,12,28,20))
        # Head
        pygame.draw.ellipse(s, color, (36,8,18,16))
        # Snout
        pygame.draw.ellipse(s, (max(0,color[0]-40), max(0,color[1]-20), max(0,color[2]-20)), (50,11,8,8))
        # Eye
        pygame.draw.circle(s, GOLD, (48,12), 3)
        pygame.draw.circle(s, BLACK, (49,12), 1)
        # Wings
        wing_off = int(math.sin(frame*0.25)*4)
        pygame.draw.polygon(s, (min(255,color[0]+40),color[1],color[2]),
            [(20,14),(2,4-wing_off),(8,18)])
        pygame.draw.polygon(s, (min(255,color[0]+40),color[1],color[2]),
            [(20,26),(2,36+wing_off),(8,22)])
        # Tail
        pygame.draw.lines(s, color, False, [(16,20),(8,22),(2,28),(0,32)], 3)
        # Claws
        pygame.draw.line(s, BLACK, (32,30),(28,38), 2)
        pygame.draw.line(s, BLACK, (36,30),(34,38), 2)
        return s

    @staticmethod
    def dragon_medium(color=ORANGE, frame=0):
        s = make_surface(80, 56)
        pygame.draw.ellipse(s, color, (20,18,44,26))
        pygame.draw.ellipse(s, color, (54,10,26,22))
        pygame.draw.ellipse(s, (max(0,color[0]-40),max(0,color[1]-30),0), (76,14,10,10))
        pygame.draw.circle(s, GOLD, (72,14), 4)
        pygame.draw.circle(s, BLACK, (73,14), 2)
        wing_off = int(math.sin(frame*0.2)*5)
        pygame.draw.polygon(s, (min(255,color[0]+50),max(0,color[1]-20),0),
            [(28,20),(2,2-wing_off),(12,26)])
        pygame.draw.polygon(s, (min(255,color[0]+50),max(0,color[1]-20),0),
            [(28,38),(2,56+wing_off),(12,32)])
        pygame.draw.lines(s, color, False, [(20,26),(10,30),(4,38),(0,44)], 4)
        for cx,cy in [(42,44),(48,44),(54,44)]:
            pygame.draw.line(s, (80,80,80), (cx,42),(cx-2,52), 2)
        return s

    @staticmethod
    def boss_dragon(frame=0):
        s = make_surface(160, 120)
        # Body
        pygame.draw.ellipse(s, (160,10,10), (30,40,100,60))
        pygame.draw.ellipse(s, (200,20,20), (35,45,90,50))
        # Belly scales
        for i in range(6):
            pygame.draw.ellipse(s, (220,60,60), (50+i*10,65,8,12))
        # Head
        pygame.draw.ellipse(s, (160,10,10), (110,20,50,44))
        pygame.draw.polygon(s, (140,5,5), [(130,20),(160,10),(155,26)])  # horn1
        pygame.draw.polygon(s, (140,5,5), [(140,18),(165,14),(158,28)])  # horn2
        # Eyes (glowing)
        pygame.draw.circle(s, FIRE2, (128,34), 8)
        pygame.draw.circle(s, FIRE1, (128,34), 5)
        pygame.draw.circle(s, BLACK,  (128,34), 2)
        pygame.draw.circle(s, FIRE2, (148,30), 6)
        pygame.draw.circle(s, FIRE1, (148,30), 4)
        pygame.draw.circle(s, BLACK,  (148,30), 2)
        # Snout
        pygame.draw.ellipse(s, (120,5,5), (152,36,20,14))
        # Teeth
        for tx in [156,162,168]:
            pygame.draw.polygon(s, WHITE, [(tx,46),(tx+3,46),(tx+1,52)])
        # Wings
        wo = int(math.sin(frame*0.15)*8)
        pygame.draw.polygon(s, (120,5,5),
            [(50,50),(2,2-wo),(0,60-wo),(30,70)])
        pygame.draw.lines(s, (80,5,5), False,
            [(50,50),(20,10-wo),(5,40-wo),(15,65-wo),(30,70)], 2)
        pygame.draw.polygon(s, (120,5,5),
            [(50,70),(2,118+wo),(0,58+wo),(30,50)])
        pygame.draw.lines(s, (80,5,5), False,
            [(50,70),(20,110+wo),(5,78+wo),(15,55+wo),(30,50)], 2)
        # Tail
        pts = [(30,80),(15,90),(5,100),(0,112),(4,118)]
        pygame.draw.lines(s, (160,10,10), False, pts, 6)
        pygame.draw.lines(s, (200,20,20), False, pts, 3)
        # Fire breath (random frames)
        if frame % 8 < 4:
            for i in range(5):
                fx = 160 + random.randint(-4,4)
                fy = 42 + random.randint(-3,3)
                r  = random.randint(4,10)
                c  = random.choice([FIRE1, FIRE2, (255,255,100)])
                pygame.draw.circle(s, c, (fx,fy), r)
        return s

    @staticmethod
    def bullet_player(spell_type=0):
        s = make_surface(12, 24)
        if spell_type == 0:   # Arcane bolt
            pygame.draw.ellipse(s, CYAN,   (2,4,8,16))
            pygame.draw.ellipse(s, WHITE,  (4,6,4,12))
            pygame.draw.circle(s, LBLUE,   (6,4),  4)
        elif spell_type == 1: # Fire ball
            pygame.draw.circle(s, FIRE1,   (6,12), 6)
            pygame.draw.circle(s, FIRE2,   (6,12), 4)
            pygame.draw.circle(s, WHITE,   (6,12), 2)
        elif spell_type == 2: # Ice shard
            pygame.draw.polygon(s, ICE1,   [(6,0),(2,16),(10,16)])
            pygame.draw.polygon(s, WHITE,  [(6,4),(4,12),(8,12)])
        elif spell_type == 3: # Lightning
            pygame.draw.lines(s, GOLD, False, [(6,0),(3,8),(8,8),(4,16),(7,24)], 3)
            pygame.draw.lines(s, WHITE,False, [(6,0),(3,8),(8,8),(4,16),(7,24)], 1)
        return s

    @staticmethod
    def fireball_enemy(size=8):
        s = make_surface(size*3, size*3)
        cx = cy = size + size//2
        pygame.draw.circle(s, (255,60,0),  (cx,cy), size)
        pygame.draw.circle(s, (255,160,0), (cx,cy), size-2)
        pygame.draw.circle(s, (255,255,100),(cx,cy),size-4)
        return s

    @staticmethod
    def particle(color, size):
        s = make_surface(size*2, size*2)
        pygame.draw.circle(s, color, (size,size), size)
        return s

    @staticmethod
    def powerup(kind):
        s = make_surface(28,28)
        cx,cy = 14,14
        if kind == 'hp':
            pygame.draw.circle(s, (200,20,20), (cx,cy), 12)
            pygame.draw.rect(s, WHITE, (cx-2,cy-6,4,12))
            pygame.draw.rect(s, WHITE, (cx-6,cy-2,12,4))
        elif kind == 'mana':
            pygame.draw.circle(s, (40,40,200), (cx,cy), 12)
            pygame.draw.polygon(s, CYAN, [(cx,cy-8),(cx-7,cy+4),(cx+7,cy+4)])
        elif kind == 'spell':
            pygame.draw.circle(s, (120,40,180), (cx,cy), 12)
            pygame.draw.circle(s, GOLD, (cx,cy), 6)
            pygame.draw.circle(s, WHITE,(cx,cy), 3)
        elif kind == 'shield':
            pygame.draw.circle(s, (40,100,200), (cx,cy), 12)
            pygame.draw.arc(s, CYAN, (cx-8,cy-8,16,16), 0.5, 2.6, 3)
        elif kind == 'bomb':
            pygame.draw.circle(s, (60,60,60), (cx,cy), 12)
            pygame.draw.circle(s, ORANGE, (cx,cy), 7)
            pygame.draw.line(s, GOLD, (cx,cy-7),(cx+4,cy-12), 2)
        return s

    @staticmethod
    def star_bg(n=200):
        """Return list of (x,y,size,brightness) tuples."""
        return [(random.randint(0,SW), random.randint(0,SH),
                 random.choice([1,1,1,2,2,3]),
                 random.randint(100,255)) for _ in range(n)]

    @staticmethod
    def castle_silhouette():
        s = make_surface(SW, 140)
        # Draw distant castle
        def tower(sx, h, w):
            pygame.draw.rect(s, (30,10,60), (sx, 140-h, w, h))
            # Battlements
            for bx in range(sx, sx+w, 8):
                pygame.draw.rect(s, (30,10,60), (bx, 140-h-8, 6, 8))
            # Window
            pygame.draw.rect(s, (80,40,140), (sx+w//2-3, 140-h+10, 6, 10))
        tower(60, 80, 30)
        tower(100,110, 40)
        tower(148, 70, 25)
        tower(600, 90, 35)
        tower(640,120, 45)
        tower(690, 75, 28)
        # Main keep
        pygame.draw.rect(s, (25,8,50), (350,60,200,80))
        for bx in range(350,550,10):
            pygame.draw.rect(s, (25,8,50),(bx,50,8,12))
        pygame.draw.polygon(s, (40,10,80), [(440,20),(450,60),(430,60)])
        # Moon
        pygame.draw.circle(s, (220,210,180), (760,30), 30)
        pygame.draw.circle(s, BG_TOP,        (770,24), 26)
        return s

# ─── PARTICLE SYSTEM ──────────────────────────────────────
class Particle:
    def __init__(self, x, y, vx, vy, color, size, life):
        self.x,self.y = x,y
        self.vx,self.vy = vx,vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1
        self.size = max(1, self.size * (self.life / self.max_life))
        return self.life > 0

    def draw(self, surf):
        alpha = int(255 * self.life / self.max_life)
        col = (*self.color[:3], alpha)
        s = make_surface(int(self.size*2)+1, int(self.size*2)+1)
        pygame.draw.circle(s, col, (int(self.size),int(self.size)), int(self.size))
        surf.blit(s, (int(self.x-self.size), int(self.y-self.size)))

def explosion(particles, x, y, color, count=20, speed=4):
    for _ in range(count):
        ang = random.uniform(0, 2*math.pi)
        spd = random.uniform(1, speed)
        particles.append(Particle(x,y,
            math.cos(ang)*spd, math.sin(ang)*spd,
            color, random.uniform(2,7), random.randint(20,50)))

# ─── BULLETS ──────────────────────────────────────────────
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, spell_type=0, angle=0):
        super().__init__()
        self.spell_type = spell_type
        self.image = Assets.bullet_player(spell_type)
        self.rect  = self.image.get_rect(midbottom=(x,y))
        speed = [14, 10, 13, 16][spell_type]
        self.vx = math.sin(angle) * speed
        self.vy = -math.cos(angle) * speed
        self.damage = [20, 35, 25, 15][spell_type]
        self.pierce = spell_type == 3   # lightning pierces

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.bottom < 0 or self.rect.top > SH or
            self.rect.right < 0 or self.rect.left > SW):
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, tx, ty, speed=4, size=10, big=False):
        super().__init__()
        self.image = Assets.fireball_enemy(size)
        self.rect  = self.image.get_rect(center=(x,y))
        dx,dy = tx-x, ty-y
        dist  = max(1, math.hypot(dx,dy))
        self.vx = dx/dist * speed
        self.vy = dy/dist * speed
        self.damage = 25 if not big else 40

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if (self.rect.bottom < 0 or self.rect.top > SH+20 or
            self.rect.right < 0 or self.rect.left > SW+20):
            self.kill()

# ─── PLAYER ───────────────────────────────────────────────
class Player(pygame.sprite.Sprite):
    SPELLS = ['Arcane Bolt','Fireball','Ice Shard','Lightning']
    SPELL_MANA = [5, 15, 10, 20]
    SPELL_COLORS= [CYAN, FIRE1, ICE1, GOLD]

    def __init__(self):
        super().__init__()
        self.frame   = 0
        self.image   = Assets.wizard(0)
        self.rect    = self.image.get_rect(midbottom=(SW//2, SH-20))
        self.hp      = 100
        self.max_hp  = 100
        self.mana    = 100
        self.max_mana= 100
        self.speed   = 5
        self.score   = 0
        self.lives   = 3
        self.shield  = 0          # frames of invincibility
        self.spell   = 0          # active spell index
        self.spells_unlocked = [True, False, False, False]
        self.shoot_cd= 0
        self.bomb_count = 2
        self.spread  = False       # powerup: spread shot
        self.spread_timer = 0
        self.invincible= 0
        self.anim_timer= 0

    def get_image(self):
        self.anim_timer += 1
        if self.anim_timer % 4 == 0:
            self.frame += 1
        return Assets.wizard(self.frame)

    def update(self, keys, particles):
        # Movement
        dx = dy = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += self.speed
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += self.speed
        if dx and dy:
            dx *= 0.707; dy *= 0.707
        self.rect.x = max(0, min(SW-48, self.rect.x+dx))
        self.rect.y = max(0, min(SH-64, self.rect.y+dy))

        # Mana regen
        if self.mana < self.max_mana:
            self.mana = min(self.max_mana, self.mana + 0.08)

        # Timers
        if self.shoot_cd > 0: self.shoot_cd -= 1
        if self.invincible > 0: self.invincible -= 1
        if self.spread_timer > 0:
            self.spread_timer -= 1
            if self.spread_timer == 0: self.spread = False

        # Trail particles
        if random.random() < 0.3:
            c = self.SPELL_COLORS[self.spell]
            particles.append(Particle(
                self.rect.centerx + random.randint(-8,8),
                self.rect.bottom,
                random.uniform(-0.5,0.5), random.uniform(0.5,2),
                c, random.uniform(1,3), random.randint(10,20)))

        self.image = self.get_image()

    def shoot(self, bullets):
        if self.shoot_cd > 0: return
        if self.mana < self.SPELL_MANA[self.spell]: return
        self.mana -= self.SPELL_MANA[self.spell]
        cx,cy = self.rect.centerx, self.rect.top+10
        bullets.add(PlayerBullet(cx, cy, self.spell))
        if self.spread:
            bullets.add(PlayerBullet(cx, cy, self.spell, -0.25))
            bullets.add(PlayerBullet(cx, cy, self.spell,  0.25))
        self.shoot_cd = [6, 20, 10, 14][self.spell]

    def take_damage(self, dmg, particles):
        if self.invincible > 0: return
        self.hp -= dmg
        self.invincible = 90
        explosion(particles, self.rect.centerx, self.rect.centery,
                  ORANGE, 15, 3)
        if self.hp <= 0:
            self.hp = 0

    def use_bomb(self, enemy_bullets, enemies, particles):
        if self.bomb_count <= 0: return False
        self.bomb_count -= 1
        enemy_bullets.empty()
        for e in list(enemies):
            if not getattr(e, 'is_boss', False):
                explosion(particles, e.rect.centerx, e.rect.centery, FIRE1, 30, 6)
                e.kill()
        return True

    def cycle_spell(self, direction=1):
        start = self.spell
        for _ in range(4):
            self.spell = (self.spell + direction) % 4
            if self.spells_unlocked[self.spell]:
                return
        self.spell = start

# ─── ENEMIES ──────────────────────────────────────────────
class DragonSmall(pygame.sprite.Sprite):
    def __init__(self, x, y, color=RED):
        super().__init__()
        self.color = color
        self.frame = 0
        self.image = Assets.dragon_small(color, 0)
        self.rect  = self.image.get_rect(topleft=(x,y))
        self.hp    = 40
        self.speed = random.uniform(1.5, 2.5)
        self.shoot_cd = random.randint(60,120)
        self.score_val= 100
        self.move_angle= random.uniform(0, 2*math.pi)
        self.dive = False
        self.dive_target_y = random.randint(SH//4, SH//2)
        self.at_pos = False
        self.wave_offset = random.uniform(0, 2*math.pi)
        self.is_boss = False

    def update(self, player, enemy_bullets, particles):
        self.frame += 1
        if not self.at_pos:
            self.rect.y += 3
            if self.rect.y >= self.dive_target_y:
                self.at_pos = True
        else:
            self.rect.x += math.cos(self.frame*0.03 + self.wave_offset) * 2.5
            self.rect.y += math.sin(self.frame*0.02) * 0.8
        self.rect.x = max(-30, min(SW+30, self.rect.x))

        self.shoot_cd -= 1
        if self.shoot_cd <= 0:
            self.shoot_cd = random.randint(80,160)
            enemy_bullets.add(EnemyBullet(
                self.rect.centerx, self.rect.bottom,
                player.rect.centerx, player.rect.centery, 4))

        self.image = Assets.dragon_small(self.color, self.frame)
        if self.rect.top > SH+40:
            self.kill()

class DragonMedium(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame = 0
        self.color = ORANGE
        self.image = Assets.dragon_medium(ORANGE, 0)
        self.rect  = self.image.get_rect(topleft=(x,y))
        self.hp    = 120
        self.speed = random.uniform(1.0, 1.8)
        self.shoot_cd = random.randint(40,80)
        self.score_val= 300
        self.wave_offset = random.uniform(0,2*math.pi)
        self.dive_y = random.randint(SH//5, SH//3)
        self.at_pos = False
        self.is_boss = False
        self.shoot_count = 0

    def update(self, player, enemy_bullets, particles):
        self.frame += 1
        if not self.at_pos:
            self.rect.y += 2.5
            if self.rect.y >= self.dive_y:
                self.at_pos = True
        else:
            self.rect.x += math.cos(self.frame*0.025 + self.wave_offset)*3
            self.rect.y += math.sin(self.frame*0.015)*1.5

        self.shoot_cd -= 1
        if self.shoot_cd <= 0:
            self.shoot_cd = random.randint(50,100)
            # 3-way shot
            for ang in [-0.2, 0, 0.2]:
                enemy_bullets.add(EnemyBullet(
                    self.rect.centerx, self.rect.bottom,
                    player.rect.centerx + math.sin(ang)*200,
                    player.rect.centery + math.cos(ang)*200, 5))
        self.image = Assets.dragon_medium(self.color, self.frame)
        if self.rect.top > SH+60:
            self.kill()

class BossDragon(pygame.sprite.Sprite):
    PHASE_HP = [1.0, 0.6, 0.3]

    def __init__(self, level):
        super().__init__()
        self.frame   = 0
        self.image   = Assets.boss_dragon(0)
        self.rect    = self.image.get_rect(midtop=(SW//2, -130))
        self.max_hp  = 800 + level * 400
        self.hp      = self.max_hp
        self.phase   = 0
        self.shoot_cd= 0
        self.score_val= 5000 + level*1000
        self.entering= True
        self.target_y= 60
        self.is_boss = True
        self.direction= 1
        self.speed   = 1.5
        self.level   = level
        self.enrage  = False
        self.enrage_timer = 0
        self.shoot_pattern = 0

    def update(self, player, enemy_bullets, particles):
        self.frame += 1

        # Enter screen
        if self.entering:
            self.rect.y += 2
            if self.rect.y >= self.target_y:
                self.entering = False
            return

        # Phase transitions
        hp_ratio = self.hp / self.max_hp
        if hp_ratio < self.PHASE_HP[1] and self.phase == 0:
            self.phase = 1
            self.speed = 2.5
            explosion(particles, self.rect.centerx, self.rect.centery, RED, 40, 8)
        if hp_ratio < self.PHASE_HP[2] and self.phase == 1:
            self.phase = 2
            self.speed = 4
            self.enrage = True
            explosion(particles, self.rect.centerx, self.rect.centery, FIRE1, 60, 10)

        # Movement
        self.rect.x += self.speed * self.direction
        if self.rect.right >= SW-10 or self.rect.left <= 10:
            self.direction *= -1
        if self.phase >= 1:
            self.rect.y += math.sin(self.frame*0.05) * 2

        # Shooting
        self.shoot_cd -= 1
        cd = [40, 25, 15][self.phase]
        if self.shoot_cd <= 0:
            self.shoot_cd = cd
            self._shoot(player, enemy_bullets)

        self.image = Assets.boss_dragon(self.frame)

    def _shoot(self, player, enemy_bullets):
        cx,cy = self.rect.right+10, self.rect.centery
        px,py = player.rect.centerx, player.rect.centery
        pat = self.shoot_pattern % (3 + self.phase)
        self.shoot_pattern += 1

        if pat == 0:  # Aimed burst
            for _ in range(3):
                offset = random.randint(-40,40)
                enemy_bullets.add(EnemyBullet(cx,cy,px+offset,py+offset,6,10))
        elif pat == 1:  # Spread fan
            for i in range(5 + self.phase*2):
                ang = math.radians(-40 + i*16)
                tx = cx + math.cos(ang)*300
                ty = cy + math.sin(ang)*300
                enemy_bullets.add(EnemyBullet(cx,cy,tx,ty,5,8,big=self.phase>=2))
        elif pat == 2:  # Big fireball
            enemy_bullets.add(EnemyBullet(cx,cy,px,py,8,16,big=True))
        elif pat == 3:  # Spiral (phase 2+)
            for i in range(8):
                ang = math.radians(self.frame*10 + i*45)
                tx = cx+math.cos(ang)*200
                ty = cy+math.sin(ang)*200
                enemy_bullets.add(EnemyBullet(cx,cy,tx,ty,4,7))

# ─── POWERUPS ─────────────────────────────────────────────
class PowerUp(pygame.sprite.Sprite):
    KINDS = ['hp','mana','spell','shield','bomb']
    def __init__(self, x, y, kind=None):
        super().__init__()
        self.kind  = kind or random.choice(self.KINDS)
        self.image = Assets.powerup(self.kind)
        self.rect  = self.image.get_rect(center=(x,y))
        self.vy    = 1.5
        self.bob   = 0

    def update(self):
        self.bob   += 0.1
        self.rect.y += self.vy + math.sin(self.bob)*0.5
        if self.rect.top > SH+10:
            self.kill()

# ─── FORMATION SPAWNER ────────────────────────────────────
class FormationSpawner:
    def __init__(self, level):
        self.level  = level
        self.timer  = 0
        self.interval = max(60, 180 - level*10)
        self.wave   = 0

    def update(self, enemies, level):
        self.timer += 1
        if self.timer < self.interval: return
        self.timer = 0
        self.wave += 1
        pattern = self.wave % 6

        if pattern == 0:   # V formation
            for i in range(5):
                x = SW//2 + (i-2)*80
                y = -40 - abs(i-2)*40
                enemies.add(DragonSmall(x,y, random.choice([RED,(180,30,30),(200,50,50)])))
        elif pattern == 1: # Line
            for i in range(6):
                enemies.add(DragonSmall(80+i*130, -40))
        elif pattern == 2: # Diamond
            for x,y in [(SW//2,0),(SW//2-100,-50),(SW//2+100,-50),(SW//2,-100)]:
                enemies.add(DragonMedium(x,y))
        elif pattern == 3: # Swarm
            for _ in range(8):
                enemies.add(DragonSmall(random.randint(50,SW-50),-60,
                    random.choice([RED,ORANGE,(160,20,80)])))
        elif pattern == 4: # Escort
            enemies.add(DragonMedium(SW//2-50,-60))
            for i in range(4):
                x = SW//2-180+i*120 if i<2 else SW//2-60+(i-2)*120
                enemies.add(DragonSmall(x,-40))
        elif pattern == 5: # Flanks
            for i in range(3):
                enemies.add(DragonSmall(0, 120+i*80))
                enemies.add(DragonSmall(SW-56, 120+i*80))

# ─── HUD ──────────────────────────────────────────────────
def load_font(size, bold=False):
    try:
        return pygame.font.SysFont('segoeuisymbol,dejavusans,freesansbold', size, bold=bold)
    except:
        return pygame.font.SysFont(None, size, bold=bold)

FONT_LG  = load_font(48, True)
FONT_MD  = load_font(28, True)
FONT_SM  = load_font(20)
FONT_XS  = load_font(16)

def draw_bar(surf, x, y, w, h, val, maxval, fg, bg=(30,30,50), border=GOLD):
    pygame.draw.rect(surf, bg,     (x-1,y-1,w+2,h+2))
    pygame.draw.rect(surf, border, (x-1,y-1,w+2,h+2), 1)
    fill = int(w * max(0,val) / max(1,maxval))
    if fill > 0:
        pygame.draw.rect(surf, fg, (x,y,fill,h))
    # Shine
    pygame.draw.line(surf, (*[min(255,c+60) for c in fg],100), (x,y),(x+fill,y), 1)

def draw_hud(surf, player, level, boss=None):
    # Dark panel top
    panel = make_surface(SW, 60)
    panel.fill((10,5,25,200))
    surf.blit(panel,(0,0))
    pygame.draw.line(surf, GOLD, (0,60),(SW,60), 1)

    # HP
    draw_bar(surf, 10, 10, 180, 14, player.hp, player.max_hp, (220,40,40))
    surf.blit(FONT_XS.render(f"HP {int(player.hp)}/{player.max_hp}",True,WHITE),(12,12))

    # Mana
    draw_bar(surf, 10, 32, 180, 14, player.mana, player.max_mana, BLUE)
    surf.blit(FONT_XS.render(f"MP {int(player.mana)}/{player.max_mana}",True,WHITE),(12,34))

    # Score
    sc = FONT_MD.render(f"✦ {player.score:,}", True, GOLD)
    surf.blit(sc, (SW//2 - sc.get_width()//2, 10))

    # Level
    lv = FONT_SM.render(f"LEVEL {level}", True, CYAN)
    surf.blit(lv, (SW//2 - lv.get_width()//2, 40))

    # Lives
    for i in range(player.lives):
        pygame.draw.polygon(surf, PURPLE, [
            (SW-20-i*26, 15),
            (SW-32-i*26, 30),
            (SW-8-i*26,  30)])
        pygame.draw.polygon(surf, GOLD, [
            (SW-20-i*26, 17),
            (SW-30-i*26, 28),
            (SW-10-i*26, 28)], 1)

    # Bombs
    for i in range(player.bomb_count):
        pygame.draw.circle(surf, ORANGE, (SW-85-i*22, 50), 8)
        pygame.draw.circle(surf, FIRE2,  (SW-85-i*22, 50), 5)

    # Spell selector
    for i, name in enumerate(Player.SPELLS):
        col  = Player.SPELL_COLORS[i]
        bx   = 210 + i*100
        locked = not player.spells_unlocked[i]
        if i == player.spell:
            pygame.draw.rect(surf, col, (bx-2,6,92,48), 2)
        if locked:
            surf.blit(FONT_XS.render("🔒",True,GRAY),(bx+36,28))
        else:
            surf.blit(FONT_XS.render(name[:7],True,col if i==player.spell else GRAY),(bx,8))
            cd = f"MP:{Player.SPELL_MANA[i]}"
            surf.blit(FONT_XS.render(cd,True,LBLUE),(bx,28))

    # Boss bar
    if boss:
        bw = SW - 40
        draw_bar(surf, 20, SH-30, bw, 18,
                 boss.hp, boss.max_hp,
                 [RED, ORANGE, FIRE1][boss.phase],
                 border=(200,50,50))
        lbl = FONT_SM.render(f"⚔ BOSS — PHASE {boss.phase+1}", True, RED)
        surf.blit(lbl,(SW//2-lbl.get_width()//2, SH-48))

# ─── SCREENS ──────────────────────────────────────────────
def draw_bg(surf, stars, scroll, castle_surf):
    # Gradient background
    for y in range(0, SH, 4):
        t = y/SH
        r = int(BG_TOP[0]*(1-t) + BG_BOT[0]*t)
        g = int(BG_TOP[1]*(1-t) + BG_BOT[1]*t)
        b = int(BG_TOP[2]*(1-t) + BG_BOT[2]*t)
        pygame.draw.line(surf,(r,g,b),(0,y),(SW,y))
        if y+4 < SH:
            pygame.draw.line(surf,(r,g,b),(0,y+1),(SW,y+1))
            pygame.draw.line(surf,(r,g,b),(0,y+2),(SW,y+2))
            pygame.draw.line(surf,(r,g,b),(0,y+3),(SW,y+3))
    # Stars parallax
    for x,y,sz,bright in stars:
        sy = (y + scroll//3) % SH
        c = (bright,bright,bright)
        if sz == 1:
            surf.set_at((x,sy), c)
        else:
            pygame.draw.circle(surf, c, (x,sy), sz//2)
    # Castle at bottom
    surf.blit(castle_surf,(0, SH-140))

def draw_main_menu(surf, stars, scroll, castle_surf, frame):
    draw_bg(surf, stars, scroll, castle_surf)

    # Title glow effect
    glow = make_surface(700, 80)
    pygame.draw.ellipse(glow, (60,0,100,60),(0,0,700,80))
    surf.blit(glow,(SW//2-350, 100))

    # Title
    for i,line in enumerate(["DRAGON SIEGE","ARCANE SKIES"]):
        col = GOLD if i==0 else PURPLE
        sz  = 64 if i==0 else 44
        fnt = load_font(sz, True)
        t   = fnt.render(line, True, col)
        # Shadow
        sh  = fnt.render(line, True, (30,0,60))
        surf.blit(sh, (SW//2 - t.get_width()//2 + 3, 110+i*66 + 3))
        surf.blit(t,  (SW//2 - t.get_width()//2,     110+i*66))

    # Animated subtitle
    pulse = abs(math.sin(frame*0.05))
    sc = int(160+95*pulse)
    sub = FONT_MD.render("— A Fantasy Shooter —", True, (sc,sc,255))
    surf.blit(sub, (SW//2-sub.get_width()//2, 250))

    # Menu options
    opts = [("ENTER  —  New Game","N"),
            ("L  —  Load Game","L"),
            ("H  —  How to Play","H"),
            ("Q  —  Quit","Q")]
    for i,(text,_) in enumerate(opts):
        col = WHITE if i>0 else GOLD
        o = FONT_MD.render(text, True, col)
        surf.blit(o,(SW//2-o.get_width()//2, 320+i*50))

    # Decorative dragons
    d = Assets.dragon_small(RED, frame)
    surf.blit(d, (80 + int(math.sin(frame*0.04)*30), 300))
    d2= Assets.dragon_small(ORANGE, frame+20)
    surf.blit(pygame.transform.flip(d2,True,False),
              (SW-140+int(math.sin(frame*0.04+1)*30), 300))

def draw_how_to_play(surf, stars, scroll, castle_surf):
    draw_bg(surf, stars, scroll, castle_surf)
    overlay = make_surface(SW,SH)
    overlay.fill((0,0,0,160))
    surf.blit(overlay,(0,0))

    t = FONT_LG.render("HOW TO PLAY", True, GOLD)
    surf.blit(t,(SW//2-t.get_width()//2,30))
    pygame.draw.line(surf,GOLD,(100,90),(SW-100,90),2)

    lines = [
        ("WASD / Arrow Keys","Move your wizard"),
        ("SPACE / Z","Shoot current spell"),
        ("1-4 or Q/E","Switch spell"),
        ("X / B","Use Magic Bomb (clears screen)"),
        ("P","Pause game"),
        ("F5","Quick Save"),
        ("",""),
        ("🧙 Spells:", ""),
        (" 1. Arcane Bolt","Fast, low mana cost"),
        (" 2. Fireball","Slow, high damage"),
        (" 3. Ice Shard","Pierces, medium cost"),
        (" 4. Lightning","Spread pierce, high mana"),
        ("",""),
        ("Collect powerups dropped by enemies!",""),
        ("Defeat the boss to advance levels.",""),
        ("",""),
        ("ESC — Back to Menu",""),
    ]
    for i,(k,v) in enumerate(lines):
        if k.startswith("🧙"):
            t2 = FONT_SM.render(k, True, GOLD)
        elif k.startswith(" "):
            t2 = FONT_XS.render(k, True, Player.SPELL_COLORS[int(k[1])-1])
        elif k == "":
            continue
        else:
            t2 = FONT_XS.render(k, True, CYAN)
        surf.blit(t2, (80, 110+i*22))
        if v:
            v2 = FONT_XS.render("— "+v, True, WHITE)
            surf.blit(v2,(420, 110+i*22))

def draw_pause(surf):
    ov = make_surface(SW,SH)
    ov.fill((0,0,0,150))
    surf.blit(ov,(0,0))
    t = FONT_LG.render("⏸  PAUSED", True, GOLD)
    surf.blit(t,(SW//2-t.get_width()//2, SH//2-60))
    s = FONT_MD.render("P to Resume  |  Q to Quit", True, GRAY)
    surf.blit(s,(SW//2-s.get_width()//2, SH//2+20))

def draw_level_clear(surf, level, score):
    ov = make_surface(SW,SH)
    ov.fill((0,0,0,170))
    surf.blit(ov,(0,0))
    t = FONT_LG.render(f"LEVEL {level} CLEARED!", True, GOLD)
    surf.blit(t,(SW//2-t.get_width()//2,SH//2-80))
    s = FONT_MD.render(f"Score: {score:,}", True, WHITE)
    surf.blit(s,(SW//2-s.get_width()//2,SH//2))
    n = FONT_SM.render("Press ENTER for next level", True, CYAN)
    surf.blit(n,(SW//2-n.get_width()//2,SH//2+70))

def draw_game_over(surf, score, level, high):
    ov = make_surface(SW,SH)
    ov.fill((0,0,0,200))
    surf.blit(ov,(0,0))
    t  = FONT_LG.render("GAME OVER", True, RED)
    surf.blit(t,(SW//2-t.get_width()//2,SH//2-120))
    s  = FONT_MD.render(f"Score: {score:,}", True, WHITE)
    surf.blit(s,(SW//2-s.get_width()//2,SH//2-40))
    l  = FONT_MD.render(f"Reached Level {level}", True, CYAN)
    surf.blit(l,(SW//2-l.get_width()//2,SH//2))
    h  = FONT_MD.render(f"High Score: {high:,}", True, GOLD)
    surf.blit(h,(SW//2-h.get_width()//2,SH//2+50))
    r  = FONT_SM.render("ENTER — Restart  |  Q — Quit", True, GRAY)
    surf.blit(r,(SW//2-r.get_width()//2,SH//2+110))

# ─── SAVE / LOAD ──────────────────────────────────────────
def save_game(player, level):
    data = {
        'hp':         player.hp,
        'mana':       player.mana,
        'score':      player.score,
        'lives':      player.lives,
        'level':      level,
        'bomb_count': player.bomb_count,
        'spell':      player.spell,
        'spells_unlocked': player.spells_unlocked,
        'timestamp':  time.strftime("%Y-%m-%d %H:%M")
    }
    with open(SAVE_FILE,'w') as f:
        json.dump(data, f)
    return True

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE,'r') as f:
            return json.load(f)
    except:
        return None

def apply_save(player, data):
    player.hp              = data.get('hp', 100)
    player.mana            = data.get('mana', 100)
    player.score           = data.get('score', 0)
    player.lives           = data.get('lives', 3)
    player.bomb_count      = data.get('bomb_count', 2)
    player.spell           = data.get('spell', 0)
    player.spells_unlocked = data.get('spells_unlocked', [True,False,False,False])
    return data.get('level', 1)

def load_high_score():
    d = load_game()
    return d.get('high_score',0) if d else 0

def save_high_score(score):
    d = load_game() or {}
    if score > d.get('high_score',0):
        d['high_score'] = score
        with open(SAVE_FILE,'w') as f:
            json.dump(d, f)

# ─── MAIN GAME LOOP ───────────────────────────────────────
class Game:
    STATE_MENU     = 'menu'
    STATE_PLAYING  = 'playing'
    STATE_PAUSED   = 'paused'
    STATE_HOWTO    = 'howto'
    STATE_LVLCLEAR = 'levelclear'
    STATE_GAMEOVER = 'gameover'
    STATE_BOSS     = 'boss'

    def __init__(self):
        self.state      = self.STATE_MENU
        self.stars      = Assets.star_bg(250)
        self.castle_surf= Assets.castle_silhouette()
        self.scroll     = 0
        self.frame      = 0
        self.level      = 1
        self.high_score = load_high_score()
        self.save_flash = 0
        self.reset_game()

    def reset_game(self):
        self.player        = Player()
        self.enemies       = pygame.sprite.Group()
        self.player_bullets= pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups      = pygame.sprite.Group()
        self.particles     = []
        self.boss          = None
        self.boss_group    = pygame.sprite.Group()
        self.spawner       = FormationSpawner(self.level)
        self.boss_spawned  = False
        self.kills         = 0
        self.kills_to_boss = 12 + self.level * 4
        self.level_clear_timer = 0
        self.notify_text   = ""
        self.notify_timer  = 0

    def notify(self, text, color=GOLD):
        self.notify_text  = text
        self.notify_color = color
        self.notify_timer = 120

    def handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_n):
                self.level = 1
                self.reset_game()
                self.state = self.STATE_PLAYING
            elif event.key == pygame.K_l:
                data = load_game()
                if data:
                    self.reset_game()
                    self.level = apply_save(self.player, data)
                    self.state = self.STATE_PLAYING
                    self.notify("Game Loaded!", GREEN)
                else:
                    self.notify("No save found!", RED)
            elif event.key == pygame.K_h:
                self.state = self.STATE_HOWTO
            elif event.key == pygame.K_q:
                pygame.quit(); sys.exit()

    def handle_play_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state = self.STATE_PAUSED
            elif event.key == pygame.K_F5:
                save_game(self.player, self.level)
                self.notify("Game Saved! ✔", TEAL)
                self.save_flash = 90
            elif event.key in (pygame.K_x, pygame.K_b):
                if self.player.use_bomb(self.enemy_bullets, self.enemies, self.particles):
                    self.notify("💥 MAGIC BOMB!", FIRE2)
            elif event.key == pygame.K_q:
                self.state = self.STATE_MENU
            elif event.key == pygame.K_e:
                self.player.cycle_spell(1)
                self.notify(f"Spell: {Player.SPELLS[self.player.spell]}", Player.SPELL_COLORS[self.player.spell])
            elif event.key == pygame.K_q:
                self.player.cycle_spell(-1)
            for i,k in enumerate([pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4]):
                if event.key == k and self.player.spells_unlocked[i]:
                    self.player.spell = i
                    self.notify(f"Spell: {Player.SPELLS[i]}", Player.SPELL_COLORS[i])

    def spawn_powerup(self, x, y):
        if random.random() < 0.25:
            self.powerups.add(PowerUp(x,y))

    def update_playing(self, keys):
        self.frame  += 1
        self.scroll += 1

        # Player
        self.player.update(keys, self.particles)
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            self.player.shoot(self.player_bullets)

        # Spawning
        if not self.boss_spawned:
            self.spawner.update(self.enemies, self.level)
        if self.kills >= self.kills_to_boss and not self.boss_spawned and not self.boss:
            self.boss = BossDragon(self.level)
            self.boss_group.add(self.boss)
            self.enemies.empty()
            self.enemy_bullets.empty()
            self.boss_spawned = True
            self.notify(f"⚔ BOSS INCOMING — Level {self.level}!", RED)

        # Enemies
        for e in list(self.enemies):
            e.update(self.player, self.enemy_bullets, self.particles)
        if self.boss:
            self.boss.update(self.player, self.enemy_bullets, self.particles)

        # Bullets
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.powerups.update()

        # Collisions: player bullets → enemies
        for bullet in list(self.player_bullets):
            hits = pygame.sprite.spritecollide(bullet, self.enemies, False, pygame.sprite.collide_rect)
            for enemy in hits:
                enemy.hp -= bullet.damage
                explosion(self.particles, bullet.rect.centerx, bullet.rect.centery,
                          Player.SPELL_COLORS[bullet.spell_type], 8, 3)
                if not bullet.pierce:
                    bullet.kill()
                    break
                if enemy.hp <= 0:
                    self.player.score += enemy.score_val
                    self.kills += 1
                    explosion(self.particles, enemy.rect.centerx, enemy.rect.centery, FIRE1, 25, 5)
                    self.spawn_powerup(enemy.rect.centerx, enemy.rect.centery)
                    enemy.kill()
            # Boss
            if self.boss and pygame.sprite.collide_rect(bullet, self.boss):
                self.boss.hp -= bullet.damage
                explosion(self.particles, bullet.rect.centerx, bullet.rect.centery,
                          Player.SPELL_COLORS[bullet.spell_type], 6, 4)
                if not bullet.pierce:
                    bullet.kill()
                if self.boss.hp <= 0:
                    self.player.score += self.boss.score_val
                    explosion(self.particles, self.boss.rect.centerx, self.boss.rect.centery,
                              FIRE1, 80, 10)
                    explosion(self.particles, self.boss.rect.centerx, self.boss.rect.centery,
                              GOLD, 50, 8)
                    self.boss_group.empty()
                    self.boss = None
                    self.notify(f"🏆 BOSS DEFEATED!", GOLD)
                    # Drop lots of powerups
                    for _ in range(4):
                        self.powerups.add(PowerUp(
                            random.randint(200,SW-200),
                            random.randint(100,400)))
                    self.level_clear_timer = 180

        # Enemies still alive → remove dead
        for e in list(self.enemies):
            if e.hp <= 0:
                self.player.score += e.score_val
                self.kills += 1
                explosion(self.particles, e.rect.centerx, e.rect.centery, FIRE1, 20, 5)
                self.spawn_powerup(e.rect.centerx, e.rect.centery)
                e.kill()

        # Enemy bullets → player
        if self.player.invincible == 0:
            hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            for h in hits:
                self.player.take_damage(h.damage, self.particles)

        # Enemy collision with player
        if self.player.invincible == 0:
            if pygame.sprite.spritecollide(self.player, self.enemies, False):
                self.player.take_damage(30, self.particles)

        # Powerup collection
        for pu in pygame.sprite.spritecollide(self.player, self.powerups, True):
            self._apply_powerup(pu.kind)

        # Player death
        if self.player.hp <= 0:
            self.player.lives -= 1
            if self.player.lives > 0:
                self.player.hp = self.player.max_hp
                self.player.mana = self.player.max_mana
                self.player.invincible = 180
                self.notify(f"💀 Life Lost! {self.player.lives} remaining", RED)
            else:
                save_high_score(self.player.score)
                self.high_score = max(self.high_score, self.player.score)
                self.state = self.STATE_GAMEOVER

        # Level clear
        if self.level_clear_timer > 0:
            self.level_clear_timer -= 1
            if self.level_clear_timer == 0:
                self.state = self.STATE_LVLCLEAR

        # Particles
        self.particles = [p for p in self.particles if p.update()]

        # Notify timer
        if self.notify_timer > 0:
            self.notify_timer -= 1

    def _apply_powerup(self, kind):
        if kind == 'hp':
            self.player.hp = min(self.player.max_hp, self.player.hp + 40)
            self.notify("❤ +40 HP", GREEN)
        elif kind == 'mana':
            self.player.mana = min(self.player.max_mana, self.player.mana + 50)
            self.notify("💧 +50 Mana", BLUE)
        elif kind == 'spell':
            # Unlock next spell
            for i in range(1,4):
                if not self.player.spells_unlocked[i]:
                    self.player.spells_unlocked[i] = True
                    self.notify(f"✨ Unlocked: {Player.SPELLS[i]}!", PURPLE)
                    break
            else:
                self.player.score += 500
                self.notify("+500 bonus score!", GOLD)
        elif kind == 'shield':
            self.player.invincible += 300
            self.notify("🛡 Shield +5 seconds!", CYAN)
        elif kind == 'bomb':
            self.player.bomb_count = min(5, self.player.bomb_count+1)
            self.notify("💣 +1 Magic Bomb!", ORANGE)

    def draw_playing(self):
        draw_bg(screen, self.stars, self.scroll, self.castle_surf)

        # Particles
        for p in self.particles:
            p.draw(screen)

        # Sprites
        self.powerups.draw(screen)
        self.enemy_bullets.draw(screen)
        self.enemies.draw(screen)
        self.boss_group.draw(screen)

        # Player (flicker when invincible)
        if self.player.invincible == 0 or (self.frame//6)%2 == 0:
            screen.blit(self.player.image, self.player.rect)

        self.player_bullets.draw(screen)

        # HUD
        draw_hud(screen, self.player, self.level,
                 self.boss if self.boss_spawned else None)

        # Kill counter
        if not self.boss_spawned:
            kc = FONT_XS.render(
                f"Kills: {self.kills}/{self.kills_to_boss}", True, GRAY)
            screen.blit(kc,(SW-120,65))

        # Notification
        if self.notify_timer > 0:
            alpha = min(255, self.notify_timer*3)
            ntxt  = FONT_MD.render(self.notify_text, True, self.notify_color)
            ns    = make_surface(ntxt.get_width()+20, ntxt.get_height()+10)
            ns.fill((0,0,0,100))
            ns.blit(ntxt,(10,5))
            ns.set_alpha(alpha)
            screen.blit(ns,(SW//2-ns.get_width()//2, SH//2-50))

        # Save flash
        if self.save_flash > 0:
            self.save_flash -= 1
            sf = FONT_XS.render("💾 Saved", True, TEAL)
            screen.blit(sf,(SW-80,65))

    def run(self):
        while True:
            dt = clock.tick(FPS)
            keys = pygame.key.get_pressed()
            self.scroll += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if self.state == self.STATE_MENU:
                    self.handle_menu_events(event)
                elif self.state == self.STATE_HOWTO:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = self.STATE_MENU
                elif self.state == self.STATE_PLAYING:
                    self.handle_play_events(event)
                elif self.state == self.STATE_PAUSED:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.state = self.STATE_PLAYING
                        elif event.key == pygame.K_q:
                            self.state = self.STATE_MENU
                elif self.state == self.STATE_LVLCLEAR:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.level += 1
                        self.reset_game()
                        self.state = self.STATE_PLAYING
                        self.notify(f"Level {self.level} — Begin!", CYAN)
                elif self.state == self.STATE_GAMEOVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.level = 1
                            self.reset_game()
                            self.state = self.STATE_PLAYING
                        elif event.key == pygame.K_q:
                            self.state = self.STATE_MENU

            # Update
            if self.state == self.STATE_PLAYING:
                self.update_playing(keys)
            self.frame += 1

            # Draw
            if self.state == self.STATE_MENU:
                draw_main_menu(screen, self.stars, self.scroll,
                               self.castle_surf, self.frame)
                if self.notify_timer > 0:
                    self.notify_timer -= 1
                    nt = FONT_SM.render(self.notify_text, True, self.notify_color)
                    screen.blit(nt,(SW//2-nt.get_width()//2, SH-80))
            elif self.state == self.STATE_HOWTO:
                draw_how_to_play(screen, self.stars, self.scroll, self.castle_surf)
            elif self.state == self.STATE_PLAYING:
                self.draw_playing()
            elif self.state == self.STATE_PAUSED:
                self.draw_playing()
                draw_pause(screen)
            elif self.state == self.STATE_LVLCLEAR:
                self.draw_playing()
                draw_level_clear(screen, self.level, self.player.score)
            elif self.state == self.STATE_GAMEOVER:
                draw_bg(screen, self.stars, self.scroll, self.castle_surf)
                draw_game_over(screen, self.player.score, self.level, self.high_score)

            pygame.display.flip()

# ─── ENTRY POINT ──────────────────────────────────────────
if __name__ == "__main__":
    Game().run()
