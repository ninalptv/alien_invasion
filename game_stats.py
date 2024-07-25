import json


class GameStats():
    """Отслеживаение статистики для игры Alien Invasion."""
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()  #часть статистики будет сбрасываться в начале каждой игры. Для этого большая часть статистики
        #будет инициализ в методе reset_stats(). Этот метод будет вызываться из __init__, чтобы статистика правильно иниц
        #при первом создании экземпляра GameStats
        self.game_active = False  #устанавливается флаг для игры, программа запускается в неактивном состоянии, ее можно запустить с пом кнопки Play
        self.file_record = 'record.json'
        with open(self.file_record) as f:
            self.high_score = json.load(f)


    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ship_left = self.settings.ship_limit
        self.score = 0 # счет, добавляем его в этот метод, что бы он сбрасывался при запуске новой игры
        self.level = 1  # атрибут уровня, в функции определен, тк он должен сбрасываться