"""Define the Pac-Man player entity.

This module should contain the player's position, direction, movement rules,
lives-related state, and interactions with walls and collectibles. It should
not load configuration files or draw directly; those responsibilities belong
to the systems and UI layers.
"""

import pygame

U, D, R, L = 1, 4, 2, 8

class Player:

    def __init__(self, start_grid_x, start_grid_y, tile_size):
        self.pixel_x = start_grid_x * tile_size
        self.pixel_y = start_grid_y * tile_size
        self.current_direction = "STOP"
        self.next_direction = "STOP"
        self.last_direction = "RIGHT"
        self.speed = 5 
        self.load_images()
        self.animation_tick = 0

    def pac_animation(self, img, x , y):
        self.window.blit((img),(x,y))

    def load_images(self):
        self.pac1_head = pygame.image.load("img/pac/1.png")
        self.pac2_R = pygame.image.load("img/pac/R/2.png")
        self.pac3_R = pygame.image.load("img/pac/R/3.png")
        self.pac2_L = pygame.image.load("img/pac/L/2.png")
        self.pac1_L = pygame.image.load("img/pac/L/1.png")
        self.pac2_D = pygame.image.load("img/pac/D/2.png")
        self.pac1_D = pygame.image.load("img/pac/D/1.png")
        self.pac2_U = pygame.image.load("img/pac/U/2.png")
        self.pac1_U = pygame.image.load("img/pac/U/1.png")

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.next_direction = "UP"
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.next_direction = "DOWN"
                
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.next_direction = "RIGHT"
            
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.next_direction = "LEFT"

    def update(self, maze, tile_size):
        """Called every frame in your game.py PLAYING state."""
        grid_x = self.pixel_x // tile_size
        grid_y = self.pixel_y // tile_size

        if self.pixel_x % tile_size == 0 and self.pixel_y % tile_size == 0:
            cell = maze[grid_y][grid_x]
            can_turn = False
            
            if self.next_direction == "UP" and not (cell & U):
                can_turn = True
            elif self.next_direction == "DOWN" and not (cell & D):
                can_turn = True
            elif self.next_direction == "RIGHT" and not (cell & R):
                can_turn = True
            elif self.next_direction == "LEFT" and not (cell & L):
                can_turn = True

            if can_turn:
                self.current_direction = self.next_direction

            is_blocked = False
            
            if self.current_direction == "UP" and (cell & U):
                is_blocked = True
            elif self.current_direction == "DOWN" and (cell & D):
                is_blocked = True
            elif self.current_direction == "RIGHT" and (cell & R):
                is_blocked = True
            elif self.current_direction == "LEFT" and (cell & L):
                is_blocked = True
                
            if is_blocked:
                self.current_direction = "STOP"

        if self.current_direction == "UP":
            self.pixel_y -= self.speed
        elif self.current_direction == "DOWN":
            self.pixel_y += self.speed
        elif self.current_direction == "RIGHT":
            self.pixel_x += self.speed
        elif self.current_direction == "LEFT":
            self.pixel_x -= self.speed
        if self.current_direction != "STOP":
            self.animation_tick += 1
            self.last_direction = self.current_direction

    def draw(self, window, padding, hud_height, tile_size):

        img_width = self.pac1_head.get_width()
        img_height = self.pac1_head.get_height()
        
        offset_x = (tile_size - img_width) // 2
        offset_y = (tile_size - img_height) // 2

        draw_x = self.pixel_x + padding + offset_x
        draw_y = self.pixel_y + padding + hud_height + offset_y
        
        frame = (self.animation_tick // 5) % 5
        
        image_to_draw = self.pac1_head 
        
        if self.last_direction == "RIGHT":
            if frame == 0: image_to_draw = self.pac1_head
            elif frame == 1 : image_to_draw = self.pac2_R
            elif frame == 2 : image_to_draw = self.pac3_R
            elif frame == 3 : image_to_draw = self.pac2_R
            elif frame == 4 : image_to_draw = self.pac1_head

        elif self.last_direction == "LEFT":
            if frame == 0: image_to_draw = self.pac1_head
            elif frame == 1 : image_to_draw = self.pac2_L
            elif frame == 2 : image_to_draw = self.pac1_L
            elif frame == 3 : image_to_draw = self.pac2_L
            elif frame == 4 : image_to_draw = self.pac1_head

        elif self.last_direction == "UP":
            if frame == 0: image_to_draw = self.pac1_head
            elif frame == 1 : image_to_draw = self.pac2_U
            elif frame == 2 : image_to_draw = self.pac1_U
            elif frame == 3 : image_to_draw = self.pac2_U
            elif frame == 4 : image_to_draw = self.pac1_head

        elif self.last_direction == "DOWN":
            if frame == 0: image_to_draw = self.pac1_head
            elif frame == 1 : image_to_draw = self.pac2_D
            elif frame == 2 : image_to_draw = self.pac1_D
            elif frame == 3 : image_to_draw = self.pac2_D
            elif frame == 4 : image_to_draw = self.pac1_head
        
        window.blit(image_to_draw, (draw_x, draw_y))









