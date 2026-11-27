"""Matched filter and threshold detector for a single target."""

import numpy as np
from scipy.stats import norm, t as student_t
from scipy.signal import correlate
from scipy.ndimage import uniform_filter, gaussian_filter

def matched_filter(z, p):
    """Correlate the image with the psf at every position"""
    return correlate(z, p, mode="valid")


def threshold(sigma, p_fa, K):
    """Detection threshold """
    return sigma**2 * norm.isf(p_fa /(2*K))**2


def detect(y, gamma):
    """Square-law detection with unknown position"""
    y2 = np.abs(y)**2
    pos = np.unravel_index(np.argmax(y2), y2.shape)
    return y2[pos] > gamma, pos


def template_fft(p, shape):
    """FFT of the template, zero-padded to the image size and with its center moved to pixel (0, 0)"""
    h = p.shape[0] // 2
    p_full = np.zeros(shape)
    p_full[:p.shape[0], :p.shape[1]] = p
    return np.fft.fft2(np.roll(p_full, (-h, -h), axis=(0, 1)))


def estimate_spectrum(z, smooth=2.0, floor=1e-8):
    """Spectrum estimate from a single image: periodogram smoothed over neighboring frequencies.
    smooth: width of the Gaussian smoothing in frequency bins; floor: lower bound relative to the maximum"""
    S = gaussian_filter(np.abs(np.fft.fft2(z - z.mean()))**2 / z.size, smooth, mode="wrap")
    return np.maximum(S, floor * S.max())


def whitened_matched_filter(z, p, smooth=2.0, floor=1e-8):
    """Prewhitening + matched filter y = p^T C^-1 z, normalized to unit variance under H0, cropped to the valid size.
    p: template of size (2h+1)x(2h+1), centered; smooth, floor: passed to estimate_spectrum.
    Returns (y, G): filter output and its power spectrum G = |P|^2 / S under H0"""
    h = p.shape[0] // 2
    p_hat = template_fft(p, z.shape)
    S = estimate_spectrum(z, smooth, floor)
    y = np.real(np.fft.ifft2(np.fft.fft2(z - z.mean()) * np.conj(p_hat) / S))
    G = np.abs(p_hat)**2 / S  # power spectrum of y under H0
    return y[h:-h, h:-h] / np.sqrt(G.sum() / G.size), G


def cfar(y, guard, ref):
    """Local normalization (y - mean) / std, estimated on a square ring around each pixel.
    guard: half width of the inner square left out; ref: half width of the outer square"""
    n_out, n_in = (2 * ref + 1)**2, (2 * guard + 1)**2
    n = n_out - n_in
    s1 = uniform_filter(y, 2 * ref + 1) * n_out - uniform_filter(y, 2 * guard + 1) * n_in
    s2 = uniform_filter(y**2, 2 * ref + 1) * n_out - uniform_filter(y**2, 2 * guard + 1) * n_in
    mean = s1 / n
    std = np.sqrt(np.maximum(s2 / n - mean**2, 1e-12))
    return (y - mean) / std



def cfar_threshold(G, guard, ref, p_fa, K):
    """Analytic two-sided CFAR thresholds (gamma_1, gamma_0) on |t|^2 for known and unknown position, used with detect.
    G: power spectrum of y under H0 (|P|^2 / S); K: number of positions (Bonferroni).
    Student-t with effective ring size n_eff = n_ring^2 / sum(ring pairs * correlation of y)"""
    ring = np.zeros(G.shape)
    ring[:2 * ref + 1, :2 * ref + 1] = 1
    ring[ref - guard:ref + guard + 1, ref - guard:ref + guard + 1] = 0
    ring = np.roll(ring, (-ref, -ref), axis=(0, 1))  # ring centered at offset 0
    n_ring = ring.sum()
    ring_pairs = np.real(np.fft.ifft2(np.abs(np.fft.fft2(ring))**2))  # number of ring pairs with offset x
    rho = np.real(np.fft.ifft2(G))
    rho = rho / rho[0, 0]
    n_eff = n_ring**2 / np.sum(ring_pairs * rho)
    scale = np.sqrt(1 + 1 / n_eff)
    return (scale * student_t.isf(p_fa / 2, n_eff - 1))**2, (scale * student_t.isf(p_fa / (2 * K), n_eff - 1))**2


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from image.image_sim import make_psf

    shape, pos0 = (128, 128), (64.0, 64.0)
    psf_width, sigma, p_fa = 2.5, 1.0, 1e-2
    snr_db = 16
    rng = np.random.default_rng(3)

    h = int(np.ceil(4 * psf_width))
    p = make_psf((2 * h + 1, 2 * h + 1), (h, h), psf_width)

    # target as unit-energy PSF placed in the full image
    rows, cols = np.indices(shape)
    target = np.exp(-((rows - pos0[0])**2 + (cols - pos0[1])**2) / (2 * psf_width**2))
    target = target / np.linalg.norm(target)

    z = np.sqrt(10**(snr_db / 10)) * sigma * target + sigma * rng.standard_normal(shape)
    y2 = np.abs(matched_filter(z, p))**2
    gamma = threshold(sigma, p_fa, y2.size)
    extent = (h - 0.5, h + y2.shape[1] - 0.5, h + y2.shape[0] - 0.5, h - 0.5)  # y in image coordinates

    fig, ax = plt.subplots(1, 2, figsize=(8, 3.8))

    # left: image before the matched filter
    ax[0].imshow(z, cmap="gray")
    ax[0].set_title(f"before MF: SNR {snr_db} dB", fontsize=9)

    # right: matched-filter output, red contour = threshold
    ax[1].imshow(y2, cmap="gray", extent=extent)
    ax[1].contour(y2, levels=[gamma], colors="red", linewidths=1, extent=extent, origin="upper")
    ax[1].set_title("after MF: |y|$^2$, red = above threshold", fontsize=9)

    for a in ax:
        a.plot(pos0[1], pos0[0], "o", mfc="none", mec="tab:blue", ms=18)
        a.set_xlim(0, shape[1] - 1)
        a.set_ylim(shape[0] - 1, 0)
        a.axis("off")

    fig.tight_layout()
    fig.savefig("figures/before_after_mf_image.png", dpi=150)
    plt.show()