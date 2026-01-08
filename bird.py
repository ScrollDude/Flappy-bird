import arcade


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.on_game_view = False
        self.on_the_ground = False
        self.textures = [arcade.load_texture("src/assets/sprites/yellowbird-downflap.png"),
                         arcade.load_texture("src/assets/sprites/yellowbird-midflap.png"),
                         arcade.load_texture("src/assets/sprites/yellowbird-upflap.png")]
        self.jump_high = 0
        self.gravity = None
        self.current_angle = 0
        self.current_texture = 0
        self.current_switching = 1
        self.current_time = 0
        self.texture = self.textures[self.current_texture]

    def update(self, delta_time):
        self.angle = self.current_angle
        if not self.on_the_ground:
            self.current_time += delta_time
            if self.current_time > 0.25:
                self.current_time = 0
                self.current_texture += self.current_switching
                if self.current_texture >= len(self.textures) or self.current_texture < 0:
                    self.current_switching *= -1
                    self.current_texture += self.current_switching
                self.texture = self.textures[self.current_texture]
        else:
            self.texture = self.textures[1]
        if self.on_game_view and not self.on_the_ground:
            if self.jump_high > 0:
                self.jump_high -= self.gravity
            if self.jump_high <= 0 and self.current_angle < 60:
                self.jump_high = 0
                self.current_angle += 5