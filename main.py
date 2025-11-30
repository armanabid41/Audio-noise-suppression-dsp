import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import noisereduce as nr

def main():
    # 1. Load the Noisy File
    print("Loading audio file...")
    try:
        rate, noisy_data = wavfile.read("real_noise.wav")
    except FileNotFoundError:
        print("Error: 'real_noise.wav' not found! Please record it first.")
        return

    # Convert to mono if stereo (takes just one channel)
    if len(noisy_data.shape) > 1:
        noisy_data = noisy_data[:, 0]

    # 2. Perform Noise Reduction
    print("Reducing noise (this might take a few seconds)...")
    # stationary=True means it assumes the noise (like fan/hiss) is constant throughout
    cleaned_data = nr.reduce_noise(y=noisy_data, sr=rate, prop_decrease=0.90, stationary=True)

    # 3. Save the Cleaned File
    print("Saving output file...")
    wavfile.write("real_cleaned.wav", rate, cleaned_data)

    # 4. Visualization (Spectrogram)
    print("Generating spectrograms...")
    plt.figure(figsize=(12, 10))

    # Plot 1: Original Waveform
    plt.subplot(2, 2, 1)
    plt.title("Original Audio (Time Domain)")
    plt.plot(noisy_data, color='r', alpha=0.5)
    plt.grid()

    # Plot 2: Cleaned Waveform
    plt.subplot(2, 2, 2)
    plt.title("Cleaned Audio (Time Domain)")
    plt.plot(cleaned_data, color='g', alpha=0.7)
    plt.grid()

    # Plot 3: Original Spectrogram
    plt.subplot(2, 2, 3)
    plt.specgram(noisy_data, Fs=rate, NFFT=1024, noverlap=512, cmap='inferno')
    plt.title("Original Spectrogram (Bright = Noise)")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")

    # Plot 4: Cleaned Spectrogram
    plt.subplot(2, 2, 4)
    plt.specgram(cleaned_data, Fs=rate, NFFT=1024, noverlap=512, cmap='inferno')
    plt.title("Cleaned Spectrogram (Darker = Less Noise)")
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Time (s)")

    plt.tight_layout()
    plt.savefig("spectrogram_analysis.png") # Saves the image automatically
    print("Done! Image saved as 'spectrogram_analysis.png'")
    plt.show()

if __name__ == "__main__":
    main()