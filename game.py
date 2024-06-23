import pygame
import sys
import random
import time

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
YELLOW = (255, 250, 0)

# Gravity constant
gravity = 0.5

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# Load the background image
background_image = pygame.image.load("background.jpg").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the bird image
bird_image = pygame.image.load("bird.png").convert_alpha()  # Load with alpha channel
bird_width, bird_height = bird_image.get_size()
bird_x = SCREEN_WIDTH // 2 - bird_width // 2  # Center the bird horizontally
bird_y = SCREEN_HEIGHT // 2

# Bird properties (adjust based on your image size)
bird_velocity = 0

# Function to draw the bird
def draw_bird(x, y):
  screen.blit(bird_image, (x, y))

# Rectangle class with an additional 'scored' attribute
class Rectangle(pygame.Rect):
  def __init__(self, x, y, width, height):
    super().__init__(x, y, width, height)
    self.scored = False

# Function to generate a pair of rectangles (pipes)
def generate_rectangles(gap_size=200):
  rect_width = 70
  rect_height = random.randint(50, SCREEN_HEIGHT - gap_size - 100)
  rect_x = SCREEN_WIDTH

  bottom_rect_y = SCREEN_HEIGHT - rect_height
  bottom_rect = Rectangle(rect_x, bottom_rect_y, rect_width, rect_height)

  top_rect_height = SCREEN_HEIGHT - rect_height - gap_size
  top_rect = Rectangle(rect_x, 0, rect_width, top_rect_height)

  return top_rect, bottom_rect

# Score counter
score = 0

# Font for displaying the score
font = pygame.font.Font(None, 36)

rectangles = []

last_time = time.time()
# Main game loop
running = True
while running:
  screen.blit(background_image, (0, 0))

  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        bird_velocity = -10  # Jumping velocity

  # Update bird position
  bird_y += bird_velocity
  bird_velocity += gravity

  # Check for collisions (top of screen and bottom of screen)
  if bird_y <= 0 or bird_y + bird_height >= SCREEN_HEIGHT:
    running = False

  # Draw bird
  draw_bird(bird_x, int(bird_y))

  curr = time.time()

  # Generate a new pair of rectangles with a certain probability
  if curr - last_time >= 1.3:  # Adjust the probability as desired
    top_rect, bottom_rect = generate_rectangles()
    rectangles.append(top_rect)
    rectangles.append(bottom_rect)
    last_time = curr

  # Update and draw all rectangles
  for rect in rectangles[:]:
    rect.x -= 5  # Adjust the speed as desired
    pygame.draw.rect(screen, GREEN, rect)
    if rect.right < 0:
      rectangles.remove(rect)

    # Check for collision with the bird
    if rect.colliderect(pygame.Rect(bird_x, bird_y, bird_width, bird_height)):
      pygame.draw.rect(screen, RED, rect)  # Visual indication of collision (optional)
      running = False  # End the game on collision

    # Check if the bird has successfully passed the rectangle
    if rect.right < bird_x and not rect.scored:
      score += 0.5  # Increment by 0.5 to account for passing both top and bottom rectangles
      rect.scored = True  # Mark this rectangle as passed

  # Display the score
  score_text = font.render(f"Score: {int(score)}", True, BLACK)
  screen.blit(score_text, (10, 10))

  # Update the screen
  pygame.display.update()

  # Cap the frame rate
  clock.tick(60)

pygame.quit()
sys.exit()
