import math
import random
import sys
import pygame

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = [random.randint(0, 50) for x in range(3)]
FPS = 60
SQUARE_COUNT = 45 # Total of 5 + 10 + 30 from Q1 with their respective pixels

class Square:
    def __init__(self, initial_size) -> None:
        self.size = initial_size
        self.original_size = initial_size
        
        self.x = random.randint(0, WINDOW_WIDTH - self.size)
        self.y = random.randint(0, WINDOW_HEIGHT - self.size)

        self.life = random.randint(FPS * 2, FPS * 6)

        self.max_speed = 3
        self.vx = random.choice([-1, 1]) * random.randint(1, self.max_speed)
        self.vy = random.choice([-1, 1]) * random.randint(1, self.max_speed)
        
        self.color = (
            random.randint(80, 255),
            random.randint(80, 255),
            random.randint(80, 255),
        )
        self.alive = True
        
    def check_collision(self, other: "Square") -> bool:
        my_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        other_rect = pygame.Rect(other.x, other.y, other.size, other.size)
        return my_rect.colliderect(other_rect)
    
    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy

        if self.x > WINDOW_WIDTH:
            self.x = -self.size
        elif self.x < -self.size:
            self.x = WINDOW_WIDTH
            
        if self.y > WINDOW_HEIGHT:
            self.y = -self.size
        elif self.y < -self.size:
            self.y = WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Exercise 5")
    clock = pygame.time.Clock()

    squares = []
    configs = [(5, 25), (10, 10), (30, 4)] # the pixels from Q1
    for count, size in configs:
        for _ in range(count):
            squares.append(Square(size))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)
        

        for i in range(len(squares)):
            for j in range(len(squares)):
                
                s1 = squares[i]
                s2 = squares[j]
                
                if s1.alive and s2.alive:
                    if s1.check_collision(s2):
                        if s1.size > s2.size:
                            s2.alive = False 
                        elif s2.size > s1.size:
                            s1.alive = False 

        for i in range(len(squares)):
            if not squares[i].alive:
                squares[i] = Square(squares[i].original_size)
            
            squares[i].update()
            squares[i].draw(screen)


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    