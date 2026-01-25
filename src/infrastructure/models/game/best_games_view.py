import arcade
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from src.infrastructure.repositories.game_session_repository import (
    game_session_repository,
)
from src.infrastructure.services.game_session_service import GameSessionService


SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512


class BestGamesView(arcade.View):
    def __init__(self, previous_view=None):
        super().__init__()
        self.manager = UIManager()
        self.manager.enable()
        self.game_session_service = GameSessionService(
            repository=game_session_repository
        )

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

        self.stats = self.game_session_service.get_game_statistics()

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
            "GAME STATS",
            self.width // 2,
            self.height - 60,
            arcade.color.YELLOW_ROSE,
            font_size=20,
            anchor_x="center",
            bold=True,
        )

        arcade.draw_text(
            f"Games: {self.stats['games_count']}",
            self.width // 2,
            self.height // 2 + 145,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Score: {self.stats['avg_score']}",
            self.width // 2,
            self.height // 2 + 110,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Time: {self.stats['avg_duration']:.1f}s",
            self.width // 2,
            self.height // 2 + 75,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Pipes: {self.stats['avg_pipes']:.1f}",
            self.width // 2,
            self.height // 2 + 40,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Powerups: {self.stats['avg_powerups']:.1f}",
            self.width // 2,
            self.height // 2 + 5,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Distance: {self.stats['avg_distance']}",
            self.width // 2,
            self.height // 2 - 30,
            arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        arcade.draw_text(
            f"Best: {self.stats['max_score']}",
            self.width // 2,
            self.height // 2 - 65,
            arcade.color.YELLOW,
            font_size=15,
            bold=True,
            anchor_x="center",
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
