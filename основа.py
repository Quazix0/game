import os
import pygame
from time import sleep

width = 1000
height = 700
ufo_width = 50
ufo_height = 26
ship_speed = 4
bullet_speed = 7
ufo_speed_x = 3
ufo_speed_y = 11
direction = 1
lifes = 3


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Ship(Sprite):
    '''наш корабль'''

    def __init__(self, screen):
        super().__init__(ship_group)
        self.image = load_image('ship.png', -1)
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.rect.bottom = self.screen_rect.bottom
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= ship_speed
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx


class Bullet(Sprite):

    def __init__(self, screen, ship):
        super().__init__(bullets)
        self.width = 2
        self.len = 10
        self.color = 60, 60, 60
        self.screen = screen
        self.rect = pygame.Rect(0, 0, self.width, self.len)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)

    def update(self):
        self.y -= bullet_speed
        self.rect.y = self.y
        collisions = pygame.sprite.groupcollide(bullets, ufo_group, True, True)
        if len(ufo_group) == 0:
            bullets.empty()
            create_fleet()

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Ufo(Sprite):
    '''летающая тарелка'''

    def __init__(self, screen):
        super().__init__(ufo_group)
        self.image = load_image('ufo.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.screen = screen

    def update(self):
        self.x += (ufo_speed_x * direction)
        self.rect.x = self.x
        if pygame.sprite.spritecollideany(ship, ufo_group):
            ship_damaged()

    def check(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def create_fleet():
    space_left_x = width - 2 * ufo_width
    num_of_ufo_x = int(space_left_x / (2 * ufo_width))
    num_of_ufo_y = 6
    for j in range(num_of_ufo_y):
        for i in range(num_of_ufo_x):
            ufo = Ufo(screen)
            ufo.x = ufo_width + 2 * ufo_width * i
            ufo.rect.x = ufo.x
            ufo.rect.y = ufo_height + 2.5 * ufo_height * j


def change_direction():
    global direction
    for ufo in ufo_group:
        ufo.rect.y += ufo_speed_y
    direction *= -1


def check_fleet():
    for ufo in ufo_group.sprites():
        if ufo.check():
            change_direction()
            break


def ship_damaged():
    global lifes
    global running
    if lifes > 0:
        lifes -= 1
        ufo_group.empty()
        bullets.empty()
        create_fleet()
        ship.center_ship()
        sleep(0.5)
    else:
        running = False


def check_bottom(screen):
    screen_rect = screen.get_rect()
    for ufo in ufo_group.sprites():
        if ufo.rect.bottom >= screen_rect.bottom:
            ship_damaged()
            break


def start_screen():
    intro_text = []
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
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


pygame.init()
fps = 30
clock = pygame.time.Clock()
background_color = (230, 230, 230)
screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
'''start_screen()'''
ship_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ship = Ship(screen)
create_fleet()
pygame.display.set_caption('')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(screen, ship)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
    screen.fill(background_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship_group.draw(screen)
    ufo_group.draw(screen)
    ship.update()
    bullets.update()
    check_fleet()
    ufo_group.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
