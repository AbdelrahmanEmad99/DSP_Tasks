import tkinter as tk

import task1
import task2
import task3
import task4
import task5


def open_task1():
    task1.start_task()

def open_task2():
    task2.start_task()

def open_task3():
    task3.start_task()

def open_task4():
    task4.start_task()

def open_task5():
    task5.start_task()

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

button4 = tk.Button(root, text="Open Task 4 (Convolution)", command=open_task4, width=25, height=2)
button4.pack(pady=10)

button5 = tk.Button(root, text="Fourier", command=open_task5, width=25, height=2)
button5.pack(pady=10)

# Run the main application loop
root.mainloop()
