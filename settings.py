class Settings():
    """Класс храниния всех настроек игры"""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        #Параметры экрана:
        self.screen_width = 1200  #ширина экрана
        self.screen_heihgt = 800   #высота экрана
        self.bg_color = (45, 95, 204) #назначение цвета фона, цвета задаются в схеме RGB

        self.ship_limit = 3
        self.bullet_width = 3  #ширина снаряда 3 пикселя
        self.bullet_height = 15  #высота снаряда 15 пикселей
        self.bullet_color = (60, 60, 60)  #цвет снарядов серый
        self.bullet_allowed = 3 #количество снарядок, которые могут находиться одновременно на экране
        self.fleet_drop_speed = 7.0  # величина снижения флота
        self.speedup_scale = 1.1  # быстрота нарастания скорости
        self.score_scale = 1.5 # коэфициэнт роста начисяемых очков за пришельцев
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Настройки для разных сложностей игры"""
        self.initialize_dynamic_settings_easy()  # метод для инициализ настроек, изменяющихся в ходе игры
        self.initialize_dynamic_settings_normal()
        self.initialize_dynamic_settings_hard()

    def initialize_dynamic_settings_easy(self):
        """Инизиализация настороек, изм в ходе игры"""
        self.ship_speed_factor = 1.1  # добавилась переменная скорости 1,1
        self.bullet_speed_factor = 2.0  # скорость снаряда
        self.alien_speed_factor = 0.4  # скорость пришельцев
        self.fleet_direction = 1  # обозначает движение вправо, -1 влево
        self.alien_points = 50  # стоимость сбитого пришельца

    def initialize_dynamic_settings_normal(self):
        """Инизиализация настороек, изм в ходе игры"""
        self.ship_speed_factor = 1.5  # добавилась переменная скорости 1,5
        self.bullet_speed_factor = 2.5  # скорость снаряда
        self.alien_speed_factor = 0.6  # скорость пришельцев
        self.fleet_direction = 1  # обозначает движение вправо, -1 влево
        self.alien_points = 60  # стоимость сбитого пришельца

    def initialize_dynamic_settings_hard(self):
        """Инизиализация настороек, изм в ходе игры"""
        self.ship_speed_factor = 1.7  # добавилась переменная скорости 1,5
        self.bullet_speed_factor = 2.8  # скорость снаряда
        self.alien_speed_factor = 0.8  # скорость пришельцев
        self.fleet_direction = 1  # обозначает движение вправо, -1 влево
        self.alien_points = 70  # стоимость сбитого пришельца

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
