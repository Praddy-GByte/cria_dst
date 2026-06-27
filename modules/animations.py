"""
modules/animations.py — Seasonal & Drought Animations

Static, looping animations (GIFs) built from the real PRISM-calibrated VIC reanalysis,
the Colorado River drainage network, and major dam locations. Files live in
assets/animations/ and are served directly by Dash (no callbacks / no tiles needed).
"""
from dash import html
import dash_bootstrap_components as dbc
from utils.components import howto

MAROON = "#8C1D40"; NAVY = "#0D2137"

ANIMS = [
    {
        "src": "/assets/animations/snow_swe.gif",
        "title": "Seasonal snowpack — the basin's water tower",
        "what": "Monthly snow-water equivalent (SWE) across the basin through a year.",
        "read": "Snow builds up in the high headwaters through winter (Jan–Mar), then melts "
                "away by late summer (Jul–Sep) — the seasonal mountain 'water tower' that feeds "
                "the river. Watch the snow appear and then vanish.",
        "data": "VIC reanalysis · daily SWE → monthly mean (WY2023)",
    },
    {
        "src": "/assets/animations/runoff.gif",
        "title": "Seasonal runoff — the spring melt pulse",
        "what": "Monthly runoff / streamflow generation across the basin.",
        "read": "Most of the year's water enters the river during the spring melt pulse "
                "(Apr–Jun), concentrated in the high Upper-Basin headwaters. The arid lower "
                "basin generates very little runoff.",
        "data": "VIC reanalysis · daily runoff → monthly mean (WY2023)",
    },
    {
        "src": "/assets/animations/soil_moisture.gif",
        "title": "Seasonal soil moisture — wet ↔ dry",
        "what": "Total-column soil moisture (green = wet, brown = dry).",
        "read": "The basin wets up after snowmelt and dries steadily through the summer. "
                "Soil-moisture state controls how much of each storm actually becomes runoff.",
        "data": "VIC reanalysis · daily soil moisture → monthly mean (WY2023)",
    },
    {
        "src": "/assets/animations/drought_4decades.gif",
        "title": "Four decades of drought — 1984 → 2024",
        "what": "Annual runoff anomaly versus the 1984–2024 average, year by year.",
        "read": "Brown = drier than normal (drought), green = wetter. Severe drought years light "
                "up brown across the whole basin (e.g., WY2002 ≈ −62%), wet years green "
                "(e.g., WY2011 ≈ +54%). The recent decades show widespread, intensifying drought.",
        "data": "VIC reanalysis · annual runoff anomaly, WY1984–2024",
    },
    {
        "src": "/assets/animations/drainage_3d.gif",
        "title": "3D drainage & runoff relief (rotating)",
        "what": "A rotating 3D view: surface height = mean annual runoff; base = drainage network + dams.",
        "read": "Peaks are the high-runoff headwaters that generate the basin's water; the dark-blue "
                "network is the Colorado River drainage and red ▼ are major dams. Note: the surface "
                "is a hydrologic quantity (runoff), not land-surface elevation — a true terrain DEM "
                "is not bundled with the tool.",
        "data": "VIC reanalysis · mean annual runoff + Colorado River + 7 major dams",
    },
]


def _card(a):
    return html.Div([
        html.Div([
            html.Span(a["title"], style={"fontWeight": "700", "fontSize": "13.5px",
                                         "color": NAVY}),
        ], className="crb-card-header"),
        html.Div([
            html.Img(src=a["src"], style={"width": "100%", "maxWidth": "560px",
                                          "height": "auto", "display": "block",
                                          "margin": "0 auto", "borderRadius": "8px",
                                          "border": "1px solid #e2e8f0"}),
            html.Div([
                html.Div([html.B("What it shows:  "), a["what"]],
                         style={"fontSize": "12.5px", "marginTop": "10px", "color": "#1e293b"}),
                html.Div([html.B("How to read it:  "), a["read"]],
                         style={"fontSize": "12.5px", "marginTop": "6px", "color": "#1e293b",
                                "lineHeight": "1.5"}),
                html.Div([html.Span("Data: ", style={"fontWeight": "700"}), a["data"]],
                         style={"fontSize": "11px", "marginTop": "8px", "color": "#64748b",
                                "fontStyle": "italic"}),
            ], style={"padding": "4px 6px 2px"}),
        ], className="crb-card-body"),
    ], className="crb-card")


def layout():
    return html.Div([
        html.Div([
            html.H2("Seasonal & Drought Animations"),
            html.P("Watch the Colorado River Basin's water move through the seasons — and dry out "
                   "over four decades — built from the real PRISM-calibrated VIC reanalysis."),
        ], className="tab-header"),
        html.Div([
            html.Div([
                html.Span("In short — ", style={"fontWeight": "700"}),
                html.Span("these animations summarize the basin's whole water story: snow accumulates "
                          "and melts seasonally, runoff peaks in spring, soils wet and dry — and over "
                          "1984–2024 drought has become widespread and more frequent."),
            ], style={"background": "#e8f5e9", "border": "1px solid #a5d6a7",
                      "borderRadius": "6px", "padding": "10px 14px", "fontSize": "12.5px",
                      "color": "#1b5e20", "marginBottom": "12px"}),

            howto("Each clip loops automatically. The dark background is the basin; the cyan line is "
                  "the Colorado River drainage and red ▼ are major dams (Glen Canyon, Hoover, Flaming "
                  "Gorge, Navajo, Davis, Parker, Blue Mesa). Colour scales are fixed within each clip "
                  "so months / years are directly comparable."),

            dbc.Row([
                dbc.Col(_card(ANIMS[0]), xs=12, lg=6),
                dbc.Col(_card(ANIMS[1]), xs=12, lg=6),
            ], className="g-3"),
            dbc.Row([
                dbc.Col(_card(ANIMS[2]), xs=12, lg=6),
                dbc.Col(_card(ANIMS[3]), xs=12, lg=6),
            ], className="g-3"),
            dbc.Row([
                dbc.Col(_card(ANIMS[4]), xs=12, lg=6),
            ], className="g-3"),

            html.Div("All animations derive from the peer-reviewed VIC 5.0 PRISM-calibrated "
                     "reanalysis (NSE 0.96). Snow, runoff and soil-moisture clips are a single "
                     "representative water year (WY2023); the drought clip spans WY1984–2024. "
                     "Geographic maps are rendered tile-free, so they display in any browser.",
                     style={"fontSize": "10.5px", "color": "#64748b", "marginTop": "14px",
                            "fontStyle": "italic"}),
        ], className="tab-body"),
    ])


def register_callbacks(app):
    # Static animations — no callbacks required.
    return
