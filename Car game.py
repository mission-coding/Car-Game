import pygame
import sys
import random

pygame.init()

screen_w = 360
screen_h = 550
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Car Game by Vivek")

# Colors:
grey = (70,70,70)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

# Images
road_img = pygame.image.load("gallery/road.jpg").convert_alpha()
player_img = pygame.image.load("gallery/player.png").convert_alpha()
enemy_imgs = [pygame.image.load("gallery/enemy.png").convert_alpha(),
              pygame.image.load("gallery/enemy2.png").convert_alpha(),
              pygame.image.load("gallery/enemy3.png").convert_alpha(),
              pygame.image.load("gallery/enemy4.png").convert_alpha()
              ]

class Player():
    def __init__(self) -> None:
        self.w = 70
        self.h = 125
        self.x = 145
        self.y = screen_h - self.h
        self.speed = 117

    def draw(self):
        screen.blit(player_img, [self.x, self.y])
        self.hitbox = (self.x, self.y, self.w, self.h)

    def move(self):
        # Stoping Player when it goes out of the screen
        if self.x >= screen_w - self.w -28:
            self.x = screen_w - self.w -28

        if self.x <= 28:
            self.x = 28 

        if self.y >= screen_h - self.h:
            self.y = screen_h - self.h 

        if self.y <= 0:
            self.y = 0 

class Enemy():
    def __init__(self) -> None:
        self.w = 70
        self.h = 138
        self.x = random.choice([28, 145, 262])
        self.y = -self.h
        self.speed = 7
        self.hitbox = (self.x, self.y, self.w, self.h)
        self.image = random.choice(enemy_imgs)

    def draw(self):
        screen.blit(self.image, [self.x, self.y])
        self.hitbox = (self.x, self.y, self.w, self.h)

    def move(self):
        self.y += self.speed

class Road():
    def __init__(self) -> None:
        self.x = 0
        self.y1 = 0
        self.y2 = screen_h
        self.speed = 7

    def draw(self):
        screen.blit(road_img, [self.x, self.y1])
        screen.blit(road_img, [self.x, self.y2])

    def move(self):
        self.y1 += self.speed
        self.y2 += self.speed

        if self.y1 > screen_h:
            self.y1 = -screen_h
        if self.y2 > screen_h:
            self.y2 = -screen_h

def game_loop():
    player = Player()
    enemy = Enemy()
    road = Road()
    clock = pygame.time.Clock()
    fps = 30
    count = 0
    enemies = []
    over = False
    score = 0
    speed_count = 0

    def draw_text(text, color, size, x, y):
        font = pygame.font.Font(None, size)
        display_text = font.render(text, True, color)
        screen.blit(display_text, [x, y])

    def game_over():
        player.speed = 0
        road.speed = 0
        for i in enemies:
            i.speed = 0
        draw_text("Game Over!", red, 40, screen_w/2-75, screen_h/2-30)
        draw_text("Press Enter to play again", green, 35, screen_w/2-145, screen_h/2+20)
        
        if score >= hiscore:
            with open("gallery/hiscore.txt", "w") as f:
                f.write(str(score))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if 262 >= player.x >=28:
                    if event.key == pygame.K_LEFT:
                        player.x -= player.speed
                    if event.key == pygame.K_RIGHT:
                        player.x += player.speed
                if over:
                    if event.key == pygame.K_RETURN:
                        game_loop()

        with open("gallery/hiscore.txt", "r") as f:
            hiscore = int(f.read())

        if not over:
            count += 1
            if count > 45:
                enemies.append(Enemy())
                count = 0

            for enemy_car in enemies:
                if enemy_car.y > screen_h:
                    enemies.remove(enemy_car)

                if (player.hitbox[1] + player.hitbox[3] >= enemy_car.hitbox[1] and
                        player.hitbox[1] <= enemy_car.hitbox[1] + enemy_car.hitbox[3] and
                        player.hitbox[0] + player.hitbox[2] > enemy_car.hitbox[0] and
                        player.hitbox[0] <= enemy_car.hitbox[0] + enemy_car.hitbox[2]):
                        over = True

            score += 1

            if score >= hiscore:
                hiscore = score

            speed_count += 1
            if speed_count > 500:
                road.speed += 0.5
                enemy.speed += 0.5
                speed_count = 0

        road.draw()
        road.move()

        for i in enemies:
            i.draw()
            i.move()

        player.draw()
        player.move()

        if over:
            game_over()

        pygame.draw.rect(screen, grey, [0, 0, screen_w, 25])
        draw_text(f"Hi-score: {hiscore}     Score: {score}", white, 27, 10, 4)

        clock.tick(fps)
        pygame.display.update()

game_loop()