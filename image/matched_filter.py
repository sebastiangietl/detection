"""Matched filter and threshold detector for a single target."""

import numpy as np
from scipy.stats import norm


def matched_filter(z, p):
    """Correlate the image with the psf at every position"""
    M1, M2 = z.shape
    N1, N2 = p.shape
    return np.array([[np.vdot(p, z[i:i + N1, j:j + N2])
                      for j in range(M2 - N2 + 1)]
                     for i in range(M1 - N1 + 1)])


def threshold(sigma, p_fa, K):
    """Detection threshold for GLRT"""
    return sigma**2 * norm.isf(p_fa /(2*K))**2


def detect(y, gamma):
    """Square-law detection with unknown position"""
    y2 = np.abs(y)**2
    pos = np.unravel_index(np.argmax(y2), y2.shape)
    return y2[pos] > gamma, pos

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    shape, pos0 = (128, 128), (64.0, 64.0)
    psf_width, sigma, p_fa = 2.5, 1.0, 1e-2
    rng = np.random.default_rng(3)

    # PSF template, unit energy
    h = int(np.ceil(4 * psf_width))
    rows, cols = np.indices((2 * h + 1, 2 * h + 1)) - h
    p = np.exp(-(rows**2 + cols**2) / (2 * psf_width**2))
    p = p / np.linalg.norm(p)

    # target as unit-energy PSF placed in the full image
    rows, cols = np.indices(shape)
    target = np.exp(-((rows - pos0[0])**2 + (cols - pos0[1])**2) / (2 * psf_width**2))
    target = target / np.linalg.norm(target)

    fig, ax = plt.subplots(2, 2, figsize=(8, 7))
    for row, snr_db in enumerate([16, 10]):
        z = np.sqrt(10**(snr_db / 10)) * sigma * target + sigma * rng.standard_normal(shape)
        y2 = np.abs(matched_filter(z, p))**2
        gamma = threshold(sigma, p_fa, y2.size)
        extent = (h - 0.5, h + y2.shape[1] - 0.5, h + y2.shape[0] - 0.5, h - 0.5)  # y in image coordinates

        # column 0: image before the matched filter
        ax[row, 0].imshow(z, cmap="gray")
        ax[row, 0].set_title(f"before MF: SNR {snr_db} dB", fontsize=9)

        # column 1: matched-filter output, red contour = threshold
        ax[row, 1].imshow(y2, cmap="gray", extent=extent)
        ax[row, 1].contour(y2, levels=[gamma], colors="red", linewidths=1, extent=extent, origin="upper")
        ax[row, 1].set_title(f"after MF: |y|$^2$, red = above threshold", fontsize=9)

        for a in ax[row]:
            a.plot(pos0[1], pos0[0], "o", mfc="none", mec="tab:blue", ms=18)
            a.set_xlim(0, shape[1] - 1)
            a.set_ylim(shape[0] - 1, 0)
            a.axis("off")

    fig.tight_layout()
    fig.savefig("figures/before_after_mf_image.png", dpi=150)
    plt.show()