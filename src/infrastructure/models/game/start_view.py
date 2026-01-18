import arcade
from src.infrastructure.models.game.bird import Bird
from src.infrastructure.models.game.flappy_bird_game import FlappyBirdGame

# Константы
SPEED = 1.0


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