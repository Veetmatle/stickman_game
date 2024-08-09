import pygame, sys
from button import Button
from main_game import Game

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Global variables for StickMan's attributes and remaining points
global_strength = 0
global_intellect = 0
global_popularity = 0
global_points_left = 10


def get_font(size):
    """
    Returns a font object of the specified size.
    """
    return pygame.font.Font("assets/font.ttf", size)


def play():
    """
    Starts the game with the globally set attributes for StickMan.
    """
    game = Game(strength=global_strength, intellect=global_intellect, popularity=global_popularity)
    game.run()


def options():
    """
    Opens the options menu where the player can allocate points to StickMan's attributes.
    Points are saved globally and adjusted with mouse clicks.
    """
    global global_strength, global_intellect, global_popularity, global_points_left

    stickman_attributes = {
        "Strength": global_strength,
        "Intellect": global_intellect,
        "Popularity": global_popularity
    }
    points_left = global_points_left

    click_delay = 200
    last_click_time = pygame.time.get_ticks()

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        INFO_TEXT = get_font(45).render("Target: 30 lvl in 30 days", True, pygame.Color("black"))
        OPTIONS_TEXT = get_font(45).render("Allocate your points:", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 100))
        INFO_RECT = INFO_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 25))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        SCREEN.blit(INFO_TEXT, INFO_RECT)

        # Display remaining points
        POINTS_LEFT_TEXT = get_font(35).render(f"Points left: {points_left}", True, "Black")
        POINTS_LEFT_RECT = POINTS_LEFT_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 150))
        SCREEN.blit(POINTS_LEFT_TEXT, POINTS_LEFT_RECT)

        # Display attributes and buttons
        attribute_y_start = 250

        for i, (attr, value) in enumerate(stickman_attributes.items()):
            attr_text = get_font(35).render(f"{attr}: {value}", True, "Black")
            attr_rect = attr_text.get_rect(center=(SCREEN_WIDTH // 2, attribute_y_start + i * 100))
            SCREEN.blit(attr_text, attr_rect)

            plus_button = Button(image=None, pos=(SCREEN_WIDTH // 2 + 110, attribute_y_start + i * 100),
                                 text_input="+", font=get_font(50), base_color="Black", hovering_color="Green")
            minus_button = Button(image=None, pos=(SCREEN_WIDTH // 2 - 110, attribute_y_start + i * 100),
                                  text_input="-", font=get_font(50), base_color="Black", hovering_color="Green")

            plus_button.changeColor(OPTIONS_MOUSE_POS)
            minus_button.changeColor(OPTIONS_MOUSE_POS)

            plus_button.update(SCREEN)
            minus_button.update(SCREEN)

            current_time = pygame.time.get_ticks()

            if pygame.mouse.get_pressed()[0] and current_time - last_click_time > click_delay:
                if plus_button.checkForInput(OPTIONS_MOUSE_POS) and points_left > 0:
                    stickman_attributes[attr] += 1
                    points_left -= 1
                    last_click_time = current_time
                elif minus_button.checkForInput(OPTIONS_MOUSE_POS) and stickman_attributes[attr] > 0:
                    stickman_attributes[attr] -= 1
                    points_left += 1
                    last_click_time = current_time

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    global_strength = stickman_attributes["Strength"]
                    global_intellect = stickman_attributes["Intellect"]
                    global_popularity = stickman_attributes["Popularity"]
                    global_points_left = points_left
                    return

        pygame.display.update()


def main_menu():
    """
    Displays the main menu where the player can choose to start the game, go to options, or quit.
    """
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    main_menu()
