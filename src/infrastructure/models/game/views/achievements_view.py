import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from src.infrastructure.repositories.achievement_repository import achievement_repository
from src.infrastructure.services.achievement_service import AchievementService


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

        self.achievement_service = AchievementService(
            repo=achievement_repository
        )

        self.batch = Batch()

        self.completed_achievements = [achievement for achievement in self.achievement_service.get_all_completed()]

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
        achievements_list = []

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
                self.result_texture.height * 3.8,
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

        for achievement in self.completed_achievements:
            text = arcade.Text(
                str(achievement.name),
                self.width // 2 - 50,
                self.height // 2 + 162 - (35 * (achievement.id - 1)),
                anchor_x='center',
                batch=self.batch
            )
            achievements_list.append(text)

            arcade.draw_texture_rect(
                arcade.load_texture(achievement.icon_url),
                arcade.rect.XYWH(
                    self.width // 2 + 50,
                    self.height // 2 + 170 - (35 * (achievement.id - 1)),
                    35,
                    35
                )
            )

        self.base_list.draw()

        self.manager.draw()
        self.batch.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.back_to_game_over(None)
