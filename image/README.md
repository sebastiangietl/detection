# Infrared

## Model

$$z = a \cdot p(\theta) + b + w$$

Point target with Gaussian PSF $p$ at unknown position $\theta$, amplitude $a$, structured background $b$, white Gaussian noise $w \sim \mathcal{N}(0, \sigma^2 I)$. Unknown noise level and target motion are added step by step.

The background models clouds as bright patches with soft edges and internal texture, blurred by the same PSF as the target:

```math
b = p \ast \left(c \cdot s \cdot \left(1 + \tfrac{1}{2}(u - \tau)\right)\right), \qquad s = \frac{1}{1 + e^{-(u - \tau)/\kappa}}
```

The cloud field $u$ is Gaussian noise $n$ with a power-law spectrum, normalized to zero mean and unit variance:

```math
u = \mathcal{F}^{-1}\left[\, |f|^{-\beta/2} \, \mathcal{F}[n] \,\right]
```

with spectral exponent $\beta$ (larger $\beta$: smoother clouds), contrast $c$, edge softness $\kappa$ and threshold $\tau$, chosen as a quantile of $u$ so that a given fraction of the image is covered by clouds. The field is generated at twice the image size and cropped, so the background is not periodic. Parameters: $\beta = 3.7$, $c = 50\,\sigma$, cloud cover $0.5$, $\kappa = 0.15$.

<img src="../figures/simulated_image.png" width="350">

Simulated image at SNR = 30 dB, the red circle marks the target.
## Detection
<img src="../figures/pd_curve_image.png" width="450">

Detection without background ($b = 0$). With known position, the matched-filter output |y|² at the true position is compared against the Neyman–Pearson threshold. With unknown position, the GLRT is used.

## Run

```
python -m ir.matched_filter   # before / after matched filter
python -m ir.hit_rate         # P_D vs. SNR
```
