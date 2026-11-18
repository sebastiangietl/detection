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

# PSF template, unit energy
h = int(np.ceil(4 * psf_width))
rows, cols = np.indices((2 * h + 1, 2 * h + 1)) - h
p = np.exp(-(rows**2 + cols**2) / (2 * psf_width**2))
p = p / np.linalg.norm(p)

K = (shape[0] - p.shape[0] + 1) * (shape[1] - p.shape[1] + 1)    
gamma = threshold(1.0, p_fa, K)



snr_dbs = np.arange(6, 21)
p_d = []
for snr_db in snr_dbs:
    hits = 0
    for _ in range(n_runs):
        z = make_image(shape, pos0, 10**(snr_db/10),psf_width, rng)
        detected, (r, c) = detect(matched_filter(z, p), gamma)
        hits += detected and abs(r + h - pos0[0]) <= 2 and abs(c + h - pos0[1]) <= 2
    p_d.append(hits / n_runs)

false_alarms = 0
for _ in range(10 * n_runs):
    z = make_image(shape, pos0, 10**(snr_db/10),psf_width, rng)
    false_alarms += detect(matched_filter(z, p), gamma)[0]
print(f"P_FA = {false_alarms/(10*n_runs):.3f}   (should be at most {p_fa})")

fig, ax = plt.subplots(figsize=(5, 3.5))
ax.plot(snr_dbs, p_d, "o-")
ax.set_xlabel("SNR after matched filter [dB]")
ax.set_ylabel("$P_D$")
ax.set_title(f"2D matched filter, unknown position, $P_{{FA}}$ = {p_fa}")
ax.grid(True)
fig.tight_layout()
fig.savefig("figures/pd_curve_image.png", dpi=150)
plt.show()