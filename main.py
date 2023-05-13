import pygame, random

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

BRICK_WIDTH = 150
BRICK_HEIGHT = 50
BRICK_COLORS = ["red", "green", "blue", "pink", "orange", "black", "gray"]
BRICK_ROWS = 3
BRICK_COLS = 8
BRICK_GAP = 12


class Brick:
    def __init__(self, coords):
        self.y = coords["y"]
        self.x = coords["x"]
        self.color = random.choice(BRICK_COLORS)

        print({self.y, self.x})
        self.rect = pygame.Rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT)


def handle_draw(paddle, ball_coords, bricks):
    SCREEN.fill(WHITE)

    pygame.draw.rect(SCREEN, "red", paddle)
    pygame.draw.circle(SCREEN, "green", ball_coords, BALL_RADIUS)

    for brick in bricks:
        pygame.draw.rect(SCREEN, brick.color, brick.rect)


def handle_input(pressed_keys, has_fired, ball_x, paddle):
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
    return has_fired, ball_x


def handle_ball_movement(ball_y, ball_x, ball_direction, ball_x_offset, ball_vel):
    if ball_direction == "up":
        ball_y -= ball_vel  # Goes up
    if ball_direction == "down":
        ball_y += ball_vel

    if ball_x - ball_x_offset - BALL_RADIUS <= 0:  # Left wall hit
        ball_x_offset = 2
    if ball_x + ball_x_offset + BALL_RADIUS >= WIDTH:  # Right wall hit
        ball_x_offset = -2

    ball_x += ball_x_offset  # Goes left / right

    return ball_y, ball_x, ball_x_offset


def generate_bricks():
    bricks = []

    for i in range(BRICK_ROWS):
        brick_y = (BRICK_HEIGHT + BRICK_GAP) * i
        for x in range(BRICK_COLS):
            brick_x = (BRICK_WIDTH + BRICK_GAP) * x

            bricks.append(Brick({"y": brick_y, "x": brick_x}))

    return bricks


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

    bricks = generate_bricks()

    while running:
        ball_coords = (ball_x, ball_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pressed_keys = pygame.key.get_pressed()

        has_fired, ball_x = handle_input(pressed_keys, has_fired, ball_x, paddle)

        # Handle ball movement
        if has_fired:
            if ball_y + ball_vel - BALL_RADIUS <= 0:  # Ceiling is hit
                ball_direction = "down"
            if paddle.collidepoint(ball_coords):  # Paddle is hit
                ball_direction = "up"
                ball_x_offset = (ball_coords[0] - paddle.centerx) / 25

            ball_y, ball_x, ball_x_offset = handle_ball_movement(
                ball_y, ball_x, ball_direction, ball_x_offset, ball_vel
            )

        # Generate Bricks

        handle_draw(paddle, ball_coords, bricks)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
