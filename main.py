import pygame
from pygame import mixer
from fighter import Fighter
import button

mixer.init()
pygame.init()

#создаем игровое окно
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #создает окно игры с указанными размерами
pygame.display.set_caption('Жесткие бои') #устанавливает заголовок окна с названием игры

#выставляем фреймрейт
clock = pygame.time.Clock()
FPS = 60

#цвета для игры
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#гровые переменные
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  #очки игроков. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
start_game = False
start_intro = False

WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#музыка и звуки
pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/sword.mp3")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/magic.mp3")
magic_fx.set_volume(0.75)

#кнопки
start_img = pygame.image.load('assets/start_btn.png').convert_alpha()
exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('assets/restart_btn.png').convert_alpha()

#фон
bg_image = pygame.image.load('assets/portal.png').convert_alpha()
bg_menu = (102,0,102)

#создание кнопок
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, restart_img, 1)

#загрузка спрайтов персонажей
warrior_sheet = pygame.image.load("warrior/sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("wizard/sprites/wizard.png").convert_alpha()

#загрузка победного изображения
victory_img = pygame.image.load("assets/victory.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#шрифты
count_font = pygame.font.Font("assets/ARCADECLASSIC.TTF", 80)
score_font = pygame.font.Font("assets/ARCADECLASSIC.TTF", 30)

#функция для отрисовки текса
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#функция для выведения фона
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#функция для отображения здоровья персонажей
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#плавный переход экрана
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed

        pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.colour,
                         (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, self.colour,
                         (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))

        return fade_complete

intro_fade = ScreenFade(1, BLACK, 4)

#создание двух персонажей
fighter_1 = Fighter(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# тело игры
run = True  # флаг для основного игрового цикла
game_over = False  # флаг для состояния завершения игры

while run:  # основной игровой цикл
    clock.tick(FPS)  # ограничение кадров в секунду
    if start_game == False:
        # отрисовка меню игры
        screen.fill(bg_menu)  # заполнение экрана цветом меню
        if start_button.draw(screen):  # проверка нажатия кнопки старта
            start_game = True  # начало игры
            start_intro = True  # начало вступления
        if exit_button.draw(screen):  # проверка нажатия кнопки выхода
            run = False  # выход из игры
    else:
        # проверка очков
        if score[0] >= 3 or score[1] >= 3:  # проверка на завершение игры по очкам
            game_over = True  # игра завершена

        if game_over:
            # затемнение экрана и отрисовка победного изображения и кнопки рестарта
            screen.fill((0, 0, 0))  # затемнение экрана
            screen.blit(victory_img, (250, 150))  # отрисовка победного изображения
            if restart_button.draw(screen):  # проверка нажатия кнопки рестарта
                # сброс игры
                score = [0, 0]  # сброс очков
                fighter_1 = Fighter(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)  # перезапуск первого бойца
                fighter_2 = Fighter(2, 700, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)  # перезапуск второго бойца
                start_game = False  # сброс состояния игры
                game_over = False  # сброс состояния завершения игры
            pygame.display.update()  # обновление экрана
        else:
            # отрисовка фона
            draw_bg()  # отрисовка фонового изображения

            # здоровье персонажей
            draw_health_bar(fighter_1.health, 20, 20)  # отрисовка полоски здоровья первого бойца
            draw_health_bar(fighter_2.health, 580, 20)  # отрисовка полоски здоровья второго бойца
            draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)  # отображение очков первого игрока
            draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)  # отображение очков второго игрока

            if intro_count <= 0:
                # движение персонажей
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)  # движение первого бойца
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)  # движение второго бойца
            else:
                # отсчет времени
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)  # отображение счетчика времени
                # обновление счетчика времени
                if (pygame.time.get_ticks() - last_count_update) >= 1000:  # проверка, прошла ли 1 секунда
                    intro_count -= 1  # уменьшение счетчика времени
                    last_count_update = pygame.time.get_ticks()  # обновление времени последнего изменения

            # обновление персонажей
            fighter_1.update()  # обновление состояния первого бойца
            fighter_2.update()  # обновление состояния второго бойца

            # отрисовка персонажей
            fighter_1.draw(screen)  # отрисовка первого бойца
            fighter_2.draw(screen)  # отрисовка второго бойца

            if start_intro == True:
                if intro_fade.fade():  # плавное затухание вступления
                    start_intro = False  # завершение вступления
                    intro_fade.fade_counter = 0  # сброс счетчика затухания

            if round_over == False:
                if fighter_1.alive == False:  # проверка, если первый боец мертв
                    score[1] += 1  # увеличение очков второго игрока
                    round_over = True  # окончание раунда
                    round_over_time = pygame.time.get_ticks()  # сохранение времени окончания раунда
                elif fighter_2.alive == False:  # проверка, если второй боец мертв
                    score[0] += 1  # увеличение очков первого игрока
                    round_over = True  # окончание раунда
                    round_over_time = pygame.time.get_ticks()  # сохранение времени окончания раунда

            else:
                # вывод победного изображения
                screen.blit(victory_img, (250, 150))  # отрисовка победного изображения
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:  # проверка времени окончания раунда
                    round_over = False  # сброс состояния раунда
                    intro_count = 3  # сброс счетчика времени
                    fighter_1 = Fighter(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)  # перезапуск первого бойца
                    fighter_2 = Fighter(2, 700, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)  # перезапуск второго бойца

    # обработка событий
    for event in pygame.event.get():  # перебор всех событий
        if event.type == pygame.QUIT:  # проверка события выхода
            run = False  # завершение игрового цикла

    pygame.display.update()  # обновление экрана

# выход из pygame
pygame.quit()