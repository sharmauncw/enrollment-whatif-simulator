"""Enrollment What-If Simulator — interactive Streamlit dashboard.

Move the levers and watch projected headcount and net tuition revenue over
five years. EVERYTHING here is SYNTHETIC demo data for a fictional
university; this is a teaching tool, not a real forecast.

Run:
    python generate_data.py  # once, creates data/enrollment_baseline.csv
    streamlit run app.py
"""
import os

import pandas as pd
import plotly.express as px
import streamlit as st

from model import admits_required, kpis, project_enrollment

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE_CSV = os.path.join(HERE, "data", "enrollment_baseline.csv")

st.set_page_config(page_title="Enrollment What-If Simulator", layout="wide")
st.title("Enrollment What-If Simulator")
st.warning(
    "SYNTHETIC DEMO DATA — every number on this page is invented for "
    "teaching. Fictional 'Harborview University'. Not a real forecast."
)


@st.cache_data
def load_baseline():
    if not os.path.exists(BASELINE_CSV):
        st.error(
            "Baseline data not found. Run `python generate_data.py` first."
        )
        st.stop()
    return pd.read_csv(BASELINE_CSV)


baseline_hist = load_baseline()
latest = baseline_hist.iloc[-1]

baseline = {
    "total_headcount": float(latest["total_headcount"]),
    "transfers_per_year": float(latest["new_transfers"]),
    "sticker": float(latest["sticker_tuition_usd"]),
    "fte_factor": 0.92,
    "sticker_growth": 0.025,
}

# ---------------------------------------------------------------- levers ---
st.sidebar.header("Levers — move these")
yield_pct = st.sidebar.slider("Admit yield (%)", 10.0, 40.0,
                              float(latest["yield_pct"]), 0.5,
                              help="Share of admitted students who enroll. "
                                   "Summer melt is folded into this lever.")
retention_pct = st.sidebar.slider("Fall-to-fall retention (%)", 60.0, 90.0,
                                  float(latest["retention_pct"]), 0.5,
                                  help="Blended rate applied to total "
                                       "headcount each year.")
discount_pct = st.sidebar.slider("Tuition discount rate (%)", 20.0, 55.0,
                                 float(latest["discount_pct"]), 0.5,
                                 help="Institutional grant aid as a share of "
                                      "sticker tuition.")
freshman_target = st.sidebar.slider("New freshman target (headcount)",
                                    1500, 3500, int(latest["new_freshmen"]),
                                    50)

levers = {
    "yield_pct": yield_pct,
    "retention_pct": retention_pct,
    "discount_pct": discount_pct,
    "freshman_target": freshman_target,
}
projection = project_enrollment(baseline, levers, years=5)
k = kpis(projection)
admits = admits_required(freshman_target, yield_pct)

# ------------------------------------------------------------------ KPIs ---
st.subheader("Five-year outlook (synthetic)")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Year-5 headcount", f"{k['year5_headcount']:,}",
          f"{k['headcount_change']:+,} vs Year 1")
c2.metric("Year-5 net tuition revenue",
          f"${k['year5_net_revenue'] / 1e6:.1f}M",
          f"${k['revenue_change'] / 1e6:+.1f}M vs Year 1")
c3.metric("Admits required", f"{admits:,}",
          help="Freshman target ÷ yield. Lower yield → more admits needed.")
c4.metric("Year-5 FTE", f"{int(projection.iloc[-1]['fte']):,}")

# ----------------------------------------------------------------- charts --
ch1, ch2 = st.columns(2)
with ch1:
    fig_h = px.line(projection, x="year", y="total_headcount", markers=True,
                    title="Projected total headcount (synthetic)",
                    labels={"year": "", "total_headcount": "Headcount"})
    fig_h.update_traces(line_color="#0f766e", line_width=3)
    st.plotly_chart(fig_h, use_container_width=True)
with ch2:
    fig_r = px.line(projection, x="year", y="net_tuition_revenue",
                    markers=True,
                    title="Projected net tuition revenue (synthetic)",
                    labels={"year": "",
                            "net_tuition_revenue": "Net tuition revenue (USD)"})
    fig_r.update_traces(line_color="#b45309", line_width=3)
    st.plotly_chart(fig_r, use_container_width=True)

# ------------------------------------------------------- projection table --
st.subheader("Projection detail")
show = projection.copy()
show["net_tuition_revenue"] = show["net_tuition_revenue"].map(
    lambda v: f"${v:,.0f}")
show["sticker_tuition"] = show["sticker_tuition"].map(lambda v: f"${v:,.0f}")
st.dataframe(show, use_container_width=True, hide_index=True)

# ------------------------------------------------------ historical context --
st.subheader("Where we start: synthetic history")
fig_hist = px.bar(baseline_hist, x="fall_term", y="total_headcount",
                  title="Historical fall headcount (synthetic)",
                  labels={"fall_term": "Fall term",
                          "total_headcount": "Headcount"},
                  text="total_headcount")
fig_hist.update_traces(marker_color="#0f766e", textposition="outside")
st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------------------------------------------- explainers --
with st.expander("How to read this"):
    st.markdown(
        """
        - **Headcount compounds.** Each year's total is last year's total ×
          retention + new students. That is why a 2-point retention move
          matters more over five years than a one-time freshman bump.
        - **Discount is leverage, not just aid.** A higher discount rate
          directly shrinks net tuition revenue per student — watch revenue
          fall as you raise it, even while headcount holds.
        - **Yield sets the top of the funnel.** Admits required = freshman
          target ÷ yield. If yield slips, admissions must admit more students
          to hit the same class.
        - **FTE vs headcount.** FTE (full-time equivalent) is the
          budget-relevant number; part-time students count fractionally.
        """
    )

with st.expander("Model assumptions (all synthetic)"):
    st.markdown(
        """
        - One blended retention rate applied to total headcount; graduation
          is folded into the non-retained outflow (no cohort model).
        - Discount rate applied uniformly to sticker tuition.
        - Sticker tuition grows 2.5% per year; transfer intake and the FTE
          factor (0.92) are held constant.
        - This is a teaching simplification — real IR models use
          cohort survival, program mix, and residency.
        """
    )

st.caption("Synthetic demo data — Harborview University (fictional).")
