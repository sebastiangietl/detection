# RF Signal

Single-pulse radar: a linear chirp is sent, the echo arrives with unknown delay
and unknown phase in complex white Gaussian noise.

## Pulse compression

<img src="../figures/before_after_mf.png" width="650">

The echo is buried in noise per sample. The matched filter collects the energy
of all 400 samples into one peak (+26 dB).

## Detection with unknown delay

<img src="../figures/pd_curve.png" width="450">

One decision per receive window: maximum of |y|² over all 625 delays against a
Neyman–Pearson threshold. P_FA = 0.01, checked by Monte Carlo.

## Status

- [x] Signal model: unit-energy linear chirp, complex white Gaussian noise
- [x] Matched filter / pulse compression
- [x] Threshold detection with unknown delay
- [ ] CFAR detection (unknown noise level)
- [ ] Range estimation error vs. SNR
- [ ] Kalman tracking of a moving target

## Run

```
python -m rf.matched_filter   # before / after matched filter
python -m rf.hit_rate         # P_D vs. SNR
```
