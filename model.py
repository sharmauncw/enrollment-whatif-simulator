"""Projection math for the enrollment what-if simulator.

Pure functions (no Streamlit dependency) so the model can be unit-tested.

ALL inputs and outputs are SYNTHETIC demo values. The model is a simplified
teaching tool, not a real institutional forecast.

Model (per projected year t):
    new_students[t] = freshman_target + transfers_per_year
    headcount[t] = headcount[t-1] * retention + new_students[t]
    fte[t] = headcount[t] * fte_factor
    sticker[t] = sticker[t-1] * (1 + sticker_growth)
    net_revenue[t] = headcount[t] * sticker[t] * (1 - discount_rate)

Key assumptions (stated in the app UI too):
  * One blended retention rate is applied to total headcount; graduation is
    folded into the non-retained outflow rather than modeled by cohort.
  * Discount rate is applied uniformly to sticker tuition.
  * Summer melt is folded into the yield lever: admits_required =
    freshman_target / yield.
"""
import pandas as pd


def project_enrollment(baseline, levers, years=5):
    """Project headcount and net tuition revenue.

    baseline: dict with total_headcount, transfers_per_year, sticker,
              fte_factor, sticker_growth
    levers: dict with yield_pct, retention_pct, discount_pct,
              freshman_target
    returns: pandas DataFrame, one row per projected year.
    """
    retention = levers["retention_pct"] / 100.0
    discount = levers["discount_pct"] / 100.0

    rows = []
    headcount = float(baseline["total_headcount"])
    sticker = float(baseline["sticker"])
    for t in range(1, years + 1):
        new_students = levers["freshman_target"] + baseline["transfers_per_year"]
        headcount = headcount * retention + new_students
        sticker = sticker * (1 + baseline["sticker_growth"])
        net_revenue = headcount * sticker * (1 - discount)
        rows.append({
            "year": f"Year {t}",
            "new_students": round(new_students),
            "total_headcount": round(headcount),
            "fte": round(headcount * baseline["fte_factor"]),
            "sticker_tuition": round(sticker),
            "discount_rate_pct": levers["discount_pct"],
            "net_tuition_revenue": round(net_revenue),
        })
    return pd.DataFrame(rows)


def admits_required(freshman_target, yield_pct):
    """Admits needed to hit the freshman target at a given yield."""
    if yield_pct <= 0:
        raise ValueError("yield_pct must be positive")
    return round(freshman_target / (yield_pct / 100.0))


def kpis(projection):
    """Pull headline numbers off a projection DataFrame."""
    last = projection.iloc[-1]
    first = projection.iloc[0]
    return {
        "year5_headcount": int(last["total_headcount"]),
        "year5_net_revenue": int(last["net_tuition_revenue"]),
        "headcount_change": int(last["total_headcount"]
                                - first["total_headcount"]),
        "revenue_change": int(last["net_tuition_revenue"]
                              - first["net_tuition_revenue"]),
    }
