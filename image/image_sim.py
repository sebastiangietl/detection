"""Synthetic infrared image: point target in cloud background and noise."""

import numpy as np
from scipy.ndimage import gaussian_filter


def make_psf(shape, pos, psf_width):
    """Gaussian point spread function at a sub-pixel position"""
    rows, cols = np.indices(shape)
    r2 = (rows - pos[0])**2 + (cols - pos[1])**2
    p = np.exp(-r2 / (2 * psf_width**2))
    return p / np.linalg.norm(p)


def make_cloud_patches(shape, corr_len, contrast, fill, psf_width, rng):
    """Cloud background: bright patches with sharp edges, blurred by the PSF"""
    field = gaussian_filter(rng.standard_normal(shape), corr_len)
    mask = field > np.quantile(field, 1 - fill)
    return gaussian_filter(contrast * mask.astype(float), psf_width)


def make_image(shape, pos, snr_lin, psf_width, rng, sigma=1.0, b=0.0):
    """Single image z = a * p(pos) + b + w"""
    a = np.sqrt(snr_lin) * sigma
    w = sigma * rng.standard_normal(shape)
    return a * make_psf(shape, pos, psf_width) + b + w


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    shape, pos, snr_db, seed = (128, 128), (64.0, 64.0), 20, 4

    rng = np.random.default_rng(seed)
    b = make_cloud_patches(shape, corr_len=12.0, contrast=5.0, fill=0.5,
                           psf_width=2.5, rng=rng)
    z = make_image(shape, pos, 10**(snr_db / 10), psf_width=2.5, rng=rng, b=b)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(z, cmap="gray")
    ax.plot(pos[1], pos[0], "ro", mfc="none", ms=22)
    ax.set_title(f"Simulated image, SNR = {snr_db} dB", fontsize=9)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig("figures/simulated_image.png", dpi=150)
    plt.show()