import sys
import pygame as py
from stickman_player import StickMan
from BUILDINGS.home_building import Home
from BUILDINGS.university_building import University
from BUILDINGS.MCdonalds import MCDonald
from BUILDINGS.hospital import Hospital
from BUILDINGS.office import Office
from BUILDINGS.castle import Castle
from BUILDINGS.drug_store import DrugStore
from BUILDINGS.weapon_shop import WeaponShop
from BUILDINGS.bank import Bank
from BUILDINGS.game_end_bar import GameEndBar
from BUILDINGS.casino import Casino

class Game:
    def __init__(self):
        """
        Initializes the Game class, setting up the basic game parameters such as
        window size, map size, background, collision mask, and initializes the
        player and building objects.
        """
        py.init()
        self.window_size = (1000, 800)  # Size of the camera
        self.map_size = (2048, 1732)  # Main map size
        self.screen = py.display.set_mode(self.window_size)
        py.display.set_caption('StickMan Jr')
        self.clock = py.time.Clock()
        self.running = True

        # Load background image
        self.background = py.image.load('images/game_background.png').convert()

        # Load collision mask
        collision_mask_image = py.image.load('images/maska.png').convert()
        self.collision_mask = py.mask.from_threshold(collision_mask_image, (255, 255, 255), (1, 1, 1, 255))

        # Initialize StickMan (player character)
        self.stickman = StickMan(self)

        # Initialize BUILDINGS
        self.home = Home(self)
        self.university = University(self)
        self.mcd = MCDonald(self)
        self.hospital = Hospital(self)
        self.office = Office(self)
        self.castle = Castle(self)
        self.drug_store = DrugStore(self)
        self.weapon_shop = WeaponShop(self)
        self.bank = Bank(self)
        self.game_end_bar = GameEndBar(self)
        self.casino = Casino(self)

        #initialize NPC

    def run(self):
        """
        Main game loop that keeps the game running. It handles events, updates
        the game state, and draws the current frame. The loop continues until
        the game is quit.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        py.quit()
        sys.exit()

    def handle_events(self):
        """
        Handles user input and game events. Checks if the player has entered a
        building and handles specific events for that building, otherwise processes
        general game events such as quitting the game or interacting with BUILDINGS.
        """
        if self.home.entered:
            self.home.handle_events()
        elif self.university.entered:
            self.university.handle_events()
        elif self.mcd.entered:
            self.mcd.handle_events()
        elif self.hospital.entered:
            self.hospital.handle_events()
        elif self.office.entered:
            self.office.handle_events()
        elif self.castle.entered:
            self.castle.handle_events()
        elif self.drug_store.entered:
            self.drug_store.handle_events()
        elif self.weapon_shop.entered:
            self.weapon_shop.handle_events()
        elif self.bank.entered:
            self.bank.handle_events()
        elif self.game_end_bar.entered:
            self.game_end_bar.handle_events()
        elif self.casino.entered:
            self.casino.handle_events()
        else:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        self.running = False
                    elif event.key == py.K_e and self.home.able_to_enter and self.stickman.rect.colliderect(self.home.entry_rect):
                        self.home.enter_building()
                    elif event.key == py.K_e and self.university.able_to_enter and self.stickman.rect.colliderect(self.university.entry_rect):
                        self.university.enter_building()
                    elif event.key == py.K_e and self.mcd.able_to_enter and self.stickman.rect.colliderect(self.mcd.entry_rect):
                        self.mcd.enter_building()
                    elif event.key == py.K_e and self.hospital.able_to_enter and self.stickman.rect.colliderect(self.hospital.entry_rect):
                        self.hospital.enter_building()
                    elif event.key == py.K_e and self.office.able_to_enter and self.stickman.rect.colliderect(self.office.entry_rect):
                        self.office.enter_building()
                    elif event.key == py.K_e and self.castle.able_to_enter and self.stickman.rect.colliderect(self.castle.entry_rect):
                        self.castle.enter_building()
                    elif event.key == py.K_e and self.drug_store.able_to_enter and self.stickman.rect.colliderect(self.drug_store.entry_rect):
                        self.drug_store.enter_building()
                    elif event.key == py.K_e and self.weapon_shop.able_to_enter and self.stickman.rect.colliderect(self.weapon_shop.entry_rect):
                        self.weapon_shop.enter_building()
                    elif event.key == py.K_e and self.bank.able_to_enter and self.stickman.rect.colliderect(self.bank.entry_rect):
                        self.bank.enter_building()
                    elif event.key == py.K_e and self.game_end_bar.able_to_enter and self.stickman.level >= 30 and self.stickman.rect.colliderect(self.game_end_bar.entry_rect):
                        self.game_end_bar.enter_building()
                    elif event.key == py.K_e and self.casino.able_to_enter and self.stickman.rect.colliderect(self.casino.entry_rect) and self.stickman.level >= 10:
                        self.casino.enter_building()
    def update(self):
        """
        Updates the game state. If the player is not inside any building, it updates
        the player's state and controls time flow. It also checks certain conditions
        in the game, such as those related to the hospital.
        """
        if not (self.home.entered or self.university.entered or self.mcd.entered or self.hospital.entered or self.office.entered
                or self.castle.entered or self.drug_store.entered or self.weapon_shop.entered or self.bank.entered or self.game_end_bar.entered or self.casino.entered):
            self.stickman.handle_keys()
        if not self.castle.entered or not self.casino.entered:
            self.stickman.control_time_flow()
            self.hospital.check_conditions()

    def draw(self):
        """
        Draws the current game frame. Depending on the player's location, it either
        draws the main map with the player and BUILDINGS or updates the display within
        a specific building. It also handles camera movement and UI elements such as
        experience bars and health points.
        """
        if not (self.home.entered or self.university.entered or self.mcd.entered or self.hospital.entered
                or self.office.entered or self.castle.entered or self.drug_store.entered or self.weapon_shop.entered
        or self.bank.entered or self.game_end_bar.entered or self.casino.entered):
            # Determine camera position
            camera_x = max(0, min(self.stickman.rect.centerx - self.window_size[0] // 2, self.map_size[0] - self.window_size[0]))
            camera_y = max(0, min(self.stickman.rect.centery - self.window_size[1] // 2, self.map_size[1] - self.window_size[1]))
            camera_offset = (-camera_x, -camera_y)

            # Draw the background with camera offset
            self.screen.blit(self.background, camera_offset)
            self.stickman.draw(self.screen, camera_offset)

            # Draw experience bar, level, HP, etc.
            self.stickman.draw_properties()

            # Check if the player is near the entrance of any building
            if self.stickman.rect.colliderect(self.home.entry_rect):
                self.home.draw_enter_message()
            elif self.stickman.rect.colliderect(self.university.entry_rect):
                self.university.draw_enter_message()
            elif self.stickman.rect.colliderect(self.mcd.entry_rect):
                self.mcd.draw_enter_message()
            elif self.stickman.rect.colliderect(self.hospital.entry_rect):
                self.hospital.draw_enter_message()
            elif self.stickman.rect.colliderect(self.office.entry_rect):
                self.office.draw_enter_message()
            elif self.stickman.rect.colliderect(self.castle.entry_rect):
                self.castle.draw_enter_message()
            elif self.stickman.rect.colliderect(self.drug_store.entry_rect):
                self.drug_store.draw_enter_message()
            elif self.stickman.rect.colliderect(self.weapon_shop.entry_rect):
                self.weapon_shop.draw_enter_message()
            elif self.stickman.rect.colliderect(self.bank.entry_rect):
                self.bank.draw_enter_message()
            elif self.stickman.rect.colliderect(self.game_end_bar.entry_rect):
                self.game_end_bar.draw_enter_message()
            elif self.stickman.rect.colliderect(self.casino.entry_rect):
                self.casino.draw_enter_message()

        elif self.home.entered:
            self.home.update()
        elif self.university.entered:
            self.university.update()
        elif self.mcd.entered:
            self.mcd.update()
        elif self.hospital.entered:
            self.hospital.update()
        elif self.office.entered:
            self.office.update()
        elif self.castle.entered:
            self.castle.update()
        elif self.drug_store.entered:
            self.drug_store.update()
        elif self.weapon_shop.entered:
            self.weapon_shop.update()
        elif self.bank.entered:
            self.bank.update()
        elif self.game_end_bar.entered:
            self.game_end_bar.update()
        elif self.casino.entered:
            self.casino.update()

        py.display.flip()

    def pause_game(self):
        """
        Pauses the main game by stopping the game loop and disabling StickMan's actions.
        """
        self.running = False
        self.stickman.active = False

    def resume_game(self):
        """
        Resumes the main game after the BlackJack game is finished.
        """
        self.running = True
        self.stickman.active = True
        self.run()

if __name__ == '__main__':
    game = Game()
    game.run()
