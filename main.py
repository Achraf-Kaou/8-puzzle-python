import tkinter as tk
import Puzzle


def main():
    root = tk.Tk()
    app = Puzzle.Puzzle(root)
    root.mainloop()

if __name__ == "__main__":
    main()