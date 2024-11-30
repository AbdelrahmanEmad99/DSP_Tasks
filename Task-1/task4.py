import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

# Global variables for indices and signals
indices1 = []
signal1 = []
indices2 = []
signal2 = []

# Function to load signals
def load_signal(global_indices, global_signal):
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return

    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]

            # Skip the first two rows
            num_rows = int(lines[2])  # Third line contains number of rows
            indices = []
            samples = []
            for line in lines[3:]:  # From the fourth line
                index, value = map(float, line.split())
                indices.append(index)
                samples.append(value)

            global_indices.clear()
            global_indices.extend(indices)
            global_signal.clear()
            global_signal.extend(samples)

            messagebox.showinfo("Success", f"Signal loaded successfully from {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load signal: {e}")

# Function to read signal file for comparison
def read_signal_file(filepath):
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]

            # Skip the first two rows
            indices = []
            samples = []
            for line in lines[3:]:  # From the fourth line
                index, value = map(float, line.split())
                indices.append(index)
                samples.append(value)
            return indices, samples
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read comparison signal: {e}")
        return [], []

# Comparison function
def compare(your_indices, your_samples, filepath):
    expected_indices, expected_samples = read_signal_file(filepath)
    if len(expected_samples) != len(your_samples):
        print("Test failed: Signal lengths differ")
        return
    for i in range(len(your_indices)):
        if your_indices[i] != expected_indices[i]:
            print("Test failed: Indices differ")
            return
    for i in range(len(expected_samples)):
        if abs(expected_samples[i] - your_samples[i]) >= 0.01:
            print("Test failed: Values differ")
            return
    print("Test passed successfully !")

# Moving average
def moving_average(indices, signal, window_size):
    averaged_indices = indices[:len(signal) - window_size + 1]
    averaged_signal = []
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        averaged_signal.append(sum(window) / window_size)
    return averaged_indices, averaged_signal

# First derivative
def first_derivative(indices, signal):
    derivative_indices = indices[0:-1]
    derivative_signal = [signal[i] - signal[i - 1] for i in range(1, len(signal))]
    return derivative_indices, derivative_signal

# Second derivative
def second_derivative(indices, signal):
    derivative_indices = indices[0:-2]
    derivative_signal = [signal[i + 1] - 2 * signal[i] + signal[i - 1] for i in range(1, len(signal) - 1)]
    return derivative_indices, derivative_signal

# Convolution
def convolve_signals(indices1, signal1, indices2, signal2):
    result_signal = [0] * (len(signal1) + len(signal2) - 1)
    result_indices = [indices1[0] + indices2[0] + i for i in range(len(result_signal))]
    # Array Method
    for i in range(len(signal1)):
        for j in range(len(signal2)):
            result_signal[i + j] += signal1[i] * signal2[j]
    return result_indices, result_signal

# Plot signal
def plot_signal(indices, signal, title):
    plt.figure()
    plt.plot(indices, signal, marker="o")
    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid()
    plt.show()

# GUI functions
def on_moving_average():
    try:
        window_size = int(window_size_entry.get())
        if not signal1 or not indices1:
            raise ValueError("Signal1 not loaded")
        if window_size < 1:
            raise ValueError("Window size must be positive")
        averaged_indices, averaged_signal = moving_average(indices1, signal1, window_size)
        compare(averaged_indices, averaged_signal, 'MovingAvg_out1.txt' if window_size == 3 else 'MovingAvg_out2.txt')
        plot_signal(averaged_indices, averaged_signal, "Moving Average")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compute moving average: {e}")

def on_first_derivative():
    try:
        if not signal1 or not indices1:
            raise ValueError("Signal1 not loaded")
        derivative_indices, derivative_signal = first_derivative(indices1, signal1)
        compare(derivative_indices, derivative_signal, '1st_derivative_out.txt')
        plot_signal(derivative_indices, derivative_signal, "First Derivative")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compute first derivative: {e}")

def on_second_derivative():
    try:
        if not signal1 or not indices1:
            raise ValueError("Signal1 not loaded")
        derivative_indices, derivative_signal = second_derivative(indices1, signal1)
        compare(derivative_indices, derivative_signal, '2nd_derivative_out.txt')
        plot_signal(derivative_indices, derivative_signal, "Second Derivative")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compute second derivative: {e}")

def on_convolve():
    try:
        if not signal1 or not indices1 or not signal2 or not indices2:
            raise ValueError("Both signals must be loaded")
        convolution_indices, convolution_signal = convolve_signals(indices1, signal1, indices2, signal2)
        compare(convolution_indices, convolution_signal, 'Conv_output.txt')
        plot_signal(convolution_indices, convolution_signal, "Convolution of Signals")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compute convolution: {e}")

# Start GUI
def start_task():
    global signal1, signal2, indices1, indices2, window_size_entry

    # GUI setup
    root = tk.Tk()
    root.title("DSP Tasks GUI with Testing")

    # Buttons and input fields
    load_signal1_btn = tk.Button(root, text="Load Signal 1", command=lambda: load_signal(indices1, signal1))
    load_signal1_btn.pack(pady=5)

    load_signal2_btn = tk.Button(root, text="Load Signal 2", command=lambda: load_signal(indices2, signal2))
    load_signal2_btn.pack(pady=5)

    window_size_label = tk.Label(root, text="Window Size for Moving Average:")
    window_size_label.pack()
    window_size_entry = tk.Entry(root)
    window_size_entry.pack(pady=5)

    moving_avg_btn = tk.Button(root, text="Moving Average", command=on_moving_average)
    moving_avg_btn.pack(pady=5)

    first_derivative_btn = tk.Button(root, text="First Derivative", command=on_first_derivative)
    first_derivative_btn.pack(pady=5)

    second_derivative_btn = tk.Button(root, text="Second Derivative", command=on_second_derivative)
    second_derivative_btn.pack(pady=5)

    convolve_btn = tk.Button(root, text="Convolve Signals", command=on_convolve)
    convolve_btn.pack(pady=5)

    # Run GUI
    root.mainloop()
