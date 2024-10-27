import math
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt


def QuantizationTest1(file_name, Your_EncodedValues, Your_QuantizedValues):
    expectedEncodedValues = []
    expectedQuantizedValues = []

    with open(file_name, 'r') as f:
        f.readline()  # Skip metadata
        f.readline()
        f.readline()
        line = f.readline()

        while line:
            L = line.strip()
            if len(L.split(' ')) == 2:
                L = line.split(' ')
                V2 = str(L[0])
                V3 = float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break

    if len(Your_EncodedValues) != len(expectedEncodedValues) or len(Your_QuantizedValues) != len(
            expectedQuantizedValues):
        print("QuantizationTest1 Test case failed: Different lengths from the expected output.")
        return

    tolerance = 0.01  # Define an error tolerance for floating-point comparisons
    for i in range(len(Your_EncodedValues)):
        if Your_EncodedValues[i] != expectedEncodedValues[i]:
            print("QuantizationTest1 Test case failed: Encoded values mismatch.")
            return

    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) > tolerance:
            print("QuantizationTest1 Test case failed: Quantized values mismatch.")
            return

    print("QuantizationTest1 Test case passed successfully.")


def QuantizationTest2(file_name, Your_IntervalIndices, Your_EncodedValues, Your_QuantizedValues, Your_SampledError):
    expectedIntervalIndices = []
    expectedEncodedValues = []
    expectedQuantizedValues = []
    expectedSampledError = []
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(' ')) == 4:
                L = line.split(' ')
                V1 = int(L[0])
                V2 = str(L[1])
                V3 = float(L[2])
                V4 = float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if (len(Your_IntervalIndices) != len(expectedIntervalIndices)
            or len(Your_EncodedValues) != len(expectedEncodedValues)
            or len(Your_QuantizedValues) != len(expectedQuantizedValues)
            or len(Your_SampledError) != len(expectedSampledError)):
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_IntervalIndices)):
        if (Your_IntervalIndices[i] != expectedIntervalIndices[i]):
            print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(Your_EncodedValues)):
        if (Your_EncodedValues[i] != expectedEncodedValues[i]):
            print(
                "QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one")
            return

    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print(
                "QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one")
            return
    for i in range(len(expectedSampledError)):
        if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one")
            return
    print("QuantizationTest2 Test case passed successfully")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    file_path_label.config(text=file_path)


def quantize_signal(run_test):
    try:
        num_bits = int(bits_entry.get()) if bits_entry.get() else None
        num_levels = int(levels_entry.get()) if levels_entry.get() else None

        if num_bits is not None:
            num_levels = 2 ** num_bits

        if num_levels is None:
            messagebox.showerror("Input Error", "Please enter either bits or levels.")
            return

        file_path = file_path_label.cget("text")
        if not file_path:
            messagebox.showerror("Input Error", "Please select an input file.")
            return

        with open(file_path, 'r') as f:
            f.readline()
            f.readline()
            f.readline()
            line = f.readline()

            signal_samples = []
            while line:
                try:
                    _, sample = line.split()
                    signal_samples.append(float(sample))
                    line = f.readline()
                except ValueError:
                    break

        min_val, max_val = min(signal_samples), max(signal_samples)
        step_size = (max_val - min_val) / num_levels

        quantized_values = []
        encoded_values = []
        quantization_errors = []

        decision_boundaries = [min_val + i * step_size for i in range(num_levels + 1)]
        reconstruction_levels = [min_val + (i + 0.5) * step_size for i in range(num_levels)]

        for sample in signal_samples:
            level = 0
            for i in range(num_levels):
                if decision_boundaries[i] <= sample < decision_boundaries[i + 1]:
                    level = i
                    break
            if sample >= decision_boundaries[-1]:
                level = num_levels - 1

            quantized_value = reconstruction_levels[level]
            quantization_error = quantized_value - sample

            if num_bits is not None:
                encoded = format(level, f'0{num_bits}b')
            else:
                encoded = format(level, f'0{int(math.log2(num_levels))}b')

            quantized_values.append(quantized_value)
            encoded_values.append(encoded)
            quantization_errors.append(quantization_error)


        intervalIndices = []
        for v in encoded_values:
            intervalIndices.append(int(v, 2) + 1)

        output_text.delete("1.0", "end")
        for i in range(len(encoded_values)):
            output_text.insert("end", f"{intervalIndices[i]} {encoded_values[i]} {quantized_values[i]:.2f} {quantization_errors[i]:.3f}\n")
        if run_test  == "test1":
            QuantizationTest1('Quan1_Out.txt', encoded_values, quantized_values)
        elif run_test == "test2":
            QuantizationTest2('Quan2_Out.txt', intervalIndices , encoded_values, quantized_values, quantization_errors)

        # Calculate and display cumulative average power error
        N = len(signal_samples)
        cumulative_avg_error = 0
        for i in range(N):
            cumulative_avg_error += quantization_errors[i] ** 2
        cumulative_avg_error /= N

        output_text.insert("end", f"\nFinal Average Power Error: {cumulative_avg_error:.8f}\n")

        plot_signals(signal_samples, quantized_values, quantization_errors)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def plot_signals(original, quantized, errors):
    plt.figure(figsize=(12, 8))

    # Plot original and quantized signals with stairs for quantized
    plt.subplot(2, 1, 1)
    plt.plot(original, label='Original Signal', color='blue')
    plt.step(range(len(quantized)), quantized, label='Quantized Signal', color='orange', linestyle='--', where='mid')
    plt.title("Original vs Quantized Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.legend()

    # Plot quantization error
    plt.subplot(2, 1, 2)
    plt.plot(errors, label='Quantization Error', color='red')
    plt.title("Quantization Error")
    plt.xlabel("Sample Index")
    plt.ylabel("Error (Original - Quantized)")
    plt.legend()

    plt.tight_layout()
    plt.show()


def start_task():
    global file_path_label, bits_entry, levels_entry, output_text

    root = tk.Tk()
    root.title("DSP Signal Quantizer")

    # Input Frame
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Enter Number of Bits:").grid(row=0, column=0, padx=5)
    bits_entry = tk.Entry(input_frame)
    bits_entry.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="Or Enter Number of Levels:").grid(row=1, column=0, padx=5)
    levels_entry = tk.Entry(input_frame)
    levels_entry.grid(row=1, column=1, padx=5)

    file_button = tk.Button(input_frame, text="Select Input File", command=open_file)
    file_button.grid(row=2, column=0, columnspan=2, pady=5)
    file_path_label = tk.Label(input_frame, text="", fg="blue")
    file_path_label.grid(row=3, column=0, columnspan=2)

    test1_button = tk.Button(input_frame, text="Run Quantization Test 1", command=lambda: quantize_signal("test1"))
    test1_button.grid(row=4, column=0, pady=10)

    test2_button = tk.Button(input_frame, text="Run Quantization Test 2", command=lambda: quantize_signal("test2"))
    test2_button.grid(row=4, column=1, pady=10)

    output_frame = tk.Frame(root)
    output_frame.pack(pady=10)

    tk.Label(output_frame, text="Quantized and Encoded Output:").grid(row=0, column=0)
    output_text = tk.Text(output_frame, height=10, width=40)
    output_text.grid(row=1, column=0, pady=5)

    root.mainloop()
