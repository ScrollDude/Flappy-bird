import arcade
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from pyglet.graphics import Batch


# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SPEED = 1.0


class ChangeButtonView(arcade.View):
    def __init__(self, start_view, selected_jump_button):
        """Инициализация стартового окна"""
        super().__init__()
        self.start_view = start_view
        self.selected_jump_button = selected_jump_button

        self.manager = UIManager()
        self.manager.enable()

        self.batch = Batch()

        self.anchor_layout = UIAnchorLayout(y=-100)
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)

        self.texture = arcade.load_texture('src/assets/sprites/background-day.png')

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(self.width // 2, self.height // 2, self.width,
                                                                self.height))
        try:
            text = arcade.Text(f'Selected button: {chr(self.selected_jump_button)}',
                               SCREEN_WIDTH // 2,
                               SCREEN_HEIGHT // 2,
                               arcade.color.WHITE,
                               font_size=19,
                               anchor_x='center',
                               batch=self.batch
                               )
        except ValueError:
            error_text = arcade.Text(f"Can't show selected symbol.",
                                     SCREEN_WIDTH // 2,
                                     SCREEN_HEIGHT // 2,
                                     arcade.color.WHITE,
                                     font_size=19,
                                     anchor_x='center',
                                     batch=self.batch
                                     )
        self.batch.draw()
        self.manager.draw()

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        restart_button = UITextureButton(texture=texture_normal)
        restart_button.text = 'Exit'
        restart_button.on_click = self.exit
        self.box_layout.add(restart_button)

    def on_key_press(self, symbol, modifiers):
        if symbol != arcade.key.P:
            self.selected_jump_button = symbol

    def exit(self, event):
        start_view = self.start_view(self.start_view, self.selected_jump_button)
        self.manager.disable()
        self.window.show_view(start_view)
