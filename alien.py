import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс представляющий одного пришельца"""
    def __init__(self, ai_game):
        """Инициализирует одного пришельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width  #пределяется начальная позиция пришельца с отступом на ширину пришельца
        self.rect.y = self.rect.height  #пределяется начальная позиция пришельца с отступом на высоту пришельца
        self.x = float(self.rect.x) #отслеживается горизонтальная позиция и что бы она была точная используется float()

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


    def update(self):
        """Перемещает пришельца вправо или влево"""
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)  # при каждом одновлении позиции пришельца, мы его сдвигаем вправо или влево, на велечину скорости пришельца, self.x хранит точную позицию и мощет принимать вещественные значения
        self.rect.x = self.x  # обновляется позиция прямоугольника пришельца

