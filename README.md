# detection

Detection and parameter estimation of weak targets in radar and passive RF signals
as well as infrared image sequences, with small drones as the application case.

Core question: how much detection and estimation performance is lost the less is known about the signal, the noise and the target? And how much of it is recovered on real data when the model is estimated from the recordings?

Models, results and analysis for each part are in the respective README:
| Part | Content |
|---|---|
| [**RF Signal →**](rf/) | Linear chirp, matched filter, threshold detection with unknown delay |
| [**Image →**](image/) | Point target in images, 2D matched filter, detection with unknown position |

## Structure

```
rf/       radar signal model, matched filter, experiments
image/    infrared image model, 2D matched filter, experiments
figures/  generated plots
```
## Status
### Infrared
- [x] Simulated images: point target with Gaussian PSF in white Gaussian noise
- [x] 2D matched filter, threshold detection with unknown position
- [ ] Unknown target size: template mismatch, multiple template sizes
- [ ] Structured background and top-hat suppression
- [ ] Adaptive threshold (2D CFAR)
- [ ] Moving target and Kalman tracking
- [ ] Evaluation on the Anti-UAV410 dataset
### RF signals
- [x] Simulated receive window: point target with linear chirp in complex white Gaussian noise
- [x] Matched filter (pulse compression), threshold detection with unknown delay
- [ ] Adaptive threshold (CFAR)
- [ ] Unknown waveform: energy detector
- [ ] Moving target and Kalman tracking
- [ ] Evaluation on the TSMS-Drone dataset

## Run

Run from the repository root:

```
pip install numpy scipy matplotlib
python -m rf.hit_rate
python -m image.hit_rate
```
