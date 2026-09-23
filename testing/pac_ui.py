import pygame
import os

class PacUI(pygame.sprite.Sprite):
    def __init__(self, x, y, size=30):
        super().__init__()
        self.direction = "R"
        self.size = size
        
        # Base path for the project
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # Load the common closed mouth frame
        self.closed_frame = self.load_image(os.path.join("pac", "1.png"))
        
        # Load the directional open mouth frames
        self.frames = {
            "U": self.load_direction_frames("U"),
            "D": self.load_direction_frames("D"),
            "L": self.load_direction_frames("L"),
            "R": self.load_direction_frames("R")
        }
        
        # Animation state
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 5  # Number of game ticks per animation frame
        
        self.image = self.closed_frame
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def load_image(self, rel_path):
        """Loads an image relative to the img directory and scales it."""
        path = os.path.join(self.project_root, "img", rel_path)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (self.size, self.size))
        else:
            # Fallback circle if image is missing
            surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 0), (self.size//2, self.size//2), self.size//2)
            return surf
            
    def load_direction_frames(self, direction):
        """Loads the sequence of open mouth frames for a given direction."""
        return [
            self.load_image(os.path.join("pac", direction, "2.png")),  # Half open
            self.load_image(os.path.join("pac", direction, "3.png")),  # Fully open
            self.load_image(os.path.join("pac", direction, "2.png"))   # Half open
        ]
        
    def update_direction(self, new_direction):
        """Updates the direction pacman is facing."""
        if new_direction in self.frames and new_direction != self.direction:
            self.direction = new_direction
            
    def set_position(self, x, y):
        """Sets absolute pixel position."""
        self.rect.x = x
        self.rect.y = y
        
    def move(self, dx, dy):
        """Moves pacman and automatically updates his facing direction."""
        self.rect.x += dx
        self.rect.y += dy
        
        if dx > 0: self.update_direction("R")
        elif dx < 0: self.update_direction("L")
        elif dy > 0: self.update_direction("D")
        elif dy < 0: self.update_direction("U")
        
    def update_animation(self):
        """Ticks the animation frame forward."""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            # 4 states: 0 (closed), 1 (half open), 2 (full open), 3 (half open)
            self.frame_index = (self.frame_index + 1) % 4
            
            if self.frame_index == 0:
                self.image = self.closed_frame
            else:
                dir_frames = self.frames[self.direction]
                self.image = dir_frames[self.frame_index - 1]

    def draw(self, screen):
        """Updates animation and blits pacman onto the screen."""
        self.update_animation()
        screen.blit(self.image, self.rect)

