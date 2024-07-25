import sys   #импортируется модуль sys завершает игру по команде игрока
from time import sleep  #импортируется sleep() что бы игру можно было ненадолго приостановить в момент столкновенияс кораблем
import pygame  #импортируется модуль pygame содержит функциональность, необходимую для создания игры
from settings import Settings #импортируется класс настроек Settings из файла settings.py
from ship import Ship  #импортируется класс из модуля
from bullet import Bullet
from bullet_alien import BulletAlien
from alien import Alien
from game_stats import GameStats
from button import Button
from botton_easy import ButtonEasy
from button_hard import ButtonHard
from button_play import ButtonPlay
from scoreboard import Scoreboard
import json


class AlienInvasion:  #создается класс самой игры
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализиует игру и создает игровые ресурсы."""
        pygame.init()  #функция pygame.init() инициализирует настройки, неодходимые для нормальной работы
        self.settings = Settings() #создается экземпляр класса Settings

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_heihgt))  #создается окно, в котором прорисовываются все шрафические элементы игры
        #аргумент (1200,800) это кортеж, определяющий размеры  игрового окна, он присваивается атрибуту, что бы можно было с ним работать во всех методах класса
        #обьект self.screen называется поверхностью(часть экрана на которой отображается игровой элемент)
        pygame.display.set_caption("Alien Invasion")  #название окна
        self.stats = GameStats(self)  # создание экземпляра для хранения статистики
        self.sb = Scoreboard(self)  # создание экземпляра для хранения панели результатов
        self.ship = Ship(self)  # создается экземпляр, параметр self предостовляет доступ ко всем ресурсам игры
        self.bullets = pygame.sprite.Group()  # группа для хранения всех летящих снарядов представлена  экземпляром класса pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()  # группа для хранения всех пришельцов
        self.bullets_aliens = pygame.sprite.Group()
        self._create_fleet()  # создание флота пришельцев
        self.play_button_normal = Button(self, " normal")  # создание кнопки Play
        self.play_button_easy = ButtonEasy(self, " easy")
        self.play_button_hard = ButtonHard(self, " hard")
        self.play_button_ = ButtonPlay(self, "Play:")



    def run_game(self):  #метод run_game() управляет процессом игры
        """Запуск основного цикла игры."""
        while True:  # цикл непрерывно выполняется, содержит цикл событьй и код, управляющий обновлением экрана
            self._check_events()  # вызывается метод,котрый Обрабатывает нажатие клавиш и события мыши.
            if self.stats.game_active: #проверяется если game_active=True, то игра продлжается(колво кораблей>0)
                self.ship.update()  # вызывается метод,котрый Обновляет позицию корабля с учетом флага
                self._update_bullets()  # вызывается метод,который Обновляет позиции снарядов и уничтожает старые снаряды"
                self._update_aliens()  # обновляются позиции всех пришельцев во флоте
                self._update_bullets_alien()
            self._update_screen()  # вызывается метод,который Обновляет изображения на экране и отображает новый экран

    def _check_events(self): #вспомогательный метод,работает во внутренней реализации класса, но не должен вызываться через экземпляр
        """Обрабатывает нажатие клавиш и события мыши."""
        for event in pygame.event.get(): #цикл событий для прослушивания событий и выполнения соответствующей операции в зависимости от типа произошедшего события
                #для получения доступа к событиям истользуется метод pygame.event.get(), он возвращает список событий, произошедших с момента последнего вызова этой функции
            if event.type == pygame.QUIT:  #обработка конкретного события. Если пользователь щеклает по кнопке закрытия экрана
                    with open(self.stats.file_record, "w") as f:
                        json.dump(self.stats.high_score, f)
                    sys.exit()  #вызывается метод sys.exit() для выхода из игры
            elif event.type == pygame.KEYDOWN:  #отслеживает событие нажатия кнопки
                self._chek_keydown_events(event)  #если кнопка нажата, то вызывается вспомогательный метод
            elif event.type == pygame.KEYUP:  # проверяет произошло ли событие отпускания кнопки
                self._check_keyup_events(event)  #если кнопку отпустили то вызывается вспомогательный метод
            elif event.type == pygame.MOUSEBUTTONDOWN: # обнаруживается события щелканья мыши в любой точке экрана
                mouse_pos = pygame.mouse.get_pos()  #используется метод mouse.get_pos(), возвращающий кортеж с коорд х у точки щелчка, для реагирования только на щелчки по кнопке
                self._check_button(mouse_pos)  # метод запускает игру при нажатии на кнопку

    def _check_button(self, mouse_pos):
        """Запускает новую игру при нажатии на кнопку"""
        button_clicked_easy = self.play_button_easy.rect.collidepoint(mouse_pos)  # метод collidepoint() используется для проверки того, находится ли точка щелчка в пределах обл, определяемой прямоуг кнопки
        if button_clicked_easy and not self.stats.game_active: # проверяется button_clicked и игра была в неактивном сост, для того что бы кнопка не была активной во время игры, что бы нельзя было нажать на эту область и игра перезапустится
            self.settings.initialize_dynamic_settings_easy()  # сброс игровых настроек
            self.start_game()
        elif self.play_button_normal.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings_normal()
            self.start_game()
        elif self.play_button_hard.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings_hard()
            self.start_game()




    def start_game(self):
        """Запускает игру"""
        self.stats.reset_stats()  # сброс игровой статистика, обновление
        self.stats.game_active = True  # если находится в передлах кнопки, то игра переводится в состояние True
        self.sb.prep_image()
        self.aliens.empty()  # чистка списков пришельцев
        self.bullets.empty()  # чистка списков снарядов
        self._create_fleet()  # создается овый флот
        self.ship.center_ship()  # корабль выравнивается по центру
        pygame.mouse.set_visible(False)  # указатель мыши скравыется после начала игры


    def _chek_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_p:
            self.start_game()
        elif event.key == pygame.K_RIGHT: #проверяет нажата ли кнопка (стрелка вправо)
            self.ship.moving_right = True  #если нажата кнопка, то флагу передается значение True и корабл перемещ на 1 пиксел вправо
        elif event.key == pygame.K_LEFT: #проверяет нажата ли кнопка (стрелка влево)
            self.ship.moving_left = True #если нажата кнопка, то флагу передается значение True и корабл перемещ на 1 пиксел влево
        elif event.key == pygame.K_q:  #Если нажимает q то происходит выход из игры
            with open(self.stats.file_record, "w") as f:
                json.dump(self.stats.high_score, f)
            sys.exit()
        elif event.key == pygame.K_SPACE:
            pygame.mixer.Sound('shut.wav').play()
            self._fire_bullet()
            self.fire_bullet_alien()

    def _check_keyup_events(self,event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT: #проверяет что отпустили кнопку в право
            self.ship.moving_right = False #если отпустили кнопку то флагу передается значение False и корабль останавливается
        elif event.key == pygame.K_LEFT: #проверяет что отпустили кнопку влево
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullet_allowed: #при нажатии пробел, программа проверяет длинну группы, если она меньше трех, создается новый снаряд
            new_bullet = Bullet(self)  #создается экземпляр класса Bullet()
            self.bullets.add(new_bullet)  #экземпляр включается в группу bullets с помощью метода add()

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        self.bullets.update()  # вызов update() группы приводит к автомотическому вызову для каждого спрайта в группе. Прорисовываются снаряды при каждом проходе основного цикла и обновляется текущая позиция каждого снаряда
        for bullet in self.bullets.copy():  # элементы из группы не должны удаляться, поэтому перебирается копия группы.
            if bullet.rect.bottom <= 0:  # программа проверяет каждый снаряд и определяет,вышел ли он за верхний край экрана
                self.bullets.remove(bullet)  # если пересек границу-он удаляется
        self._check_bullet_alien_collisions()

    def fire_bullet_alien(self):
        if len(self.bullets_aliens) < 1:
            new_bullet = BulletAlien(self)
            self.bullets_aliens.add(new_bullet)

    def _update_bullets_alien(self):
        screen_rect = self.screen.get_rect()
        self.bullets_aliens.update()
        for bullet in self.bullets_aliens.copy():
            if bullet.rect.top >= screen_rect.bottom:
                self.bullets_aliens.remove(bullet)
        self._check_alien_hit_ship()

    def _check_alien_hit_ship(self):
        collision = pygame.sprite.spritecollideany(self.ship, self.bullets_aliens)
        if collision:
            self._ship_hit()

    def _check_bullet_alien_collisions(self):
        """Обработка колизий и снарядов с пришельцами"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions: # если произошла коллизия то:
            for aliens in collisions.values(): # перебирается все значения в словаре
                self.stats.score += self.settings.alien_points * len(aliens)  # к счету прибавляется стоимость пришельца умноженная на длинну списка пришельцев
            self.sb.prep_score()  # создает новое изображение счета
            self.sb.check_high_score() # проверяет появтлся ли новый рекорд
        if not self.aliens:  # если не осталось пришельцев
            self.start_new_level()

    def start_new_level(self):
        """новый уровень"""
        self.bullets.empty()  # удаляются снаряды
        self._create_fleet()  # создается новый флот
        self.settings.increase_speed()  # метод для увелечения настроек скорости
        self.stats.level += 1  # Увеличивается уровень
        self.sb.prep_level()  # обновляет уровень

    def _create_fleet(self):
        """Создание флота пришельца"""
        alien = Alien(self)  # создание экземпляра пришельца, но он не войдет в флот, экземпляр создается для расчета сколько поместятся приш в ряду
        alien_width, alien_height = alien.rect.size  # значения ширины и высоты пришельца, используется атрибут size оторый собержит кортеж с шириной и высотой обьекта rect
        available_space_x = self.settings.screen_width - alien_width  # вычисляется доступное горизонтальное пространство и кол пришельцев, которое в нем поместятся
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height  # высота корабля для дальнейших вычислений
        available_space_y = (self.settings.screen_heihgt - (3 * alien_height) - (2 * ship_height))  # вычисляем количество рядов, помещяющихся на экране
        number_rows = available_space_y // (2 * alien_height)  # умножается на 2 тк должен быть интервал равзый высоте пришельца
        for row_number in range(number_rows):  #что бы посчитать сколько рядов используем два цикла, это считает сколько рядов
            for alien_number in range(number_aliens_x):  # цикл для создания пришельцев от 0 до кол ва созд пришельцев
                self._create_alien(alien_number, row_number)  # вызывается метод создания пришельца и размещение его в ряду



    def _create_alien(self, alien_number, row_number):  # передаются параметры, сколько пришельцев в ряду и сколько рядов
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)  # создается пришелец
        alien_width, alien_height = alien.rect.size  # значения ширины и высоты пришельца, используется атрибут size оторый собержит кортеж с шириной и высотой обьекта rect
        alien.x = alien_width + 2 * alien_width * alien_number  # определяется коорд х для размещения его в ряду
        # каждый пришелец сдвигается вправо на одну ширину от левого поля, затем *2 тк нужно учесть полное пространство
        # с учетом пустого интервала справа, и полученая величина умножается на позицию в ряду
        alien.rect.x = alien.x  # атрибут х используется для обозначения позиции его прямоугольника
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number  # определяется координата у, каждый новый ряд начинается на две высоты пришельца ниже последнего ряда
        self.aliens.add(alien)  # добавляется в группу для хранения флота

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges(): # если check_edges() возвращает True, значит пришелец находится у края и весь флот должен сменить направление
                self._change_fleet_direction()  # вызывается метод для смены направления и происходит выход из цикла
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites(): # функция перебирает всех пришельцев и меняет высоту каждого из них
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1   # находится не в цикле тк вертикальная позиция должна изменяться для каждого пришельца, но направлеие флота должно измениться единажды

    def _update_aliens(self):
        """Проверяет, достиг ли флот края экрана или столкнулся с кораблем, с последующим обновлением позиций всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  #функция spritecollideany() пытается найти любой элемент группы, вступивший
            # в коллизию со спрайтом и останавливает цикл после обнаружения. Если коллизия не обнаружена, он возвращает None и условие не выполняется
            # если же коллизия обнаружена то условие выполняется и
            self._ship_hit()
        self._check_aliens_bottom()  #проверяет с помощью метода добрался ли хоть один пришелец до нижнего края экрана

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ship_left > 0:  #если колво кораблей больше 0 то выполняется
            self.stats.ship_left -= 1  # когда произошло сталкновение, уменьшается на 1 кол-во кораблей
            self.sb.prep_ships()  # при столкновении корабля с пришельцем изображение колва кораблей обновляется
            self.aliens.empty()  # очищается список пришельцев
            self.bullets.empty()  # очищается список кораблей
            self._create_fleet()  # создается новый флот
            self.ship.center_ship()  # вызывается метод, для размещения корабля в центре нижней стороны
            sleep(0.5)  # делается пауза на 0,5 сек. После управление передается функции _update_screen()
        else:
            with open(self.stats.file_record, "w") as f:
                json.dump(self.stats.high_score, f)
            self.stats.game_active = False #если количество кораблей не осталось то происходит остановка игры
            pygame.mouse.set_visible(True) # указатель снова появится после окончания игры
    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites(): #пебирает всех пришельцев
            if alien.rect.bottom >= screen_rect.bottom: #проверяет добрался ли одтн из пришельцев до нижнего края экрана
                self._ship_hit() # если добрался, то выполняется функция обработки столкновения как с кораблем
                break #дальше перебирать не нужно, поэтому происходит выход из цикла


    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color) #при каждом проходе цикла перерисовывается экран, с пом метода fill()
        self.ship.blitme()  #после заполнения фона корабль рисуетя на экране вызовом blitme()
        for bullet in self.bullets.sprites():  #метод bullets.sprites() возвращает список всех спрайтов в группе bullets
            bullet.draw_bullet() #программа перебирает все спрайты в bullets и вызывает для каждого метод "вывод снаряда на экран"
        self.aliens.draw(self.screen)  #метод draw()  выводит каждый элемент группы с позиции, определяемой его атрибутом rect
        for bullet_alien in self.bullets_aliens.sprites():
            bullet_alien.draw_bullet_alien()
        self.sb.show_score()  #вывод информации о счете
        if not self.stats.game_active: #что бы кнопка не закрывалась другими элемпнтами экрана, мы ее отображаем после всех элем
        # в блоке if что бы кнопка отображалась только в неактивном состоянии
            self.play_button_.draw_button()
            self.play_button_normal.draw_button()
            self.play_button_easy.draw_button()
            self.play_button_hard.draw_button()

        pygame.display.flip() #вызов pygame.display.flip() приказывает Pygame отобразить последний отрисованный экран, будет постоянно обновлять экран,
            #отображая игровые элементы в новых позициях и скрывая старые изображения

if __name__ == '__main__': #Используется условие, что бы оно выполнялось про прямом вызове функции
    ai = AlienInvasion() #создание экземпляра
    ai.run_game() #запуск игры
