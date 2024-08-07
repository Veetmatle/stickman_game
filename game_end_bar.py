import pygame as py
from buildings import Buildings


class GameEndBar(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(804, 882, 63, 61), "images/game_end_bar.jpg")
        self.end_game_button = py.Rect(320, 85, 359, 304)
        self.required_level = 30  # Required level to enter this building

    def draw_enter_message(self):
        """
        Overrides the draw_enter_message method to display a different message
        depending on the player's level.
        """
        if not self.entered:
            self.able_to_enter = True
        font = py.font.SysFont(None, 24)
        if self.game.stickman.level < self.required_level:
            text = font.render(f"Level {self.required_level} required to enter", True, (255, 0, 0))
        else:
            text = font.render("Press 'E' to enter", True, (0, 0, 0))

        text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
        self.game.screen.blit(text, text_rect)

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.game.stickman.level < self.required_level:
            self.message = f"Level {self.required_level} required to enter"
        elif self.end_game_button.collidepoint(mouse_pos):
            self.message = "Click to have your victorious beer"
        else:
            self.message = "Press esc to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.game.stickman.level >= self.required_level:
            if self.end_game_button.collidepoint(mouse_pos):
                self.game.home.dim_screen_smooth()  # Perform screen dimming effect
                py.time.delay(2000)  # Optional: delay for 2 seconds to show the completed screen
                self.game.running = False  # Stop the game loop
