import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk


# Signal generation function
def generate_signal(signal_type, amplitude, phase_shift, analog_frequency, sampling_frequency, duration=1):
    T = 1 / analog_frequency  # Period of the analog signal
    t = np.arange(0, duration, 1 / sampling_frequency)  # Time vector based on sampling frequency

    if signal_type == 'Sine':
        signal = amplitude * np.sin(2 * np.pi * analog_frequency * t + phase_shift)
    elif signal_type == 'Cosine':
        signal = amplitude * np.cos(2 * np.pi * analog_frequency * t + phase_shift)

    return t, signal


# Function to display the signal
def plot_signal(signal_type, amplitude, phase_shift, analog_frequency, sampling_frequency, is_discrete):
    t, signal = generate_signal(signal_type, amplitude, phase_shift, analog_frequency, sampling_frequency)

    plt.figure(figsize=(8, 6))
    if is_discrete:
        plt.stem(t, signal, label=f'{signal_type} Wave (Discrete)')
    else:
        plt.plot(t, signal, label=f'{signal_type} Wave (Continuous)')
    plt.title(f'{signal_type} Wave')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.show()


# Function to display two signals at the same time
def plot_two_signals(signal1_type, signal2_type, amplitude1, amplitude2, phase_shift1, phase_shift2, analog_frequency1,
                     analog_frequency2, sampling_frequency1, sampling_frequency2, is_discrete):
    t1, signal1 = generate_signal(signal1_type, amplitude1, phase_shift1, analog_frequency1, sampling_frequency1)
    t2, signal2 = generate_signal(signal2_type, amplitude2, phase_shift2, analog_frequency2, sampling_frequency2)

    plt.figure(figsize=(8, 6))
    if is_discrete:
        plt.stem(t1, signal1, label=f'{signal1_type} Wave 1 (Discrete)')
        plt.stem(t2, signal2, label=f'{signal2_type} Wave 2 (Discrete)', markerfmt='C1o')
    else:
        plt.plot(t1, signal1, label=f'{signal1_type} Wave 1 (Continuous)')
        plt.plot(t2, signal2, label=f'{signal2_type} Wave 2 (Continuous)', linestyle='--')

    plt.title(f'{signal1_type} and {signal2_type} Waves')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.show()


# UI elements to handle signal input
def display_signal():
    signal_type = signal_type_var.get()
    amplitude = float(amplitude_var.get())
    phase_shift = float(phase_shift_var.get())
    analog_frequency = float(analog_frequency_var.get())
    sampling_frequency = float(sampling_frequency_var.get())
    is_discrete = discrete_var.get()

    plot_signal(signal_type, amplitude, phase_shift, analog_frequency, sampling_frequency, is_discrete)


def display_two_signals():
    signal1_type = signal1_type_var.get()
    signal2_type = signal2_type_var.get()
    amplitude1 = float(amplitude1_var.get())
    amplitude2 = float(amplitude2_var.get())
    phase_shift1 = float(phase_shift1_var.get())
    phase_shift2 = float(phase_shift2_var.get())
    analog_frequency1 = float(analog_frequency1_var.get())
    analog_frequency2 = float(analog_frequency2_var.get())
    sampling_frequency1 = float(sampling_frequency1_var.get())
    sampling_frequency2 = float(sampling_frequency2_var.get())
    is_discrete = discrete_var.get()

    plot_two_signals(signal1_type, signal2_type, amplitude1, amplitude2, phase_shift1, phase_shift2, analog_frequency1,
                     analog_frequency2, sampling_frequency1, sampling_frequency2, is_discrete)


# Create the main window
root = Tk()
root.title('Signal Processing Framework')
root.geometry('400x450')

# Signal generation menu
Label(root, text="Signal Type").grid(row=0, column=0)
signal_type_var = StringVar()
signal_type_var.set('Sine')
signal_type_menu = ttk.Combobox(root, textvariable=signal_type_var)
signal_type_menu['values'] = ('Sine', 'Cosine')
signal_type_menu.grid(row=0, column=1)

