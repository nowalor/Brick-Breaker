import pygame

pygame.init()

WIDTH = 1280
HEIGHT = 720
CLOCK = pygame.time.Clock()
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)

PADDLE_VEL = 3

PLAYER_WIDTH = 150
PLAYER_HEIGHT = 50

BALL_RADIUS = 15


def handle_draw(paddle, ball_coords):
    SCREEN.fill(WHITE)

    pygame.draw.rect(SCREEN, "red", paddle)
    pygame.draw.circle(SCREEN, "green", ball_coords, BALL_RADIUS)


def main():
    running = True

    CLOCK.tick(60)

    paddle = pygame.Rect(
        (WIDTH / 2) - (PLAYER_WIDTH / 2),
        HEIGHT - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )

    has_fired = False

    ball_y = HEIGHT - PLAYER_HEIGHT - BALL_RADIUS
    ball_x = WIDTH / 2
    ball_vel = 3
    ball_direction = "up"
    ball_x_offset = 0

    while running:
        ball_coords = (ball_x, ball_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pressed_keys = pygame.key.get_pressed()

        # Handle key presses
        if pressed_keys[pygame.K_a] and paddle.x - PADDLE_VEL >= 0:  # LEFT
            paddle.x -= PADDLE_VEL
            if not has_fired:
                ball_x -= PADDLE_VEL
        if (
            pressed_keys[pygame.K_d] and paddle.x + PADDLE_VEL + PLAYER_WIDTH <= WIDTH
        ):  # RIGHT
            paddle.x += PADDLE_VEL
            if not has_fired:
                ball_x += PADDLE_VEL
        if pressed_keys[pygame.K_SPACE] and not has_fired:
            has_fired = True

        # Handle ball movement
        if has_fired:
            if ball_y + ball_vel - 15 <= 0:  # Ceiling is hit
                ball_direction = "down"
                # ball_x_offset = -ball_x_offset
            if paddle.collidepoint(ball_coords):  # Paddle is hit
                ball_direction = "up"
                ball_x_offset = (ball_coords[0] - paddle.centerx) / 25
                print(ball_x_offset)
            if ball_direction == "up":
                ball_y -= ball_vel  # Goes up
                
            if ball_x - ball_x_offset - BALL_RADIUS <= 0:  # Left wall hit
                ball_x_offset = 2
            if ball_x + ball_x_offset + BALL_RADIUS >= WIDTH:  # Right wall hit
                ball_x_offset = -2

                print(ball_x_offset)
            ball_x += ball_x_offset  # Goes left / right

            if ball_direction == "down":
                ball_y += ball_vel

        handle_draw(paddle, ball_coords)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
