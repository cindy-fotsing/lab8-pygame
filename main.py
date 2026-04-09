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
DANGER_RADIUS = 150  # px — squares ignore threats beyond this distance


class Square:
	def __init__(self) -> None:
		self.size = random.randint(SQUARE_MIN_SIZE, SQUARE_MAX_SIZE)
		self.x = random.randint(0, WINDOW_WIDTH - self.size)
		self.y = random.randint(0, WINDOW_HEIGHT - self.size)

		# Bigger squares are slower: max speed scales inversely with size
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
		# Returns the center point of this square.
		return (self.x + self.size / 2, self.y + self.size / 2)

	def update(self, squares: list["Square"]) -> None:
		# --- TODO 2: Build bigger_neighbors (all squares larger than self) ---
		bigger_neighbors = [s for s in squares if s is not self and s.size > self.size]

		# --- TODO 3: Pick the nearest threat within DANGER_RADIUS ---
		cx, cy = self.center()
		nearby_threats = [
			s for s in bigger_neighbors
			if distance((cx, cy), s.center()) < DANGER_RADIUS
		]

		if nearby_threats:
			threat = min(nearby_threats, key=lambda s: distance((cx, cy), s.center()))

			# --- TODO 4: Compute a normalized flee direction (away from threat) ---
			tx, ty = threat.center()
			dx = cx - tx
			dy = cy - ty
			dist = distance((cx, cy), (tx, ty))

			if dist > 0:
				# Normalize to unit vector
				nx = dx / dist
				ny = dy / dist

				# --- TODO 5: Scale flee strength by proximity — closer = stronger push ---
				# At dist=0 → strength=4.0; at dist=DANGER_RADIUS → strength≈0
				flee_strength = 4.0 * (1.0 - dist / DANGER_RADIUS)
				self.vx += nx * flee_strength
				self.vy += ny * flee_strength

				# --- TODO 6: Clamp speed so we never exceed max_speed ---
				speed = math.hypot(self.vx, self.vy)
				if speed > self.max_speed:
					self.vx = (self.vx / speed) * self.max_speed
					self.vy = (self.vy / speed) * self.max_speed

		# Random nudge only fires when NOT actively fleeing, to avoid fighting the flee
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

	def draw(self, surface: pygame.Surface) -> None:
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
	# TODO 7: Reused here to find nearest bigger neighbor (see update above).
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

		for square in squares:
			# TODO 8: All squares are passed so each one can inspect its neighbors.
			square.update(squares)
			square.draw(screen)

		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	main()