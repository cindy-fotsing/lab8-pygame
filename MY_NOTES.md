import random
import sys
import pygame


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = [random.randint(0, 255) for x in range(3)]
FPS = 60
SQUARE_COUNT = 20

SQUARE_MIN_SIZE = 10
SQUARE_MAX_SIZE = 60
GLOBAL_MAX_SPEED = 8

FLEE_STRENGTH = 0.3
FLEE_RADIUS_MULT = 3  # radius = size * this


class Square:
    def __init__(self) -> None:
        self.size = random.randint(SQUARE_MIN_SIZE, SQUARE_MAX_SIZE)
        self.x = random.randint(0, WINDOW_WIDTH - self.size)
        self.y = random.randint(0, WINDOW_HEIGHT - self.size)

        size_ratio = (self.size - SQUARE_MIN_SIZE) / (SQUARE_MAX_SIZE - SQUARE_MIN_SIZE)
        self.max_speed = max(1, int(GLOBAL_MAX_SPEED * (1 - size_ratio * 0.75)))

        self.vx = random.choice([-1, 1]) * random.randint(1, self.max_speed)
        self.vy = random.choice([-1, 1]) * random.randint(1, self.max_speed)

        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255),
        )

    def get_center(self):
        return (
            self.x + self.size / 2,
            self.y + self.size / 2,
        )

    def update(self, squares) -> None:
        # --- RANDOM MOVEMENT (base behavior) ---
        if random.random() < 0.02:
            self.vx = random.choice([-1, 1]) * random.randint(1, self.max_speed)
            self.vy = random.choice([-1, 1]) * random.randint(1, self.max_speed)

        # --- FLEE BEHAVIOR ---

        # 1. Find bigger neighbors
        bigger = [s for s in squares if s.size > self.size and s is not self]

        if bigger:
            self_center = self.get_center()

            # 2. Find nearest bigger square
            nearest = None
            min_dist = float("inf")

            for s in bigger:
                sc = s.get_center()
                dx = sc[0] - self_center[0]
                dy = sc[1] - self_center[1]
                dist = (dx**2 + dy**2) ** 0.5

                if dist < min_dist:
                    min_dist = dist
                    nearest = s

            # 3. Apply flee if within radius
            flee_radius = self.size * FLEE_RADIUS_MULT

            if nearest and min_dist < flee_radius:
                threat_center = nearest.get_center()

                dx = self_center[0] - threat_center[0]
                dy = self_center[1] - threat_center[1]

                length = (dx**2 + dy**2) ** 0.5

                if length == 0:
                    dx, dy = random.choice([-1, 1]), random.choice([-1, 1])
                    length = (dx**2 + dy**2) ** 0.5

                # normalize
                dx /= length
                dy /= length

                # apply steering
                self.vx += dx * FLEE_STRENGTH
                self.vy += dy * FLEE_STRENGTH

        # --- CLAMP SPEED ---
        speed = (self.vx**2 + self.vy**2) ** 0.5
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.vx *= scale
            self.vy *= scale

        # --- MOVE ---
        self.x += self.vx
        self.y += self.vy

        # --- WALL BOUNCE ---
        if self.x <= 0 or self.x + self.size >= WINDOW_WIDTH:
            self.vx *= -1
            self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))

        if self.y <= 0 or self.y + self.size >= WINDOW_HEIGHT:
            self.vy *= -1
            self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Fleeing Squares")
    clock = pygame.time.Clock()

    squares = [Square() for _ in range(SQUARE_COUNT)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for square in squares:
            square.update(squares)
            square.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()