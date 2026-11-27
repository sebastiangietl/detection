"""Synthetic infrared image: point target in cloud background and noise."""

import numpy as np
from scipy.ndimage import gaussian_filter


def make_psf(shape, pos, psf_width):
    """Gaussian point spread function at a sub-pixel position"""
    rows, cols = np.indices(shape)
    r2 = (rows - pos[0])**2 + (cols - pos[1])**2
    p = np.exp(-r2 / (2 * psf_width**2))
    return p / np.linalg.norm(p)

def make_textured_clouds(shape, beta, contrast, cover, softness, psf_width, rng):
    """Cloud background: power-law textured field with soft cloud boundaries blurred by the PSF"""
    fy, fx = np.meshgrid(np.fft.fftfreq(shape[0]), np.fft.fftfreq(shape[1]), indexing="ij")
    f = np.hypot(fx, fy)
    f[0, 0] = np.inf
    u = np.real(np.fft.ifft2(np.fft.fft2(rng.standard_normal(shape)) * f**(-beta / 2)))
    u = (u - u.mean()) / u.std()
    tau = np.quantile(u, 1 - cover)
    s = 1 / (1 + np.exp(-(u - tau) / softness))
    b = contrast * s * (1 + 0.5 * (u - tau))
    return gaussian_filter(b, psf_width)


def make_image(shape, pos, snr_lin, psf_width, rng, sigma=1.0, b=0.0):
    """Single image z = a * p(pos) + b + w"""
    a = np.sqrt(snr_lin) * sigma
    w = sigma * rng.standard_normal(shape)
    return a * make_psf(shape, pos, psf_width) + b + w


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    shape, pos, snr_db, seed = (128, 128), (64.0, 64.0), 30, 4

    rng = np.random.default_rng(seed)
    b = make_textured_clouds((2 * shape[0], 2 * shape[1]), beta=3.7, contrast=50.0, cover=0.5,
                             softness=0.15, psf_width=2.5, rng=rng)[:shape[0], :shape[1]]
    z = make_image(shape, pos, 10**(snr_db / 10), psf_width=2.5, rng=rng, b=b)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(z, cmap="gray")
    ax.plot(pos[1], pos[0], "ro", mfc="none", ms=22)
    ax.set_title(f"Simulated image, SNR = {snr_db} dB", fontsize=9)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig("figures/simulated_image.png", dpi=150)
    plt.show()