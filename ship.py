import pygame
from pygame.sprite import Sprite  #необходима для создания группы кораблей для вывода количества кораблей поэтому используем спрайты

class Ship(Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game): #получает параметр ai_game(ссылка на текущий экземпляр AlienInvasion), так как Ship получает доступ ко всем ресурсам, определенный AlienInvasion
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen #экран присваивается атрибуту Ship , что бы к нему можно было обращаться в других модулях класса
        self.screen_rect = ai_game.screen.get_rect() #с помощью метода get_rect() можно разместить корабль в нужной позиции экрана
        self.settings = ai_game.settings #оздается атрибут, что бы он он мог использоваться в update()
        #Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship1.bmp') #загружаем изображение
        self.rect = self.image.get_rect()  #атрибуту self.rect присваивается метод get_rect() для получения поверхности корабля
        #Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom #корабль расположен в середине нижней стороны экрана
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x) #так как атрибут rect сохраняет только целое значение, то его нужно преобразовать в дробное значение

    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right: #если флагу присвается значение истина, то корабль перемещается на 1 пиксел вправо и проверятется что бы корабль не выходил за правый край экрана
            self.x += self.settings.ship_speed_factor #величина изменяется на величину хранящуюся в self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        self.rect.x = self.x #обновляет позицию корабля, в self.rect.x будет сохранена только целая часть

    def center_ship(self):
        """Размещвет корабль в центре нижней стороны"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Рисуент корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect) #выводит изображение на экран