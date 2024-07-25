import pygame
from pygame.sprite import Sprite  #импорт класса-родителя для группировки связанных элементов и выполнения операций со всеми
#группироыванными элементами обновременно
from  random import choice

class BulletAlien(Sprite): #Класс Bullet наследует Sprite
    """Класс для управления снарядами, выпущеными кораблем"""
    def __init__(self, ai_game):
        """Создает обьект снарядов в текущей позиции пришельцев"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.color = (237, 17, 58)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        for alien in ai_game.aliens.sprites():
            self.rect.midbottom = alien.rect.midbottom
            self.y = float(self.rect.y)


    def update(self):  #метод управляет позицией снаряда
        """Перемещает снаряд вверх по экрану"""
        self.y += 0.2
        self.rect.y = self.y

    def draw_bullet_alien(self):
        """Вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)  #фуекция draw.rect() заполняет часть екрана, определяемую прямоугольником снаряда, сцветом