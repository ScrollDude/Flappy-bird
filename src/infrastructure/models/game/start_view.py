import arcade
from src.infrastructure.models.game.bird import Bird
from src.infrastructure.models.game.change_button_view import ChangeButtonView
from src.infrastructure.models.game.flappy_bird_game import FlappyBirdGame
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


# Константы
SPEED = 1.0


class StartView(arcade.View):
    def __init__(self, start_view, selected_jump_button=arcade.key.SPACE):
        """Инициализация стартового окна"""
        super().__init__()
        self.start_view = start_view
        self.selected_jump_button = selected_jump_button

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout(y=-200)
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        # Загрузка всех текстур в стартовое окно
        self.texture = arcade.load_texture("src/assets/sprites/background-day.png")
        self.flappy_bird_texture = arcade.load_texture(
            "src/assets/sprites/flappy_bird.png"
        )
        self.base_texture = arcade.load_texture("src/assets/sprites/base.png")
        self.start_texture = arcade.load_texture(
            "src/assets/sprites/press_any_key_to_start.png"
        )

        self.time_appearance = 0.5
        self.show_text = True

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(
            self.base_texture,
            center_x=self.width // 2,
            center_y=self.base_texture.height // 2,
        )
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(
            self.base_texture,
            center_x=self.width + self.width // 2,
            center_y=self.base_texture.height // 2,
        )
        self.base_list.append(self.base2)

        self.player_list = arcade.SpriteList()
        self.pipe_list = arcade.SpriteList()

        self.bird = Bird()
        self.bird.center_x = (
            self.width // 2.7 + self.flappy_bird_texture.width - self.bird.width
        )
        self.bird.center_y = self.height // 1.75 + self.flappy_bird_texture.height + 125
        self.player_list.append(self.bird)

    def on_draw(self):
        """Отрисовка стартового экрана"""
        self.clear()
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(
                self.width // 2, self.height // 2, self.width, self.height
            ),
        )
        arcade.draw_texture_rect(
            self.flappy_bird_texture,
            arcade.rect.XYWH(
                self.width // 2.5,
                self.height - 50,
                self.flappy_bird_texture.width,
                self.flappy_bird_texture.height,
            ),
        )
        self.player_list.draw()
        self.base_list.draw()
        if self.show_text:
            arcade.draw_texture_rect(
                self.start_texture,
                arcade.rect.XYWH(
                    self.width // 2,
                    self.height // 2,
                    self.start_texture.width,
                    self.start_texture.height,
                ),
            )
        self.manager.draw()

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

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        texture_normal = arcade.load_texture(
            ":resources:/gui_basic_assets/button/red_normal.png"
        )
        restart_button = UITextureButton(texture=texture_normal)
        restart_button.text = "Change Jump Button"
        restart_button.on_click = self.change_jump_button
        self.box_layout.add(restart_button)

    def change_jump_button(self, event):
        change_button_view = ChangeButtonView(
            self.start_view, self.selected_jump_button
        )
        self.manager.disable()
        self.window.show_view(change_button_view)

    def on_key_press(self, key, modifiers):
        """Начало игры при нажатии любой клавиши"""
        flappy_bird = FlappyBirdGame(self.start_view, self.selected_jump_button)
        self.manager.disable()
        self.window.show_view(flappy_bird)
