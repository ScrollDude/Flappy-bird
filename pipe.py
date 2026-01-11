import arcade


class Pipe(arcade.Sprite):
    def __init__(self, flip_vertically=False):
        super().__init__()
        pipe_texture = arcade.load_texture('src/assets/sprites/pipe-green.png')
        if not flip_vertically:
            self.texture = pipe_texture
            self.passed = False
        else:
            self.texture = pipe_texture.flip_vertically()
            self.passed = True