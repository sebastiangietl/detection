"""P_D vs. SNR for the 2D matched-filter detector with unknown position"""

import numpy as np
import matplotlib.pyplot as plt

from image.image_sim import make_image
from image.matched_filter import matched_filter, detect, threshold

shape, pos0 = (128, 128), (64.0, 64.0)
psf_width = 2.5
p_fa = 1e-2
n_runs = 400

rng = np.random.default_rng(0)
background = np.zeros(shape)      


h = int(np.ceil(4 * psf_width))
rows, cols = np.indices((2 * h + 1, 2 * h + 1)) - h
p = np.exp(-(rows**2 + cols**2) / (2 * psf_width**2))
p = p / np.linalg.norm(p)

K = (shape[0] - p.shape[0] + 1) * (shape[1] - p.shape[1] + 1)    
gamma_0 = threshold(1.0, p_fa, K)
gamma_1= threshold(1.0, p_fa, 1)


r0, c0 = int(pos0[0]) - h, int(pos0[1]) - h  

snr_dbs = np.arange(6, 21)
p_d_known, p_d_unknown = [], []
for snr_db in snr_dbs:
    hits_known, hits_unknown = 0, 0
    for _ in range(n_runs):
        z = make_image(shape, pos0, 10**(snr_db/10), psf_width, rng)
        y = matched_filter(z, p)

        detected, _ = detect(y[r0, c0], gamma_1)
        hits_known += detected

        detected, (r, c) = detect(y, gamma_0)
        hits_unknown += detected and abs(r - r0) <= 2 and abs(c - c0) <= 2

    p_d_known.append(hits_known / n_runs)
    p_d_unknown.append(hits_unknown / n_runs)

fa_known, fa_unknown = 0, 0
for _ in range(10 * n_runs):
    z = make_image(shape, pos0, 0, psf_width, rng)
    y = matched_filter(z, p)
    fa_known += detect(y[r0, c0], gamma_1)[0]
    fa_unknown += detect(y, gamma_0)[0]
print(f"P_FA known   = {fa_known/(10*n_runs):.3f}   (should be about {p_fa})")
print(f"P_FA unknown = {fa_unknown/(10*n_runs):.3f}   (should be at most {p_fa})")

fig, ax = plt.subplots(figsize=(5, 3.5))
ax.plot(snr_dbs, p_d_known, "o-", label="position known")
ax.plot(snr_dbs, p_d_unknown, "o-", label="position unknown")
ax.set_xlabel("SNR after matched filter [dB]")
ax.set_ylabel("$P_D$")
ax.set_title(f"2D matched filter, $P_{{FA}}$ = {p_fa}")
ax.legend()
ax.grid(True)
fig.tight_layout()
fig.savefig("figures/pd_curve_image.png", dpi=150)
plt.show()