from bird import Bird
from pipe import Pipe
import arcade

# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Flappy Bird"
JUMP = 5


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('src/assets/sprites/background-day.png')
        self.flappy_bird_texture = arcade.load_texture('src/assets/sprites/flappy_bird.png')
        self.base_texture = arcade.load_texture('src/assets/sprites/base.png')

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(self.base_texture, center_x=self.width // 2, center_y=self.base_texture.height // 2)
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(self.base_texture, center_x=self.width + self.width // 2,
                                   center_y=self.base_texture.height // 2)
        self.base_list.append(self.base2)

        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

    def on_show(self):
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

    def on_update(self, delta_time):
        self.player_list.update()
        for base in self.base_list:
            base.center_x -= 1
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2

    def on_key_press(self, key, modifiers):
        """Начало игры при нажатии клавиши"""
        pass


class FlappyBirdGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('src/assets/sprites/background-day.png')
        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()
        self.base_list = arcade.SpriteList()
        self.keys_pressed = set()

    def setup(self):
        ...

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                                self.height))
        self.player_list.draw()
        self.base_list.draw()
        self.pipe_list.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        # Управление Красной Шапочкой
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        # Остановка при отпускании клавиш
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    start_view.on_show()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()