# detection

Detection and parameter estimation of weak targets in radar and passive RF signals as well as infrared image sequences, with small drones as the application case.

Core question: how much detection and estimation performance is lost the less is known about the signal, the noise and the target?

## Result

![P_D vs SNR](figures/pd_curve.png)

Probability of detection vs. SNR for the matched-filter detector with unknown target delay,
one decision per receive window, false-alarm probability fixed at 0.01.

## Status

### Radar signals
- [x] Signal model: unit-energy linear chirp, single-pulse receive window with complex white Gaussian noise
- [x] Matched filter / pulse compression
- [ ] CFAR detection
- [ ] Kalman tracking of the target delay
- [ ] Blind detection without known waveform
- [ ] Validation on real drone RF recordings (TSMS-Drone)

### Infrared image sequences
- [x] Synthetic images: small target in structured background, known ground truth
- [ ] Background suppression (top-hat filtering)
- [ ] 2D matched filter for small targets, verified on synthetic data
- [ ] Kalman tracking of target position across frames
- [ ] Evaluation on the annotated Anti-UAV410 dataset

## Run

Run from the repository root:

```
pip install numpy scipy matplotlib
python -m rf.chirp          # plots two simulated receive windows
python -m rf.hit_rate       # P_D curve -> figures/pd_curve.png
python -m image.image_sim   # simulated infrared image at two SNRs
```
