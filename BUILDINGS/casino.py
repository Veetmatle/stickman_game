import pygame as py
import random
import copy
from BUILDINGS.buildings import Buildings
import sys
from blackjack_game import BlackjackGame


class Casino(Buildings):
    def __init__(self, game):
        super().__init__(game, py.Rect(802, 1369, 65, 54), "images/casino.jpg")
        self.play_blackjack_button = py.Rect(513, 489, 261, 217)
        self.required_level = 10
        self.blackjack_game = BlackjackGame(game.window_size)

    def draw_enter_message(self):
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

        if self.play_blackjack_button.collidepoint(mouse_pos):
            self.message = "Click to play Blackjack"
        else:
            self.message = "Press esc to exit"

        if self.message != previous_message:
            image_scaled = py.transform.scale(self.image, self.game.window_size)
            self.game.screen.blit(image_scaled, (0, 0))

    def handle_mouse_click(self, mouse_pos):
        if self.play_blackjack_button.collidepoint(mouse_pos):
            max_stake = self.game.stickman.money
            stake = self.blackjack_game.prompt_for_stake(max_stake)
            if stake is not None:
                self.game.pause_game()
                result = self.blackjack_game.play(stake, self.game.stickman)
                if result == 'win':
                    self.game.stickman.update_experience(100)
                    self.game.stickman.money += stake * 2
                elif result == 'lose':
                    self.game.stickman.money -= stake
                self.game.resume_game()

    def prompt_for_stake(self):
        """
        Prompts the player to enter a stake amount using a simple input dialog in Pygame.

        Returns:
        - stake: The stake amount entered by the player or None if invalid.
        """
        font = py.font.SysFont(None, 48)
        input_box = py.Rect(300, 300, 200, 50)
        color_inactive = py.Color('lightskyblue3')
        color_active = py.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == py.KEYDOWN:
                    if active:
                        if event.key == py.K_RETURN:
                            if text.isdigit() and 0 < int(text) <= self.game.stickman.money:
                                return int(text)
                            else:
                                return None
                        elif event.key == py.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.game.screen.fill((30, 30, 30))
            prompt_text = font.render("Enter your stake:", True, py.Color('white'))
            self.game.screen.blit(prompt_text, (250, 250))

            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.game.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            py.draw.rect(self.game.screen, color, input_box, 2)

            py.display.flip()
