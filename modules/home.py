"""
modules/home.py — Scenario Explorer (Stakeholder Landing Page)
NASA Project: Managing the Colorado River as an Infrastructure Asset
PI: Enrique Vivoni, ASU | Collaborators: Kristen Whitney (NASA Goddard)
Stakeholders: Bureau of Reclamation, ADWR, CAWCD, Met Water District, SNWA
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from scipy import stats
from utils.data_loader import (
    load_vic_annual, load_snotel_annual, load_snotel_stations,
    load_grace, basin_label, trend_slope
)

MAROON="#8C1D40"; NAVY="#0D2137"; NAVY2="#1a3a5c"; GOLD="#FFC627"
BLUE="#01579B"; GREEN="#2E7D32"; ORANGE="#E65100"; PURPLE="#4527A0"
TEAL="#00695C"; RED="#B71C1C"
BASIN_OPTIONS = [
    {"label": "Colorado River Basin (Full)", "value": "CRB"},
    {"label": "Upper Basin",                 "value": "UpperBasin"},
    {"label": "Lower Basin",                 "value": "LowerBasin"},
    {"label": "Green River",                 "value": "Green"},
    {"label": "San Juan",                    "value": "SanJuan"},
    {"label": "Grand Canyon",                "value": "GrandCanyon"},
    {"label": "Gila River",                  "value": "Gila"},
]

METRIC_OPTIONS = [
    {"label": " Water Supply (Runoff + Baseflow)", "value": "supply"},
    {"label": " Runoff Efficiency (RBFE)",         "value": "rbfe"},
    {"label": "Snowpack (SWE)",                   "value": "swe"},
    {"label": "Temperature",                      "value": "temp"},
    {"label": "Precipitation",                    "value": "prec"},
    {"label": " Evapotranspiration",               "value": "et"},
    {"label": " Soil Moisture (total)",             "value": "sm"},
    {"label": " Soil Moisture L1 (0–10 cm)",       "value": "sm_l1"},
    {"label": " Soil Moisture L2 (10–40 cm)",      "value": "sm_l2"},
    {"label": " Soil Moisture L3 (40–200 cm)",     "value": "sm_l3"},
]

# Analysis finder — grouped "Section · Analysis" labels → route
FINDER_OPTIONS = [
    {"label": "Scenario · Climate-Sensitivity Scenario", "value": "/scenario"},
    {"label": "Scenario · Uncertainty & Confidence", "value": "/uncertainty"},
    {"label": "Water Supply · Snowpack & Runoff", "value": "/snowpack"},
    {"label": "Water Supply · Water Balance", "value": "/watbal"},
    {"label": "Water Supply · Snowmelt Timing & Flash Drought", "value": "/timing"},
    {"label": "Water Supply · Soil Moisture ↔ Streamflow", "value": "/links"},
    {"label": "Water Supply · Elevation-Dependent Snow Loss", "value": "/elevsnow"},
    {"label": "Risk · Drought & Shortage Risk", "value": "/drought"},
    {"label": "Risk · Reservoirs & Shortage Tiers", "value": "/reservoirs"},
    {"label": "Risk · Terrestrial Water Storage (GRACE)", "value": "/tws"},
    {"label": "Risk · Subsurface Storage (GW + reservoir)", "value": "/storage"},
    {"label": "Risk · Drought Recovery (WY2023)", "value": "/recovery"},
    {"label": "Projections · Hydrologic Projections to 2100", "value": "/future"},
    {"label": "Projections · Seasonal Forecasts (NMME)", "value": "/nmme"},
    {"label": "Projections · Climate Projections (CMIP)", "value": "/cmip"},
    {"label": "Spatial · Spatial Hydrology Maps", "value": "/spatial"},
    {"label": "Governance · Water Governance (Law of the River)", "value": "/governance"},
    {"label": "Governance · CRIA Asset Framework", "value": "/cria"},
    {"label": "Advanced · Aridification & Runoff Loss", "value": "/aridification"},
    {"label": "Advanced · Aridity Severity Index", "value": "/asi"},
    {"label": "Advanced · Budyko Water–Energy Balance", "value": "/budyko"},
    {"label": "Advanced · No-Analog Future Climate", "value": "/noanalog"},
    {"label": "Advanced · Drought Propagation", "value": "/cascade"},
    {"label": "Advanced · Land-Surface Warming & Energy", "value": "/warming"},
    {"label": "About · References & Validation", "value": "/references"},
]

BASELINE_OPTIONS = [
    {"label": "1983–2010 (WMO-style)",     "value": "1982_2010"},
    {"label": "1983–2024 (full record)",   "value": "1982_2024"},
    {"label": "1990–2020 (recent 30-yr)",  "value": "1990_2020"},
]

METRIC_MAP = {
    "supply": {"col": "supply",         "label": "Water Supply",        "unit": "mm/yr", "icon": " "},
    "rbfe":   {"col": "RBFE",           "label": "Runoff Efficiency",   "unit": "%",     "icon": " "},
    "swe":    {"col": "OUT_SWE",        "label": "Snowpack (SWE)",      "unit": "mm",    "icon": ""},
    "temp":   {"col": "OUT_AIR_TEMP",   "label": "Temperature",         "unit": "°C",    "icon": ""},
    "prec":   {"col": "OUT_PREC",       "label": "Precipitation",       "unit": "mm/yr", "icon": ""},
    "et":     {"col": "OUT_EVAP",       "label": "Total ET",            "unit": "mm/yr", "icon": " "},
    "sm":     {"col": "OUT_SOIL_MOIST",    "label": "Soil Moisture (total)", "unit": "mm", "icon": " "},
    "sm_l1":  {"col": "OUT_SOIL_MOIST_L1","label": "Soil Moisture L1",      "unit": "mm", "icon": " "},
    "sm_l2":  {"col": "OUT_SOIL_MOIST_L2","label": "Soil Moisture L2",      "unit": "mm", "icon": " "},
    "sm_l3":  {"col": "OUT_SOIL_MOIST_L3","label": "Soil Moisture L3",      "unit": "mm", "icon": " "},
}

CONTEXT = {
    "supply": [
        "Bureau of Reclamation manages Lee Ferry compact (7.5 MAF/yr to Upper Basin states).",
        "CAP receives ~1.5 MAF/yr — first to be cut under shortage declarations.",
        "Lake Mead Tier 1 shortage triggers at elevation 1,075 ft (~10.5 km³ storage).",
        "SNWA and Metropolitan Water District face similar shortage risk as storage falls.",
    ],
    "swe": [
        "April 1 SWE is the primary operational predictor of spring runoff volume.",
        "NRCS SNOTEL network monitors snowpack at 103 CRB stations daily.",
        "Earlier snowmelt reduced summer baseflow stress on late-season water rights.",
        "Upper Basin headwaters (Green, San Juan) supply majority of mainstem flow.",
    ],
    "temp": [
        "Warming increases evaporative demand, reducing runoff efficiency basin-wide.",
        "Higher temperatures accelerate snowmelt timing, shifting runoff earlier in season.",
        "Every 1°C warming reduces CRB runoff by ~2–9% through increased ET losses.",
        "Urban heat stress increases municipal water demand, compounding supply shortfall.",
    ],
    "prec": [
        "Precipitation uncertainty is large — CMIP6 models diverge on future P for CRB.",
        "Increased P variability means both intensified floods and prolonged droughts.",
        "Rain-snow transition elevation is rising more precipitation falling as rain.",
        "NMME seasonal forecasts provide 6–9 month operational precipitation outlooks.",
    ],
    "et": [
        "ET is the dominant water loss (60–80% of precipitation) throughout the CRB.",
        "Rising ET under warming directly reduces water available for compact delivery.",
        "Agriculture (~80% of CRB consumptive use) is the primary ET driver.",
        "ECOSTRESS provides field-scale ET at 70 m resolution for irrigation monitoring.",
    ],
    "rbfe": [
        "RBFE = (Runoff + Baseflow) / Precipitation × 100 — % of rain/snow that becomes streamflow.",
        "Declining RBFE under warming signals 'hot drought': higher ET consuming more of each mm of rain.",
        "CRB RBFE (~10%) is among the lowest of major US river basins due to high aridity.",
        "A 1 percentage point drop in RBFE translates directly to ~1% less compact-deliverable water.",
    ],
    "sm": [
        "Soil moisture deficit drives demand for supplemental irrigation and municipal water.",
        "Low spring soil moisture reduces snowmelt-to-runoff conversion efficiency.",
        "SMAP L4 (9 km, daily) provides near-real-time root zone soil moisture globally.",
        "Soil moisture integrates antecedent precipitation and ET, signaling drought onset.",
    ],
    "sm_l1": [
        "Layer 1 (0–10 cm) responds rapidly to rainfall — best indicator of surface evaporation.",
        "Warm-season drying in L1 accelerates bare-soil evaporation losses from the top layer.",
        "SMAP satellite observes the top 5 cm; VIC L1 provides the closest model analog.",
        "L1 moisture drives the partitioning between infiltration and surface runoff generation.",
    ],
    "sm_l2": [
        "Layer 2 (10–40 cm) represents the active root zone for most CRB vegetation types.",
        "L2 depletion precedes plant water stress and drives transpiration decline.",
        "Spring L2 replenishment from snowmelt determines summer drought resilience.",
        "Agriculture relies heavily on L2 moisture for crop water availability.",
    ],
    "sm_l3": [
        "Layer 3 (40–200 cm) is the deep storage buffer — responds slowly to surface forcing.",
        "L3 trends reveal multi-year drought accumulation and groundwater recharge signals.",
        "Deep moisture depletion persists across years — a key indicator of compound drought.",
        "Baseflow generation is tightly coupled to L3 saturation status.",
    ],
}


def _safe(fn):
    try:
        return fn()
    except Exception:
        return pd.DataFrame()


def _get_bl_range(bl_key):
    m = {"1982_2010": (1983, 2010), "1982_2024": (1983, 2023), "1990_2020": (1990, 2020)}
    return m.get(bl_key, (1982, 2010))


def _prep(basin, metric_key, bl_key):
    """Returns (df_hist_with_val, None, base_mean, base_std) or (None,...) on failure."""
    df_h = _safe(load_vic_annual)
    if df_h.empty:
        return None, None, None, None

    y0, y1 = _get_bl_range(bl_key)
    col = METRIC_MAP[metric_key]["col"]

    if metric_key == "supply":
        if "OUT_RUNOFF" not in df_h.columns or "OUT_BASEFLOW" not in df_h.columns:
            return None, None, None, None
        df_h = df_h.copy()
        df_h["supply"] = df_h["OUT_RUNOFF"] + df_h["OUT_BASEFLOW"]

    if col not in df_h.columns:
        return None, None, None, None

    bh = df_h[df_h["basin"] == basin].sort_values("water_year").copy()
    bh["val"] = bh[col]

    baseline_vals = bh[(bh["water_year"] >= y0) & (bh["water_year"] <= y1)]["val"].dropna()
    base_mean = baseline_vals.mean() if not baseline_vals.empty else None
    base_std  = baseline_vals.std()  if not baseline_vals.empty else None

    return bh, None, base_mean, base_std


def _empty_fig(msg="Preprocessing required — run 01_basin_aggregation.py"):
    fig = go.Figure()
    fig.add_annotation(text=msg, xref="paper", yref="paper",
                       x=0.5, y=0.5, showarrow=False,
                       font=dict(size=12, color="#90a4ae"))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20), height=360,
    )
    return fig


def _tile(val, label, icon, color):
    return html.Div([
        html.Div(str(val), className="info-tile-value"),
        html.Div(label,    className="info-tile-label"),
        html.Div(icon,     className="info-tile-icon"),
    ], className=f"info-tile {color}")


# ─────────────────────────────────────────────────────────────
def layout():
    return html.Div([
        html.Div([
            html.H2("Overview"),
            html.P("Pick a basin and variable to explore the Colorado River Basin at a glance, "
                   "then dive into any section from the sidebar."),
        ], className="tab-header"),

        html.Div([

            # ── Start here — the 3 questions a manager asks ──
            html.Div([
                html.Div([
                    html.I(className="bi bi-compass", style={"color": MAROON, "marginRight": "8px",
                                                             "fontSize": "18px"}),
                    html.Span("Start here", style={"fontSize": "16px", "fontWeight": "800",
                                                   "color": MAROON, "letterSpacing": "0.3px"}),
                    html.Span("  three questions, three tabs — the rest is optional depth",
                              style={"fontSize": "11px", "color": "#1e293b", "marginLeft": "10px"}),
                ], style={"borderBottom": f"2px solid {MAROON}", "paddingBottom": "8px",
                          "marginBottom": "14px", "display": "flex", "alignItems": "center"}),
                dbc.Row([
                    dbc.Col(html.A([
                        html.Div([html.Span(_n, className="step-num"),
                                  html.Span(_q, style={"fontWeight": "700", "fontSize": "13px",
                                                       "color": NAVY})],
                                 style={"display": "flex", "alignItems": "center", "marginBottom": "6px"}),
                        html.Img(src=_gif, style={"width": "100%", "height": "auto",
                                                  "borderRadius": "6px", "border": "1px solid #e2e8f0",
                                                  "margin": "2px 0 8px"}),
                        html.Div(_desc, style={"fontSize": "11px", "color": "#1e293b",
                                               "lineHeight": "1.45"}),
                        html.Div([_open, html.I(className="bi bi-arrow-right")],
                                 style={"fontSize": "11px", "fontWeight": "700", "color": BLUE,
                                        "marginTop": "8px"}),
                    ], href=_href, className="step-card",
                        style={"display": "block", "textDecoration": "none"}),
                        xs=12, md=4, className="mb-2")
                    for _n, _q, _gif, _desc, _open, _href in [
                        ("1", "How much water is there?", "/assets/animations/snow_swe.gif",
                         "Supply & snowpack — runoff, SWE, and how this year compares to the record.",
                         "Open Water Supply & Snow ", "/snowpack"),
                        ("2", "How bad is the risk?", "/assets/animations/drought_4decades.gif",
                         "Drought, storage & shortage — shortage probability and Lake Mead tier exposure.",
                         "Open Drought & Risk ", "/drought"),
                        ("3", "What if it gets warmer/drier?", "/assets/animations/runoff.gif",
                         "Scenario explorer — dial ΔT and ΔP, see projected streamflow with 95% confidence.",
                         "Open Scenario Explorer ", "/scenario"),
                    ]
                ], className="g-2"),
            ], className="crb-card", style={"padding": "14px 16px", "marginBottom": "18px"}),

            # ── Analysis Finder — pick from the menu, then open ──
            html.Div([
                html.Div([
                    html.I(className="bi bi-search", style={"color": MAROON, "marginRight": "8px",
                                                            "fontSize": "18px"}),
                    html.Span("Find an analysis", style={"fontSize": "16px", "fontWeight": "800",
                                                        "color": MAROON}),
                    html.Span("  choose from the menu — nothing loads until you pick",
                              style={"fontSize": "11px", "color": "#1e293b", "marginLeft": "10px"}),
                ], style={"borderBottom": f"2px solid {MAROON}", "paddingBottom": "8px",
                          "marginBottom": "14px", "display": "flex", "alignItems": "center"}),
                dbc.Row([
                    dbc.Col([
                        html.Div("STARTING BASIN", className="control-label"),
                        dcc.Dropdown(id="home-finder-basin", options=BASIN_OPTIONS, value="CRB",
                                     clearable=False, style={"fontSize": "12.5px"}),
                        html.Div("(each analysis also has its own basin selector)",
                                 style={"fontSize": "10px", "color": "#1e293b", "marginTop": "3px"}),
                    ], xs=12, md=4),
                    dbc.Col([
                        html.Div("CHOOSE AN ANALYSIS", className="control-label"),
                        dcc.Dropdown(id="home-finder", options=FINDER_OPTIONS, value=None,
                                     placeholder="Select an analysis to open…",
                                     clearable=False, style={"fontSize": "12.5px"}),
                    ], xs=12, md=8),
                ]),
            ], className="crb-card", style={"padding": "14px 16px", "marginBottom": "18px"}),

            # ── Explore In Depth (top — between header and overview) ──
            html.Div([
              html.Div([
                html.I(className="bi bi-compass", style={"color": MAROON, "marginRight": "8px",
                                                         "fontSize": "18px"}),
                html.Span("Explore In Depth", style={"fontSize": "16px", "fontWeight": "800",
                                                     "color": MAROON, "letterSpacing": "0.3px"}),
                html.Span("  choose an analysis to open",
                          style={"fontSize": "11px", "color": "#1e293b", "marginLeft": "10px"}),
              ], style={"borderBottom": f"2px solid {MAROON}", "paddingBottom": "8px",
                      "marginBottom": "14px",
                      "display": "flex", "alignItems": "center"}),
              dbc.Row([
                dbc.Col([
                    html.A([
                        html.Div([
                            html.I(className=f"bi {c['icon']}", style={"fontSize": "18px",
                                   "marginRight": "8px", "color": MAROON}),
                            html.Span(c["title"]),
                        ], style={"fontSize": "13px", "fontWeight": "700",
                                  "color": "#0D2137", "marginBottom": "5px",
                                  "display": "flex", "alignItems": "center"}),
                        html.Div(c["desc"],
                                 style={"fontSize": "10.5px", "color": "#1e293b",
                                        "lineHeight": "1.4"}),
                        html.Div(["Open ", html.I(className="bi bi-arrow-right")],
                                 style={"fontSize": "10.5px", "fontWeight": "700",
                                        "color": "#01579B", "marginTop": "6px"}),
                    ], href=c["href"],
                       className=f"info-tile {c['color']}",
                       style={"display": "block", "textDecoration": "none"}),
                ], xs=12, sm=6, md=4, className="mb-3")
                for c in [
                    {"icon": "bi-snow", "title": "Snowpack & Runoff",
                     "desc": "SNOTEL SWE trends · SWE→Q forecast · Seasonal shift",
                     "href": "/snowpack", "color": "tile-navy"},
                    {"icon": "bi-droplet", "title": "Water Balance",
                     "desc": "P→ET + Q + ΔS · Runoff ratio trends · ET partition",
                     "href": "/watbal", "color": "tile-green"},
                    {"icon": "bi-globe-americas", "title": "Water Storage (GRACE)",
                     "desc": "TWS anomaly · Drought memory · SMAP validation",
                     "href": "/tws", "color": "tile-blue"},
                    {"icon": "bi-exclamation-triangle", "title": "Drought & Risk",
                     "desc": "VIC basin runoff · Shortage probability · SM deficit index",
                     "href": "/drought", "color": "tile-maroon"},
                    {"icon": "bi-graph-up-arrow", "title": "Projections to 2100",
                     "desc": "VIC projections · All variables · Basin ranking",
                     "href": "/future", "color": "tile-purple"},
                    {"icon": "bi-map", "title": "Spatial Analysis",
                     "desc": "~22k-cell CRB VIC grid · Trend maps · Period compare",
                     "href": "/spatial", "color": "tile-orange"},
                ]
              ], className="g-2"),
            ], className="crb-card", style={"padding": "14px 16px", "marginBottom": "18px"}),

            # ── Scenario Controls ───────────────────────────────
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div(" BASIN", className="control-label"),
                        dcc.Dropdown(id="se-basin", options=BASIN_OPTIONS,
                                     value="CRB", clearable=False,
                                     style={"fontSize": "12.5px"}),
                    ], xs=12, md=4),
                    dbc.Col([
                        html.Div("SHOW ME", className="control-label"),
                        dcc.Dropdown(id="se-metric", options=METRIC_OPTIONS,
                                     value="supply", clearable=False,
                                     style={"fontSize": "12.5px"}),
                    ], xs=12, md=4),
                    dbc.Col([
                        html.Div("HISTORICAL BASELINE", className="control-label"),
                        dcc.Dropdown(id="se-baseline", options=BASELINE_OPTIONS,
                                     value="1982_2010", clearable=False,
                                     style={"fontSize": "12.5px"}),
                    ], xs=12, md=4),
                ]),
            ], className="control-panel"),

            # ── Outcome Tiles ───────────────────────────────────
            dbc.Row(id="se-tiles", className="mb-3 g-2"),

            # ── Key Findings Banner ─────────────────────────────
            html.Div(id="se-findings",
                     style={"background": "#fff3e0",
                            "borderLeft": f"4px solid {ORANGE}",
                            "padding": "10px 14px", "borderRadius": "0 6px 6px 0",
                            "fontSize": "11.5px", "color": "#bf360c",
                            "marginBottom": "12px"}),

            # ── Main Chart ──────────────────────────────────────
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span(id="se-chart-title",
                                      style={"fontWeight": "700", "fontSize": "13px"}),
                            html.Span("· VIC 5.0 PRISM-calibrated historical record WY1983–2024",
                                      style={"color": "#1e293b", "fontSize": "11px"}),
                            dbc.Button("CSV", id="se-dl-btn", size="sm",
                                       className="btn-download",
                                       style={"float": "right", "marginTop": "-3px"}),
                        ], className="crb-card-header"),
                        dcc.Graph(id="se-main-chart",
                                  config={"displayModeBar": False},
                                  style={"height": "360px"}),
                        dcc.Download(id="se-dl-data"),
                    ], className="crb-card"),
                ], md=12),
            ], className="g-3 mb-2"),

            # ── Basin Comparison + Context ───────────────────────
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span(" Basin Comparison",
                                      style={"fontWeight": "700", "fontSize": "13px"}),
                            html.Span("— Recent decade (WY2015–2024) vs baseline (%)",
                                      style={"color": "#1e293b", "fontSize": "11px"}),
                        ], className="crb-card-header"),
                        dcc.Graph(id="se-basin-chart",
                                  config={"displayModeBar": False},
                                  style={"height": "300px"}),
                    ], className="crb-card"),
                ], md=6),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span("Stakeholder Implications",
                                      style={"fontWeight": "700", "fontSize": "13px"}),
                        ], className="crb-card-header"),
                        html.Div(id="se-context-card",
                                 style={"padding": "14px 16px", "maxHeight": "300px",
                                        "overflowY": "auto"}),
                    ], className="crb-card"),
                ], md=6),
            ], className="g-3 mb-2"),

        ], className="tab-body"),
    ])


# ─────────────────────────────────────────────────────────────
def register_callbacks(app):

    # Analysis Finder → navigate to the chosen analysis
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Input("home-finder", "value"),
        prevent_initial_call=True,
    )
    def _finder_go(route):
        from dash.exceptions import PreventUpdate
        if not route:
            raise PreventUpdate
        return route

    @app.callback(
        Output("se-tiles", "children"),
        Input("se-basin", "value"),
        Input("se-metric", "value"),
        Input("se-baseline", "value"),
    )
    def update_tiles(basin, metric_key, bl_key):
        bh, _, base_mean, _ = _prep(basin, metric_key, bl_key)
        y0, y1 = _get_bl_range(bl_key)
        mi = METRIC_MAP[metric_key]
        is_pct = mi["unit"] == "%"
        def _fmt(val):
            """Format a scalar value appropriate to the metric."""
            if val is None:
                return "—"
            if is_pct:
                return f"{val:.1f}%"
            return f"{val:.1f} {mi['unit']}"

        # Tile 1: baseline mean
        t1 = _tile(_fmt(base_mean), f"Baseline mean ({y0}–{y1})", mi["icon"], "tile-navy")

        # Tile 2: recent decade mean (WY2015–2024, real data)
        recent_val = None
        if bh is not None and not bh.empty:
            rec = bh[bh["water_year"] >= 2015]["val"].dropna()
            if not rec.empty:
                recent_val = rec.mean()
        t2 = _tile(_fmt(recent_val), "Recent decade mean (WY2015–2024)", " ", "tile-maroon")

        # Tile 3: Mann-Kendall trend per decade
        trend_str, t3_color = "—", "tile-slate"
        if bh is not None and not bh.empty:
            t = trend_slope(bh["val"], bh["water_year"])
            if t["slope"] is not None:
                per_dec = t["slope"] * 10
                sig = " " if t["pvalue"] is not None and t["pvalue"] < 0.05 else ""
                if is_pct:
                    trend_str = f"{per_dec:+.2f}%/dec{sig}"
                else:
                    trend_str = f"{per_dec:+.2f}/dec{sig}"
                t3_color = "tile-maroon" if per_dec < 0 else "tile-green"
                trend_icon = " " if trend_str.startswith("-") else " "
                unit_lbl = "" if is_pct else f" ({mi['unit']}/decade)"
                t3 = _tile(trend_str, f"Sen's slope{unit_lbl}", trend_icon, t3_color)

        # Tile 4: recent decade vs baseline %
        chg_str, t4_color = "—", "tile-slate"
        if base_mean and recent_val is not None and abs(base_mean) > 1e-6:
            pct = (recent_val - base_mean) / abs(base_mean) * 100
            chg_str = f"{pct:+.1f}%"
            t4_color = "tile-maroon" if pct < 0 else "tile-green"
            t4 = _tile(chg_str, "Recent decade vs baseline", " ", t4_color)

        return [dbc.Col(t1, xs=6, md=3), dbc.Col(t2, xs=6, md=3),
                dbc.Col(t3, xs=6, md=3), dbc.Col(t4, xs=6, md=3)]

    @app.callback(
        Output("se-main-chart", "figure"),
        Output("se-chart-title", "children"),
        Input("se-basin", "value"),
        Input("se-metric", "value"),
        Input("se-baseline", "value"),
    )
    def update_main_chart(basin, metric_key, bl_key):
        bh, fut_val, base_mean, base_std = _prep(basin, metric_key, bl_key)
        mi = METRIC_MAP[metric_key]
        y0, y1 = _get_bl_range(bl_key)
        title = f"{mi['icon']} {mi['label']} — {basin_label(basin)}"
        if bh is None or bh.empty:
            return _empty_fig(), title

        fig = go.Figure()

        # Baseline shading
        fig.add_vrect(x0=y0, x1=y1,
                      fillcolor="rgba(13,33,55,0.05)", line_width=0,
                      annotation_text=f"Baseline {y0}–{y1}",
                      annotation_position="top left",
                      annotation_font=dict(size=9, color="#78909c"))

        # Historical time series
        fig.add_trace(go.Scatter(
            x=bh["water_year"], y=bh["val"],
            mode="lines", name="Historical (VIC 5.0)",
            line=dict(color=BLUE, width=2, shape="spline", smoothing=0.4),
            hovertemplate="WY %{x}<br>%{y:.1f} " + mi["unit"] + "<extra></extra>",
        ))

        # 5-year rolling mean
        bh["r5"] = bh["val"].rolling(5, center=True).mean()
        fig.add_trace(go.Scatter(
            x=bh["water_year"], y=bh["r5"],
            mode="lines", name="5-yr mean",
            line=dict(color=NAVY, width=2.5),
            hovertemplate="WY %{x} (5-yr mean)<br>%{y:.1f} " + mi["unit"] + "<extra></extra>",
        ))

        # Baseline mean
        if base_mean is not None:
            fig.add_hline(y=base_mean,
                          line_dash="dash", line_color="#90a4ae", line_width=1.5,
                          annotation_text=f"Baseline: {base_mean:.1f}",
                          annotation_position="right",
                          annotation_font=dict(size=9, color="#78909c"))

        # Historical trend line
        vals = bh["val"].dropna()
        wyrs = bh.loc[vals.index, "water_year"]
        if len(vals) >= 5:
            slope, intercept, _, pval, _ = stats.linregress(wyrs, vals)
            x_ext = np.array([int(wyrs.min()), 2023])
            y_ext = slope * x_ext + intercept
            sig_label = " " if pval < 0.05 else ""
            fig.add_trace(go.Scatter(
                x=x_ext, y=y_ext,
                mode="lines",
                name=f"Historical trend {slope:+.2f}/yr{sig_label}",
                line=dict(color=NAVY2, width=1.5, dash="dot"),
                hoverinfo="skip",
            ))

        # WY2024 partial-year marker (Jan–Sep only)
        fig.add_vline(x=2024, line_dash="dash", line_color="#FFC627", line_width=1,
                      annotation_text="WY2024 (Jan–Sep)", annotation_position="top left",
                      annotation_font=dict(size=8, color="#B8860B"))

        fig.update_layout(
            xaxis=dict(title="Water Year", range=[1980, 2026]),
            yaxis=dict(title=f"{mi['label']} ({mi['unit']})"),
            legend=dict(orientation="h", y=-0.15, x=0, font=dict(size=10)),
            margin=dict(l=60, r=90, t=15, b=55),
            height=360,
            paper_bgcolor="white", plot_bgcolor="white",
            transition=dict(duration=400, easing="cubic-in-out"),
        )
        return fig, title

    @app.callback(
        Output("se-basin-chart", "figure"),
        Input("se-metric", "value"),
        Input("se-baseline", "value"),
    )
    def update_basin_chart(metric_key, bl_key):
        y0, y1 = _get_bl_range(bl_key)
        mi = METRIC_MAP[metric_key]
        col = mi["col"]

        df_h = _safe(load_vic_annual)
        if df_h.empty:
            return _empty_fig()

        if metric_key == "supply":
            if "OUT_RUNOFF" not in df_h.columns:
                return _empty_fig()
            df_h = df_h.copy()
            df_h["supply"] = df_h["OUT_RUNOFF"] + df_h["OUT_BASEFLOW"]

        if col not in df_h.columns:
            return _empty_fig(f"{col} not available")

        records = []
        for bid in ["CRB", "UpperBasin", "LowerBasin", "Green", "SanJuan", "GrandCanyon", "Gila"]:
            base = df_h[(df_h["basin"] == bid) & (df_h["water_year"] >= y0) &
                        (df_h["water_year"] <= y1)][col].mean()
            recent = df_h[(df_h["basin"] == bid) & (df_h["water_year"] >= 2015)][col].mean()
            if (base is not None and recent is not None
                    and not np.isnan(float(base)) and not np.isnan(float(recent))
                    and abs(float(base)) > 0.01):
                pct = (recent - base) / abs(base) * 100
                records.append({"label": basin_label(bid), "pct": pct,
                                 "recent": recent, "base": base})

        if not records:
            return _empty_fig("Insufficient data for basin comparison")

        df_r = pd.DataFrame(records).sort_values("pct")
        colors = [RED if v < -30 else MAROON if v < 0 else GREEN for v in df_r["pct"]]

        fig = go.Figure()
        for _, row in df_r.iterrows():
            c = RED if row["pct"] < -30 else MAROON if row["pct"] < 0 else GREEN
            fig.add_trace(go.Scatter(
                x=[0, row["pct"]], y=[row["label"], row["label"]],
                mode="lines", line=dict(color=c, width=2.5),
                showlegend=False, hoverinfo="skip",
            ))
        fig.add_trace(go.Scatter(
            x=df_r["pct"], y=df_r["label"],
            mode="markers",
            marker=dict(color=colors, size=14, line=dict(color="white", width=2)),
            customdata=np.stack([df_r["recent"], df_r["base"]], axis=-1),
            hovertemplate=(
                "<b>%{y}</b><br>Recent (WY2015–2024): %{customdata[0]:.1f} " + mi["unit"] +
                "<br>Baseline: %{customdata[1]:.1f} " + mi["unit"] +
                "<br>Change: %{x:+.1f}%<extra></extra>"),
            showlegend=False,
        ))
        fig.add_vline(x=0, line_dash="dash", line_color="#b0bec5", line_width=1.5)
        fig.update_layout(
            xaxis_title=f"% Change: WY2015–2024 vs Baseline ({y0}–{y1})",
            yaxis=dict(tickfont=dict(size=11)),
            margin=dict(l=120, r=50, t=15, b=40),
            height=300,
            paper_bgcolor="white", plot_bgcolor="white",
            transition=dict(duration=400, easing="cubic-in-out"),
        )
        return fig

    @app.callback(
        Output("se-context-card", "children"),
        Input("se-basin", "value"),
        Input("se-metric", "value"),
        Input("se-baseline", "value"),
    )
    def update_context(basin, metric_key, bl_key):
        bh, fut_val, base_mean, _ = _prep(basin, metric_key, bl_key)
        y0, y1 = _get_bl_range(bl_key)
        mi = METRIC_MAP[metric_key]

        lines = []

        # Context bullets
        for item in CONTEXT.get(metric_key, []):
            lines.append(html.Div([
                html.Span("▸ ", style={"color": NAVY, "fontWeight": "700"}),
                item,
            ], style={"fontSize": "11.5px", "color": "#37474f", "marginBottom": "5px"}))

        # Snotel note — use station-level parquet for correct per-station stats
        df_sta = _safe(load_snotel_stations)
        if not df_sta.empty:
            crb_sta = df_sta[df_sta["basin"]=="CRB"].drop_duplicates("site_id")
            n_tot   = len(crb_sta)
            n_dec   = (crb_sta["mk_slope"].dropna() < 0).sum()
            lines.append(html.Div([
                html.Span(" ", style={"fontSize": "13px"}),
                html.Span(f"{n_dec}/{n_tot} SNOTEL stations show declining peak SWE.",
                          style={"fontSize": "11px", "color": BLUE}),
            ], style={"marginTop": "8px"}))

        # GRACE note
        df_g = _safe(load_grace)
        if not df_g.empty:
            crb_g = df_g[df_g["basin"] == "CRB"]["tws_mm"]
            if not crb_g.empty:
                lines.append(html.Div([
                    html.Span("", style={"fontSize": "13px"}),
                    html.Span(f"GRACE minimum TWS anomaly: {crb_g.min():.0f} mm.",
                              style={"fontSize": "11px", "color": TEAL}),
                ], style={"marginTop": "2px"}))

        lines.append(html.Div(
            "VIC 5.0 · PRISM-calibrated · Historical record WY1983–2024.",
            style={"fontSize": "10px", "color": "#1e293b", "marginTop": "8px"},
        ))
        return html.Div(lines)

    @app.callback(
        Output("se-findings", "children"),
        Input("se-basin", "value"),
        Input("se-metric", "value"),
        Input("se-baseline", "value"),
    )
    def update_findings(basin, metric_key, bl_key):
        bh, _, base_mean, _ = _prep(basin, metric_key, bl_key)
        y0, y1 = _get_bl_range(bl_key)
        mi = METRIC_MAP[metric_key]

        if bh is None or bh.empty:
            return " Preprocessing required — run 01_basin_aggregation.py first."
        parts = [html.Strong("Key Finding — ")]
        bname = basin_label(basin)

        if base_mean:
            parts.append(f"{bname} {mi['label']} baseline ({y0}–{y1}): {base_mean:.1f} {mi['unit']}. ")

        # Historical trend
        t = trend_slope(bh["val"], bh["water_year"])
        if t["slope"] is not None and t["pvalue"] is not None:
            sig = " statistically significant (p<0.05)" if t["pvalue"] < 0.05 else f" (p={t['pvalue']:.2f})"
            parts.append(f"Historical trend: {t['slope']:+.2f} {mi['unit']}/yr{sig}. ")

        # Recent decade vs baseline (real data)
        rec = bh[bh["water_year"] >= 2015]["val"].dropna()
        if not rec.empty and base_mean and abs(base_mean) > 0.01:
            rec_mean = rec.mean()
            pct = (rec_mean - base_mean) / abs(base_mean) * 100
            parts.append(f"Recent decade (WY2015–2024): {rec_mean:.1f} {mi['unit']} ({pct:+.1f}% vs baseline). ")
            if abs(pct) > 15:
                parts.append(html.Strong(
                    f"{'Notable decline' if pct < 0 else 'Notable increase'} over recent decade — ""based on VIC 5.0 PRISM-calibrated historical record.",
                    style={"color": RED if pct < -15 else ORANGE if pct < 0 else GREEN},
                ))

        return parts

    @app.callback(
        Output("se-dl-data", "data"),
        Input("se-dl-btn", "n_clicks"),
        Input("se-basin", "value"),
        Input("se-metric", "value"),
        prevent_initial_call=True,
    )
    def download(n, basin, metric_key):
        if not n:
            return None
        bh, _, _, _ = _prep(basin, metric_key, "1982_2024")
        if bh is None:
            return None
        mi = METRIC_MAP[metric_key]
        out = bh[["water_year", "val"]].rename(columns={"val": mi["label"]})
        out["source"] = "historical_VIC_WY1983-2024"
        return dcc.send_data_frame(out.to_csv, f"crb_{metric_key}_{basin}.csv", index=False)
