from bird import Bird
from pipe import Pipe
import random
import arcade
from pyglet.image import load
from pyglet.graphics import Batch
from arcade.particles import FadeParticle, Emitter, EmitBurst

# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Flappy Bird"
JUMP = 7
GRAVITY = 0.55
TIME_APPEARANCE_FOR_TEXT = 0.5
TIME_APPEARANCE_FOR_PIPE = 2.75
IMMORTALITY_TIME = 3.0
TIME_OF_POWER_UP = 10
SPEED = 1.0
SPEED_UPDATE = 1.2
GAP_BETWEEN_PIPES = 100
CIRCLE_WIDTH = 50.0
CIRCLE_HEIGHT = 50.0
CIRCLE_START_ANGLE = 0.0
CIRCLE_END_ANGLE = 360.0
MAX_SPEED = 4.0
CAMERA_LERP = 0.12


# Сделаем набор текстур прямо в рантайме
SPARK_TEX = [arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON)]


class StartView(arcade.View):
    def __init__(self):
        """Инициализация стартового окна"""
        super().__init__()

        # Загрузка всех текстур в стартовое окно
        self.texture = arcade.load_texture('src/assets/sprites/background-day.png')
        self.flappy_bird_texture = arcade.load_texture('src/assets/sprites/flappy_bird.png')
        self.base_texture = arcade.load_texture('src/assets/sprites/base.png')
        self.start_texture = arcade.load_texture('src/assets/sprites/press_any_key_to_start.png')

        self.time_appearance = 0.5
        self.show_text = True

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(self.base_texture, center_x=self.width // 2, center_y=self.base_texture.height // 2)
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(self.base_texture, center_x=self.width + self.width // 2,
                                   center_y=self.base_texture.height // 2)
        self.base_list.append(self.base2)

        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        self.bird = Bird()
        self.bird.center_x = self.width // 2.7 + self.flappy_bird_texture.width - self.bird.width
        self.bird.center_y = self.height // 1.75 + self.flappy_bird_texture.height + 125
        self.player_list.append(self.bird)

    def on_draw(self):
        """Отрисовка стартового экрана"""
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                                self.height))
        arcade.draw_texture_rect(self.flappy_bird_texture, arcade.rect.XYWH(self.width // 2.5, self.height - 50,
                                                                            self.flappy_bird_texture.width,
                                                                            self.flappy_bird_texture.height))
        self.player_list.draw()
        self.base_list.draw()
        if self.show_text:
            arcade.draw_texture_rect(self.start_texture, arcade.rect.XYWH(self.width // 2,
                                                                          self.height // 2,
                                                                          self.start_texture.width,
                                                                          self.start_texture.height))

    def on_update(self, delta_time):
        """Обновление стартового экрана"""
        self.player_list.update()
        for base in self.base_list:
            base.center_x -= SPEED
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2
        self.time_appearance -= delta_time
        if self.time_appearance < 0:
            self.time_appearance = 0.5
            self.show_text = not self.show_text

    def on_key_press(self, key, modifiers):
        """Начало игры при нажатии любой клавиши"""
        flappy_bird = FlappyBirdGame()
        self.window.show_view(flappy_bird)


