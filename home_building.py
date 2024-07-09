import pygame as py
import time


class Home(object):
    def __init__(self, game):
        self.game = game
        self.house_entry_rect = py.Rect(324, 267, 51, 90)
        self.able_to_enter = False
        self.home_image = py.image.load('dom_stickman.png').convert()
        self.entered = False
        # buttons inside
        self.message_button = py.Rect(358, 404, 286, 79)
        self.sleep_button = py.Rect(361, 516, 151, 80)
        self.leave_button = py.Rect(792, 514, 160, 80)
        self.message = ""

    def draw_enter_message(self):
        if not self.entered:
            self.able_to_enter = True
            font = py.font.SysFont(None, 24)
            text = font.render("Press 'E' to enter", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
            self.game.screen.blit(text, text_rect)

    def enter_the_home(self):
        if self.able_to_enter and not self.entered:
            self.entered = True
            self.able_to_enter = False
            # Stop displaying and handling the player
            self.game.stickman.active = False
            # Show the mouse cursor
            py.mouse.set_visible(True)
            # Change the background to the home image
            home_image_scaled = py.transform.scale(self.home_image, self.game.window_size)
            self.game.screen.blit(home_image_scaled, (0, 0))
            py.display.flip()

    def exit_the_home(self):
        if self.entered:
            self.entered = False
            self.game.stickman.active = True
            # Hide the mouse cursor
            py.mouse.set_visible(False)
            # Clear the message
            self.message = ""

    def update(self):
        if self.entered:
            self.handle_buttons()
            home_image_scaled = py.transform.scale(self.home_image, self.game.window_size)
            self.game.screen.blit(home_image_scaled, (0, 0))
            self.game.stickman.draw_properties()
            if self.message:
                font = py.font.SysFont(None, 24)
                text = font.render(self.message, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
                self.game.screen.blit(text, text_rect)
                self.game.stickman.draw_properties()
            py.display.flip()

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
            home_image_scaled = py.transform.scale(self.home_image, self.game.window_size)
            self.game.screen.blit(home_image_scaled, (0, 0))

    def handle_home_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game.running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_the_home()
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = py.mouse.get_pos()
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
                        self.exit_the_home()

    def dim_screen_smooth(self):
        screen = py.display.get_surface()
        overlay = py.Surface(screen.get_size())
        overlay.set_alpha(0)

        start_time = time.time()
        duration = 1  # time of darkening
        target_alpha = 150  # level of transparency

        while time.time() - start_time < duration:
            current_time = time.time() - start_time
            alpha = int((current_time / duration) * target_alpha)
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
            py.display.flip()
            py.time.Clock().tick(60)

        overlay.set_alpha(target_alpha)
        screen.blit(overlay, (0, 0))
        py.display.flip()
