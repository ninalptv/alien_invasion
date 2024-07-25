import pygame.font  #импортирует данный модуль для вывода текста на экран

class ButtonPlay():
    """Класс описываеющий кнопку начала игры"""
    def __init__(self, ai_game, msg):  # получает параметры self, объект ai_game, строку с текстом кнопки msg
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.width, self.height = 200, 50  # размеры кнопки
        self.button_color = (0, 255, 0) # цвет кнопки
        self.text_color = (255, 255, 255)  # цвет текста
        self.font = pygame.font.SysFont(None, 48)  # подготовка для вывлода текста(None-штифт по умолчанию, 48-размер шрифта)
        self.rect = pygame.Rect(0, 0, self.width, self.height)  # строится прямоугольник кнопки
        self.rect.centerx = self.screen_rect.centerx  # выравнивается по центру экрана
        self.rect.centery = self.screen_rect.centery - 100
        self.prep_msg(msg)  # метод преобразует msg в прямоугольник  и выравнивает текст по центру

    def prep_msg(self, msg): # метод получает параметр self и текст, который нужно вывести в графическом виде
        """Преобразует msg в прямоугольник  и выравнивает текст по центру"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) # font.render преобразует текст
        # хранящийся в msg в изображение, True- значит режим сглаживания текста,
        self.msg_image_rect = self.msg_image.get_rect() #  метод get_rect() вызывается для того, что бы потом выравнить по центру
        self.msg_image_rect.center = self.rect.center # изображение текста выравнивается по центру кнопки

    def draw_button(self):
        """Отображение пустой кнопки и вывод сообщения"""
        self.screen.fill(self.button_color, self.rect) # метод screen.fill() рисует прямоугольную часть кнопки
        self.screen.blit(self.msg_image, self.msg_image_rect)  # метод screen.blit() выводит изображение текста на экран, с передачей изображения и объекта rect, связвнного с изображением
