"""Render gameplay status information.

This module should display the player's score, remaining lives, current level,
and any timer or status messages. It should receive values from game state and
draw them consistently without calculating collisions, movement, or scores.
"""

HUD_COLOR = (255, 255, 255)
LIFE_ICON_GAP = 8

def draw_hud(window, font, level, score,lives, pac_image):
    """Draw the HUD with score, lives, and Pac-Man image."""
    score_text = font.render(f"Score: {score}", True, HUD_COLOR)
    lives_text = font.render(f"Lives: ", True, HUD_COLOR)
    level_text = font.render(f"Level: {level}", True, HUD_COLOR)

    x = window.get_width() // 2
    
    window.blit(level_text, (10, 10))    
    window.blit(score_text, (10, 40))
    window.blit(lives_text, (x, 10))
    
    for i in range(lives):
        pac_x = x + i * (pac_image.get_width() + 10)
        pac_y = 35
        window.blit(pac_image, (pac_x, pac_y))

