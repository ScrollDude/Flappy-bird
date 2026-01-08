from bird import Bird
from pipe import Pipe
import random
import arcade

# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Flappy Bird"
JUMP = 7
GRAVITY = 0.55
TIME_APPEARANCE = 0.5
TIME_APPEARANCE_FOR_PIPE = 3.0
SPEED = 1.0
GAP_BETWEEN_PIPES = 100


class StartView(arcade.View):
    def __init__(self):
        """Инициализация стартового окна"""
        super().__init__()
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

    def setup(self):
        """Настройка начального экрана"""
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
        flappy_bird.setup()
        self.window.show_view(flappy_bird)


class FlappyBirdGame(arcade.View):
    def __init__(self):
        """Инициализация игрового окна"""
        super().__init__()
        self.texture = arcade.load_texture('src/assets/sprites/background-day.png')
        self.flappy_bird_texture = arcade.load_texture('src/assets/sprites/flappy_bird.png')
        self.base_texture = arcade.load_texture('src/assets/sprites/base.png')
        self.message_texture = arcade.load_texture('src/assets/sprites/get_ready.png')

        # Загрузка звуков в игру
        self.jump_sound = arcade.load_sound("src/assets/audio/wing.wav")
        self.hit_sound = arcade.load_sound("src/assets/audio/hit.wav")
        self.point_sound = arcade.load_sound("src/assets/audio/point.wav")

        self.stand_by = True
        self.show_text = True

        self.health = 3
        self.time_appearance = TIME_APPEARANCE
        self.time_appearance_for_pipe = TIME_APPEARANCE_FOR_PIPE
        self.speed = SPEED

        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(self.base_texture, center_x=self.width // 2, center_y=self.base_texture.height // 2)
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(self.base_texture, center_x=self.width + self.width // 2,
                                   center_y=self.base_texture.height // 2)
        self.base_list.append(self.base2)

        self.physics_engine = None

    def setup(self):
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

    def on_update(self, delta_time):
        """Обновление игрового экрана"""
        if self.health:
            if self.physics_engine is not None:
                self.physics_engine.update()
            self.player_list.update(delta_time)

            self.move_base()

            self.time_appearance -= delta_time
            if self.time_appearance < 0:
                self.time_appearance = TIME_APPEARANCE
                self.show_text = not self.show_text

            if not self.stand_by:
                self.time_appearance_for_pipe -= delta_time

            if self.time_appearance_for_pipe < 0:
                self.time_appearance_for_pipe = TIME_APPEARANCE_FOR_PIPE
                self.generate_pipes()

            for pipe in self.pipe_list:
                pipe.center_x -= self.speed
                if pipe.right < 0:
                      self.pipe_list.remove(pipe)
                if pipe.center_x < self.bird.center_x and not pipe.passed and pipe.passed is not None:
                    self.point_sound.play()
                    pipe.passed = True

            if self.physics_engine is not None:
                if self.physics_engine.can_jump(6) and not self.bird.on_the_ground:
                    self.bird.current_angle = 0
                    self.bird.on_the_ground = True
                    self.health -= 1
                    self.hit_sound.play()
                elif not self.physics_engine.can_jump(6) and self.bird.on_the_ground:
                    self.bird.on_the_ground = False

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

    def generate_pipes(self):
        gap = random.randint(self.base_texture.height // 3, self.height // 3)
        pipe1 = Pipe()
        pipe1.center_x = self.width + pipe1.width // 2
        pipe1.center_y = gap

        pipe2 = Pipe(True)
        pipe2.center_x = self.width + pipe2.width // 2
        pipe2.center_y = pipe1.top + GAP_BETWEEN_PIPES + pipe2.height // 2

        self.pipe_list.append(pipe1)
        self.pipe_list.append(pipe2)

    def move_base(self):
        for base in self.base_list:
            base.center_x -= self.speed
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()