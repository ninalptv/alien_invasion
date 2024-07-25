import pygame
from pygame.sprite import Sprite  #импорт класса-родителя для группировки связанных элементов и выполнения операций со всеми
#группироыванными элементами обновременно

class Bullet(Sprite): #Класс Bullet наследует Sprite
    """Класс для управления снарядами, выпущеными кораблем"""
    def __init__(self, ai_game):
        """Создает обьект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  #Строится прямоугольник с пом pygame.Rect
        #При создании необходимо задать координаты левого верхнего угла, его ширивы и высоту
        self.rect.midtop = ai_game.ship.rect.midtop  #чтобы верхний край снаряда появлялся у верхнего края корабля rect.midtop присваивается midtop корабля
        self.y = float(self.rect.y) #позиция снаряда хранится в вещественно формате

    def update(self):  #метод управляет позицией снаряда
        """Перемещает снаряд вверх по экрану"""
        self.y -= self.settings.bullet_speed_factor #Когда происходит выстрел, снаряд двигается вверх по экрану(уменьшение y). обновление снаряда в вещественном формате
        self.rect.y = self.y #обновление позиции прямоугольника

    def draw_bullet(self):
        """Вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)  #фуекция draw.rect() заполняет часть екрана, определяемую прямоугольником снаряда, сцветом