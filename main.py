from bird import Bird
from pipe import Pipe
import random
import arcade
from pyglet.image import load

# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Flappy Bird"
JUMP = 7
GRAVITY = 0.55
TIME_APPEARANCE_FOR_TEXT = 0.5
TIME_APPEARANCE_FOR_PIPE = 2.75
IMMORTALITY_TIME = 3.0
ACTIVE_TIME_OF_POWER_UP = 10
SPEED = 1.0
SPEED_UPDATE = 1.2
GAP_BETWEEN_PIPES = 100


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
        """Отрисовка начального экрана"""
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
        """Обновление начального экрана"""
        self.player_list.update()
        for base in self.base_list:
            base.center_x -= 1
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2
        self.time_appearance -= delta_time
        if self.time_appearance < 0:
            self.time_appearance = 0.5
            self.show_text = not self.show_text

    def on_key_press(self, key, modifiers):
        """Начало игры при нажатии клавиши"""
        flappy_bird = FlappyBirdGame()
        self.window.show_view(flappy_bird)


class FlappyBirdGame(arcade.View):
    def __init__(self):
        """Инициализация игрового окна"""
        super().__init__()

        # Загрузка всех текстур в игровое окно
        self.texture = arcade.load_texture('src/assets/sprites/background-day.png')
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

        # Загрузка звуков в игру
        self.jump_sound = arcade.load_sound("src/assets/audio/wing.wav")
        self.hit_sound = arcade.load_sound("src/assets/audio/hit.wav")
        self.point_sound = arcade.load_sound("src/assets/audio/point.wav")
        self.broken_glass_sound = arcade.load_sound("src/assets/audio/broken_glass_sound.wav")

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
        self.speed = SPEED
        self.immortality_time = IMMORTALITY_TIME
        self.time_appearance = TIME_APPEARANCE_FOR_TEXT
        self.time_appearance_for_pipe = TIME_APPEARANCE_FOR_PIPE
        self.time_appearance_for_power_ups = random.randint(15, 20)
        self.active_time_of_power_up = ACTIVE_TIME_OF_POWER_UP

        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()
        self.power_up_lists = arcade.SpriteList()

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(self.base_texture, center_x=self.width // 2, center_y=self.base_texture.height // 2)
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(self.base_texture, center_x=self.width + self.width // 2,
                                   center_y=self.base_texture.height // 2)
        self.base_list.append(self.base2)

        self.physics_engine = None

        self.bird = Bird()
        self.bird.center_x = self.width // 3
        self.bird.center_y = self.height // 2
        self.bird.gravity = GRAVITY
        self.player_list.append(self.bird)

    def on_draw(self):
        """Отрисовка игрового экрана"""
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                                self.height))
        if self.stand_by and self.show_text:
            arcade.draw_texture_rect(self.message_texture, arcade.rect.XYWH(self.width // 2, self.height // 2,
                                                                            self.message_texture.width,
                                                                            self.message_texture.height))
        self.pipe_list.draw()
        self.base_list.draw()
        self.player_list.draw()
        self.power_up_lists.draw()

    def on_update(self, delta_time):
        """Обновление игрового экрана"""
        delta_time_speed = delta_time + (delta_time * (self.level // 3))
        if self.health:
            if self.physics_engine is not None:
                self.physics_engine.update()
            self.player_list.update(delta_time)

            # Функция для сдвига земли
            self.move_base()

            self.time_appearance -= delta_time
            if self.time_appearance < 0:  # Проверка "Пришло ли время тексту исчезнуть/появиться?"
                self.time_appearance = TIME_APPEARANCE_FOR_TEXT
                self.show_text = not self.show_text

            if not self.can_spawn_power_up and not self.stand_by:
                self.time_appearance_for_power_ups -= delta_time
                if self.time_appearance_for_power_ups < 0:
                    self.time_appearance_for_power_ups = random.randint(15, 20)
                    self.can_spawn_power_up = True

            # Проверка "Нажал ли игрок на пробел (SPACE) хотя бы 1 раз?"
            if not self.stand_by:
                self.time_appearance_for_pipe -= delta_time_speed
                self.duration_seconds += delta_time
                if self.duration_seconds // 10 > self.level:
                    self.level += 1
                    self.speed = self.speed * SPEED_UPDATE
                    delta_time_speed = delta_time + (delta_time * (self.level // 2))

            # Проверка "Пришло ли время появится трубе?"
            if self.time_appearance_for_pipe < 0:
                self.time_appearance_for_pipe = TIME_APPEARANCE_FOR_PIPE
                self.generate_pipes()

            # Проверка "Столкнулся ли игрок с трубой?"
            if (arcade.check_for_collision_with_list(self.bird, self.pipe_list) and not self.immortality and
                    not self.ghost_mode):
                self.immortality = True
                if self.shield:
                    self.disable_power_up()
                    self.broken_glass_sound.play()
                else:
                    self.health -= 1
                    self.hit_sound.play()

            if self.immortality:
                self.bird.alpha = 127
                self.immortality_time -= delta_time
                if self.immortality_time < 0 and not self.ghost_mode:
                    self.bird.alpha = 255
                    self.immortality_time = IMMORTALITY_TIME
                    self.immortality = False

            # Передвижение трубы влево и проверка "прошла ли через неё птичка?"
            self.move_pipes()

            # Передвижение усиления влево
            for power_up in self.power_up_lists:
                power_up.center_x -= self.speed
                if power_up.right < -SCREEN_WIDTH:
                    self.power_up_lists.remove(power_up)

            # Проверка "Коснулись ли мы усиления?"
            self.can_grab_power_up()

            # Проверка на активность усиления
            if self.power_up_is_active:
                self.active_time_of_power_up -= delta_time
                if self.active_time_of_power_up > 0:
                    self.set_power_up()
                else:
                    self.disable_power_up()

            # Проверка "Коснулась ли птичка земли?" и "Сделала ли птичка прыжок?"
            self.touched_base()

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

    def touched_base(self):
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

    def can_grab_power_up(self):
        grab_power_up = arcade.check_for_collision_with_list(self.bird, self.power_up_lists)
        for elem in grab_power_up:
            for key, value in self.power_up_textures.items():
                if key != 'Extra Heart':
                    if elem.texture == value[0]:
                        if key == 'Double Points':
                            self.double_points = True
                        elif key == 'Shield':
                            self.shield = True
                            self.shield_sprite = arcade.Sprite(self.shield_texture,
                                                               center_x=self.bird.center_x,
                                                               center_y=self.bird.center_y, scale=0.1)
                            self.shield_sprite.alpha = 127
                            self.power_up_lists.append(self.shield_sprite)
                        elif key == 'Ghost Mode':
                            self.ghost_mode = True
                        elif key == 'Wide Passage':
                            self.wide_passage = True
                        self.power_up_is_active = True
                else:
                    if elem.texture == value:
                        self.health += 1
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
            keys = list(self.power_up_textures.keys())
            key = random.choice(keys)
            for k, value in self.power_up_textures.items():
                if k == key and key != 'Extra Heart' and value[1] > 0:
                    self.power_up_textures[key] = [value[0], value[1] - 1]
                    powerup_texture = value[0]
                    if key != 'Double Points':
                        powerup_sprite = arcade.Sprite(powerup_texture, center_x=self.width + pipe2.width // 2,
                                                       center_y=pipe1.top + GAP_BETWEEN_PIPES // 2, scale=0.1)
                    else:
                        powerup_sprite = arcade.Sprite(powerup_texture, center_x=self.width + pipe2.width // 2,
                                                       center_y=pipe1.top + GAP_BETWEEN_PIPES // 2)
                    if value[1] == 0:
                        self.power_up_textures.pop(key)
                    break
                elif k == key and key == 'Extra Heart' and self.health < 3:
                    powerup_texture = value
                    powerup_sprite = arcade.Sprite(powerup_texture, center_x=self.width + pipe2.width // 2,
                                                   center_y=pipe1.top + GAP_BETWEEN_PIPES // 2, scale=0.1)
                    break
            if powerup_sprite is not None:
                self.power_up_lists.append(powerup_sprite)
            self.can_spawn_power_up = False

    def move_base(self):
        for base in self.base_list:
            base.center_x -= self.speed
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2

    def move_pipes(self):
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

    def set_power_up(self):
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
        self.power_up_is_active = False
        self.active_time_of_power_up = ACTIVE_TIME_OF_POWER_UP
        self.double_points = False

        self.shield = False
        self.power_up_lists.clear()
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