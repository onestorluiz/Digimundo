# Fallback implementation for librosa when not available
import numpy as np

class MockLibrosa:
    """Mock librosa implementation for audio processing fallback"""

    @staticmethod
    def load(file_path, sr=22050):
        """Mock audio loading - returns synthetic audio data"""
        # Generate synthetic audio data (sine wave)
        duration = 2.0  # 2 seconds
        t = np.linspace(0, duration, int(sr * duration))
        y = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        return y, sr

    @staticmethod
    def stft(y, hop_length=512, n_fft=2048):
        """Mock Short-Time Fourier Transform"""
        n_samples = len(y)
        n_frames = (n_samples - n_fft) // hop_length + 1
        n_freqs = n_fft // 2 + 1
        # Return random complex spectrogram
        return np.random.random((n_freqs, n_frames)) + 1j * np.random.random((n_freqs, n_frames))

    @staticmethod
    def istft(stft_matrix, hop_length=512):
        """Mock Inverse Short-Time Fourier Transform"""
        n_frames = stft_matrix.shape[1]
        n_samples = (n_frames - 1) * hop_length + 2048
        # Return synthetic audio
        return np.random.random(n_samples) * 0.1

    @staticmethod
    def feature_mfcc(y=None, sr=22050, n_mfcc=13):
        """Mock MFCC feature extraction"""
        if y is None:
            y = np.random.random(sr)  # 1 second of random audio

        n_frames = len(y) // 512
        return np.random.random((n_mfcc, n_frames))

    @staticmethod
    def feature_spectral_centroid(y=None, sr=22050):
        """Mock spectral centroid"""
        if y is None:
            y = np.random.random(sr)

        n_frames = len(y) // 512
        return np.random.random((1, n_frames)) * sr / 4

    @staticmethod
    def feature_spectral_rolloff(y=None, sr=22050):
        """Mock spectral rolloff"""
        if y is None:
            y = np.random.random(sr)

        n_frames = len(y) // 512
        return np.random.random((1, n_frames)) * sr / 2

    @staticmethod
    def feature_zero_crossing_rate(y):
        """Mock zero crossing rate"""
        n_frames = len(y) // 512
        return np.random.random((1, n_frames))

    @staticmethod
    def onset_detect(y=None, sr=22050):
        """Mock onset detection"""
        if y is None:
            y = np.random.random(sr)

        # Return random onset times
        n_onsets = np.random.randint(5, 20)
        return np.sort(np.random.random(n_onsets) * len(y) / sr)

    @staticmethod
    def tempo(y=None, sr=22050):
        """Mock tempo estimation"""
        return np.random.uniform(60, 180), np.array([120.0])  # BPM

    @staticmethod
    def beat_track(y=None, sr=22050):
        """Mock beat tracking"""
        if y is None:
            y = np.random.random(sr)

        tempo = 120.0
        beat_times = np.arange(0, len(y)/sr, 60.0/tempo)
        beat_frames = (beat_times * sr / 512).astype(int)

        return tempo, beat_frames

    @staticmethod
    def resample(y, orig_sr, target_sr):
        """Mock resampling"""
        ratio = target_sr / orig_sr
        new_length = int(len(y) * ratio)
        return np.interp(np.linspace(0, len(y)-1, new_length), np.arange(len(y)), y)

# Create the main librosa object
librosa = MockLibrosa()

# Create feature module
class FeatureModule:
    @staticmethod
    def mfcc(*args, **kwargs):
        return librosa.feature_mfcc(*args, **kwargs)

    @staticmethod
    def spectral_centroid(*args, **kwargs):
        return librosa.feature_spectral_centroid(*args, **kwargs)

    @staticmethod
    def spectral_rolloff(*args, **kwargs):
        return librosa.feature_spectral_rolloff(*args, **kwargs)

    @staticmethod
    def zero_crossing_rate(*args, **kwargs):
        return librosa.feature_zero_crossing_rate(*args, **kwargs)

# Create onset module
class OnsetModule:
    @staticmethod
    def onset_detect(*args, **kwargs):
        return librosa.onset_detect(*args, **kwargs)

# Create beat module
class BeatModule:
    @staticmethod
    def tempo(*args, **kwargs):
        return librosa.tempo(*args, **kwargs)

    @staticmethod
    def beat_track(*args, **kwargs):
        return librosa.beat_track(*args, **kwargs)

# Attach modules
librosa.feature = FeatureModule()
librosa.onset = OnsetModule()
librosa.beat = BeatModule()

# Core functions at module level
load = librosa.load
stft = librosa.stft
istft = librosa.istft
resample = librosa.resample