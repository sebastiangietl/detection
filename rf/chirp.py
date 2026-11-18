"""Linear chirp pulse and simulated single-pulse receive window."""

import numpy as np


def make_chirp(B, T, fs):
    """Linear chirp in complex baseband"""
    n = round(T * fs)
    t = (np.arange(n) - (n - 1) / 2) / fs
    s = np.exp(1j * np.pi * (B / T) * t**2)
    return s / np.linalg.norm(s)


def make_rx_window(s, tau, snr_lin, fs, n_samples, rng, sigma=1.0):
    """Single-pulse receive window x = a * s(.- tau) + w"""
    if not np.isclose(np.linalg.norm(s), 1.0):
        raise ValueError("s must have unit energy")

    d = round(tau * fs)
    if d < 0 or d + len(s) > n_samples:
        raise ValueError("echo does not fit into the window")

    a = np.sqrt(snr_lin) * sigma * np.exp(2j * np.pi * rng.random())
    x = np.zeros(n_samples, dtype=complex)
    x[d:d + len(s)] = a * s

    w = sigma / np.sqrt(2) * (rng.standard_normal(n_samples) + 1j * rng.standard_normal(n_samples))
    return x + w, d




