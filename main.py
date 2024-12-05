import tkinter as tk
from tkinter import messagebox
import time  # To measure time taken to solve the puzzle

# Global variables to store the state of the game
moves = []  # List of moves (recorded as tuples)
pegs = {'A': [], 'B': [], 'C': []}  # State of the pegs
current_move_index = 0  # Index to track which move we are on
start_time = None  # Variable to store the start time


def move_disk(from_peg, to_peg, pegs, canvas):
    """Move the disk from one peg to another visually."""
    disk = pegs[from_peg].pop()  # Remove the disk from the source peg
    pegs[to_peg].append(disk)  # Add the disk to the destination peg

    # Redraw all pegs and disks after the move
    draw_pegs(pegs, canvas)


def draw_pegs(pegs, canvas):
    """Redraw the pegs and disks on the canvas."""
    canvas.delete("all")  # Clear the canvas

    # Coordinates for peg positions (x, y)
    peg_positions = {'A': (100, 300), 'B': (300, 300), 'C': (500, 300)}

    # Draw the 3 pegs
    for peg, (x, y) in peg_positions.items():
        canvas.create_line(x, y, x, y - 150, width=10, fill="black")

    # Draw the disks
    for peg, disks in pegs.items():
        x, y = peg_positions[peg]
        for i, disk in enumerate(disks):
            canvas.create_rectangle(x - (disk * 10), y - 20 * (i + 1), x + (disk * 10), y - 20 * i,
                                    fill="blue", outline="black")


def solve_tower_of_hanoi(n, from_peg, to_peg, aux_peg, pegs, moves):
    """Solve Tower of Hanoi recursively and record the moves."""
    if n == 1:
        moves.append((from_peg, to_peg))
    else:
        solve_tower_of_hanoi(n - 1, from_peg, aux_peg, to_peg, pegs, moves)
        moves.append((from_peg, to_peg))
        solve_tower_of_hanoi(n - 1, aux_peg, to_peg, from_peg, pegs, moves)


def start_game():
    """Start the Tower of Hanoi game and solve it step by step."""
    global moves, pegs, current_move_index, start_time
    try:
        # Get number of disks from the input field
        n = int(entry.get())
        if n <= 0:
            messagebox.showerror("Input Error", "Please enter a positive integer.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input. Please enter a valid number.")
        return

    # Initialize the pegs with disks (A has all disks, B and C are empty)
    pegs = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}

    # Clear the moves list and reset the current move index
    moves = []
    current_move_index = 0

    # Start the timer to calculate time taken
    start_time = time.time()

    # Solve the Tower of Hanoi puzzle and record the moves
    solve_tower_of_hanoi(n, 'A', 'C', 'B', pegs, moves)

    # Start the automatic move sequence
    show_move()

    # Update the time complexity and formula on the UI
    time_complexity_label.config(text=f"Time Complexity: O(2^{n} - 1)")


def show_move():
    """Display the current move and update the step counter."""
    global current_move_index, moves
    if current_move_index < len(moves):
        # Get the current move to perform
        from_peg, to_peg = moves[current_move_index]

        # Move the disk
        move_disk(from_peg, to_peg, pegs, canvas)

        # Update the move label to show which disk is moving
        move_label.config(text=f"Move disk from {from_peg} to {to_peg}")

        # Update the step counter label
        step_counter_label.config(text=f"Step {current_move_index + 1} of {len(moves)}")

        # Increment the move index to track the next move
        current_move_index += 1

        # After 1 second, call show_move again to continue to the next step
        root.after(1000, show_move)
    else:
        # Once all moves are complete, calculate the time taken
        end_time = time.time()
        time_taken = end_time - start_time

        # Update the time taken label
        time_taken_label.config(text=f"Time Taken: {time_taken:.2f} seconds")

        move_label.config(text="Puzzle solved!")


# Set up the main window
root = tk.Tk()
root.title("Tower of Hanoi")

# Frame for the user input and button
frame = tk.Frame(root)
frame.pack(pady=20)

# Label for instructions
label = tk.Label(frame, text="Enter the number of disks:")
label.grid(row=0, column=0)

# Entry field for number of disks
entry = tk.Entry(frame, width=5)
entry.grid(row=0, column=1)

# Button to start the game
start_button = tk.Button(frame, text="Start", command=start_game)
start_button.grid(row=0, column=2)

# Label to show the current move details
move_label = tk.Label(root, text="Click Start to begin")
move_label.pack(pady=10)

# Step counter label
step_counter_label = tk.Label(root, text="Step 0 of 0")
step_counter_label.pack(pady=5)

# Time taken label
time_taken_label = tk.Label(root, text="Time Taken: 0.00 seconds")
time_taken_label.pack(pady=5)

# Time complexity label
time_complexity_label = tk.Label(root, text="Time Complexity: O(2^n - 1)")
time_complexity_label.pack(pady=5)

# Canvas to draw the pegs and disks
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack()

# Start the Tkinter main loop
root.mainloop()
