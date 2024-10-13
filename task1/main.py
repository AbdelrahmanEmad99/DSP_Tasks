import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk, Button, Label, Entry, Toplevel
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def read_signal_from_file(file_name):
    indices, samples = [], []
    with open(file_name, 'r') as f:

        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            index, value = map(float, line.split())
            indices.append(int(index))
            samples.append(value)
            line = f.readline()
    return np.array(indices), np.array(samples)


def add_signals(signal1, signal2):
    indices1, samples1 = signal1
    indices2, samples2 = signal2

    all_indices = sorted(set(indices1).union(set(indices2)))

    samples1_dict = dict(zip(indices1, samples1))
    samples2_dict = dict(zip(indices2, samples2))

    result_samples = []

    for idx in all_indices:
        sample1 = samples1_dict.get(idx, 0)
        sample2 = samples2_dict.get(idx, 0)
        result_samples.append(sample1 + sample2)

    return np.array(all_indices), np.array(result_samples)


def subtract_signals(signal1, signal2):
    indices, samples = add_signals(signal1, multiply_signal(signal2, -1))
    return indices, samples


def multiply_signal(signal, constant):
    return signal[0], signal[1] * constant


def shift_signal(signal, k):
    indices = signal[0] - k
    return indices, signal[1]


def fold_signal(signal):
    indices = -signal[0]
    indices = np.flip(indices)

    return indices, tuple(np.flip(list(signal[1])))


def plot_signal_in_new_window(indices, samples, title="Signal"):
    new_window = Toplevel()
    new_window.title(title)

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.plot(indices, samples, marker='o')
    ax.set_title(title)
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Amplitude')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, new_window)
    toolbar.update()
    canvas.get_tk_widget().pack()

