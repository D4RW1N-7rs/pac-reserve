import pygame
import sys
import os

# Add parent directory to path just in case
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import testing.maze_window as maze_window
except ImportError:
    maze_window = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Pacman - Start")
    
    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 72)
    
    button_rect = pygame.Rect(200, 200, 200, 80)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    if maze_window:
                        # Close the start window and start the game
                        running = False
                        maze_window.main()
                        pygame.quit()
                        sys.exit()
                    else:
                        print("maze_window.py not found. Cannot start game.")
                        
        screen.fill((0, 0, 0)) # black background
        
        # Draw Title
        title_text = title_font.render("PACMAN", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(300, 100))
        screen.blit(title_text, title_rect)
        
        # Draw Start Button
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 2)
        
        # Draw Start Text
        text = font.render("START", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        
if __name__ == "__main__":
    main()