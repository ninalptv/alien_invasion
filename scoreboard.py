import pygame.font
from pygame.sprite import Group  # для создания группа кораблей и вывода на экран
from ship import Ship  # тк нужна группа кораблей

class Scoreboard():
    """Класс для вывода игровой информации."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков"""
        self.ai_game = ai_game  # экземпляр игры присваивается атрибуту, тк он нужен для создания кораблей
        self.screen = ai_game.screen  # передается параметр ai_game для обращения к settings screen stats, что бы класс мог выводить инфу об отслеживаемых показателях
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)  # создается экземпляр обекта шрифта
        self.prep_image()


    def prep_image(self):
        """Преобразование в изображение"""
        self.prep_score()  # преобразует текущий счет в графическое изображение
        self.prep_high_score()  # преобразует рекордный счет в графическое изображение
        self.prep_level()  # преобразует уровень в графическое изображение
        self.prep_ships()  # сообщает количество оставшихся кораблей

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        rounded_score = round(self.stats.score, -1)  # приказывает Python округлить stats.score до десятков и сохр в rounded_score
        score_str = "{:,}".format(rounded_score)  # директива форматирования приказывает вставить запятые при преобразовании числового значения строку
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color) #создается изображение
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  #что бы счет всегда оставался выровненым по правой стороне, мы созд прямоугольник
        #и смещем его праву сторону на 20 пикселов от правого края
        self.score_rect.top = 20 # смещаем его на 20 пикселов вниз

    def prep_high_score(self):
        """преобразует рекордный счет в графическое изображение"""
        high_score = round(self.stats.high_score, -1)  # Округляет до десятков
        high_score_str = "{:,}".format(high_score)  # форматируется с запятыми
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)  # преобразуется в изображение
        self.high_score_rect = self.high_score_image.get_rect()  # выравнивается по центру сверху
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Выводит счет, рекорд, уровень, количество кораблей на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)  #для группы вызывается метод draw()

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд"""
        if self.stats.score > self.stats.high_score: # если счет больше рекорда
            self.stats.high_score = self.stats.score # рекодр сохраняется новый
            self.prep_high_score() # преобразует новый рекорд в графтческое изображение

    def prep_level(self):
        """Преобразует уровень в графическое изображение"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Cообщает количество оставшихся кораблей"""
        self.ships = Group()  # создает пустую группу для хранения экземпляров кораблей
        for ship_number in range(self.stats.ship_left):  # цикл выполняется по одному разу для каждого корабля, оставшегося у игрока
            ship = Ship(self.ai_game)  # создается новый корабль
            ship.rect.x = 10 + ship_number * ship.rect.width #координата х задается так, что бы корабли размещались рядом друг с друггом с инт 10 пилсеков
            ship.rect.y = 10
            self.ships.add(ship)  # корабль добавляется в группу

