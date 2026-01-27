import arcade
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


# Константы
SPEED = 1.0
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
CAMERA_LERP = 0.12


class AchievementsView(arcade.View):
    def __init__(self, previous_view=None):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout(y=-180)
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.previous_view = previous_view
        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.texture = arcade.load_texture("src/assets/sprites/background-day.png")
        self.base_texture = arcade.load_texture("src/assets/sprites/base.png")
        self.result_texture = arcade.load_texture("src/assets/sprites/result.png")

        self.base_list = arcade.SpriteList()
        self.base = arcade.Sprite(
            self.base_texture,
            center_x=SCREEN_WIDTH // 2,
            center_y=self.base_texture.height // 2,
        )
        self.base_list.append(self.base)

        self.base2 = arcade.Sprite(
            self.base_texture,
            center_x=SCREEN_WIDTH + SCREEN_WIDTH // 2,
            center_y=self.base_texture.height // 2,
        )
        self.base_list.append(self.base2)

    def setup_widgets(self):
        texture_normal = arcade.load_texture(
            ":resources:/gui_basic_assets/button/red_normal.png"
        )

        back_button = UITextureButton(texture=texture_normal)
        back_button.text = "Back"
        back_button.on_click = self.back_to_game_over
        self.box_layout.add(back_button)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def back_to_game_over(self, event):
        if self.previous_view:
            self.window.show_view(self.previous_view)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(
                self.width // 2, self.height // 2, self.width, self.height
            ),
        )

        arcade.draw_texture_rect(
            self.result_texture,
            arcade.rect.XYWH(
                self.width // 2,
                self.height // 1.7,
                self.result_texture.width * 2.3,
                self.result_texture.height * 3.5,
            ),
        )

        arcade.draw_text(
            "GAME ACHIEVEMENTS",
            self.width // 2,
            self.height - 60,
            arcade.color.YELLOW_ROSE,
            font_size=20,
            anchor_x="center",
            bold=True,
        )

        self.base_list.draw()

        self.manager.draw()

    def on_update(self, delta_time):
        self.move_base()

    def move_base(self):
        for base in self.base_list:
            base.center_x -= 1.0
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.back_to_game_over(None)
