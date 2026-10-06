# TV Session Analytics

## Goal
Transform high-volume TV-session events into an analysis-ready model and quantify viewing behavior, session duration, peak-hour load, and channel performance.

## Business context
This is a portfolio reconstruction based on a project described on a resume. The original employer datasets are not included. This repository therefore uses synthetic data designed to reproduce the analytical problem without exposing confidential information.

## Method
1. Generate deterministic synthetic data with `generate_data.py`.
2. Run the analytical pipeline in `analysis.py`.
3. Review files in `outputs/`.
4. Replace the synthetic generator with approved real data if reproducing the workflow in an authorized environment.

## Reproducibility
```bash
python -m pip install -r requirements.txt
python generate_data.py
python analysis.py
```

## Important portfolio note
The numerical outputs produced here are synthetic demonstrations. They should not be represented as actual employer data or as independently verified historical business results.
