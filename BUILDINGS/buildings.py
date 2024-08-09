import pygame as py
import time


class Buildings:
    def __init__(self, game, entry_rect, image_path):
        """
        Initializes the Buildings class which represents a building in the game.

        Parameters:
        - game: The Game instance that this building belongs to.
        - entry_rect: A pygame Rect object that defines the entrance area of the building.
        - image_path: The file path to the image representing the building's interior.
        """
        self.game = game
        self.entered = False
        self.entry_rect = entry_rect
        self.image = py.image.load(image_path).convert()
        self.able_to_enter = False
        self.message = ""

    def draw_enter_message(self):
        """
        Draws a message on the screen prompting the player to press 'E' to enter the building,
        if the player is near the entrance and has not yet entered the building.
        """
        if not self.entered:
            self.able_to_enter = True
            font = py.font.SysFont(None, 24)
            text = font.render("Press 'E' to enter", True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.game.window_size[0] // 2, self.game.window_size[1] - 30))
            self.game.screen.blit(text, text_rect)

    def enter_building(self):
        """
        Handles the logic for entering the building. When the player presses 'E',
        the building's interior is displayed, and the player's controls are disabled.
        """
        if self.able_to_enter and not self.entered:
            self.entered = True
            self.able_to_enter = False
            self.game.stickman.active = False
            py.mouse.set_visible(True)
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))
            py.display.flip()

    def exit_building(self):
        """
        Handles the logic for exiting the building. Restores the player's controls
        and hides the building's interior.
        """
        if self.entered:
            self.entered = False
            self.game.stickman.active = True
            py.mouse.set_visible(False)
            self.message = ""

    def update(self):
        """
        Updates the building's state while the player is inside. Handles drawing
        the building's interior and any on-screen messages.
        """
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
        """
        Placeholder method for handling button interactions within the building.
        Can be overridden by subclasses to define specific button behaviors.
        """
        pass

    def handle_events(self):
        """
        Handles events such as quitting the game, exiting the building, and mouse clicks
        while the player is inside the building.
        """
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
        """
        Placeholder method for handling mouse clicks within the building.
        Can be overridden by subclasses to define specific click behaviors.

        Parameters:
        - mouse_pos: The position of the mouse click.
        """
        pass

    def dim_screen_smooth(self):
        """
        Smoothly dims the screen by overlaying a semi-transparent layer.
        This effect can be used for transitions or to highlight certain actions.
        """
        screen = py.display.get_surface()
        overlay = py.Surface(screen.get_size())
        overlay.set_alpha(0)

        start_time = time.time()
        duration = 1
        target_alpha = 150  # Level of transparency for the dim effect

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
