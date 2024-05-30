import tkinter as tk
from tkinter import messagebox
import random
import heapq
from collections import deque
from Node import Node
from Solutions import Solutions
import time

class Puzzle:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Game")

        self.final_state = [[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 0]]

        self.tile_size = 100
        self.canvas_size = self.tile_size * 3

        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.moves = 0
        self.initial_state = None
        self.board = None
        self.empty_pos = None

        self.create_state_labels()
        self.create_buttons()
        self.shuffle_board()
        self.draw_board()

    def create_state_labels(self):
        frame = tk.Frame(self.master)
        frame.pack()

        tk.Label(frame, text="État initial:", font=('Arial', 14)).pack(side=tk.LEFT)
        self.initial_label = tk.Label(frame, text="", font=('Arial', 14))
        self.initial_label.pack(side=tk.LEFT, padx=10)

        tk.Label(frame, text="État final:", font=('Arial', 14)).pack(side=tk.LEFT)
        self.final_label = tk.Label(frame, text=self.format_state(self.final_state), font=('Arial', 14))
        self.final_label.pack(side=tk.LEFT, padx=10)

        tk.Label(frame, text="Steps:", font=('Arial', 14)).pack(side=tk.LEFT)
        self.steps_label = tk.Label(frame, text=self.moves, font=('Arial', 14))
        self.steps_label.pack(side=tk.LEFT, padx=10)
        
    def update_state_moves(self):
        self.steps_label.config(text=str(self.moves))

    def create_buttons(self):
        frame = tk.Frame(self.master)
        frame.pack()

        shuffle_button = tk.Button(frame, text="Mélanger", command=self.shuffle_board)
        shuffle_button.pack(side=tk.LEFT, padx=10)

        a_star_button = tk.Button(frame, text="A* Search", command=self.a_star_search)
        a_star_button.pack(side=tk.LEFT, padx=10)
        
        beam_search=tk.Button(frame, text="Beam Search", command=self.beam_search)
        beam_search.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame, text="Best First Search", command=self.best_first_search).pack(side=tk.LEFT, padx=5)

    def format_state(self, state):
        return "\n".join(" ".join(str(cell) for cell in row) for row in state)

    def shuffle_board(self):
        self.board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.empty_pos = (2, 2)
        for _ in range(100):
            neighbors = self.get_neighbors(self.board, self.empty_pos)
            self.board, self.empty_pos = random.choice(neighbors)
        self.initial_state = [row[:] for row in self.board]
        self.initial_label.config(text=self.format_state(self.initial_state))
        self.draw_board()

    def get_neighbors(self, state, empty_pos):
        neighbors = []
        x, y = empty_pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append((new_state, (nx, ny)))
        return neighbors
    
    def click_tile(self, event):
        x, y = event.x, event.y
        row, col = y // self.tile_size, x // self.tile_size
        self.move_tile(row, col)

    def move_tile(self, row, col):
        if (row, col) == self.empty_pos:
            return
        
        empty_row, empty_col = self.empty_pos
        
        if (abs(empty_row - row) == 1 and empty_col == col) or (abs(empty_col - col) == 1 and empty_row == row):
            self.board[empty_row][empty_col], self.board[row][col] = self.board[row][col], self.board[empty_row][empty_col]
            self.empty_pos = (row, col)
            self.draw_board()
            if self.check_victory():
                self.show_victory_message()

    
    
    def check_victory(self):
        return self.board == self.final_state

    def show_victory_message(self):
        tk.messagebox.showinfo("Victoire!", "Félicitations, vous avez résolu le puzzle!")
        
    def show_solution_path(self, path):
        solution_text = ""
        for i, node in enumerate(path):
            solution_text += f"move {i}\n{self.format_state(node.state)}\n\n"
        print("Chemin de la solution :\n\n", solution_text)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value != 0:
                    self.canvas.create_rectangle(j*self.tile_size, i*self.tile_size,
                                                 (j+1)*self.tile_size, (i+1)*self.tile_size,
                                                 fill="lightblue")
                    self.canvas.create_text(j*self.tile_size + self.tile_size/2,
                                            i*self.tile_size + self.tile_size/2,
                                            text=str(value), font=('Arial', 24))
        self.canvas.bind("<Button-1>", self.click_tile)

    def a_star_search(self):
        path, iterations = Solutions.a_star_search(self.initial_state, self.final_state)
        self.moves = 0
        if path:
            for node in path:
                self.board = node.state
                self.moves += 1
                self.draw_board()
                self.master.update()
                self.update_state_moves()
                time.sleep(0.5)
            print("________________________________________________________________________________________________________________________________")
            print("chemin A*")
            self.show_solution_path(path)
            print("________________________________________________________________________________________________________________________________")
            messagebox.showinfo("Success", f"A* found the solution in {iterations} iterations and {self.moves} moves.")
        else:
            messagebox.showinfo("Failure", "No solution found using A* Search.")
        self.steps_label.config(text=str(self.moves))
        
    def beam_search(self):
        path, iterations = Solutions.beam_search(self.initial_state, self.final_state, beam_width=2)
        self.moves = 0
        if path:
            for node in path:
                self.board = node.state
                self.moves += 1
                self.draw_board()
                self.steps_label.config(text=str(self.moves))
                self.master.update()
                self.update_state_moves()
                time.sleep(0.5)
            print("________________________________________________________________________________________________________________________________")
            print("chemin Beam Search")
            self.show_solution_path(path)
            print("________________________________________________________________________________________________________________________________")
            messagebox.showinfo("Success", f"Beam Search found the solution in {iterations} iterations and {self.moves} moves.")
        else:
            messagebox.showinfo("Failure", "No solution found using Beam Search.")
        self.steps_label.config(text=str(self.moves))
    
    def best_first_search(self):
        path, iterations = Solutions.best_first_search(self.initial_state, self.final_state)
        self.moves = 0
        if path:
            for node in path:
                self.board = node.state
                self.moves += 1
                self.draw_board()
                self.steps_label.config(text=str(self.moves))
                self.master.update()
                self.update_state_moves()
                time.sleep(0.5)
            print("________________________________________________________________________________________________________________________________")
            print("chemin best first search")
            self.show_solution_path(path)
            messagebox.showinfo("Success", f"Best First Search found the solution in {iterations} iterations and {self.moves} moves.")
            print("________________________________________________________________________________________________________________________________")
        else:
            messagebox.showinfo("Failure", "No solution found using Best First Search.")
        self.steps_label.config(text=str(self.moves))
