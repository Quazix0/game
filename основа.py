import os
import pygame
import sys


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
        self.speed = 1

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.speed
        self.rect.centerx = self.center


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
        self.speed = 1

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


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


pygame.init()
width = 1000
height = 600
fps = 60
background_color = (230, 230, 230)
screen = pygame.display.set_mode((width, height))
screen.fill(background_color)
ship_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ship = Ship(screen)
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
                bullets.add(bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
    screen.fill(background_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship_group.draw(screen)
    ship.update()
    bullets.update()
    pygame.display.flip()
pygame.quit()
