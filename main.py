import math
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
DANGER_RADIUS = 150 


class Square:
	def __init__(self) -> None:
		self.size = random.randint(SQUARE_MIN_SIZE, SQUARE_MAX_SIZE)
		self.x = random.randint(0, WINDOW_WIDTH - self.size)
		self.y = random.randint(0, WINDOW_HEIGHT - self.size)

		self.life = random.randint(FPS * 2, FPS * 6)

		# Bigger squares are slower
		size_ratio = (self.size - SQUARE_MIN_SIZE) / (SQUARE_MAX_SIZE - SQUARE_MIN_SIZE)
		self.max_speed = max(1, int(GLOBAL_MAX_SPEED * (1 - size_ratio * 0.75)))

		self.vx = random.choice([-1, 1]) * random.randint(1, self.max_speed)
		self.vy = random.choice([-1, 1]) * random.randint(1, self.max_speed)
		self.color = (
			random.randint(80, 255),
			random.randint(80, 255),
			random.randint(80, 255),
		)

	def center(self) -> tuple[float, float]:
		return (self.x + self.size / 2, self.y + self.size / 2)

	def update(self, squares: list["Square"]) -> None:
		bigger_neighbors = [s for s in squares if s is not self and s.size > self.size]

		cx, cy = self.center()
		nearby_threats = [
			s for s in bigger_neighbors
			if distance((cx, cy), s.center()) < DANGER_RADIUS
		]

		if nearby_threats:
			threat = min(nearby_threats, key=lambda s: distance((cx, cy), s.center()))

			tx, ty = threat.center()
			dx = cx - tx
			dy = cy - ty
			dist = distance((cx, cy), (tx, ty))

			if dist > 0:
				nx = dx / dist
				ny = dy / dist

				flee_strength = 4.0 * (1.0 - dist / DANGER_RADIUS)
				self.vx += nx * flee_strength
				self.vy += ny * flee_strength

				speed = math.hypot(self.vx, self.vy)
				if speed > self.max_speed:
					self.vx = (self.vx / speed) * self.max_speed
					self.vy = (self.vy / speed) * self.max_speed

		elif random.random() < 0.02:
			self.vx = random.choice([-1, 1]) * random.randint(1, self.max_speed)
			self.vy = random.choice([-1, 1]) * random.randint(1, self.max_speed)

		self.x += self.vx
		self.y += self.vy

		if self.x <= 0 or self.x + self.size >= WINDOW_WIDTH:
			self.vx *= -1
			self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))

		if self.y <= 0 or self.y + self.size >= WINDOW_HEIGHT:
			self.vy *= -1
			self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

		self.life -= 1

	def draw(self, surface: pygame.Surface) -> None:
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
	return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Random Moving Squares")
	clock = pygame.time.Clock()

	squares = [Square() for _ in range(SQUARE_COUNT)]

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		screen.fill(BACKGROUND_COLOR)

		# Update squares
		for square in squares:
			square.update(squares)

		# Remove dead squares
		squares = [s for s in squares if s.life > 0]

		# Spawn new ones
		while len(squares) < SQUARE_COUNT:
			squares.append(Square())

		# Draw squares
		for square in squares:
			square.draw(screen)

		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	main()