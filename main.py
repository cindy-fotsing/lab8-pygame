import random
import sys

import pygame


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (20, 20, 30)
FPS = 60
SQUARE_COUNT = 10


class Square:
	def __init__(self) -> None:
		self.size = random.randint(20, 50)
		self.x = random.randint(0, WINDOW_WIDTH - self.size)
		self.y = random.randint(0, WINDOW_HEIGHT - self.size)
		self.vx = random.choice([-1, 1]) * random.randint(2, 6)
		self.vy = random.choice([-1, 1]) * random.randint(2, 6)
		self.color = (
			random.randint(80, 255),
			random.randint(80, 255),
			random.randint(80, 255),
		)

	def update(self) -> None:
		if random.random() < 0.02:
			self.vx = random.choice([-1, 1]) * random.randint(2, 6)
			self.vy = random.choice([-1, 1]) * random.randint(2, 6)

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
			square.update()
			square.draw(screen)

		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()
	sys.exit()


if __name__ == "__main__":
	main()
