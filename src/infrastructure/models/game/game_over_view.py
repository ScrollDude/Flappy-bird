import arcade
from pyglet.graphics import Batch
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from src.infrastructure.models.game.best_games_view import BestGamesView
from src.infrastructure.models.game.achievements_view import AchievementsView


# Константы
SPEED = 1.0
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
CAMERA_LERP = 0.12


class GameOverView(arcade.View):
    def __init__(self, previous_screen, start_view, jump_button):
        super().__init__()
        self.start_view = start_view
        self.jump_button = jump_button
        self.batch = Batch()
        self.best_games_view = None
        self.achievements_view = None

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout(y=-170)
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.texture = arcade.load_texture("src/assets/sprites/background-day.png")
        self.base_texture = arcade.load_texture("src/assets/sprites/base.png")
        self.game_over_texture = arcade.load_texture("src/assets/sprites/game_over.png")
        self.result_texture = arcade.load_texture("src/assets/sprites/result.png")

        self.die_sound = arcade.load_sound("src/assets/audio/die.wav")

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

        self.level = previous_screen.level
        self.distance = previous_screen.distance
        self.duration_seconds = previous_screen.duration_seconds
        self.score = previous_screen.score
        self.pipes_passed = previous_screen.pipes_passed
        self.powerup_types_count = previous_screen.powerup_types_count
        self.death_reason = previous_screen.death_reason
        self.zooming = previous_screen.zooming

        self.world_camera = previous_screen.world_camera

    def setup_widgets(self):
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        restart_button = UITextureButton(texture=texture_normal)
        restart_button.text = "Restart"
        restart_button.on_click = self.restart
        self.box_layout.add(restart_button)

        best_games_button = UITextureButton(texture=texture_normal)
        best_games_button.text = "Best games"
        best_games_button.on_click = self.best_games
        self.box_layout.add(best_games_button)

        achievements_button = UITextureButton(texture=texture_normal)
        achievements_button.text = "Achievements"
        achievements_button.on_click = self.achievements
        self.box_layout.add(achievements_button)

    def restart(self, event):
        self.manager.disable()
        start_view = self.start_view(self.start_view, self.jump_button)
        self.window.show_view(start_view)

    def best_games(self, event):
        self.manager.disable()
        if self.best_games_view is None:
            self.best_games_view = BestGamesView(previous_view=self)
        self.window.show_view(self.best_games_view)

    def achievements(self, event):
        self.manager.disable()
        if self.achievements_view is None:
            self.achievements_view = AchievementsView(previous_view=self)
        self.window.show_view(self.achievements_view)

    def on_draw(self):
        self.clear()
        if self.world_camera is not None:
            self.world_camera.use()
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(
                self.width // 2, self.height // 2, self.width, self.height
            ),
        )
        arcade.draw_texture_rect(
            self.game_over_texture,
            arcade.rect.XYWH(
                self.width // 2,
                self.height - 50,
                self.game_over_texture.width,
                self.game_over_texture.height,
            ),
        )
        arcade.draw_texture_rect(
            self.result_texture,
            arcade.rect.XYWH(
                self.width // 2,
                self.height // 1.5,
                self.result_texture.width * 2.5,
                self.result_texture.height * 2.5,
            ),
        )
        text_survival = arcade.Text(
            f"Survival Time: {round(self.duration_seconds, 2)}",
            self.width // 2,
            self.height - (self.height // 3 - 65),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        text_score = arcade.Text(
            f"Score: {self.score}",
            self.width // 2,
            self.height - (self.height // 3 - 40),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        text_power_up = arcade.Text(
            f"Pick up power ups: {self.powerup_types_count}",
            self.width // 2,
            self.height - (self.height // 3 - 15),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        text_pipes_count = arcade.Text(
            f"Pipes passed: {self.pipes_passed}",
            self.width // 2,
            self.height - (self.height // 3 + 10),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        text_level = arcade.Text(
            f"Game over on level: {self.level}",
            self.width // 2,
            self.height - (self.height // 3 + 35),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        text_distance = arcade.Text(
            f"Distance: {round(self.distance, 2)}",
            self.width // 2,
            self.height - (self.height // 3 + 60),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        text_death_reason = arcade.Text(
            f"Death reason: {self.death_reason}",
            self.width // 2,
            self.height - (self.height // 3 + 85),
            arcade.color.WHITE,
            anchor_x="center",
            font_size=16,
            batch=self.batch,
        )
        self.base_list.draw()
        self.batch.draw()
        if self.zooming == 1.0:
            self.manager.draw()

    def on_update(self, delta_time):
        self.zoom_down(delta_time)
        self.move_base()
        self.manager.enable()

    def zoom_down(self, delta_time):
        if self.zooming > 1.0:
            self.world_camera = arcade.camera.Camera2D(zoom=self.zooming)
            self.zooming -= delta_time * 10
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.world_camera.position = arcade.math.lerp_2d(
                self.world_camera.position, position, CAMERA_LERP
            )
        else:
            self.zooming = 1.0
            self.world_camera = arcade.camera.Camera2D(zoom=self.zooming)
            if self.die_sound is not None:
                die_sound = self.die_sound
                die_sound.play(volume=0.5)
                self.die_sound = None
                self.world_camera = None

    def move_base(self):
        for base in self.base_list:
            base.center_x -= SPEED
            if base.right < 0:
                self.base_list[0].center_x = self.width // 2
                self.base_list[1].center_x = self.width + self.width // 2 + 1.2
