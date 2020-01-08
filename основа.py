import os
import pygame
import sys


class Settings():
    '''здесь будут храниться все настройки игры'''

    def __init__(self):
        self.width = 1000
        self.height = 600
        self.fps = 60
        self.background_color = (230, 230, 230)


class Ship():
    '''наш корабль'''

    def __init__(self, screen):
        self.screen = screen
        self.image = load_image('ship.png', -1)
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blit_ship(self):
        self.screen.blit(self.image, self.rect)


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
settings = Settings()
screen = pygame.display.set_mode((settings.width, settings.height))
ship = Ship(screen)
pygame.display.set_caption('')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(settings.background_color)
    ship.blit_ship()
pygame.quit()