class FlappyBirdGame(arcade.View):
    def __init__(self):
        """Инициализация игрового окна"""
        super().__init__()
        # Загрузка всех текстур в игровое окно
        self.texture_day = arcade.load_texture('src/assets/sprites/background-day.png')
        self.texture_night = arcade.load_texture('src/assets/sprites/background-night.png')
        self.flappy_bird_texture = arcade.load_texture('src/assets/sprites/flappy_bird.png')
        self.base_texture = arcade.load_texture('src/assets/sprites/base.png')
        self.message_texture = arcade.load_texture('src/assets/sprites/get_ready.png')
        self.double_points_texture = arcade.load_texture('src/assets/sprites/double_points.png')
        self.shield_texture = arcade.load_texture('src/assets/sprites/bubble_shield.png')
        self.extra_heart_full_texture = arcade.load_texture('src/assets/sprites/extra_heart_full.png')
        self.extra_heart_empty_texture = arcade.load_texture('src/assets/sprites/extra_heart_empty.png')
        self.ghost_texture = arcade.load_texture('src/assets/sprites/ghost.png')
        self.wide_pipes_texture = arcade.load_texture('src/assets/sprites/wide_pipes.png')
        self.shield_sprite = None

        self.power_up_textures = {'Double Points': [self.double_points_texture, 1],
                                  'Shield': [self.shield_texture, random.randint(3, 5)],
                                  'Extra Heart': self.extra_heart_full_texture,
                                  'Ghost Mode': [self.ghost_texture, 1],
                                  'Wide Passage': [self.wide_pipes_texture, 1]}
        self.hearts_texture = {1: [self.extra_heart_full_texture, self.extra_heart_empty_texture],
                               2: [self.extra_heart_full_texture, self.extra_heart_empty_texture],
                               3: [self.extra_heart_full_texture, self.extra_heart_empty_texture]}
        self.number_textures = {'0': arcade.load_texture('src/assets/sprites/0.png'),
                                '1': arcade.load_texture('src/assets/sprites/1.png'),
                                '2': arcade.load_texture('src/assets/sprites/2.png'),
                                '3': arcade.load_texture('src/assets/sprites/3.png'),
                                '4': arcade.load_texture('src/assets/sprites/4.png'),
                                '5': arcade.load_texture('src/assets/sprites/5.png'),
                                '6': arcade.load_texture('src/assets/sprites/6.png'),
                                '7': arcade.load_texture('src/assets/sprites/7.png'),
                                '8': arcade.load_texture('src/assets/sprites/8.png'),
                                '9': arcade.load_texture('src/assets/sprites/9.png')}

        # Загрузка звуков в игру
        self.jump_sound = arcade.load_sound("src/assets/audio/wing.wav")
        self.hit_sound = arcade.load_sound("src/assets/audio/hit.wav")
        self.point_sound = arcade.load_sound("src/assets/audio/point.wav")
        self.broken_glass_sound = arcade.load_sound("src/assets/audio/broken_glass_sound.wav")
        self.die_sound = arcade.load_sound("src/assets/audio/die.wav")

        # Булевые рычаги для работы с игрой и усилителями
        self.stand_by = True
        self.show_text = True
        self.immortality = False
        self.can_spawn_power_up = False
        self.power_up_is_active = False
        self.double_points = False
        self.shield = False
        self.ghost_mode = False
        self.wide_passage = False

        # Числовые значения для взаимодействия с достижениями и функционалами игры
        self.level = 0
        self.duration_seconds = 0
        self.health = 3
        self.score = 0
        self.pipes_passed = 0
        self.powerup_types_count = 0
        self.zooming = 1.0
        self.speed = SPEED
        self.immortality_time = IMMORTALITY_TIME
        self.time_appearance = TIME_APPEARANCE_FOR_TEXT
        self.time_appearance_for_pipe = TIME_APPEARANCE_FOR_PIPE
        self.time_appearance_for_power_ups = random.randint(3, 10)
        self.active_time_of_power_up = TIME_OF_POWER_UP

        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()
        self.power_up_lists = arcade.SpriteList()
        self.shield_list = arcade.SpriteList()
        self.time_list = arcade.SpriteList()
        self.emitters = []

        self.day = arcade.Sprite(self.texture_day, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2)
        self.night = arcade.Sprite(self.texture_night, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2)
        self.night.alpha = 0

        self.time_list.extend([self.day, self.night])

        self.hearts_list = arcade.SpriteList()
        for ind in range(1, max(self.hearts_texture.keys()) + 1):
            heart = arcade.Sprite(self.hearts_texture[ind][0], scale=0.1,
                                  center_x=self.width - (self.width // 10) * ind,
                                  center_y=self.width // 10)
            self.hearts_list.append(heart)

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(self.base_texture, center_x=self.width // 2, center_y=self.base_texture.height // 2)
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(self.base_texture, center_x=self.width + self.width // 2,
                                   center_y=self.base_texture.height // 2)
        self.base_list.append(self.base2)

        self.physics_engine = None
        self.world_camera = None
        self.batch = Batch()

        self.bird = Bird()
        self.bird.center_x = self.width // 3
        self.bird.center_y = self.height // 2
        self.bird.gravity = GRAVITY
        self.player_list.append(self.bird)

        self.bird_in_night = Bird(True)
        self.bird_in_night.center_x = self.width // 3
        self.bird_in_night.center_y = self.height // 2
        self.bird_in_night.gravity = GRAVITY
        self.bird_in_night.alpha = 0
        self.player_list.append(self.bird_in_night)

    def on_draw(self):
        """Отрисовка игрового экрана"""
        self.clear()

        # Рисование дня/ночи и текста посередине экрана
        self.time_list.draw()
        if self.stand_by and self.show_text:
            arcade.draw_texture_rect(self.message_texture, arcade.rect.XYWH(self.width // 2, self.height // 2,
                                                                            self.message_texture.width,
                                                                            self.message_texture.height))

        # Рисование спрайтов
        self.pipe_list.draw()
        self.base_list.draw()
        self.player_list.draw()
        self.power_up_lists.draw()
        self.shield_list.draw()
        self.hearts_list.draw()

        # Рисовка частиц
        for emit in self.emitters:
            emit.draw()

        # Активация камеры после окончания жизней
        if self.world_camera is not None:
            self.world_camera.use()

        # Рисование текстур сердец
        for ind in range(1, max(self.hearts_texture.keys()) + 1):
            self.hearts_list[ind - 1].texture = (self.hearts_texture[ind][0] if 0 < self.health >= ind else
                                                self.hearts_texture[ind][1])

        # Рисовка таймера действия усилителя в качестве круга
        if self.power_up_is_active:
            arcade.draw_arc_filled(self.width // 2, self.height // 10, CIRCLE_WIDTH, CIRCLE_HEIGHT, arcade.color.WHITE,
                                   start_angle=CIRCLE_START_ANGLE,
                                   end_angle=CIRCLE_END_ANGLE * (self.active_time_of_power_up / TIME_OF_POWER_UP),
                                   tilt_angle=-90)

        # Рисование очков
        for number in range(len(str(self.score)) - 1, -1, -1):
            width_for_text = self.width // 2 - self.number_textures[str(self.score)[::-1][0]].width * number
            arcade.draw_texture_rect(self.number_textures[str(self.score)[::-1][number]],
                                     arcade.rect.XYWH(width_for_text,
                                                      self.height  - (self.height // 10),
                                                      self.number_textures[str(self.score)[::-1][number]].width,
                                                      self.number_textures[str(self.score)[::-1][number]].height))

        # Рисовка текста
        text = arcade.Text(f'Level: {self.level}', self.width // 5, self.height // 25, anchor_x='center',
                           font_size=24, batch=self.batch)
        self.batch.draw()

    def on_update(self, delta_time):
        """Обновление игрового экрана"""
        delta_time_speed = delta_time + (delta_time * (self.level / 4))
        if self.health:
            if self.physics_engine is not None:
                self.physics_engine.update()
            self.player_list.update(delta_time)

            # Не позволяет птице улететь за экран
            if self.bird.top > SCREEN_HEIGHT:
                self.bird.change_y = 0
                self.bird.center_y = SCREEN_HEIGHT - self.bird.height // 2
                self.bird.angle = 0

            # Функция для сдвига земли
            self.move_base()

            self.time_appearance -= delta_time
            if self.time_appearance < 0:  # Проверка "Пришло ли время тексту исчезнуть/появиться?"
                self.time_appearance = TIME_APPEARANCE_FOR_TEXT
                self.show_text = not self.show_text

            # Проверка "Можно ли 'заспавнить' усилитель"
            if not self.can_spawn_power_up and not self.stand_by:
                self.time_appearance_for_power_ups -= delta_time
                if self.time_appearance_for_power_ups < 0:
                    self.time_appearance_for_power_ups = 10
                    self.can_spawn_power_up = True

            # Проверка "Нажал ли игрок на пробел (SPACE) хотя бы 1 раз?"
            if not self.stand_by:
                self.time_appearance_for_pipe -= delta_time_speed
                self.duration_seconds += delta_time
                if self.duration_seconds // 10 > self.level:
                    if MAX_SPEED > self.speed:
                        self.level += 1
                        self.speed = self.speed * SPEED_UPDATE

            # Проверка "Пришло ли время появится трубе?"
            if self.time_appearance_for_pipe < 0:
                self.time_appearance_for_pipe = TIME_APPEARANCE_FOR_PIPE
                self.generate_pipes()

            # Проверка "Столкнулся ли игрок с трубой?"
            self.touched_pipe()

            self.check_immortality(delta_time)

            # Передвижение трубы влево и проверка "прошла ли через неё птичка?"
            self.move_pipes()

            # Передвижение усиления влево
            for power_up in self.power_up_lists:
                power_up.center_x -= self.speed
                if power_up.right < -SCREEN_WIDTH:
                    self.power_up_lists.remove(power_up)

            # Проверка "Коснулись ли мы усиления?"
            self.grab_power_up()

            # Проверка на активность усиления
            if self.power_up_is_active:
                self.active_time_of_power_up -= delta_time
                if self.active_time_of_power_up > 0:
                    self.set_power_up()
                else:
                    self.disable_power_up()

            # Проверка "Коснулась ли птичка земли?" и "Сделала ли птичка прыжок?"
            self.touched_base()

            # Обновляем частицы
            emitters_copy = self.emitters.copy()  # Защищаемся от мутаций списка
            for emit in emitters_copy:
                emit.update(delta_time)
            for emit in emitters_copy:
                if emit.can_reap():  # Готов к уборке?
                    self.emitters.remove(emit)

            # Изменяем центр X и Y голубой птички, а также угол наклона
            self.bird_in_night.center_x, self.bird_in_night.center_y = (self.bird.center_x, self.bird.center_y)
            self.bird_in_night.angle = self.bird.angle

            # Меняем день и ночь каждые 30 секунд
            if self.duration_seconds // 30 % 2 == 1:
                self.night.alpha += 5 if self.night.alpha < 255 else 0
                self.bird_in_night.alpha += 5 if self.bird_in_night.alpha < 255 else 0
                self.bird.alpha -= 5 if self.bird.alpha > 0 else 0
            else:
                self.night.alpha -= 5 if self.night.alpha > 0 else 0
                self.bird_in_night.alpha -= 5 if self.bird_in_night.alpha > 0 else 0
                self.bird.alpha += 5 if self.bird.alpha < 255 else 0

        else:
            # Уменьшаем масштабируемость камеры перед переключением экрана
            self.world_camera = arcade.camera.Camera2D(zoom=self.zooming)
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
                self.world_camera.position,
                position,
                CAMERA_LERP)

            self.zooming += delta_time * 5

    def on_key_press(self, key, modifiers):
        """Управление птичкой"""
        if key == arcade.key.SPACE and self.bird.on_game_view and self.health:
            self.physics_engine.jump(JUMP)
            self.bird.jump_high = JUMP
            self.bird.current_angle = -60
            self.jump_sound.play()
        elif key == arcade.key.SPACE and not self.bird.on_game_view and self.health:
            self.stand_by = False
            self.bird.on_game_view = True
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.bird, walls=self.base_list,
                                                                 gravity_constant=GRAVITY)
            self.physics_engine.jump(JUMP)
            self.bird.jump_high = JUMP
            self.bird.current_angle = -60
            self.jump_sound.play()

    def gravity_drag(self, p):
        """Для искр: чуть вниз и затухание скорости"""
        p.change_y += -0.03
        p.change_x *= 0.92
        p.change_y *= 0.92

    def make_ring(self, x, y, count=40, radius=5.0):
        """Кольцо искр (векторы направлены по окружности)"""
        return Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(count),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=random.choice(SPARK_TEX),
                change_xy=arcade.math.rand_on_circle((0.0, 0.0), radius),
                lifetime=random.uniform(0.8, 1.4),
                start_alpha=255, end_alpha=0,
                scale=random.uniform(0.4, 0.7),
                mutation_callback=self.gravity_drag,
            ),
        )

    def touched_base(self):
        """Коснулся ли игрок земли?"""
        if self.physics_engine is not None:
            if self.physics_engine.can_jump(6) and not self.bird.on_the_ground:
                self.bird.current_angle = 0
                self.bird.on_the_ground = True
                if not self.immortality:
                    self.immortality = True
                    if self.shield:
                        self.disable_power_up()
                        self.broken_glass_sound.play()
                    else:
                        self.health -= 1
                        self.hit_sound.play()
            elif not self.physics_engine.can_jump(6) and self.bird.on_the_ground:
                self.bird.on_the_ground = False

    def touched_pipe(self):
        """Коснулся ли игрок трубы?"""
        if (arcade.check_for_collision_with_list(self.bird, self.pipe_list) and not self.immortality and
                not self.ghost_mode):
            self.immortality = True
            if self.shield:
                self.disable_power_up()
                self.broken_glass_sound.play()
            else:
                self.health -= 1
                self.hit_sound.play()

    def grab_power_up(self):
        """Схватил ли усилитель?"""
        grab_power_up = arcade.check_for_collision_with_list(self.bird, self.power_up_lists)
        for elem in grab_power_up:
            for key, value in self.power_up_textures.items():
                if key != 'Extra Heart':
                    self.power_up_textures[key] = [value[0], value[1] - 1]
                    if elem.texture == value[0]:
                        if key == 'Double Points':
                            self.double_points = True
                        elif key == 'Shield':
                            self.shield = True
                            self.shield_sprite = arcade.Sprite(self.shield_texture,
                                                               center_x=self.bird.center_x,
                                                               center_y=self.bird.center_y, scale=0.1)
                            self.shield_sprite.alpha = 127
                            self.shield_list.append(self.shield_sprite)
                        elif key == 'Ghost Mode':
                            self.ghost_mode = True
                            self.immortality = False
                        elif key == 'Wide Passage':
                            self.wide_passage = True
                        self.power_up_is_active = True
                else:
                    if elem.texture == value:
                        self.health += 1
            self.emitters.append(self.make_ring(self.bird.center_x, self.bird.center_y))
            elem.remove_from_sprite_lists()
            self.powerup_types_count += 1

    def generate_pipes(self):
        """Генерация труб (снизу и сверху друг от друга на 100 пикселей)"""
        powerup_sprite = None
        gap = random.randint(self.base_texture.height // 3, self.height // 3)
        pipe1 = Pipe()
        pipe1.center_x = self.width + pipe1.width // 2
        pipe1.center_y = gap

        pipe2 = Pipe(True)
        pipe2.center_x = self.width + pipe2.width // 2
        pipe2.center_y = pipe1.top + GAP_BETWEEN_PIPES + pipe2.height // 2

        self.pipe_list.append(pipe1)
        self.pipe_list.append(pipe2)

        if self.can_spawn_power_up:
            key = self.generate_power_up()
            for k, value in self.power_up_textures.items():
                if k == key and key != 'Extra Heart' and value[1] > 0:
                    powerup_texture = value[0]
                    if key != 'Double Points':
                        powerup_sprite = arcade.Sprite(powerup_texture, center_x=self.width + pipe2.width // 2,
                                                       center_y=pipe1.top + GAP_BETWEEN_PIPES // 2, scale=0.1)
                    else:
                        powerup_sprite = arcade.Sprite(powerup_texture, center_x=self.width + pipe2.width // 2,
                                                       center_y=pipe1.top + GAP_BETWEEN_PIPES // 2)
                    if value[1] == 0:
                        del self.power_up_textures[key]
                    break
                elif k == key and key == 'Extra Heart':
                    powerup_texture = value
                    powerup_sprite = arcade.Sprite(powerup_texture, center_x=self.width + pipe2.width // 2,
                                                   center_y=pipe1.top + GAP_BETWEEN_PIPES // 2, scale=0.1)
                    break
            if powerup_sprite is not None:
                self.power_up_lists.append(powerup_sprite)
            self.can_spawn_power_up = False

    def generate_power_up(self):
        """Генерация усилителя"""
        keys = list(self.power_up_textures.keys())
        while True:
            key = random.choice(keys)
            if key == 'Extra Heart' and self.health >= 3:
                continue
            return key

    def move_base(self):
        """Передвижение земли"""
        for base in self.base_list:
            base.center_x -= self.speed
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2

    def move_pipes(self):
        """Передвижение трубы"""
        for pipe in self.pipe_list:
            pipe.center_x -= self.speed
            if pipe.right < -SCREEN_WIDTH:
                pipe.remove_from_sprite_lists()
            if pipe.center_x < self.bird.center_x and not pipe.passed:
                if not self.immortality:
                    self.point_sound.play()
                    self.score += 2 if self.double_points else 1
                    self.pipes_passed += 1
                pipe.passed = True

    def check_immortality(self, delta_time):
        """Проверка на режим бессмертия"""
        if self.immortality:
            if self.duration_seconds // 30 % 2 == 0:
                self.bird.alpha = 127
            else:
                self.bird_in_night.alpha = 127
            self.immortality_time -= delta_time
            if self.immortality_time < 0:
                if self.duration_seconds // 30 % 2 == 0:
                    self.bird.alpha = 255 if not self.ghost_mode else 127
                else:
                    self.bird_in_night.alpha = 255 if not self.ghost_mode else 127
                self.immortality_time = IMMORTALITY_TIME
                self.immortality = False

    def set_power_up(self):
        """Активация усилителя"""
        if self.shield:
            self.shield_sprite.center_x = self.bird.center_x
            self.shield_sprite.center_y = self.bird.center_y
        elif self.ghost_mode:
            self.bird.alpha = 127
        elif self.wide_passage and len(self.pipe_list) % 2 == 0:
            for i in range(0, len(self.pipe_list), 2):
                self.pipe_list[i + 1].center_y = (self.pipe_list[i].top + GAP_BETWEEN_PIPES +
                                                  (GAP_BETWEEN_PIPES // 2) +
                                                  self.pipe_list[i + 1].height // 2)

    def disable_power_up(self):
        """Деактивация усилителя"""
        self.power_up_is_active = False
        self.active_time_of_power_up = TIME_OF_POWER_UP
        self.double_points = False

        self.shield = False
        if self.shield_sprite is not None:
            self.shield_list.remove(self.shield_sprite)
        self.shield_sprite = None

        self.ghost_mode = False
        self.bird.alpha = 255

        self.wide_passage = False
        if len(self.pipe_list) % 2 == 0:
            for i in range(0, len(self.pipe_list), 2):
                self.pipe_list[i + 1].center_y = (self.pipe_list[i].top + GAP_BETWEEN_PIPES +
                                                  self.pipe_list[i + 1].height // 2)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.icon = load('src/assets/favicon.ico')
    window.set_icon(window.icon)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()