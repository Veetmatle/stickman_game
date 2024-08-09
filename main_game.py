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
    def __init__(self, strength=1, intellect=1, popularity=1):
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
        self.stickman = StickMan(self, strength, intellect, popularity)

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

        # Add BUILDINGS to a list
        self.buildings = [
            self.home,
            self.university,
            self.mcd,
            self.hospital,
            self.office,
            self.castle,
            self.drug_store,
            self.weapon_shop,
            self.bank,
            self.game_end_bar,
            self.casino
        ]

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
        for building in self.buildings:
            if building.entered:
                building.handle_events()
                return

        for event in py.event.get():
            if event.type == py.QUIT:
                self.running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    self.running = False
                elif event.key == py.K_e:
                    for building in self.buildings:
                        if building.able_to_enter and self.stickman.rect.colliderect(building.entry_rect):
                            if hasattr(building, 'required_level') and self.stickman.level < building.required_level:
                                continue
                            building.enter_building()
                            break

    def update(self):
        """
        Updates the game state. If the player is not inside any building, it updates
        the player's state and controls time flow. It also checks certain conditions
        in the game, such as those related to the hospital.
        """
        if not any(building.entered for building in self.buildings):
            self.stickman.handle_keys()
        if not any(building.entered for building in [self.castle, self.casino]):
            self.stickman.control_time_flow()
            self.hospital.check_conditions()

    def draw(self):
        """
        Draws the current game frame. Depending on the player's location, it either
        draws the main map with the player and BUILDINGS or updates the display within
        a specific building. It also handles camera movement and UI elements such as
        experience bars and health points.
        """
        if not any(building.entered for building in self.buildings):
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
            for building in self.buildings:
                if self.stickman.rect.colliderect(building.entry_rect):
                    building.draw_enter_message()
                    break
        else:
            for building in self.buildings:
                if building.entered:
                    building.update()
                    break

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
