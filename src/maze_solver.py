import tkinter as tk
import random
import heapq

# Constants for maze size and cell size
MAZE_SIZE = 15
CELL_SIZE = 30
WIDTH = MAZE_SIZE * CELL_SIZE
HEIGHT = MAZE_SIZE * CELL_SIZE
START = (0, 0)
END = (MAZE_SIZE - 1, MAZE_SIZE - 1)

# Create a maze with a known path
maze = [[0] * MAZE_SIZE for _ in range(MAZE_SIZE)]
path = [(x, 0) for x in range(MAZE_SIZE)]
path.extend((MAZE_SIZE - 1, y) for y in range(1, MAZE_SIZE))
path.extend((x, MAZE_SIZE - 1) for x in range(1, MAZE_SIZE))

# Randomly add walls
for y in range(MAZE_SIZE):
    for x in range(MAZE_SIZE):
        if (x, y) not in path and random.random() < 0.3:
            maze[y][x] = 1

# Initialize variables to store the user-drawn path and user finished flag
user_path = []
user_finished = False

def create_maze_solver():
    root = tk.Tk()
    root.title("Maze Solver")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    def reset_maze():
        global maze, user_path, user_finished
        maze = generate_random_maze()
        user_path = []  # Clear user-drawn path
        user_finished = False
        clear_solution()  # Clear the solution
        draw_maze()

    def generate_random_maze():
        maze = [[0] * MAZE_SIZE for _ in range(MAZE_SIZE)]
        for y in range(MAZE_SIZE):
            for x in range(MAZE_SIZE):
                if (x, y) not in path and random.random() < 0.3:
                    maze[y][x] = 1
        return maze

    def draw_maze():
        canvas.delete("all")
        for y in range(MAZE_SIZE):
            for x in range(MAZE_SIZE):
                if (x, y) == START:
                    color = "green"
                elif (x, y) == END:
                    color = "red"
                elif maze[y][x] == 1:
                    color = "black"
                else:
                    color = "white"
                canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill=color, outline="gray"
                )
        # Draw the user-drawn path
        for i in range(1, len(user_path)):
            x1, y1 = user_path[i - 1]
            x2, y2 = user_path[i]
            canvas.create_line(
                x1 * CELL_SIZE + CELL_SIZE // 2, y1 * CELL_SIZE + CELL_SIZE // 2,
                x2 * CELL_SIZE + CELL_SIZE // 2, y2 * CELL_SIZE + CELL_SIZE // 2, fill="blue", width=3
            )

    def solve_maze(user_finished):
        def shortest_path(maze):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            visited = set()
            start = START
            end = END
            heap = [(0, start, [start])]
            while heap:
                (cost, current, path) = heapq.heappop(heap)
                if current == end:
                    return path
                if current in visited:
                    continue
                visited.add(current)
                for direction in directions:
                    x, y = current
                    next_x, next_y = x + direction[0], y + direction[1]
                    if 0 <= next_x < MAZE_SIZE and 0 <= next_y < MAZE_SIZE and maze[next_y][next_x] == 0:
                        heapq.heappush(heap, (cost + 1, (next_x, next_y), path + [(next_x, next_y)]))
            return None

        if not user_finished:
            user_finished = True
            clear_solution()  # Clear the previous solution
            draw_maze()
            shortest = shortest_path(maze)
            if shortest:
                for x, y in shortest:
                    canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="green"
                    )

            if len(user_path) == len(shortest):
                response = "Congratulations! You've finished the maze!"
            else:
                response = "You've finished, but there might be a shorter path."

            canvas.create_text(WIDTH // 2, HEIGHT // 2, text=response, font=("Helvetica", 14), fill="blue")

    def clear_solution():
        # Remove the green solution path and user response
        for item in canvas.find_all():
            tags = canvas.gettags(item)
            if "green" in tags or "blue" in tags:
                canvas.delete(item)

    def on_canvas_click(event):
        if not user_finished:
            # Calculate the cell coordinates based on the click position
            x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
            if 0 <= x < MAZE_SIZE and 0 <= y < MAZE_SIZE:
                if not user_path:
                    user_path.append((x, y))
                else:
                    last_x, last_y = user_path[-1]
                    if (x == last_x and abs(y - last_y) == 1) or (y == last_y and abs(x - last_x) == 1):
                        if maze[y][x] == 0:  # Check if the cell is not a black wall
                            user_path.append((x, y))
                            draw_maze()

    def on_canvas_drag(event):
        if not user_finished:
            on_canvas_click(event)


    # Bind the mouse click and drag events
    canvas.bind("<Button-1>", on_canvas_click)
    canvas.bind("<B1-Motion>", on_canvas_drag)

    draw_maze()

    solve_button = tk.Button(root, text="Solve Maze", command=lambda: solve_maze(user_finished))
    solve_button.pack()

    reset_button = tk.Button(root, text="Reset Maze", command=reset_maze)
    reset_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_maze_solver()