import pygame


class Settings():
    '''здесь будут храниться все настройки игры'''

    def __init__(self):
        self.width = 1200
        self.height = 800
        self.fps = 60
        self.background_color = (230, 230, 230)


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
