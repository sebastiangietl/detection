"""Matched filter and threshold detector for a single target."""

import numpy as np


def matched_filter(r, s):
    """Correlate the receive window with the signal for every delay."""
    M = len(r)
    N = len(s)
    return np.array([np.vdot(s, r[d:d + N]) for d in range(M - N + 1)])


def threshold(sigma, p_fa, K):
    """Detection threshold for GLRT"""
    return -sigma**2 * np.log(p_fa / K)



def detect(y, gamma):
    """Square-law detection with unknown delay """
    y2 = np.abs(y)**2
    d_hat = np.argmax(y2)
    return y2[d_hat] > gamma, d_hat


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from rf.chirp import make_chirp, make_rx_window

    B, T, fs = 1e6, 100e-6, 4e6
    n_samples, tau = 1024, 150e-6
    sigma, p_fa = 1.0, 1e-2
    rng = np.random.default_rng(3)
    s = make_chirp(B, T, fs)

    fig, ax = plt.subplots(2, 2, figsize=(10, 5))
    for row, snr_db in enumerate([13, 5]):
        x, d = make_rx_window(s, tau, 10**(snr_db / 10), fs, n_samples, rng)
        y2 = np.abs(matched_filter(x, s))**2
        gamma = threshold(sigma, p_fa, len(y2))

        # column 0: receive window before the matched filter
        ax[row, 0].plot(np.abs(x), lw=0.6)
        ax[row, 0].axvspan(d, d + len(s), alpha=0.15)
        ax[row, 0].set_title(f"before MF: per-sample SNR "
                             f"{snr_db - 10 * np.log10(len(s)):.0f} dB", fontsize=9)

        # column 1: matched-filter output
        ax[row, 1].plot(y2, lw=0.8)
        ax[row, 1].axvline(d, ls="--", color="gray")
        ax[row, 1].axhline(gamma, color="red", ls=":", label="threshold γ")
        ax[row, 1].set_title(f"after MF: SNR {snr_db} dB", fontsize=9)
        ax[row, 1].legend(fontsize=8, loc="upper right")

    ax[1, 0].set_xlabel("Sample")
    ax[1, 1].set_xlabel("Delay d [samples]")
    fig.tight_layout()
    fig.savefig("figures/before_after_mf.png", dpi=150)
    plt.show()