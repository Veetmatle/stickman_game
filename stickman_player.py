import pygame as py
import time


class StickMan(object):
    def __init__(self, game):
        self.game = game
        self.window_size = self.game.window_size
        self.size = 50
        self.x = (self.window_size[0] - self.size) // 2
        self.y = (self.window_size[1] - self.size) // 2
        self.images = {
            'up': py.image.load('resized_player_no_bg.png').convert_alpha(),
            'right': py.image.load('resized_player_no_right.png').convert_alpha(),
            'down': py.image.load('resized_player_no_down.png').convert_alpha(),
            'left': py.image.load('resized_player_no_left.png').convert_alpha()
        }
        self.images['up_right'] = py.transform.rotate(self.images['up'], -45)
        self.images['up_left'] = py.transform.rotate(self.images['up'], 45)
        self.images['down_right'] = py.transform.rotate(self.images['down'], 45)
        self.images['down_left'] = py.transform.rotate(self.images['down'], -45)

        self.image = self.images['up']
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collision_mask = self.game.collision_mask

        # experience
        self.experience = 0
        self.level = 1

        # hp and stuff
        self.hp = 1000
        self.money = 0

        # intellect, strength and popularity
        self.intellect = 20
        self.strength = 1
        self.popularity = 0

        # tiredness, hunger
        self.tiredness = 0
        self.hunger = 0

        # active
        self.active = True

        # clock
        self.clock = "12:00"
        self.last_time_update = time.time()

    def can_move(self, dx, dy):
        next_rect = self.rect.move(dx, dy)
        if 0 <= next_rect.centerx < self.collision_mask.get_size()[0] and 0 <= next_rect.centery < \
                self.collision_mask.get_size()[1]:
            return self.collision_mask.get_at((next_rect.centerx, next_rect.centery)) == 1
        return False

    def handle_keys(self):
        keys = py.key.get_pressed()
        if keys[py.K_d] and keys[py.K_w]:
            if self.can_move(3, -4):
                self.rect.x += 3
                self.rect.y -= 4
                self.image = self.images['up_right']
        elif keys[py.K_d] and keys[py.K_s]:
            if self.can_move(3, 4):
                self.rect.x += 3
                self.rect.y += 4
                self.image = self.images['down_right']
        elif keys[py.K_a] and keys[py.K_w]:
            if self.can_move(-3, -4):
                self.rect.x -= 3
                self.rect.y -= 4
                self.image = self.images['up_left']
        elif keys[py.K_a] and keys[py.K_s]:
            if self.can_move(-3, 4):
                self.rect.x -= 3
                self.rect.y += 4
                self.image = self.images['down_left']
        elif keys[py.K_d]:
            if self.can_move(5, 0):
                self.rect.x += 5
                self.image = self.images['right']
        elif keys[py.K_a]:
            if self.can_move(-5, 0):
                self.rect.x -= 5
                self.image = self.images['left']
        elif keys[py.K_w]:
            if self.can_move(0, -5):
                self.rect.y -= 5
                self.image = self.images['up']
        elif keys[py.K_s]:
            if self.can_move(0, 5):
                self.rect.y += 5
                self.image = self.images['down']

    def update_experience(self, amount):
        self.experience += amount
        if self.experience >= 1000:
            self.experience = 0
            self.level += 1
        elif self.experience < 0:
            self.experience = 0
            if self.level > 1:
                self.level -= 1

    def draw(self, screen, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        screen.blit(self.image, adjusted_rect.topleft)

    def draw_properties(self):
        self.draw_experience_bar()
        self.draw_money_amount()
        self.draw_hp_bar()
        self.draw_popularity()
        self.draw_strength()
        self.draw_intellect()
        self.draw_tired()
        self.draw_hunger()
        self.draw_clock()

    def draw_experience_bar(self):
        bar_width = 200
        bar_height = 20
        border_thickness = 2
        x = 10
        y = self.window_size[1] - bar_height - 10

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # Current experience state
        current_exp_width = int(bar_width * (self.experience / 1000))
        py.draw.rect(self.game.screen, (0, 255, 0), (x, y, current_exp_width, bar_height))

        # Display level inside the bar
        font = py.font.SysFont(None, 24)
        text = font.render(f'LVL: {self.level}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.game.screen.blit(text, text_rect)

    def draw_hp_bar(self):
        bar_width = 200
        bar_height = 20
        border_thickness = 2
        x = 10
        y = self.window_size[1] - bar_height - 40

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # Current HP state
        current_hp_width = int(bar_width * (self.hp / 1000))
        py.draw.rect(self.game.screen, (255, 0, 0), (x, y, current_hp_width, bar_height))

        # Display HP inside the bar
        font = py.font.SysFont(None, 24)
        text = font.render(f'HP: {self.hp}/1000', True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.game.screen.blit(text, text_rect)

    def draw_money_amount(self):
        bar_width = 200
        bar_height = 20
        border_thickness = 2
        x = 10
        y = self.window_size[1] - bar_height - 70

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Draw the background of the bar
        py.draw.rect(self.game.screen, (255, 253, 208), (x, y, bar_width, bar_height))

        # Display the money amount inside the bar
        font = py.font.SysFont(None, 24)
        text = font.render(f'Money: ${self.money}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.game.screen.blit(text, text_rect)

    def draw_popularity(self):
        bar_width = 150
        bar_height = 20
        border_thickness = 2
        x = self.window_size[0] - 175
        y = self.window_size[1] - 25

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (255, 253, 208), (x, y, bar_width, bar_height))

        # Display popularity inside the bar
        font = py.font.SysFont(None, 24)
        text = font.render(f'Popularity: {self.popularity}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.game.screen.blit(text, text_rect)

    def draw_strength(self):
        bar_width = 150
        bar_height = 20
        border_thickness = 2
        x = self.window_size[0] - 175
        y = self.window_size[1] - 45
        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (255, 253, 208), (x, y, bar_width, bar_height))

        # Display strength inside the bar
        font = py.font.SysFont(None, 24)
        text = font.render(f'Strength: {self.strength}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.game.screen.blit(text, text_rect)

    def draw_intellect(self):
        bar_width = 150
        bar_height = 20
        border_thickness = 2
        x = self.window_size[0] - 175
        y = self.window_size[1] - 65

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (255, 253, 208), (x, y, bar_width, bar_height))

        # Display intellect inside the bar
        font = py.font.SysFont(None, 24)
        text = font.render(f'Intellect: {self.intellect}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.game.screen.blit(text, text_rect)

    def draw_tired(self):
        bar_width = 200
        bar_height = 20
        border_thickness = 2
        x = self.window_size[0] - 215
        y = 10

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # Current tiredness state
        current_tired_width = int(bar_width * (self.tiredness / 100))
        py.draw.rect(self.game.screen, (0, 120, 120), (x, y, current_tired_width, bar_height))

        # Display tiredness inside the bar
        font = py.font.SysFont(None, 24)
        if self.tiredness >= 100:
            text = font.render(f'Tired: {self.tiredness}/100', True, (255, 0, 0))
            text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
            self.game.screen.blit(text, text_rect)
        else:
            text = font.render(f'Tired: {self.tiredness}/100', True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
            self.game.screen.blit(text, text_rect)

    def draw_hunger(self):
        bar_width = 200
        bar_height = 20
        border_thickness = 2
        x = self.window_size[0] - 215
        y = 40

        # Draw the border
        py.draw.rect(self.game.screen, (0, 0, 0), (
            x - border_thickness, y - border_thickness, bar_width + 2 * border_thickness,
            bar_height + 2 * border_thickness))

        # Background of the bar
        py.draw.rect(self.game.screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # Current hunger state
        current_hunger_width = int(bar_width * (self.hunger / 100))
        py.draw.rect(self.game.screen, (0, 120, 120), (x, y, current_hunger_width, bar_height))

        # Display hunger inside the bar
        font = py.font.SysFont(None, 24)
        if self.hunger >= 100:
            text = font.render(f'Hunger: {self.hunger}/100', True, (255, 0, 0))
            text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
            self.game.screen.blit(text, text_rect)
        else:
            text = font.render(f'Hunger: {self.hunger}/100', True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
            self.game.screen.blit(text, text_rect)

    def draw_clock(self):
        clock_radius = 40
        border_thickness = 5
        x = clock_radius + 10
        y = clock_radius + 10

        # Draw the border
        py.draw.circle(self.game.screen, (0, 0, 0), (x, y), clock_radius + border_thickness)

        # Draw the clock face
        py.draw.circle(self.game.screen, (255, 255, 255), (x, y), clock_radius)

        # Display the clock time inside the clock
        font = py.font.SysFont(None, 24)
        text = font.render(self.clock, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        self.game.screen.blit(text, text_rect)

    def control_time_flow(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_time_update
        if elapsed_time >= 1:  # Update every second
            # Convert real-time seconds to in-game minutes (1 second = 3 in-game minutes)
            in_game_minutes = int(elapsed_time * 5)
            self.last_time_update = current_time
            # update stick resources from time
            self.update_hunger_from_time()
            self.update_tiredness_from_time()
            # Update the clock
            hours, minutes = map(int, self.clock.split(':'))
            minutes += in_game_minutes
            if minutes >= 60:
                hours += minutes // 60
                minutes %= 60
            if hours >= 24:
                hours %= 24

            self.clock = f"{hours:02d}:{minutes:02d}"

    def update_tiredness_from_time(self):
        if self.tiredness < 100:
            self.tiredness += 0.25

    def update_hunger_from_time(self):
        if self.hunger < 100:
            self.hunger = round(self.hunger + 0.2, 1)

