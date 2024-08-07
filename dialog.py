import pygame as py
import time
from BUILDINGS import Buildings


class Dialog(Buildings):
    def __init__(self, game, entry_rect, background_image):
        """
        Initializes the Dialog class, treating it like a building with a dialog interface.

        Parameters:
        - game: The Game instance that this dialog belongs to.
        - entry_rect: A pygame Rect object that defines the interaction area of the dialog.
        - background_image: The file path to the image used as the background during the dialog.
        """
        super().__init__(game, entry_rect, background_image)
        self.dialog_active = False
        self.dialog_text = ""
        self.options = []
        self.selected_option = 0

    def start_dialog(self, text, options):
        """Starts the dialog by displaying the provided text and options."""
        self.dialog_active = True
        self.dialog_text = text
        self.options = options
        self.selected_option = 0
        self.entered = True  # Treat this as if we have 'entered' the dialog

    def end_dialog(self):
        """Ends the dialog and returns control back to the game."""
        self.dialog_active = False
        self.exit_building()  # Exit the dialog area

    def update(self):
        """Handles updating the dialog display, including the dimming and options."""
        if self.dialog_active:
            self.dim_screen_smooth()  # Dim the screen when dialog is active
            self.draw_dialog()

    def draw_dialog(self):
        """Draws the dialog box, text, and options on the screen."""
        if not self.dialog_active:
            return

        dialog_box_rect = py.Rect(100, self.game.window_size[1] - 250, self.game.window_size[0] - 200, 200)
        py.draw.rect(self.game.screen, (50, 50, 50), dialog_box_rect)
        py.draw.rect(self.game.screen, (200, 200, 200), dialog_box_rect, 3)

        font = py.font.SysFont(None, 32)
        text_surf = font.render(self.dialog_text, True, (255, 255, 255))
        self.game.screen.blit(text_surf, (dialog_box_rect.x + 20, dialog_box_rect.y + 20))

        for i, option in enumerate(self.options):
            option_color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            option_surf = font.render(option, True, option_color)
            self.game.screen.blit(option_surf, (dialog_box_rect.x + 20, dialog_box_rect.y + 70 + i * 40))

    def handle_input(self, event):
        """Handles keyboard input to navigate through dialog options."""
        if not self.dialog_active:
            return

        if event.type == py.KEYDOWN:
            if event.key == py.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == py.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == py.K_RETURN:
                selected = self.options[self.selected_option]
                print(f"Selected option: {selected}")
                self.end_dialog()
