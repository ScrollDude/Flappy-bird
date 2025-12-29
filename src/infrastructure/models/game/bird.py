import arcade


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = [arcade.load_texture("src/assets/sprites/yellowbird-downflap.png"),
                         arcade.load_texture("src/assets/sprites/yellowbird-midflap.png"),
                         arcade.load_texture("src/assets/sprites/yellowbird-upflap.png")]
        self.current_texture = 0
        self.current_switching = 1
        self.current_time = 0
        self.texture = self.textures[self.current_texture]

    def update(self, delta_time):
        self.current_time += delta_time
        if self.current_time > 0.25:
            self.current_time = 0
            self.current_texture += self.current_switching
            if self.current_texture >= len(self.textures) or self.current_texture < 0:
                self.current_switching *= -1
                self.current_texture += self.current_switching
            self.texture = self.textures[self.current_texture]