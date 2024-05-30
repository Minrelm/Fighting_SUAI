import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()  # ширина исходного изображения кнопки
        height = image.get_height()  # высота исходного изображения кнопки
        # масштабирование изображения кнопки
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()  # создание прямоугольника для кнопки
        self.rect.topleft = (x, y)  # установка верхнего левого угла прямоугольника
        self.clicked = False  # флаг, указывающий, была ли нажата кнопка

    def draw(self, surface):
        action = False  # флаг для действия по нажатию кнопки

        # получение позиции мыши
        pos = pygame.mouse.get_pos()

        # проверка, был ли клик по кнопке
        if self.rect.collidepoint(pos):  # проверка, находится ли мышь над кнопкой
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # проверка, была ли нажата левая кнопка мыши
                action = True  # действие подтверждено
                self.clicked = True  # установка флага нажатия

        if pygame.mouse.get_pressed()[0] == 0:  # сброс флага нажатия, когда кнопка мыши отпущена
            self.clicked = False

        # отрисовка кнопки
        surface.blit(self.image, (self.rect.x, self.rect.y))  # отображение изображения кнопки на поверхности

        return action  # возврат флага действия