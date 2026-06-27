---
title: CRIA — Colorado River Infrastructure Asset
emoji: 🌊
colorFrom: indigo
colorTo: red
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# CRIA — Colorado River Infrastructure Asset

An interactive decision-support tool for water-resource management in the Colorado River Basin (CRB).
It fuses NASA Earth observations with a calibrated hydrologic reanalysis and presents the results in
the terms water managers actually use — basin by basin, question by question.

**Built with:** Python · Plotly Dash (Flask + Bootstrap) · VIC 5.0 · SNOTEL · GRACE/GRACE-FO · SMAP L4 ·
pandas / scipy / geopandas / xarray · matplotlib · Dockerized on Hugging Face Spaces.

**Project:** *Managing the Colorado River as an Infrastructure Asset: Fusing Remote Sensing and
Numerical Modeling in the Operations of the Central Arizona Project.*
**Affiliation:** Arizona State University, in collaboration with the Central Arizona Project ·
NASA Applied Sciences – Water Resources (Award 80NSSC22K0925, PI Enrique R. Vivoni).

## Decision-framed sections

| Section | What it answers |
|---------|-----------------|
| Overview | The three questions the tool answers, then any analysis |
| Water Supply & Snow | Where the water comes from — snowpack→runoff, water balance, snowmelt timing, elevation, Budyko |
| Drought & Risk | Drought & shortage risk, reservoir tiers, water storage (GRACE), recovery, aridification |
| Scenarios & Future | ΔT / ΔP scenario engine, projections to 2100, CMIP5/CMIP6, seasonal (NMME) forecasts |
| Basin Maps | Side-by-side maps of every variable, SNOTEL stations, rivers, plus seasonal & drought animations |
| Governance & About | Water governance, the CRIA asset framework, methods, publications, and project reports |

## Validated hydrologic model

All analyses derive from a PRISM-calibrated VIC 5.0 reanalysis of the CRB (WY1984–2024), calibrated on
snow and streamflow and independently evaluated against NASA SMAP and GRACE:

> Wang, Z., Ghimire, S., Whitney, K. M., Mascaro, G., Xiao, M., Yue, H., & Vivoni, E. R. (2026).
> *Revisiting the application of the Variable Infiltration Capacity (VIC) model in the Colorado River
> Basin using SMAP and GRACE.* **Scientific Reports, 16, 15890.**
> Streamflow NSE = 0.96 (Upper Basin); SMAP soil moisture R² = 0.71 (surface), 0.81 (root-zone);
> GRACE terrestrial water storage R² = 0.66–0.86.

## Data

- **VIC 5.0** — PRISM-calibrated reanalysis, ~6 km (1/16°), WY1984–2024; basin-aggregated parquet cache (deployed)
- **SNOTEL** — 103 CRB-region NRCS stations, peak-SWE annual records and trends
- **GRACE / GRACE-FO** — terrestrial water storage anomalies (2002–present)
- **SMAP L4** — surface and root-zone soil moisture

Raw NetCDF inputs (~58 GB) are processed locally; only the parquet cache (~200–400 MB) is deployed.

---

Developed by Pradeepika Kaushik (Praddy) — Geospatial & Data-Visualization Scientist, Arizona State University.
