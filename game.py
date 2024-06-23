import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255,250,0)

# Gravity constant
gravity = 0.5

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Ball")

clock = pygame.time.Clock()

# Ball properties
ball_radius = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_velocity = 0

# Function to draw the ball
def draw_ball(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), ball_radius)

# Rectangle class with an additional 'scored' attribute
class Rectangle(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.scored = False

# Function to generate a random rectangle
def generate_rectangle():
    rect_width = 70
    rect_height = random.randint(50, SCREEN_HEIGHT - 100)
    rect_x = SCREEN_WIDTH
    rect_y = SCREEN_HEIGHT - rect_height
    return Rectangle(rect_x, rect_y, rect_width, rect_height)

# Score counter
score = 0

# Font for displaying the score
font = pygame.font.Font(None, 36)

rectangles = []

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_velocity = -10  # Jumping velocity

    # Update ball position
    ball_y += ball_velocity
    ball_velocity += gravity

    if ball_y >= SCREEN_HEIGHT:
        running = False
    # Draw ball
    draw_ball(ball_x, int(ball_y))

    # Generate a new rectangle with a certain probability
    if random.random() < 0.02:  # Adjust the probability as desired
        new_rect = generate_rectangle()
        rectangles.append(new_rect)

    # Update and draw all rectangles
    for rect in rectangles[:]:
        rect.x -= 5  # Adjust the speed as desired
        pygame.draw.rect(screen, GREEN, rect)
        if rect.right < 0:
            rectangles.remove(rect)

        # Check for collision with the ball
        if rect.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
            pygame.draw.rect(screen, RED, rect)  # Visual indication of collision (optional)
            running = False  # End the game on collision

        # Check if the ball has successfully passed the rectangle
        if rect.right < ball_x and not rect.scored:
            score += 1
            rect.scored = True  # Mark this rectangle as passed

    # Display the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.update()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
sys.exit()
