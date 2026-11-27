"""P_D vs. SNR for the 2D matched-filter detector: known and unknown position, without and with clouds"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from image.image_sim import make_image, make_textured_clouds, make_psf
from image.matched_filter import (matched_filter, detect, threshold,
                                  whitened_matched_filter, cfar, cfar_threshold)

shape, pos0 = (128, 128), (64.0, 64.0)
psf_width = 2.5
p_fa = 1e-2
n_runs = 400
guard, ref = 3, 17

rng = np.random.default_rng(0)
rng_bg = np.random.default_rng(1)


def make_background():
    b = make_textured_clouds((2 * shape[0], 2 * shape[1]), beta=3.7, contrast=50.0, cover=0.5,
                               softness=0.15, psf_width=psf_width, rng=rng_bg)
    return b[:shape[0], :shape[1]]


h = int(np.ceil(4 * psf_width))
p = make_psf((2 * h + 1, 2 * h + 1), (h, h), psf_width)
r0, c0 = int(pos0[0]) - h, int(pos0[1]) - h


K = (shape[0] - p.shape[0] + 1) * (shape[1] - p.shape[1] + 1)
gamma_0 = threshold(1.0, p_fa, K)
gamma_1 = threshold(1.0, p_fa, 1)

snr_dbs = np.arange(5, 41)
p_d_known, p_d_unknown = [], []
p_d_known_cfar, p_d_unknown_cfar = [], []


for snr_db in tqdm(snr_dbs, desc="P_D, no clouds"):
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


for snr_db in tqdm(snr_dbs, desc="P_D, clouds"):
    hits_known_cfar, hits_unknown_cfar = 0, 0
    for _ in range(n_runs):
        zb = make_image(shape, pos0, 10**(snr_db/10), psf_width, rng, b=make_background())
        t, G = whitened_matched_filter(zb, p)
        
        t_cfar = cfar(t, guard, ref)
        gamma_1_cfar, gamma_0_cfar = cfar_threshold(G, guard, ref, p_fa, K)

        detected, _ = detect(t_cfar[r0, c0], gamma_1_cfar)
        hits_known_cfar += detected

        detected, (r, c) = detect(t_cfar, gamma_0_cfar)
        hits_unknown_cfar += detected and abs(r - r0) <= 2 and abs(c - c0) <= 2

    p_d_known_cfar.append(hits_known_cfar / n_runs)
    p_d_unknown_cfar.append(hits_unknown_cfar / n_runs)


fa_known, fa_unknown = 0, 0
fa_known_cfar, fa_unknown_cfar = 0, 0
for _ in tqdm(range(10 * n_runs), desc="false alarms"):
    z = make_image(shape, pos0, 0, psf_width, rng)
    y = matched_filter(z, p)
    fa_known += detect(y[r0, c0], gamma_1)[0]
    fa_unknown += detect(y, gamma_0)[0]
    zb = make_image(shape, pos0, 0, psf_width, rng, b=make_background())
    t, G = whitened_matched_filter(zb, p)
    t_cfar = cfar(t, guard, ref)
    gamma_1_cfar, gamma_0_cfar = cfar_threshold(G, guard, ref, p_fa, K)
    fa_known_cfar += detect(t_cfar[r0, c0], gamma_1_cfar)[0]
    fa_unknown_cfar += detect(t_cfar, gamma_0_cfar)[0]


fig_white, ax_white = plt.subplots(figsize=(5, 3.5))
fk, fu = fa_known / (10 * n_runs), fa_unknown / (10 * n_runs)
white = snr_dbs <= 20
ax_white.plot(snr_dbs[white], np.array(p_d_known)[white], "o-", label=f"position known ($P_{{FA}}$ {fk:.3f})")
ax_white.plot(snr_dbs[white], np.array(p_d_unknown)[white], "o-", label=f"position unknown ($P_{{FA}}$ {fu:.3f})")
ax_white.set_xlabel("SNR after matched filter [dB]")
ax_white.set_ylabel("$P_D$")
ax_white.set_title(f"2D matched filter, $P_{{FA}}$ = {p_fa}")
ax_white.legend()
ax_white.grid(True)
fig_white.tight_layout()
fig_white.savefig("figures/pd_curve_image.png", dpi=150)


fig, ax = plt.subplots(figsize=(7, 4.5))
fk, fu = fa_known / (10 * n_runs), fa_unknown / (10 * n_runs)
ax.plot(snr_dbs, p_d_known, "k-", label=f"known, no clouds ($P_{{FA}}$ {fk:.3f})")
ax.plot(snr_dbs, p_d_unknown, "k--", label=f"unknown, no clouds ($P_{{FA}}$ {fu:.3f})")
fk, fu = fa_known_cfar / (10 * n_runs), fa_unknown_cfar / (10 * n_runs)
line, = ax.plot(snr_dbs, p_d_known_cfar, "o-", ms=4,
                label=f"known, clouds, prewhitening, CA-CFAR ($P_{{FA}}$ {fk:.3f})")
ax.plot(snr_dbs, p_d_unknown_cfar, "s--", ms=4, color=line.get_color(),
        label=f"unknown, clouds, prewhitening, CA-CFAR ($P_{{FA}}$ {fu:.3f})")
ax.set_xlabel("SNR after matched filter [dB]")
ax.set_ylabel("$P_D$")
ax.set_title(f"2D matched filter, target $P_{{FA}}$ = {p_fa}")
ax.grid(True)
ax.set_ylim(-0.03, 1.3)
ax.set_yticks(np.arange(0, 1.01, 0.2))

leg = ax.legend(fontsize=7, loc="upper center", ncol=2, framealpha=0.95)
legend_to_line = dict(zip(leg.get_lines(), ax.get_lines()))
for legline in legend_to_line:
    legline.set_picker(5)


def on_pick(event):
    """Toggle the visibility of the curve whose legend entry was clicked"""
    line = legend_to_line[event.artist]
    line.set_visible(not line.get_visible())
    event.artist.set_alpha(1.0 if line.get_visible() else 0.2)
    fig.canvas.draw()


fig.canvas.mpl_connect("pick_event", on_pick)
fig.tight_layout()
fig.savefig("figures/pd_curve_clouds.png", dpi=150, bbox_inches="tight")

plt.show()