<div align="center">

# 🎓 Enrollment What-If Simulator

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Higher Ed](https://img.shields.io/badge/Higher_Ed-4ECDC4?style=for-the-badge)
![Synthetic Data](https://img.shields.io/badge/Synthetic_Data-9B59B6?style=for-the-badge)

**An interactive Streamlit dashboard for exploring how enrollment levers move headcount and net tuition revenue over five years — built entirely on synthetic demo data for the fictional "Harborview University."**

</div>

## 🎛️ What you can play with

Move **four levers** in the sidebar and watch the five-year projection update live:

| Lever | What it teaches |
|---|---|
| 🎯 Admit yield % | Funnel math — yield slips, the top of the funnel has to widen |
| 🔁 Retention % | Compounding retention — a 2-point gain beats a one-time freshman bump |
| 💰 Discount rate % | Discount leverage — aid strategy *is* revenue strategy |
| 🧑‍🎓 Freshman target | Headcount vs. FTE — seats filled vs. budget driven |

## What this demonstrates (the IR thinking)

Institutional research isn't just reporting what happened — it's helping leaders reason about what *could* happen. This toy model captures four habits of that thinking:

1. **Funnel math.** Admits required = freshman target ÷ yield. Yield slips, the top of the funnel has to widen.
2. **Compounding retention.** A 2-point retention gain beats a one-time freshman bump over five years, because retained students persist.
3. **Discount leverage.** Net tuition revenue = headcount × sticker × (1 − discount). Aid strategy and revenue strategy are the same math.
4. **Headcount vs. FTE.** Headcount fills seats; FTE (full-time equivalent) drives the budget.

## Higher-ed vocabulary you'll see

**Headcount** (every enrolled student) · **FTE** (full-time equivalent) · **Yield** (admitted → enrolled) · **Melt** (summer melt, folded into the yield lever) · **Retention** (fall-to-fall persistence) · **Discount rate** (institutional aid as a share of sticker) · **Net tuition revenue** (what the university actually keeps).

## How to run

```bash
pip install -r requirements.txt
python generate_data.py   # creates data/enrollment_baseline.csv (synthetic)
streamlit run app.py
```

Move the four levers in the sidebar — admit yield %, retention %, discount rate %, freshman target — and watch the five-year projection, KPIs, and charts update.

## Model

Per projected year: `headcount[t] = headcount[t-1] × retention + new_students`, `net_revenue[t] = headcount[t] × sticker[t] × (1 − discount)`. One blended retention rate; graduation folded into non-retained outflow. See `model.py` and the in-app "Model assumptions" expander. Teaching simplification — real IR shops model by cohort, program, and residency.

## Caveats

- **All data is synthetic.** Nothing here comes from any real institution.
- Streamlit must be installed to run the app (`pip install -r requirements.txt`); `model.py` has no Streamlit dependency and is unit-testable on its own.
