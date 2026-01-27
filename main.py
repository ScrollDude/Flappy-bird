from src.infrastructure.models.game.start_view import StartView
import arcade
from pyglet.image import load


# Константы
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Flappy Bird"


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.icon = load("src/assets/favicon.ico")
    window.set_icon(window.icon)
    start_view = StartView(StartView)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
