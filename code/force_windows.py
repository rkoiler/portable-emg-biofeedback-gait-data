from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def values(frame, column, start, end):
    section = frame.loc[frame["gait_cycle_pct"].between(start, end)]
    section = section.sort_values("gait_cycle_pct")
    return section["gait_cycle_pct"].to_numpy(float), section[column].to_numpy(float)


def main():
    waveforms = pd.read_csv(DATA / "gait_cycle_waveforms.csv")
    rows = []

    group_columns = ["subject_id", "condition", "goal_percent", "side"]
    for (subject, condition, goal, side), frame in waveforms.groupby(group_columns, sort=False):
        frame = frame.sort_values("gait_cycle_pct").copy()
        frame["ml_outward"] = -frame["mlgrf_norm_mean"] if side == "R" else frame["mlgrf_norm_mean"]

        _, ml_early = values(frame, "ml_outward", 5, 25)
        _, ap_brake = values(frame, "apgrf_norm_mean", 5, 25)
        _, ap_prop = values(frame, "apgrf_norm_mean", 35, 60)
        x_v_impact, v_impact = values(frame, "vgrf_norm_mean", 0, 15)
        x_v_first, v_first = values(frame, "vgrf_norm_mean", 5, 25)
        _, v_mid = values(frame, "vgrf_norm_mean", 20, 40)
        x_v_second, v_second = values(frame, "vgrf_norm_mean", 35, 55)

        first_peak = int(np.nanargmax(v_first))
        second_peak = int(np.nanargmax(v_second))
        rows.append(
            {
                "subject_id": int(subject),
                "condition": condition,
                "goal_percent": int(goal),
                "side": side,
                "ml_outward_peak_5_25": float(np.nanmax(ml_early)),
                "ap_braking_peak_5_25": float(np.nanmin(ap_brake)),
                "ap_propulsion_peak_35_60": float(np.nanmax(ap_prop)),
                "vertical_impact_peak_0_15": float(np.nanmax(v_impact)),
                "vertical_loading_slope_nbw_per_pct_0_15": float(
                    np.nanmax(np.gradient(v_impact, x_v_impact))
                ),
                "vertical_first_peak_5_25": float(np.nanmax(v_first)),
                "vertical_first_peak_timing_pct_5_25": float(x_v_first[first_peak]),
                "vertical_midstance_minimum_20_40": float(np.nanmin(v_mid)),
                "vertical_second_peak_35_55": float(np.nanmax(v_second)),
                "vertical_second_peak_timing_pct_35_55": float(x_v_second[second_peak]),
            }
        )

    output = DATA / "force_window_metrics_recalculated.csv"
    pd.DataFrame(rows).to_csv(output, index=False)
    print(output)


if __name__ == "__main__":
    main()
