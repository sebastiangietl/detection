# detection

Detection and parameter estimation of weak targets in radar and passive RF signals
as well as infrared image sequences, with small drones as the application case.

Core question: how much detection and estimation performance is lost the less is known
about the signal, the noise and the target?

| Part | Content |
|---|---|
| [**RF Signals →**](rf/) | Linear chirp, matched filter, threshold detection with unknown delay |
| [**Image →**](image/) | Point target in images, 2D matched filter, detection with unknown position |

## Structure

```
rf/       radar signal model, matched filter, experiments
image/    infrared image model, 2D matched filter, experiments
figures/  generated plots
```

## Run

Run from the repository root:

```
pip install numpy scipy matplotlib
python -m rf.hit_rate
python -m image.hit_rate
```
