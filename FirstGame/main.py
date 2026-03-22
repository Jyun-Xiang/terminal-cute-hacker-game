import pygame
#from pygame.sprite import Group
import random
import os

FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (160, 160, 160)
BLUE = (153, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 500
HEIGHT = 600

#遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('第一個遊戲')     #設定遊戲窗口標題
clock = pygame.time.Clock()     #時間管理、操控

#載入圖片
background_img = pygame.image.load(os.path.join('img', 'FirstGameBackground.png')).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.image.load(os.path.join('img', 'Player_1.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (35, 42))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
rock_img_I = pygame.image.load(os.path.join('img', 'Q版蟲蟲.png')).convert()
rock_img_II = pygame.image.load(os.path.join('img', 'Q版幽靈.png')).convert()
rock_img_III = pygame.image.load(os.path.join('img', 'Q版小蛇.png')).convert()
rock_img_IV = pygame.image.load(os.path.join('img', 'Q版小史萊姆.png')).convert()
rock_img = [rock_img_I, rock_img_II, rock_img_III, rock_img_IV]
bullet_img_I = pygame.image.load(os.path.join('img', 'Bullet_1.png')).convert_alpha()
bullet_img_II = pygame.image.load(os.path.join('img', 'Bullet_2.png')).convert_alpha()
#bullet_img = random.choice([bullet_img_I, bullet_img_II])
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(5):
    expl_img = pygame.image.load(os.path.join('img', f'burst{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (40, 40)))
    expl_anim['player'].append(pygame.transform.scale(expl_img, (120, 120)))
# power_img = pygame.image.load(os.path.join('img', 'vanpire_mask.png')).convert()
power_imgs = {}
power_imgs['double'] = pygame.image.load(os.path.join('img', '強化寶石.png')).convert()
power_imgs['damage'] = pygame.image.load(os.path.join('img', '傷害寶石.png')).convert()
power_imgs['shield'] = pygame.image.load(os.path.join('img', '防禦寶石.png')).convert()
power_imgs['energy'] = pygame.image.load(os.path.join('img', '能量寶石.png')).convert()
power_imgs['heal'] = pygame.image.load(os.path.join('img', '生命寶石.png')).convert()


#載入音效

shoot_sound = pygame.mixer.Sound(os.path.join('sound', 'MA_Designed_ResistanceBlaster_1.wav'))
shoot_sound.set_volume(0.2)
""" increase_sound = pygame.mixer.Sound(os.path.join('sound', '')) """
burst_sound_I = pygame.mixer.Sound(os.path.join('sound', 'MA_Originals_StaticGlitches_5.wav'))
""" die_sound = pygame.mixer.Sound(os.path.join('sound', '')) """

pygame.mixer.music.load(os.path.join('sound', 'fidelfortune-cyberpunk-synthwave-351505.mp3'))
pygame.mixer.music.set_volume(0.1)

#設置分數
font_name = os.path.join('MantouSans-Regular.ttf')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surf, hp, x, y):
    if hp < 0 :
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_energy(surf, energy, x, y):
    if energy < 0:
        energy = 0
    BAR_HEIGHT = 10
    BAR_LENGTH = 200
    fill = (energy/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img,  x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_rockHealth(surf, hp, max_hp, bar_length, x, y):
    if hp < 0 :
        hp = 0
    BAR_HEIGHT = 10
    fill = (hp/max_hp)*bar_length
    outline_rect = pygame.Rect(x, y, bar_length, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_init():
    bg_rect = background_img.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(background_img, bg_rect.topleft)
    #draw_text(screen, 'B1Tの奇妙', 60, WIDTH/2, HEIGHT/7)
    draw_text(screen, 'Debug大挑戰!!!', 60, WIDTH/2, HEIGHT/4)
    draw_text(screen, 'A D移動角色 空白鍵發射子彈\。皿。/', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False


class Player(pygame.sprite.Sprite):     #繼承內建sprite的類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #call內建sprite的初始函式
        self.image = pygame.transform.scale(player_img, (70, 84))     #image表示要顯示的圖片
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()#rect定位圖片
        self.radius = 25
        #pygame.draw.circle(self.image, GRAY, self.rect.center, self.radius)     #碰撞測試
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.strength = 1
        self.strength_time = 0
        # 傷害增幅（乘算）與一次性護盾
        self.damage_multiplier = 1.0
        self.damage_time = 0
        self.shield = False
        # 能量系統
        self.max_energy = 100
        self.energy = self.max_energy
        self.regen_rate = 30  # 每秒回復量
        self.energy_cost_single = 10
        self.energy_cost_double = 18
    
    def update(self):
        now = pygame.time.get_ticks()
        if self.strength > 1 and now - self.strength_time > 3000:    #3000毫秒
            self.strength -= 1
            self.strength_time = now
        # 傷害增幅效果持續 5 秒
        if self.damage_multiplier > 1.0 and now - self.damage_time > 5000:
            self.damage_multiplier = 1.0
            self.damage_time = 0
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        # 能量回復（基於 FPS）
        self.energy = min(self.max_energy, self.energy + self.regen_rate / FPS)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):
            if self.strength == 1:
                cost = self.energy_cost_single
                if self.energy >= cost:
                    self.energy -= cost
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    bullet.damage = int(bullet.damage * self.damage_multiplier)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
            elif self.strength >= 2:
                cost = self.energy_cost_double
                if self.energy >= cost:
                    self.energy -= cost
                    bullet1 = Bullet(self.rect.left, self.rect.centery)
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                    bullet1.damage = int(bullet1.damage * self.damage_multiplier)
                    bullet2.damage = int(bullet2.damage * self.damage_multiplier)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()
            

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def strengthen(self):
        self.strength += 1
        self.strength_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 隨機選擇大小：小、中、大
        self.size = random.choice(['small', 'medium', 'large'])
        
        # 根據大小設置縮放比例
        if self.size == 'small':
            scale = (30, 30)
            self.max_health = 30
            self.damage = 5
        elif self.size == 'medium':
            scale = (40, 40)
            self.max_health = 60
            self.damage = 10
        else:  # large
            scale = (50, 50)
            self.max_health = 100
            self.damage = 15
        
        self.image_ori = pygame.transform.scale(random.choice(rock_img), scale)#隨機選取圖片
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        self.health = self.max_health
        self.is_hit = False  # 記錄是否被擊中過
        # 根據大小設置血條長度
        if self.size == 'small':
            self.bar_length = 50
        elif self.size == 'medium':
            self.bar_length = 75
        else:  # large
            self.bar_length = 100
    
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bullet_img = random.choice([bullet_img_I, bullet_img_II])
        self.image = pygame.transform.scale(bullet_img, (35, 42))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        self.damage = 25  # 子彈傷害值
        
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
       
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Strengthen(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # 支援多種類型：傷害增幅、回血、一次性護盾、能量回復
        self.type = random.choice(['damage', 'heal', 'shield', 'energy', 'double'])
        size = 24
        color_map = {
            'damage': (255, 80, 80),
            'heal': (80, 255, 120),
            'shield': (255, 220, 80),
            'energy': (100, 180, 255),
            'double': (180, 100, 255)
        }
        if self.type == 'double' in power_imgs:
            self.image = pygame.transform.scale(power_imgs['double'], (50, 60))
            try:
                self.image.set_colorkey(BLACK)
            except Exception:
                pass
        elif self.type == 'damage' in power_imgs:
            self.image = pygame.transform.scale(power_imgs['damage'], (50, 60))
            try:
                self.image.set_colorkey(BLACK)
            except Exception:
                pass
        elif self.type == 'shield' in power_imgs:
            self.image = pygame.transform.scale(power_imgs['shield'], (50, 60))
            try:
                self.image.set_colorkey(BLACK)
            except Exception:
                pass
        elif self.type == 'energy' in power_imgs:
            self.image = pygame.transform.scale(power_imgs['energy'], (50, 60))
            try:
                self.image.set_colorkey(BLACK)
            except Exception:
                pass
        elif self.type == 'heal' in power_imgs:
            self.image = pygame.transform.scale(power_imgs['heal'], (50, 60))
            try:
                self.image.set_colorkey(BLACK)
            except Exception:
                pass
        else:
            self.image = pygame.Surface((size, size))
            self.image.fill(color_map[self.type])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()




pygame.mixer.music.play(-1)

#遊戲迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()     #將所有物件加入群組
        player = Player()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0

    clock.tick(FPS)     #設定偵率
    #取得輸入
    for event in pygame.event.get():     #取得當下發生的所有事件
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, False, False)
    for rock, bullet_list in hits.items():
        rock.is_hit = True  # 標記為被擊中
        for bullet in bullet_list:
            rock.health -= bullet.damage
            bullet.kill()
            if rock.health <= 0:
                burst_sound_I.play()
                score += rock.radius
                expl = Explosion(rock.rect.center, 'lg')
                all_sprites.add(expl)
                if random.random() > 0.8:     # 20%機率掉落強化道具
                    pow = Strengthen(rock.rect.center)
                    all_sprites.add(pow)
                    powers.add(pow)
                rock.kill()
                new_rock()
            else:
                expl = Explosion(rock.rect.center, 'sm')
                all_sprites.add(expl)
    
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        if player.shield:
            player.shield = False
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
        else:
            player.health -= hit.radius
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player.health <= 0:
                die = Explosion(player.rect.center, 'player')
                all_sprites.add(die)
                """ die_sound.play() """
                player.lives -= 1
                player.health = 100
                player.hide()
    
    hits = pygame.sprite.spritecollide(player, powers, True, pygame.sprite.collide_circle)
    for hit in hits:     #判斷掉落物種類
        now = pygame.time.get_ticks()
        if hit.type == 'damage':
            player.damage_multiplier = min(2.0, player.damage_multiplier + 0.5)
            player.damage_time = now
        elif hit.type == 'heal':
            player.health = min(100, player.health + 30)
        elif hit.type == 'shield':
            player.shield = True
        elif hit.type == 'double':
            player.strengthen()
        elif hit.type == 'energy':
            player.energy = min(player.max_energy, player.energy + 50)
        
    if player.lives == 0 and not(die.alive()):
        show_init = True

    #畫面顯示
    screen.fill((BLACK))
    bg_rect = background_img.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(background_img, bg_rect.topleft)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 10)
    draw_energy(screen, player.energy, 5, 25)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 10)
    for rock in rocks:
        if rock.is_hit:  # 只顯示被擊中過的石頭的血條
            draw_rockHealth(screen, rock.health, rock.max_health, rock.bar_length, rock.rect.centerx - rock.bar_length/2, rock.rect.y - 20)
    # 顯示一次性護盾的圓環（在玩家中心，稍微比玩家大一點）
    if player.shield:
        center = player.rect.center
        pygame.draw.circle(screen, (255, 220, 80), center, player.radius + 8, 3)
    pygame.display.update()     #畫面更新

pygame.quit()