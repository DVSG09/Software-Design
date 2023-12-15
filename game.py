import pygame
import random

# Game Engine Initialization
pygame.init()

# Screen Dimensions and creation
screenX, screenY = 1000, 666
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Kavya's Limbo")
background = pygame.image.load('background_3.jpg')
gameover_background = pygame.image.load('gameover.png')
icon = pygame.image.load('pumpkin.png')
pygame.display.set_icon(icon)

# what we are showing
font = pygame.font.Font('freesansbold.ttf', 24)
candy_font = pygame.font.Font('freesansbold.ttf', 24)
hp_font = pygame.font.Font('freesansbold.ttf', 24)
level_font = pygame.font.Font('freesansbold.ttf', 24)
replay_font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 40, 10
candy_textX, candy_textY = 850, 10
hp_textX, hp_textY = 300, 10
level_textX, level_textY = 550, 10
replay_textX, replay_textY = 200, 550

pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)


def inProximity(a_x, a_y, b_x, b_y):
    return ((((b_x - a_x) ** 2) + ((b_y - a_y) ** 2)) ** 0.5) < 30


class Player:

    
    def __init__(self):
        self.playerImg = pygame.image.load('superhero.png')
        self.playerX, self.playerY = 450, 480
        self.movement_speed = 30

    def showPlayer(self, x, y):
        screen.blit(self.playerImg, (x, y))


class IconAdapter:
    def __init__(self, icon, **adapted_methods):
        self.icon = icon
        for key, val in adapted_methods.items():
            function = getattr(self.icon, val)
            setattr(key, function)

    def __setattr__(self, key, value):
        pass

    def __getattr__(self, attr):
        return getattr(self.icon, attr)


class Power:
    def __init__(self):
        self.powerImg = pygame.image.load('bolt.png')
        self.powerX, self.powerY = 0, 480
        self.powerStatus = 'Ready'

    def movePower(self, x, y):
        self.powerStatus = 'Active'
        screen.blit(self.powerImg, (x + 16, y - 50))


class Candy:
    def __init__(self, candy_id=None):
        if not candy_id:
            candy_id = random.randint(1, 12)
        self.candyImg = pygame.image.load(f'candy_{candy_id}.png')
        self.candyX, self.candyY = random.randint(50, screenX - 100), random.randint(50, screenY - 100)
        self.alive = True

    def show(self):
        screen.blit(self.candyImg, (self.candyX, self.candyY))


class Enemy:
    def __init__(self, enemy_id=None, enemy_level=0.0):
        if not enemy_id:
            enemy_id = random.randint(1, 12)
        self.enemyImg = pygame.image.load(f'villian_{enemy_id}.png')
        self.enemyX, self.enemyY = random.randint(64, screenX - 64), random.randint(64, screenY // 3)
        self.enemy_level_factor = enemy_level
        self.enemy_movement_speedX = random.uniform(0.3, self.enemy_level_factor + 1)
        self.enemy_movement_speedY = random.uniform(0.3, self.enemy_level_factor + 1)
        self.flagX, self.flagY = random.choice([-1.5, -1, -0.5, 0.5, 1, 1.5]), random.choice(
            [-1.5, -1, -0.5, 0.5, 1, 1.5])
        self.alive = True

    def move(self):
        if 32 <= self.enemyX + (self.flagX * self.enemy_movement_speedX) <= screenX - 64:
            self.enemyX += (self.flagX * self.enemy_movement_speedX)
        else:
            self.flagX = (-1 * self.flagX)

        if 32 <= self.enemyY + (self.flagY * self.enemy_movement_speedY) <= screenY - 64:
            self.enemyY += (self.flagY * self.enemy_movement_speedY)
        else:
            self.flagY = (-1 * self.flagY)

        self.enemy_movement_speedX = random.uniform(0.3, self.enemy_level_factor + 1)
        self.enemy_movement_speedY = random.uniform(0.3, self.enemy_level_factor + 1)

        screen.blit(self.enemyImg, (self.enemyX, self.enemyY))


# at every level to spawn candies and enemies
def get_enemies_info(enemy_level=0.0):
    l = [i for i in range(1, 13)]
    random.shuffle(l)
    enemies_info = {}
    num_enemies = random.randint(3, 5)
    for each in range(1, num_enemies + 1):
        enemies_info[f'enemy_{each}'] = Enemy(l[each - 1], enemy_level=0.3 * enemy_level)
    return enemies_info


def get_candies_info():
    l = [i for i in range(1, 13)]
    random.shuffle(l)
    candies_info = {}
    num_candies = random.randint(2, 4)
    for each in range(1, num_candies + 1):
        candies_info[f'candy_{each}'] = Candy(l[each - 1])
    return candies_info


# To show score, candy,hp, level on screen
def render_score(score, x, y):
    score_card = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_card, (x, y))


def render_candy_collected(candy, x, y):
    candy_card = candy_font.render("Candy: " + str(candy), True, (255, 0, 0))
    screen.blit(candy_card, (x, y))


