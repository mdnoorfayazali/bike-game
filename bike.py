import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 5
FPS = 60
DISTANCE_TO_COMPLETE_LEVEL = 1000  # in pixels (1 km)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Race Game")

# Load car image for the player
car_image = pygame.image.load("car.png")  # Load your car image
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, 30))  # Adjust the size as needed

# Load obstacle image (tree)
tree_image = pygame.image.load("tree.png")  # Load your tree image
tree_image = pygame.transform.scale(tree_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Function to draw obstacles
def draw_obstacle(obstacle_rect):
    screen.blit(tree_image, obstacle_rect)

def show_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        car_x = SCREEN_WIDTH // 2
        car_y = SCREEN_HEIGHT - 100
        car_rect = car_image.get_rect(center=(car_x, car_y))

        obstacles = []
        score = 0
        distance_traveled = 0
        start_time = time.time()
        level_completed = False

        while not level_completed:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    level_completed = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car_x > 0:
                car_x -= 5
            if keys[pygame.K_RIGHT] and car_x < SCREEN_WIDTH - CAR_WIDTH:
                car_x += 5

            car_rect.x = car_x
            screen.blit(car_image, car_rect)

            # Create new obstacles (trees)
            if random.randint(1, 20) == 1:  # Adjust frequency of obstacles
                obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
                obstacle_rect = pygame.Rect(obstacle_x, 0, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                obstacles.append(obstacle_rect)

            # Move obstacles down
            for obstacle_rect in obstacles:
                obstacle_rect.y += OBSTACLE_SPEED
                draw_obstacle(obstacle_rect)

            # Check for collisions
            for obstacle_rect in obstacles:
                if car_rect.colliderect(obstacle_rect):
                    print("Game Over! Your score: ", score)
                    level_completed = True

            # Remove off-screen obstacles
            obstacles = [obstacle for obstacle in obstacles if obstacle.y < SCREEN_HEIGHT]

            # Update distance traveled
            distance_traveled += OBSTACLE_SPEED
            score += 1

            # Display distance and time
            elapsed_time = int(time.time() - start_time)
            show_text(f"Distance: {distance_traveled} px", 24, BLACK, 10, 10)
            show_text(f"Time: {elapsed_time} s", 24, BLACK, 10, 40)

            # Check if level is completed
            if distance_traveled >= DISTANCE_TO_COMPLETE_LEVEL:
                show_text("Level Completed!", 48, GREEN, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait for 2 seconds
                level_completed = True

            pygame.display.flip()
            clock.tick(FPS)

        # Replay option
        while True:
            screen.fill(WHITE)
            show_text("Game Over! Your score: " + str(score), 36, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
            show_text("Press R to Replay or Q to Quit", 36, BLACK, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        break  # Restart the game
                    if event.key == pygame.K_q:
                        running = False
                        break

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()