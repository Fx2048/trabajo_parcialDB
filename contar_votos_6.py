import pygame
import requests
import time
import threading

# Configuración del juego
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10
VOTE_INTERVAL = 3  # Cada 3 segundos obtiene la dirección más votada
SERVER_URL = "http://localhost:5000/get_direction"  # URL del servidor Flask

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - Votación")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = "UP"
        self.food = self.spawn_food()
        self.start_voting_thread()
    
    def spawn_food(self):
        return (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
    
    def move_snake(self):
        x, y = self.snake[0]
        if self.direction == "UP":
            y -= CELL_SIZE
        elif self.direction == "DOWN":
            y += CELL_SIZE
        elif self.direction == "LEFT":
            x -= CELL_SIZE
        elif self.direction == "RIGHT":
            x += CELL_SIZE
        
        self.snake.insert(0, (x, y))
        if (x, y) == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def check_collision(self):
        x, y = self.snake[0]
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or self.snake[0] in self.snake[1:]:
            self.running = False
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
    
    def fetch_direction(self):
        try:
            response = requests.get(SERVER_URL)
            data = response.json()
            if data.get("direction"):
                self.direction = data["direction"]
        except Exception as e:
            print("Error al obtener dirección:", e)
    
    def start_voting_thread(self):
        threading.Thread(target=self.voting_system, daemon=True).start()
    
    def voting_system(self):
        while self.running:
            time.sleep(VOTE_INTERVAL)
            self.fetch_direction()
    
    def run(self):
        while self.running:
            self.move_snake()
            self.check_collision()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()

