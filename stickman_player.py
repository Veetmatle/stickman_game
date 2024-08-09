import pygame as py
import time


class StickMan(object):
    def __init__(self, game, strength=5, intellect=5, popularity=5):
        self.game = game
        self.window_size = self.game.window_size
        self.size = 50
        self.x = (self.window_size[0] - self.size) // 2
        self.y = (self.window_size[1] - self.size) // 2
        self.images = {
            'up': py.image.load('images/resized_player_no_bg.png').convert_alpha(),
            'right': py.image.load('images/resized_player_no_right.png').convert_alpha(),
            'down': py.image.load('images/resized_player_no_down.png').convert_alpha(),
            'left': py.image.load('images/resized_player_no_left.png').convert_alpha()
        }
        self.images['up_right'] = py.transform.rotate(self.images['up'], -45)
        self.images['up_left'] = py.transform.rotate(self.images['up'], 45)
        self.images['down_right'] = py.transform.rotate(self.images['down'], 45)
        self.images['down_left'] = py.transform.rotate(self.images['down'], -45)

        self.image = self.images['up']
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collision_mask = self.game.collision_mask

        self.experience = 0
        self.level = 1
        self.hp = 1000
        self.money = 20
        self.strength = strength
        self.intellect = intellect
        self.popularity = popularity

        self.tiredness = 0
        self.hunger = 0
        self.active = True

        self.clock = "12:00"
        self.last_time_update = time.time()
        self.days = 1
        self.last_bills_paid_day = 1

    def can_move(self, dx, dy):
        next_rect = self.rect.move(dx, dy)
        if 0 <= next_rect.centerx < self.collision_mask.get_size()[0] and 0 <= next_rect.centery < self.collision_mask.get_size()[1]:
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
        self.draw_days()

    def draw_bar(self, x, y, width, height, current_value, max_value, border_color, bg_color, fill_color, text, text_color):
        py.draw.rect(self.game.screen, border_color, (x - 2, y - 2, width + 4, height + 4))
        py.draw.rect(self.game.screen, bg_color, (x, y, width, height))
        fill_width = int(width * (current_value / max_value))
        py.draw.rect(self.game.screen, fill_color, (x, y, fill_width, height))

        font = py.font.SysFont(None, 24)
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        self.game.screen.blit(text_surf, text_rect)

    def draw_experience_bar(self):
        self.draw_bar(
            x=10, y=self.window_size[1] - 30,
            width=200, height=20,
            current_value=self.experience, max_value=1000,
            border_color=(0, 0, 0), bg_color=(50, 50, 50),
            fill_color=(0, 255, 0),
            text=f'LVL: {self.level}', text_color=(255, 255, 255)
        )

    def draw_hp_bar(self):
        self.draw_bar(
            x=10, y=self.window_size[1] - 60,
            width=200, height=20,
            current_value=self.hp, max_value=1000,
            border_color=(0, 0, 0), bg_color=(50, 50, 50),
            fill_color=(255, 0, 0),
            text=f'HP: {self.hp}/1000', text_color=(255, 255, 255)
        )

    def draw_money_amount(self):
        self.draw_bar(
            x=10, y=self.window_size[1] - 90,
            width=200, height=20,
            current_value=self.money, max_value=100,
            border_color=(0, 0, 0), bg_color=(255, 253, 208),
            fill_color=(255, 253, 208),
            text=f'Money: ${self.money}', text_color=(0, 0, 0)
        )

    def draw_popularity(self):
        self.draw_bar(
            x=self.window_size[0] - 175, y=self.window_size[1] - 25,
            width=150, height=20,
            current_value=self.popularity, max_value=100,
            border_color=(0, 0, 0), bg_color=(255, 253, 208),
            fill_color=(255, 253, 208),
            text=f'Popularity: {self.popularity}', text_color=(0, 0, 0)
        )

    def draw_strength(self):
        self.draw_bar(
            x=self.window_size[0] - 175, y=self.window_size[1] - 45,
            width=150, height=20,
            current_value=self.strength, max_value=100,
            border_color=(0, 0, 0), bg_color=(255, 253, 208),
            fill_color=(255, 253, 208),
            text=f'Strength: {self.strength}', text_color=(0, 0, 0)
        )

    def draw_intellect(self):
        self.draw_bar(
            x=self.window_size[0] - 175, y=self.window_size[1] - 65,
            width=150, height=20,
            current_value=self.intellect, max_value=100,
            border_color=(0, 0, 0), bg_color=(255, 253, 208),
            fill_color=(255, 253, 208),
            text=f'Intellect: {self.intellect}', text_color=(0, 0, 0)
        )

    def draw_tired(self):
        self.draw_bar(
            x=self.window_size[0] - 215, y=10,
            width=200, height=20,
            current_value=self.tiredness, max_value=100,
            border_color=(0, 0, 0), bg_color=(50, 50, 50),
            fill_color=(0, 120, 120),
            text=f'Tired: {self.tiredness}/100', text_color=(255, 255, 255)
        )

    def draw_hunger(self):
        self.draw_bar(
            x=self.window_size[0] - 215, y=40,
            width=200, height=20,
            current_value=self.hunger, max_value=100,
            border_color=(0, 0, 0), bg_color=(50, 50, 50),
            fill_color=(0, 120, 120),
            text=f'Hunger: {self.hunger}/100', text_color=(255, 255, 255)
        )

    def draw_clock(self):
        clock_radius = 40
        border_thickness = 5
        x = clock_radius + 10
        y = clock_radius + 10

        py.draw.circle(self.game.screen, (0, 0, 0), (x, y), clock_radius + border_thickness)
        py.draw.circle(self.game.screen, (255, 255, 255), (x, y), clock_radius)

        font = py.font.SysFont(None, 24)
        text = font.render(self.clock, True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        self.game.screen.blit(text, text_rect)

    def control_time_flow(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_time_update
        if elapsed_time >= 1:
            in_game_minutes = int(elapsed_time * 5)
            self.last_time_update = current_time
            self.update_hunger_from_time()
            self.update_tiredness_from_time()
            hours, minutes = map(int, self.clock.split(':'))
            minutes += in_game_minutes
            if minutes >= 60:
                hours += minutes // 60
                minutes %= 60
            if hours >= 24:
                hours %= 24
                self.days += 1
            if self.days - self.last_bills_paid_day >= 5:
                self.game.home.bills_paid = False

            self.clock = f"{hours:02d}:{minutes:02d}"

    def update_tiredness_from_time(self):
        if self.tiredness < 100:
            self.tiredness += 0.25

    def update_hunger_from_time(self):
        if self.hunger < 100:
            self.hunger = round(self.hunger + 0.2, 1)

    def draw_days(self):
        x = 50
        y = 110
        font = py.font.SysFont(None, 24)
        text = font.render(f'Day: {self.days}', True, (0, 0, 0))
        text_rect = text.get_rect(center=(x, y))
        self.game.screen.blit(text, text_rect)
