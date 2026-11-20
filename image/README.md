# Infrared

## Model

$$z = a\,p(\theta) + w$$

Point target with Gaussian PSF $p$ at unknown position $\theta$, amplitude $a$, white Gaussian noise $w \sim \mathcal{N}(0, \sigma^2)$ per pixel. SNR $= a^2/\sigma^2$.

<img src="../figures/before_after_mf_image.png" width="550">

The target is invisible in the raw image. After the 2D matched filter it stands out;
red marks pixels above the detection threshold. At 10 dB the peak stays below it.

## Detection

<img src="../figures/pd_curve_image.png" width="450">

One decision per frame: maximum over all positions against a threshold set for
P_FA = 0.01 per frame, checked by Monte Carlo.

## Run

```
python -m ir.matched_filter   # before / after matched filter
python -m ir.hit_rate         # P_D vs. SNR
```
