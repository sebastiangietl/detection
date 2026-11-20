# Image

Small point target (Gaussian PSF) at unknown position in an image with white Gaussian noise.

## Matched filter in 2D

<img src="../figures/before_after_mf_image.png" width="550">

The target is invisible in the raw image. After the 2D matched filter it stands out;
red marks pixels above the detection threshold. At 10 dB the peak stays below it.

## Detection with unknown position

<img src="../figures/pd_curve_image.png" width="450">

One decision per frame: maximum over all positions against a Neyman–Pearson threshold.
P_FA = 0.01, checked by Monte Carlo.

## Run

```
python -m image.matched_filter   # before / after matched filter
python -m image.hit_rate      # P_D vs. SNR
```
