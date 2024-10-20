import tkinter as tk
import task2

def open_task1():
    # Placeholder for task1
    print("Task 1 not implemented yet")

def open_task2():
    task2.start_task()

# Main Application Window
root = tk.Tk()
root.title("DSP Task Navigator")

# Labels and Buttons for Navigation
label = tk.Label(root, text="Select DSP Task", font=("Helvetica", 16))
label.pack(pady=20)

button1 = tk.Button(root, text="Open Task 1 (Signal Operations)", command=open_task1, width=25, height=2)
button1.pack(pady=10)

button2 = tk.Button(root, text="Open Task 2 (Signal Generation)", command=open_task2, width=25, height=2)
button2.pack(pady=10)

# Run the main application loop
root.mainloop()
