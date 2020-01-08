import os
import pygame
import sys


class Settings():
    '''здесь будут храниться все настройки игры'''

    def __init__(self):
        self.width = 1200
        self.height = 800
        self.fps = 60
        self.background_color = (230, 230, 230)


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
pygame.display.set_caption('')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(settings.background_color)
pygame.quit()
