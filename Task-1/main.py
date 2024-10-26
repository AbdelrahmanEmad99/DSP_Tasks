import tkinter as tk

import task1
import task2
import task3


def open_task1():
    task1.start_task()

def open_task2():
    task2.start_task()

def open_task3():
    task3.start_task()

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

button3 = tk.Button(root, text="Open Task 3 (Quantization)", command=open_task3, width=25, height=2)
button3.pack(pady=10)

# Run the main application loop
root.mainloop()
