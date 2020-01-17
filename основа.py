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
score = 0
ufo_points = 50


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Scoreboard:
    def __init__(self, screen, score, background_color):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.score = score
        self.text_color = (30, 30, 30)
        self.background_color = background_color
        self.font = pygame.font.SysFont(None, 36)
        self.prep_score()

    def prep_score(self):
        score_str = str(self.score)
        self.score_im = self.font.render(score_str, True, self.text_color, self.background_color)
        self.score_rect = self.score_im.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.screen_rect.top = 10

    def show_score(self):
        self.screen.blit(self.score_im, self.score_rect)


class Button():
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


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
        if collisions:
            for ufos in collisions.values():
                update_score(ufos, ufo_points)

        if len(ufo_group) == 0:
            bullets.empty()
            speed_up()
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
    global game_running
    if lifes > 0:
        lifes -= 1
        ufo_group.empty()
        bullets.empty()
        create_fleet()
        ship.center_ship()
        sleep(0.5)
    else:
        game_running = False
        pygame.mouse.set_visible(True)


def check_bottom(screen):
    screen_rect = screen.get_rect()
    for ufo in ufo_group.sprites():
        if ufo.rect.bottom >= screen_rect.bottom:
            ship_damaged()
            break


def check_play_button(play_button, x, y):
    global game_running
    global lifes
    global ufo_speed_x
    global score
    button_clicked = play_button.rect.collidepoint(x, y)
    if button_clicked and not game_running:
        pygame.mouse.set_visible(False)
        game_running = True
        lifes = 3
        ufo_group.empty()
        bullets.empty()
        create_fleet()
        ship.center_ship()
        ufo_speed_x = 3
        score = 0


def speed_up():
    global ufo_speed_x
    global ufo_points
    ufo_speed_x *= 1.1
    ufo_points += 25


def update_score(ufos, ufo_points):
    global score
    score += ufo_points * len(ufos)
    sb.prep_score()


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
start_screen()
ship_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ship = Ship(screen)
create_fleet()
play_button = Button(screen, 'Играть')
sb = Scoreboard(screen, score, background_color)
pygame.display.set_caption('Космическая защита')
game_running = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(play_button, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN and game_running:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(screen, ship)
        elif event.type == pygame.KEYUP and game_running:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
    if game_running:
        screen.fill(background_color)
        sb.show_score()
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
    else:
        start_screen()
        play_button.draw_button()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
