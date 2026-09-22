
import numpy as np


def make_chirp(B, T, fs):
    """
    B : float
        Sweep bandwidth in Hz.
    T : float
        Pulse duration in s.
    fs : float
        Sampling rate in Hz.
     """
    n = int(round(T * fs))
    t = (np.arange(n) - (n - 1) / 2) / fs
    s = np.exp(1j * np.pi * (B / T) * t**2)
    return s / np.linalg.norm(s)


def make_rx_window(s, tau, snr_lin, fs, n_samples, rng, sigma=1.0):
    """Single-pulse receive window x = a * s(t - tau) + w.

    Parameters
    ----------
    s : ndarray of complex
        Transmit pulse with unit energy.
    tau : float
        Echo delay in s, rounded to the sample grid.
    snr_lin : float
        E_s / N_0, linear.
    fs : float
        Sampling rate in Hz.
    n_samples : int
        Window length in samples.
    rng : numpy.random.Generator
    sigma : float, optional
        Noise standard deviation, N_0 = sigma**2.

    """
    if not np.isclose(np.linalg.norm(s), 1.0):
        raise ValueError("s must have unit energy")

    d = int(round(tau * fs))
    if d < 0 or d + len(s) > n_samples:
        raise ValueError("echo does not fit into the window")

    a = np.sqrt(snr_lin) * sigma * np.exp(2j * np.pi * rng.random())  
    x = np.zeros(n_samples, dtype=complex)
    x[d:d + len(s)] = a * s

    
    w = sigma / np.sqrt(2) * (rng.standard_normal(n_samples) + 1j * rng.standard_normal(n_samples))
    return x + w, d


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    B, T, fs = 1e6, 100e-6, 4e6
    rng = np.random.default_rng(0)

    s = make_chirp(B, T, fs)
    print(f"len(s) = {len(s)}, energy = {np.linalg.norm(s)**2:.6f}")

    fig, ax = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
    for axis, snr_db in zip(ax, [25, 5]):
        snr = 10 ** (snr_db / 10)
        x, d = make_rx_window(s, tau=150e-6, snr_lin=snr, fs=fs,
                              n_samples=1024, rng=rng)
        axis.plot(np.abs(x), lw=0.7)
        axis.axvspan(d, d + len(s), alpha=0.15)
        axis.set_ylabel("|x|")
        axis.set_title(f"SNR = {10*np.log10(snr):.0f} dB", fontsize=9)
    ax[-1].set_xlabel("Sample")
    plt.tight_layout()
    plt.show()