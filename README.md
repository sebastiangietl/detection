# detection

Detection and parameter estimation of weak targets in radar signals and infrared image sequences.

## Status

- [x] Signal model: unit-energy linear chirp, single-pulse receive window with complex white Gaussian noise
- [ ] Matched filter / pulse compression, verified against theory
- [ ] CFAR detection
- [ ] Kalman tracking of the target delay
- [ ] Direction-of-arrival estimation on a simulated array
- [ ] Image pipeline on the Anti-UAV410 dataset

## Run

    pip install numpy matplotlib
    python chirp.py