Label(root, text="Amplitude").grid(row=1, column=0)
amplitude_var = StringVar(value='1')
Entry(root, textvariable=amplitude_var).grid(row=1, column=1)

Label(root, text="Phase Shift (radians)").grid(row=2, column=0)
phase_shift_var = StringVar(value='0')
Entry(root, textvariable=phase_shift_var).grid(row=2, column=1)

Label(root, text="Analog Frequency (Hz)").grid(row=3, column=0)
analog_frequency_var = StringVar(value='1')
Entry(root, textvariable=analog_frequency_var).grid(row=3, column=1)

Label(root, text="Sampling Frequency (Hz)").grid(row=4, column=0)
sampling_frequency_var = StringVar(value='10')
Entry(root, textvariable=sampling_frequency_var).grid(row=4, column=1)

# Checkbox for discrete representation
discrete_var = BooleanVar()
discrete_checkbox = Checkbutton(root, text="Display as Discrete", variable=discrete_var)
discrete_checkbox.grid(row=19, column=1)

Button(root, text="Display Signal", command=display_signal).grid(row=6, column=1)

# Two signal display section
Label(root, text="---- Compare Two Signals ----").grid(row=7, column=0, columnspan=2)

Label(root, text="Signal 1 Type").grid(row=8, column=0)
signal1_type_var = StringVar()
signal1_type_var.set('Sine')
signal1_type_menu = ttk.Combobox(root, textvariable=signal1_type_var)
signal1_type_menu['values'] = ('Sine', 'Cosine')
signal1_type_menu.grid(row=8, column=1)

Label(root, text="Signal 2 Type").grid(row=9, column=0)
signal2_type_var = StringVar()
signal2_type_var.set('Cosine')
signal2_type_menu = ttk.Combobox(root, textvariable=signal2_type_var)
signal2_type_menu['values'] = ('Sine', 'Cosine')
signal2_type_menu.grid(row=9, column=1)

Label(root, text="Amplitude 1").grid(row=10, column=0)
amplitude1_var = StringVar(value='1')
Entry(root, textvariable=amplitude1_var).grid(row=10, column=1)

Label(root, text="Amplitude 2").grid(row=11, column=0)
amplitude2_var = StringVar(value='1')
Entry(root, textvariable=amplitude2_var).grid(row=11, column=1)

Label(root, text="Phase Shift 1 (radians)").grid(row=12, column=0)
phase_shift1_var = StringVar(value='0')
Entry(root, textvariable=phase_shift1_var).grid(row=12, column=1)

Label(root, text="Phase Shift 2 (radians)").grid(row=13, column=0)
phase_shift2_var = StringVar(value='0')
Entry(root, textvariable=phase_shift2_var).grid(row=13, column=1)

Label(root, text="Analog Frequency 1 (Hz)").grid(row=14, column=0)
analog_frequency1_var = StringVar(value='1')
Entry(root, textvariable=analog_frequency1_var).grid(row=14, column=1)

Label(root, text="Analog Frequency 2 (Hz)").grid(row=15, column=0)
analog_frequency2_var = StringVar(value='1')
Entry(root, textvariable=analog_frequency2_var).grid(row=15, column=1)

Label(root, text="Sampling Frequency 1 (Hz)").grid(row=16, column=0)
sampling_frequency1_var = StringVar(value='10')
Entry(root, textvariable=sampling_frequency1_var).grid(row=16, column=1)

Label(root, text="Sampling Frequency 2 (Hz)").grid(row=17, column=0)
sampling_frequency2_var = StringVar(value='10')
Entry(root, textvariable=sampling_frequency2_var).grid(row=17, column=1)

Button(root, text="Display Two Signals", command=display_two_signals).grid(row=18, column=1)

# Run the main loop
root.mainloop()
