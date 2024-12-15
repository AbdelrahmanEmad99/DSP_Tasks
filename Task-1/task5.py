import tkinter as tk
from tkinter import filedialog
import math
import matplotlib.pyplot as plt


# Test functions
def SignalComapreAmplitude(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    else:
        for i in range(len(SignalInput)):
            if abs(SignalInput[i] - SignalOutput[i]) > 0.001:
                return False
        return True


def SignalComaprePhaseShift(SignalInput=[], SignalOutput=[]):
    if len(SignalInput) != len(SignalOutput):
        return False
    else:
        for i in range(len(SignalInput)):
            A = round(SignalInput[i])
            B = round(SignalOutput[i])
            if abs(A - B) > 0.0001:
                return False
        return True


def dft(signal, sampling_frequency):
    N = len(signal)
    freq_amp_phase = []

    for k in range(N):
        real = 0
        imag = 0
        for n in range(N):
            real += signal[n] * math.cos(2 * math.pi * k * n / N)
            imag += signal[n] * math.sin(2 * math.pi * k * n / N) * -1
        amplitude = math.sqrt(real ** 2 + imag ** 2)
        phase = math.atan2(imag, real)
        freq_amp_phase.append((amplitude, phase))

    # Plot frequency vs amplitude and frequency vs phase
    frequencies = [k * (2* math.pi / (N* (1/sampling_frequency))) for k in range(N)]
    amplitudes = [amp for amp, _ in freq_amp_phase]
    phases = [phase for _, phase in freq_amp_phase]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(frequencies, amplitudes, 'b-o')
    plt.title("Frequency vs Amplitude")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")

    plt.subplot(1, 2, 2)
    plt.plot(frequencies, phases, 'r-o')
    plt.title("Frequency vs Phase")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (Radians)")

    plt.tight_layout()
    plt.show()

    return freq_amp_phase


def idft(freq_amp_phase):
    N = len(freq_amp_phase)
    signal = []

    for n in range(N):
        value = sum(
            amp * math.cos(2 * math.pi * k * n / N + phase)
            for k, (amp, phase) in enumerate(freq_amp_phase)
        ) / N
        signal.append(value)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(range(len(signal)), signal, 'b-o')
    plt.title("Frequency vs Amplitude")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()

    return signal


def load_reference_file(file_path, skip_lines, format_type):
    with open(file_path, 'r') as f:
        lines = f.readlines()[skip_lines:]
        if format_type == "DFT":
            return [tuple(map(float, line.split())) for line in lines]
        elif format_type == "IDFT":
            return [float(line.split()[1]) for line in lines]


def handle_dft(sampling_freq_entry):
    input_file_path = filedialog.askopenfilename(title="Select Input File for DFT")
    if not input_file_path:
        return

    ref_file_path = filedialog.askopenfilename(title="Select Reference File for DFT Output Comparison")
    if not ref_file_path:
        return

    # Read the input signal
    with open(input_file_path, 'r') as f:
        lines = f.readlines()[3:]  # Skip the first three rows
        signal = [float(line.split()[1]) for line in lines]

    try:
        sampling_frequency = float(sampling_freq_entry.get())
    except ValueError:
        print("Invalid sampling frequency. Please enter a numeric value.")
        return

    # Perform DFT
    freq_amp_phase = dft(signal, sampling_frequency)

    # Load reference data
    ref_data = load_reference_file(ref_file_path, 3, "DFT")
    ref_amplitudes = [amp for amp, _ in ref_data]
    ref_phases = [phase for _, phase in ref_data]

    # Extract DFT amplitudes and phases
    amplitudes = [amp for amp, _ in freq_amp_phase]
    phases = [phase for _, phase in freq_amp_phase]

    print("output of DFT amplitude and phase shift: " , freq_amp_phase)

    # Run tests
    if SignalComapreAmplitude(ref_amplitudes, amplitudes):
        print("DFT Amplitude Test Passed!")
    else:
        print("DFT Amplitude Test Failed.")

    if SignalComaprePhaseShift(ref_phases, phases):
        print("DFT Phase Shift Test Passed!")
    else:
        print("DFT Phase Shift Test Failed.")


def handle_idft():
    input_file_path = filedialog.askopenfilename(title="Select Input File for IDFT")
    if not input_file_path:
        return

    ref_file_path = filedialog.askopenfilename(title="Select Reference File for IDFT Output Comparison")
    if not ref_file_path:
        return

    # Load input frequency domain data
    freq_amp_phase = load_reference_file(input_file_path, 3, "DFT")

    # Perform IDFT
    reconstructed_signal = idft(freq_amp_phase)

    # Load reference data
    ref_signal = load_reference_file(ref_file_path, 3, "IDFT")

    print("output of IDFT amplitude" , reconstructed_signal)

    # Run tests
    if SignalComapreAmplitude(ref_signal, reconstructed_signal):
        print("IDFT Amplitude Test Passed!")
    else:
        print("IDFT Amplitude Test Failed.")


# GUI setup
def start_task():
    root = tk.Tk()
    root.title("DSP DFT and IDFT")

    # Sampling frequency input
    tk.Label(root, text="Sampling Frequency (Hz):").pack(pady=5)
    sampling_freq_entry = tk.Entry(root)
    sampling_freq_entry.pack(pady=5)

    # Buttons for DFT and IDFT
    btn_dft = tk.Button(root, text="DFT", command=lambda: handle_dft(sampling_freq_entry))
    btn_dft.pack(pady=10)

    btn_idft = tk.Button(root, text="IDFT", command=handle_idft)
    btn_idft.pack(pady=10)

    root.mainloop()
