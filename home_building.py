from buildings import Buildings
import pygame as py
import time

class Home(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(324, 267, 51, 90), 'dom_stickman.png')
        self.message_button = py.Rect(358, 404, 286, 79)
        self.sleep_button = py.Rect(361, 516, 151, 80)
        self.leave_button = py.Rect(792, 514, 160, 80)

    def handle_buttons(self):
        mouse_pos = py.mouse.get_pos()
        previous_message = self.message
        self.message = ""

        if self.message_button.collidepoint(mouse_pos):
            self.message = "Click to check messages"
        elif self.sleep_button.collidepoint(mouse_pos):
            self.message = "Click to sleep"
        elif self.leave_button.collidepoint(mouse_pos):
            self.message = "Click to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.message_button.collidepoint(mouse_pos):
            print("Check messages button clicked")
        elif self.sleep_button.collidepoint(mouse_pos):
            self.dim_screen_smooth()
            self.game.stickman.tiredness = 0
            hours, minutes = map(int, self.game.stickman.clock.split(':'))
            hours += 8
            if hours >= 24:
                hours %= 24
            self.game.stickman.clock = f"{hours:02d}:{minutes:02d}"
        elif self.leave_button.collidepoint(mouse_pos):
            self.exit_building()
