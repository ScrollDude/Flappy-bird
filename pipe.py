import arcade


class Pipe(arcade.Sprite):
    def __init__(self, flip_vertically=False):
        super().__init__()
        if not flip_vertically:
            self.texture = arcade.load_texture('src/assets/sprites/pipe-green.png')
            self.passed = False
        else:
            self.texture = arcade.load_texture('src/assets/sprites/pipe-green.png').flip_vertically()
            self.passed = None

    def update(self, delta_time):
        pass