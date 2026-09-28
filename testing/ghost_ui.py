import pygame
import os

class GhostUI(pygame.sprite.Sprite):
    def __init__(self, color, x, y, size=30):
        super().__init__()
        self.color = color  # Expected: "cyan", "orange", "pink", "red"
        self.direction = "R" # Initial direction: "U", "D", "L", "R"
        self.size = size
        
        # Load images for all 4 directions
        self.images = {
            "U": self.load_image("U"),
            "angry_red": self.load_image("angry_red"),
            "D": self.load_image("D"),
            "L": self.load_image("L"),
            "R": self.load_image("R")
        }
        
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def load_image(self, direction):
        """Loads the ghost image for a given direction."""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        folder = "angry_red" if self.color == "Ared" and direction in {"U", "D", "L", "R"} else direction
        path = os.path.join(project_root, "img", "ghosts", folder, f"{self.color}-{direction}.png")
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (self.size, self.size))
        else:
            # Fallback circle if image is missing
            surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            color_rgb = self.get_fallback_color()
            pygame.draw.circle(surf, color_rgb, (self.size//2, self.size//2), self.size//2)
            return surf
            
    def get_fallback_color(self):
        """Returns RGB tuples for fallback shapes if images aren't available."""
        colors = {
            "cyan": (0, 255, 255),
            "orange": (255, 165, 0),
            "pink": (255, 105, 180),
            "red": (255, 0, 0)
        }
        return colors.get(self.color, (255, 255, 255))
        
    def update_direction(self, new_direction):
        """Updates the ghost's sprite to face the new direction."""
        if new_direction in self.images and new_direction != self.direction:
            self.direction = new_direction
            self.image = self.images[self.direction]
            
    def set_position(self, x, y):
        """Sets absolute position for the ghost."""
        self.rect.x = x
        self.rect.y = y
        
    def move(self, dx, dy):
        """Moves the ghost by dx, dy and automatically updates its direction."""
        self.rect.x += dx
        self.rect.y += dy
        
        # Automatically update image direction based on movement vector
        if dx > 0:
            self.update_direction("R")
        elif dx < 0:
            self.update_direction("L")
        elif dy > 0:
            self.update_direction("D")
        elif dy < 0:
            self.update_direction("U")

    def draw(self, screen):
        """Blits the ghost onto the given screen surface."""
        screen.blit(self.image, self.rect)