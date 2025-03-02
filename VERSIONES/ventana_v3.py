import pygame
import random
import sqlite3
import threading
import time
import tkinter as tk
from tkinter import messagebox

# Configuración del juego
WIDTH, HEIGHT = 900, 600
CELL_SIZE = 20
FPS = 10
VOTE_INTERVAL = 3  # Reducir el tiempo de votación a 3 segundos

def init_db():
    conn = sqlite3.connect("votaciones.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            direccion TEXT,
            procesado INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def insertar_voto(direccion):
    conn = sqlite3.connect("votaciones.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO votos (direccion) VALUES (?)", (direccion,))
    conn.commit()
    conn.close()

def contar_votos():
    conn = sqlite3.connect("votaciones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT direccion, COUNT(*) FROM votos WHERE procesado = 0 GROUP BY direccion")
    votos = cursor.fetchall()
    conn.close()
    
    if not votos:
        return None
    
    max_votos = max(votos, key=lambda x: x[1])
    return max_votos[0]

def marcar_votos_como_procesados():
    conn = sqlite3.connect("votaciones.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE votos SET procesado = 1")
    conn.commit()
    conn.close()

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
            messagebox.showinfo("Game Over", "La serpiente ha chocado. Reiniciando el juego...")
            self.__init__()
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
    
    def voting_system(self):
        while self.running:
            time.sleep(VOTE_INTERVAL)  # Esperar menos tiempo para responder más rápido
            new_direction = contar_votos()
            if new_direction:
                self.direction = new_direction
                marcar_votos_como_procesados()
    
    def start_voting_thread(self):
        threading.Thread(target=self.voting_system, daemon=True).start()
    
    def run(self):
        while self.running:
            self.move_snake()
            self.check_collision()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

class VotingWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ventana de Votación")
        
        self.btn_up = tk.Button(self.root, text="Arriba", command=lambda: self.vote("UP"))
        self.btn_up.pack()
        
        self.btn_down = tk.Button(self.root, text="Abajo", command=lambda: self.vote("DOWN"))
        self.btn_down.pack()
        
        self.btn_left = tk.Button(self.root, text="Izquierda", command=lambda: self.vote("LEFT"))
        self.btn_left.pack()
        
        self.btn_right = tk.Button(self.root, text="Derecha", command=lambda: self.vote("RIGHT"))
        self.btn_right.pack()
        
        self.status_label = tk.Label(self.root, text="Esperando votación...")
        self.status_label.pack()
    
    def vote(self, direction):
        insertar_voto(direction)
        self.status_label.config(text=f"Voto registrado: {direction}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    init_db()
    game_thread = threading.Thread(target=lambda: SnakeGame().run(), daemon=True)
    game_thread.start()
    voting_window = VotingWindow()
    voting_window.run()
