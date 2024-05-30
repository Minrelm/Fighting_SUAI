import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player  # идентификатор игрока (1 или 2)
        self.size = data[0]  # размер спрайта
        self.image_scale = data[1]  # масштаб изображения
        self.offset = data[2]  # смещение спрайта
        self.flip = flip  # флаг отражения изображения
        self.animation_list = self.load_images(sprite_sheet, animation_steps)  # загрузка анимаций
        self.action = 0  # текущее действие персонажа (по умолчанию - бездействие)
        self.frame_index = 0  # текущий кадр анимации
        self.image = self.animation_list[self.action][self.frame_index]  # текущая картинка персонажа
        self.update_time = pygame.time.get_ticks()  # время последнего обновления анимации
        self.rect = pygame.Rect((x, y, 80, 180))  # прямоугольник для коллизий и отображения
        self.vel_y = 0  # вертикальная скорость
        self.running = False  # флаг движения
        self.jump = False  # флаг прыжка
        self.attacking = False  # флаг атаки
        self.attack_type = 0  # тип атаки
        self.attack_cooldown = 0  # задержка между атаками
        self.attack_sound = sound  # звук атаки
        self.hit = False  # флаг получения удара
        self.health = 100  # здоровье бойца
        self.alive = True  # жив ли

    def load_images(self, sprite_sheet, animation_steps):
        # извлечение изображений из спрайт-листа
        animation_list = []
        for y, animation in enumerate(animation_steps):  # перебор всех анимаций
            temp_img_list = []
            for x in range(animation):  # перебор всех кадров в анимации
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)  # извлечение одного кадра
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))  # масштабирование кадра
            animation_list.append(temp_img_list)  # добавление анимации в общий список
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10  # скорость персонажа
        GRAVITY = 2  # сила гравитации
        dx = 0  # изменение координаты по X
        dy = 0  # изменение координаты по Y
        self.running = False  # сброс флага движения
        self.attack_type = 0  # сброс типа атаки

        # определение нажатых клавиш
        key = pygame.key.get_pressed()

        # можно выполнять другие действия только в том случае, если не атакует и жив
        if self.attacking == False and self.alive == True and round_over == False:
            # действия для первого игрока
            if self.player == 1:
                # движение влево
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                # движение вправо
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # прыжок
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # атака
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)  # выполнение атаки
                    # определение типа атаки
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            # действия для второго игрока
            if self.player == 2:
                # движение влево
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                # движение вправо
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # прыжок
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # атака
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)  # выполнение атаки
                    # определение типа атаки
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # добавление гравитации
        self.vel_y += GRAVITY
        dy += self.vel_y

        # проверка, чтобы игрок оставался на экране
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 20:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 20 - self.rect.bottom

        # проверка, чтобы персонажи всегда смотрели друг на друга
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # перезарядка атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # обновить позиции игроков
        self.rect.x += dx
        self.rect.y += dy

    # обработка анимации
    def update(self):
        # проверка, какое действие выполняет игрок
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6: смерть
        elif self.hit == True:
            self.update_action(5)  # 5: удар
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # 3: атака1
            elif self.attack_type == 2:
                self.update_action(4)  # 4: атака2
        elif self.jump == True:
            self.update_action(2)  # 2: прыжок
        elif self.running == True:
            self.update_action(1)  # 1: бег
        else:
            self.update_action(0)  # 0: бездействие

        animation_cooldown = 50  # задержка между кадрами анимации
        # обновить изображение
        self.image = self.animation_list[self.action][self.frame_index]
        # достаточно ли прошло времени с последнего обновления
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # закончилась ли анимация
        if self.frame_index >= len(self.animation_list[self.action]):
            # если игрок умер или анимация закончилась
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # была ли выполнена атака
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # был ли получен урон
                if self.action == 5:
                    self.hit = False
                    # если игрок находился в середине атаки, то атака прекращается
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0:
            # выполнить атаку
            self.attacking = True
            self.attack_sound.play()  # воспроизвести звук атаки
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)  # создание прямоугольника для атаки
            if attacking_rect.colliderect(target.rect):  # проверка столкновения с целью
                target.health -= 10  # уменьшение здоровья цели
                target.hit = True  # установка флага получения удара для цели

    def update_action(self, new_action):
        # проверка, отличается ли новое действие от предыдущего
        if new_action != self.action:
            self.action = new_action  # установка нового действия
            # обновить настройки анимации
            self.frame_index = 0  # сброс индекса кадра
            self.update_time = pygame.time.get_ticks()  # обновление времени последнего обновления

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)  # отразить изображение, если нужно
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))  # нарисовать изображение на экране