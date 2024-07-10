import pygame as py
import time


class Buildings:
    def __init__(self, game, entry_rect, image_path):
        self.game = game
        self.entered = False
        self.entry_rect = entry_rect
        self.image = py.image.load(image_path).convert()
        self.able_to_enter = False
        self.message = ""

    def draw_enter_message(self):
        if not self.entered:
            self.able_to_enter = True
            font = py.font.SysFont(None, 24)
            text = font.render("Press 'E' to enter", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
            self.game.screen.blit(text, text_rect)

    def enter_building(self):
        if self.able_to_enter and not self.entered:
            self.entered = True
            self.able_to_enter = False
            self.game.stickman.active = False
            py.mouse.set_visible(True)
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))
            py.display.flip()

    def exit_building(self):
        if self.entered:
            self.entered = False
            self.game.stickman.active = True
            py.mouse.set_visible(False)
            self.message = ""

    def update(self):
        if self.entered:
            self.handle_buttons()
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))
            self.game.stickman.draw_properties()
            if self.message:
                font = py.font.SysFont(None, 24)
                text = font.render(self.message, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
                self.game.screen.blit(text, text_rect)
                self.game.stickman.draw_properties()
            py.display.flip()

    def handle_buttons(self):
        pass

    def handle_events(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.game.running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.exit_building()
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_mouse_click(py.mouse.get_pos())

    def handle_mouse_click(self, mouse_pos):
        pass

    def dim_screen_smooth(self):
        screen = py.display.get_surface()
        overlay = py.Surface(screen.get_size())
        overlay.set_alpha(0)

        start_time = time.time()
        duration = 1
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