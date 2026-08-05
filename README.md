# Data and code

This repository accompanies the manuscript *Gait Biomechanics with Portable EMG Biofeedback at Increasing Muscle-Activation Goals: Walking Speed, Propulsion, Braking, and Step Length*.

The `data` folder contains the deidentified analysis-ready data supporting the reported analyses. `primary_biomechanics.csv` contains participant-by-condition gait outcomes. The Delsys and synchronized mTrigger-Delsys files contain the EMG condition summaries and the 143 trial pairs used for the cross-system comparison. The remaining files contain force-time outcomes, normalized gait-cycle waveforms, force-window measures, and phase-specific ground-reaction-force values.

Twenty-four participants completed the protocol. The primary gait analysis used 23 participants. Right stance- and swing-time analyses used 22 participants, baseline waveform comparisons used 22 participants, and the synchronized mTrigger-Delsys analysis included 143 trials from 20 participants.

`code/force_windows.py` recalculates the reported force-window measures from `gait_cycle_waveforms.csv` and writes `force_window_metrics_recalculated.csv` in the data folder.

```text
python code/force_windows.py
```

The script requires NumPy and pandas.