def render_hitpoints(hitpoints, x, y):
    score_card = hp_font.render("HP: " + str(hitpoints), True, (0, 255, 0))
    screen.blit(score_card, (x, y))


def render_level(level, x, y):
    level_card = level_font.render("Level: " + str(level), True, (255, 0, 255))
    screen.blit(level_card, (x, y))


def render_wanna_play(x, y):
    replay_card = replay_font.render("Wanna Play Again? Click SPACE if Yes", True, (255, 255, 255))
    screen.blit(replay_card, (x, y))


def playgame(playerobj, score, candy, hitpoints, level):
    # global boltStatus, boltX, boltY
    GAMEOVER = False
    if not playerobj:
        return
    running = True
    enemies_info = get_enemies_info(enemy_level=0.0)
    candies_info = get_candies_info()
    powerobj = Power()
    while running:
        if GAMEOVER:
            return score, candy, hitpoints, level
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if playerobj.playerX - playerobj.movement_speed >= 0:
                        playerobj.playerX -= playerobj.movement_speed
                if event.key == pygame.K_RIGHT:
                    if playerobj.playerX + playerobj.movement_speed <= screenX - 64:
                        playerobj.playerX += playerobj.movement_speed
                if event.key == pygame.K_UP:
                    if playerobj.playerY - playerobj.movement_speed >= 0:
                        playerobj.playerY -= playerobj.movement_speed
                if event.key == pygame.K_DOWN:
                    if playerobj.playerY + playerobj.movement_speed <= screenY - 64:
                        playerobj.playerY += playerobj.movement_speed
                if event.key == pygame.K_SPACE:
                    # print('space clicked')
                    if powerobj.powerStatus == 'Ready':
                        powerobj.powerX = playerobj.playerX
                        powerobj.powerY = playerobj.playerY
                        powerobj.movePower(powerobj.powerX, powerobj.powerY)
                if event.key == pygame.K_RETURN:
                    # print('Return clicked')
                    if hitpoints < 1000:
                        while candy > 0 and hitpoints <= 1000:
                            candy -= 1
                            hitpoints += 50
                        if hitpoints > 1000:
                            hitpoints = 1000
        if powerobj.powerStatus == 'Active':
            powerobj.powerY -= 5
            powerobj.movePower(powerobj.powerX, powerobj.powerY)
            if powerobj.powerY < 0:
                powerobj.powerStatus = 'Ready'

        num_active_enemies = 0
        enemy_items = enemies_info.items()
        for enemy_name, enemy_obj in enemy_items:
            if enemy_obj.alive:
                num_active_enemies += 1
                enemy_obj.move()
            player_got_hit = inProximity(enemy_obj.enemyX + 32, enemy_obj.enemyY + 32, playerobj.playerX + 32,
                                         playerobj.playerY + 32)
            if player_got_hit:
                hitpoints -= 5
                if hitpoints <= 0:
                    GAMEOVER = True
            killed_enemy = inProximity(
                enemy_obj.enemyX + 32, enemy_obj.enemyY + 32, powerobj.powerX + 32, powerobj.powerY + 32
            )
            if killed_enemy:
                enemy_obj.alive = False
                enemy_obj.enemyX, enemy_obj.enemyY = -100, -100
                score += 100
                powerobj.powerStatus = 'Ready'

        num_active_candies = 0
        candy_items = candies_info.items()
        for candy_name, candy_obj in candy_items:
            if candy_obj.alive:
                num_active_candies += 1
                candy_obj.show()
            caught_candy = inProximity(candy_obj.candyX + 32, candy_obj.candyY + 32, playerobj.playerX + 32,
                                       playerobj.playerY + 32)
            if caught_candy:
                candy_obj.alive = False
                candy_obj.candyX, candy_obj.candyY = -200, -200
                candy += 1

        if num_active_enemies == 0:
            candies_info = get_candies_info()
            enemies_info = get_enemies_info(enemy_level=level)
            level += 1
        playerobj.showPlayer(playerobj.playerX, playerobj.playerY)
        render_score(score, textX, textY)
        render_hitpoints(hitpoints, hp_textX, hp_textY)
        render_candy_collected(candy, candy_textX, candy_textY)
        render_level(level, level_textX, level_textY)
        pygame.display.update()


# print('******Game Ended******')

def gameover(score, candy, hitpoints, level):
    running = True
    while running:
        screen.fill((230, 230, 250))
        screen.blit(gameover_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        render_score(score, textX, textY)
        render_hitpoints(hitpoints, hp_textX, hp_textY)
        render_candy_collected(candy, candy_textX, candy_textY)
        render_level(level, level_textX, level_textY)
        render_wanna_play(replay_textX, replay_textY)
        pygame.display.update()
    return False


def start_game():
    start_new_game = True
    while start_new_game:
        score, candy, hitpoints = 0, 0, 1000
        start_new_game = False
        playerobj = Player()
        level = 1
        try:
            score, candy, hitpoints, level = playgame(playerobj, score, candy, hitpoints, level)
            start_new_game = gameover(score, candy, hitpoints, level)
        except Exception as e:
            print(e)
            break
    print('Thanks for Playing. Bye.')


start_game()
