"""P_D vs. SNR for the matched-filter detector with unknown delay,
one decision per receive window; checks the false-alarm rate."""

import numpy as np
import matplotlib.pyplot as plt

from chirp import make_chirp, make_rx_window
from matched_filter import matched_filter, detect

B, T, fs = 1e6, 100e-6, 4e6
n_samples, tau = 1024, 150e-6
p_fa = 1e-2            
n_runs = 400

rng = np.random.default_rng(0)
s = make_chirp(B, T, fs)

snr_dbs = np.arange(0, 17)        
p_d = []                          
for snr_db in snr_dbs:
    hits = 0
    for _ in range(n_runs):
        x, d0 = make_rx_window(s, tau, 10**(snr_db/10), fs, n_samples, rng)
        detected, d_hat = detect(matched_filter(x, s), 1.0, p_fa)
        hits += detected and abs(d_hat - d0) <= 2
    p_d.append(hits / n_runs)
    #print(f"SNR {snr_db:>2} dB   P_D = {hits/n_runs:.2f}")

false_alarms = 0
for _ in range(10 * n_runs):
    x, _ = make_rx_window(s, tau, 0, fs, n_samples, rng)
    false_alarms += detect(matched_filter(x, s), 1.0, p_fa)[0]
print(f"P_FA = {false_alarms/(10*n_runs):.3f}   (should be at most {p_fa})")

plt.plot(snr_dbs, p_d, "o-")
plt.xlabel("SNR [dB]")
plt.ylabel("$P_D$")
plt.title(f"Matched filter, unknown delay, $P_{{FA}}$ = {p_fa}")
plt.grid(True)
plt.savefig("figures/pd_curve.png", dpi=150)
plt.show()