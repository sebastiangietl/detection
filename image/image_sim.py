"""Synthetic infrared image: point target in noise."""

import numpy as np

def make_psf(shape, pos, psf_width):
    """Gaussian point spread function at a sub-pixel position"""
    rows, cols = np.indices(shape)
    r2 = (rows - pos[0])**2 + (cols - pos[1])**2
    p = np.exp(-r2 / (2 * psf_width**2))
    return p / np.linalg.norm(p)


def make_image(shape, pos, snr_lin, psf_width, rng, sigma=1.0):
    """Single image z = a * p(pos) + w"""
    a = np.sqrt(snr_lin) * sigma
    w = sigma * rng.standard_normal(shape)
    return a * make_psf(shape, pos, psf_width) + w


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    shape, pos = (128, 128), (64.0, 64.0)
    rng = np.random.default_rng(0)

    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    for axis, snr_db in zip(ax, [35, 20]):
        z = make_image(shape, pos, 10**(snr_db / 10), psf_width=2.5, rng=rng)
        axis.imshow(z, cmap="gray")
        axis.plot(pos[1], pos[0], "ro", mfc="none", ms=22)
        axis.set_title(f"SNR = {snr_db} dB", fontsize=9)
        axis.axis("off")
    plt.tight_layout()
    plt.show()