# GUI Setup
class DSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Signal Processor")

        self.label = Label(root, text="Digital Signal Processing Tasks", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.upload_button = Button(root, text="Upload Signal File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.add_button = Button(root, text="Add Signal", command=self.add_signals_gui, state=tk.DISABLED)
        self.add_button.pack(pady=10)

        self.subtract_button = Button(root, text="Subtract Signal", command=self.subtract_signals_gui, state=tk.DISABLED)
        self.subtract_button.pack(pady=10)

        self.multiply_button = Button(root, text="Multiply Signal by Constant", command=self.multiply_signal_gui, state=tk.DISABLED)
        self.multiply_button.pack(pady=10)

        self.shift_button = Button(root, text="Shift Signal (Delay/Advance)", command=self.shift_signal_gui, state=tk.DISABLED)
        self.shift_button.pack(pady=10)

        self.fold_button = Button(root, text="Fold/Reverse Signal", command=self.fold_signal_gui, state=tk.DISABLED)
        self.fold_button.pack(pady=10)

        self.indices = None
        self.samples = None

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.indices, self.samples = read_signal_from_file(file_path)
            plot_signal_in_new_window(self.indices, self.samples, title="Uploaded Signal")
            self.enable_buttons()

    def enable_buttons(self):
        self.add_button.config(state=tk.NORMAL)
        self.subtract_button.config(state=tk.NORMAL)
        self.multiply_button.config(state=tk.NORMAL)
        self.shift_button.config(state=tk.NORMAL)
        self.fold_button.config(state=tk.NORMAL)

    def add_signals_gui(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            second_indices, second_samples = read_signal_from_file(file_path)
            result_indices, result_samples = add_signals((self.indices, self.samples), (second_indices, second_samples))
            AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", result_indices, result_samples)  # Test case call
            plot_signal_in_new_window(result_indices, result_samples, title="Added Signal")

    def subtract_signals_gui(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            second_indices, second_samples = read_signal_from_file(file_path)
            result_indices, result_samples = subtract_signals((self.indices, self.samples), (second_indices, second_samples))
            SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", result_indices, result_samples)  # Test case call
            plot_signal_in_new_window(result_indices, result_samples, title="Subtracted Signal")

    def multiply_signal_gui(self):
        top = Toplevel(self.root)
        top.title("Multiply Signal")

        label = Label(top, text="Enter Constant Value:")
        label.pack(pady=5)

        constant_entry = Entry(top)
        constant_entry.pack(pady=5)

        def apply_multiply():
            constant = float(constant_entry.get())
            result_indices, result_samples = multiply_signal((self.indices, self.samples), constant)
            MultiplySignalByConst(constant, result_indices, result_samples)
            plot_signal_in_new_window(result_indices, result_samples, title=f"Signal Multiplied by {constant}")
            top.destroy()

        apply_button = Button(top, text="Apply", command=apply_multiply)
        apply_button.pack(pady=5)

    def shift_signal_gui(self):
        top = Toplevel(self.root)
        top.title("Shift Signal")

        label = Label(top, text="Enter Shift Value (k steps):")
        label.pack(pady=5)

        shift_entry = Entry(top)
        shift_entry.pack(pady=5)

        def apply_shift():
            k = int(shift_entry.get())
            result_indices, result_samples = shift_signal((self.indices, self.samples), k)
            ShiftSignalByConst(k, result_indices, result_samples)
            plot_signal_in_new_window(result_indices, result_samples, title=f"Signal Shifted by {k} Steps")
            top.destroy()

        apply_button = Button(top, text="Apply", command=apply_shift)
        apply_button.pack(pady=5)

    def fold_signal_gui(self):
        result_indices, result_samples = fold_signal((self.indices, self.samples))
        Folding(result_indices, result_samples)
        plot_signal_in_new_window(result_indices, result_samples, title="Folded/Reversed Signal")


######################## Test Case Integration Functions  ############################
def ReadSignalFile(file_name):
    return read_signal_from_file(file_name)

def AddSignalSamplesAreEqual(userFirstSignal, userSecondSignal, Your_indices, Your_samples):
    file_name = "add.txt"  # Adjust the path for your test
    expected_indices, expected_samples = ReadSignalFile(file_name)
    if len(expected_samples) != len(Your_samples):
        print("Addition Test failed: signal lengths differ")
        return
    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            print("Addition Test failed: indices differ")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) >= 0.01:
            print("Addition Test failed: values differ")
            return
    print("Addition Test passed")


def SubSignalSamplesAreEqual(userFirstSignal, userSecondSignal, Your_indices, Your_samples):
    if (userFirstSignal == 'Signal1.txt' and userSecondSignal == 'Signal2.txt'):
        file_name = "subtract.txt"  # write here the path of the subtract output file

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        print("Subtraction Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if (Your_indices[i] != expected_indices[i]):
            print("Subtraction Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Subtraction Test case failed, your signal have different values from the expected one")
            return
    print("Subtraction Test case passed successfully")


def MultiplySignalByConst(User_Const, Your_indices, Your_samples):
    if (User_Const == 5):
        file_name = "mul5.txt"  # write here the path of the mul5 output file

    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        print("Multiply by " + str(
            User_Const) + " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if (Your_indices[i] != expected_indices[i]):
            print("Multiply by " + str(
                User_Const) + " Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Multiply by " + str(
                User_Const) + " Test case failed, your signal have different values from the expected one")
            return
    print("Multiply by " + str(User_Const) + " Test case passed successfully")


def ShiftSignalByConst(Shift_value, Your_indices, Your_samples):
    if (Shift_value == 3):  # x(n+k)
        file_name = "advance3.txt"  # write here the path of delay3 output file
    elif (Shift_value == -3):  # x(n-k)
        file_name = "delay3.txt"  # write here the path of advance3 output file

    expected_indices, expected_samples = ReadSignalFile(file_name)
    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        print("Shift by " + str(
            Shift_value) + " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if (Your_indices[i] != expected_indices[i]):
            print("Shift by " + str(
                Shift_value) + " Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Shift by " + str(
                Shift_value) + " Test case failed, your signal have different values from the expected one")
            return
    print("Shift by " + str(Shift_value) + " Test case passed successfully")


def Folding(Your_indices,Your_samples):
    file_name = "folding.txt"  # write here the path of the folding output file
    expected_indices,expected_samples=ReadSignalFile(file_name)
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Folding Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Folding Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Folding Test case failed, your signal have different values from the expected one")
            return
    print("Folding Test case passed successfully")



# Main execution
if __name__ == "__main__":
    root = Tk()
    app = DSPApp(root)
    root.mainloop()
