from random import randint
import pygame as pg
import sys

pg.init()

y_line = 0
W = 900
H = 800

fps = 50
clock = pg.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 150, 50)
RED = (255, 0, 0)
GREY = (80, 80, 80)
SKY = (135, 206, 235)
ROAD_GRAY = (60, 60, 60)
FIELD_GREEN = (34, 139, 34)
LINE_YELLOW = (255, 200, 0)
LINE_WHITE = (240, 240, 240)

CARS = ('images/car1.png', 'images/car4.png', 'images/car3.png')
PLAYER = 'images/911.png'
CARS_SURF = []

play = True
game_over = False
pause = False

sc = pg.display.set_mode((W, H))

for img in CARS:
    CARS_SURF.append(pg.image.load(img).convert_alpha())


def load_high_score():
    try:
        with open("record.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0


def save_high_score(score):
    try:
        with open("record.txt", "w") as file:
            file.write(str(score))
    except Exception as e:
        print(f"Ошибка при сохранении рекорда: {e}")


class Car(pg.sprite.Sprite):
    def __init__(self, x, surf, group):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(center=(x, -50))
        self.add(group)
        self.speed = 10

    def update(self):
        if self.rect.y < H + 50:
            self.rect.y += self.speed
        else:
            self.kill()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(PLAYER).convert_alpha()
        self.rect = self.image.get_rect(center=(W // 2, H - 110))
        self.speed = 10

    def update(self):
        if pause:
            return

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 210:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] and self.rect.right < 690:
            self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN] and self.rect.bottom < H:
            self.rect.y += self.speed


def reset_game():
    global play, game_over, pause, all_sprites, cars, player, score, high_score
    all_sprites = pg.sprite.Group()
    cars = pg.sprite.Group()

    player = Player()
    all_sprites.add(player)

    Car(randint(250, 650), CARS_SURF[randint(0, 2)], cars)

    if score > high_score:
        high_score = score
        save_high_score(high_score)
    score = 0

    play = True
    game_over = False
    pause = False


pg.mixer.music.load('sound/bubbbb.mp3')
pg.mixer.music.play(-1)

cars = pg.sprite.Group()
all_sprites = pg.sprite.Group()

player = Player()
all_sprites.add(player)
Car(randint(250, 650), CARS_SURF[randint(0, 2)], cars)

font = pg.font.Font(None, 30)

pause = False
score = 0
high_score = load_high_score()

aa = 0

while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            sys.exit()

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        pause = False
        play = True

    if pause:
        sc.fill(BLACK)
        font_big = pg.font.SysFont('Arial', 36)
        text = font_big.render('Game paused, press W to continue', True, WHITE)
        sc.blit(text, (W // 2 - text.get_width() // 2,
                       H // 2 - text.get_height() // 2))

    if play:
        aa += 1
        if aa == 50:
            Car(randint(250, 650), CARS_SURF[randint(0, 2)], cars)
            aa = 0

        score += 1

        sc.fill(SKY)
        pg.draw.circle(sc, (255, 255, 150), (80, 80), 40)

        y_line += 10
        if y_line > H:
            y_line = 0

        pg.draw.rect(sc, FIELD_GREEN, (0, 0, 200, H))
        pg.draw.rect(sc, FIELD_GREEN, (700, 0, 200, H))

        for offset in (-H, 0, H):
            pg.draw.circle(sc, (0, 120, 0), (120, y_line + offset + 80), 45)
            pg.draw.rect(sc, (90, 50, 0), (110, y_line + offset + 80, 20, 60))

            pg.draw.circle(sc, (0, 140, 0), (780, y_line + offset + 200), 45)
            pg.draw.rect(sc, (90, 50, 0), (770, y_line + offset + 200, 20, 60))

        for offset in (-H, 0, H):
            pg.draw.ellipse(sc, (160, 160, 160), (40, y_line + offset + 250, 60, 35))
            pg.draw.ellipse(sc, (150, 150, 150), (810, y_line + offset + 320, 55, 30))

        pg.draw.rect(sc, ROAD_GRAY, (200, 0, 500, H))

        for offset in (-H, 0, H):
            pg.draw.rect(sc, LINE_YELLOW,
                         (W // 2 - 5, y_line + offset, 10, 80))

        for offset in (-H, 0, H):
            pg.draw.rect(sc, LINE_WHITE, (210, y_line + offset, 6, 120))
            pg.draw.rect(sc, LINE_WHITE, (694, y_line + offset, 6, 120))

        all_sprites.update()
        cars.update()

        if keys[pg.K_p]:
            pause = True
            play = False

        if pg.sprite.spritecollideany(player, cars):
            play = False
            game_over = True
            cars.empty()

        all_sprites.draw(sc)
        cars.draw(sc)

        font_small = pg.font.SysFont('Arial', 26)
        score_text = font_small.render(f'Score: {score}', True, WHITE)
        high_score_text = font_small.render(f'High Score: {high_score}', True, WHITE)
        sc.blit(score_text, (20, 20))
        sc.blit(high_score_text, (W - high_score_text.get_width() - 20, 20))

    if game_over:
        sc.fill(BLACK)
        font_big = pg.font.SysFont('Arial', 36)
        text = font_big.render('Game over! Press R to restart or Q to exit', True, WHITE)
        sc.blit(text, (W // 2 - text.get_width() // 2,
                       H // 2 - text.get_height() // 2))

        if keys[pg.K_r]:
            reset_game()
        if keys[pg.K_q]:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(fps)
