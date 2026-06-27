# ============================================================
# CRB DST — modules/reports.py
# Project & Reports Tab
# NASA Award 80NSSC22K0925
# "Managing the Colorado River as an Infrastructure Asset"
# ============================================================

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# ── Project constants ────────────────────────────────────────
PROJECT = {
    "title":   "Managing the Colorado River as an Infrastructure Asset",
    "subtitle":"Fusing Remote Sensing and Numerical Modeling in the Operations of the Central Arizona Project",
    "award":   "80NSSC22K0925",
    "program": "NASA Science Mission Directorate · Earth Science Division · Applied Sciences — Water Resources",
    "pi":      "Enrique R. Vivoni, Arizona State University",
    "start":   "April 15, 2022",
    "end":     "April 14, 2025",
    "budget":  "$1,049,993 / year  (3-year total ≈ $3.15M)",
    "arl_start": 3,
    "arl_current": 4,
    "arl_target": 7,
}

TEAM = [
    {"name": "Enrique R. Vivoni",  "role": "Project PI",              "aff": "ASU",         "expertise": "Hydrologic Modeling · Remote Sensing · Visualization"},
    {"name": "Giuseppe Mascaro",   "role": "Co-Investigator",         "aff": "ASU",         "expertise": "Remote Sensing · Climate Products · Biophysical Assets"},
    {"name": "Dave D. White",      "role": "Co-Investigator",         "aff": "ASU",         "expertise": "Stakeholder Engagement · Sociopolitical Assets"},
    {"name": "Vineetha Kartha",    "role": "Co-Investigator",         "aff": "CAWCD",       "expertise": "Decision-making · Water Management"},
    {"name": "Haowen Yue",         "role": "Postdoctoral Scholar",    "aff": "ASU",         "expertise": "VIC Modeling · Seasonal Forecasts · NMME"},
    {"name": "Zhaocheng Wang",     "role": "Graduate Researcher",     "aff": "ASU",         "expertise": "VIC · Climate Projections · Remote Sensing"},
    {"name": "Swastik Ghimire",    "role": "Graduate Researcher",     "aff": "ASU",         "expertise": "Drought Analysis · GRACE · Hydrological Modeling"},
    {"name": "Xinyu Chen",         "role": "Graduate Researcher",     "aff": "ASU",         "expertise": "CMIP5/CMIP6 · Hydroclimate · CRB Projections"},
    {"name": "Nour Kandalaft",     "role": "Graduate Researcher",     "aff": "ASU",         "expertise": "VIC · Earth Observation Datasets · CRB"},
    {"name": "Praddy Kaushik",     "role": "Postdoctoral Scholar",    "aff": "ASU",         "expertise": "Geospatial Data Science · Visualization · Decision-Support Tools"},
    {"name": "Kristen M. Whitney", "role": "Collaborator",            "aff": "NASA Goddard","expertise": "VIC · Streamflow Attribution · Visualization Tools"},
    {"name": "Krista Lawless",     "role": "Collaborator",            "aff": "ASU",         "expertise": "Water Governance · Policy Analysis"},
    {"name": "Ray Quay",           "role": "Collaborator",            "aff": "ASU",         "expertise": "Decision Support · Stakeholder Engagement"},
    {"name": "Nolie Templeton",    "role": "Collaborator",            "aff": "CAWCD",       "expertise": "Colorado River Programs · Stakeholder Liaison"},
    {"name": "Orestes Morfin",     "role": "End-User Engineer",       "aff": "CAWCD",       "expertise": "CRSS Modeling · Workflow Implementation"},
]

STAKEHOLDERS = [
    "Bureau of Reclamation (Federal)",
    "Arizona Dept. of Water Resources (State)",
    "Central Arizona Water Conservation District (CAWCD)",
    "Metropolitan Water District of Southern California",
    "Southern Nevada Water Authority",
    "Colorado River Board of California",
    "Denver Water",
    "Utah Division of Water Resources",
    "Wyoming State Engineer's Office",
    "New Mexico Interstate Stream Commission",
    "Upper Colorado River Commission",
    "Colorado River Water Conservation District",
    "Colorado River Commission of Nevada",
    "Colorado Dept. of Natural Resources",
    "CRB Climate and Hydrology Working Group",
]

TASKS = [
    {
        "id": 1,
        "name": "Remote Sensing & Modeling Updates",
        "icon": "",
        "color": "#8C1D40",
        "status": "On-going",
        "accomplishments": [
            "Evaluated 214 CMIP6-LOCA2 and 64 CMIP5-LOCA1 gridded projections against PRISM (2006–2022)",
            "Collected and processed GRACE TWS estimates for CRB (2002–present)",
            "Collected and processed SMAP surface soil moisture for CRB (2015–present)",
            "Investigated new precipitation partitioning scheme using wet bulb temperature",
            "Addressed permanent snow regions (glaciers) in snow-rainfall partitioning",
            "Evaluated AORC, MSWEP, and PRISM gridded precipitation products for VIC forcing",
            "Completed Phase 5 VIC modeling with updated snow-rainfall partitioning (Wang et al. 2024 manuscript)",
            "Identified top-performing CMIP5 and CMIP6 projections for CRB using Comprehensive Error Index",
        ],
        "products": ["Phase 5 VIC simulation outputs", "CMIP6 model ranking", "GRACE/SMAP data pipeline"],
    },
    {
        "id": 2,
        "name": "Short & Long-range Simulations",
        "icon": " ",
        "color": "#0D2137",
        "status": "On-going",
        "accomplishments": [
            "Developed working knowledge of Index Sequential Method (ISM) at Bureau of Reclamation",
            "Implemented and tested new Precipitation Partition Method (PPM) in VIC short and long-range runs",
            "Developed seasonal streamflow forecasts using NMME products across multiple lead times",
            "Evaluated 15 selected climate projections (best 3 per scenario: RCP4.5, RCP8.5, SSP245, SSP370, SSP585)",
            "Transitioned VIC forcing from Livneh et al. (2015) to PRISM-based meteorological data",
            "Compared NMME seasonal forecasts against ISM 24-month study for CAP operations",
        ],
        "products": ["NMME seasonal forecast system", "Long-range CMIP6 VIC scenarios", "CRSS tributary inputs"],
    },
    {
        "id": 3,
        "name": "Sociopolitical Analysis & Asset Framework",
        "icon": "",
        "color": "#2E7D32",
        "status": "On-going",
        "accomplishments": [
            "Developed prototype ShinyApp visualization environment for scenario modeling (Dec 2022 CoMods)",
            "Revised visualization based on stakeholder feedback from CAWCD, USBR, and state agencies",
            "Conducted water governance analysis of the Colorado River Basin from 1922 to 2022",
            "Developed current Python-Dash CRB Decision Support Tool (this application)",
            "Infrastructure Asset Framework established with biophysical + sociopolitical asset scoring",
        ],
        "products": ["ShinyApp prototype (Phase 1)", "CRB DST Dash app (Phase 2)", "Water governance analysis"],
    },
    {
        "id": 4,
        "name": "Decision Maker & Stakeholder Engagement",
        "icon": " ",
        "color": "#E65100",
        "status": "On-going",
        "accomplishments": [
            "Project kickoff presentation to CAWCD elected board (15 members, Sept 2022)",
            "Monthly meetings with CAWCD collaborators throughout summer 2023",
            "Presentations at Colorado River Climate and Hydrology Working Group (Salt Lake City)",
            "Stakeholder presentations in Grand Junction, CO and Mexicali, Mexico",
            "Stakeholder engagement planned for Farmington, NM",
            "Media outreach: radio, print, and video articles featuring CAWCD and ASU participants",
            "Provided peer-reviewed publications to stakeholder group for Special Issue on CRB Water Management",
            "CoMods activities planned for Spring-Summer 2024: rain-snow partitioning, NMME, drought, CMIP6",
        ],
        "products": ["14 stakeholder engagements", "Media articles", "2026 CRB Compact renegotiation support"],
    },
]

AWARDS = [
    {
        "awardee": "Project Team (ASU)",
        "award": "2023 Governor's Award for Arizona's Future",
        "org": "Arizona Forward Environmental Excellence Awards",
        "icon": " ",
    },
    {
        "awardee": "Zhaocheng Wang",
        "award": "2023 AZ Water Scholarship",
        "org": "Arizona Water Association",
        "icon": " ",
    },
    {
        "awardee": "Zhaocheng Wang",
        "award": "2023 Paul F. Boulos Excellence in Computational Hydraulics Award",
        "org": "ASCE",
        "icon": " ",
    },
    {
        "awardee": "Swastik Ghimire",
        "award": "2023 Academic Award",
        "org": "Arizona Hydrological Society",
        "icon": " ",
    },
    {
        "awardee": "Kristen Whitney",
        "award": "NASA Postdoctoral Fellowship",
        "org": "Hydrology Lab, Goddard Space Flight Center (March 2023–present)",
        "icon": " ",
    },
    {
        "awardee": "Kristen Whitney & Zhaocheng Wang",
        "award": "Babbitt Center for Land and Water Policy Dissertation Fellowship",
        "org": "Lincoln Institute of Land Policy",
        "icon": " ",
    },
    {
        "awardee": "State of Arizona (leveraged)",
        "award": "$40M Water Innovation Award",
        "org": "State of Arizona — advancing water innovation for AZ and CRB",
        "icon": " ",
    },
]

MILESTONES = [
    {"date": "Apr 2022",   "event": "Project Start (ARL 3 — Proof of Concept)",      "done": True},
    {"date": "Sept 2022",  "event": "Kickoff presentation to CAWCD board",           "done": True},
    {"date": "Dec 2022",   "event": "CoMods virtual meeting — ShinyApp prototype",    "done": True},
    {"date": "2022–2023",  "event": "Task 1: VIC Phase 5 forcing development",        "done": True},
    {"date": "2023 Q1",    "event": "Task 2: NMME seasonal forecast evaluation",      "done": True},
    {"date": "Summer 2023","event": "Task 4: Monthly CAWCD stakeholder meetings",     "done": True},
    {"date": "Fall 2023",  "event": "CRB Climate+Hydrology WG — Wang leads (SLC)",   "done": True},
    {"date": "Feb 2024",   "event": "Annual Review — ARL 4 achieved",                 "done": True},
    {"date": "Spring 2024","event": "CoMods: rain-snow, NMME, drought, CMIP6 analyses","done": True},
    {"date": "2024",       "event": "Wang et al. — Snow-Rainfall Partitioning paper (WRR)",  "done": True},
    {"date": "2025",       "event": "CRB DST Python-Dash dashboard deployed",         "done": True},
    {"date": "2026",       "event": "Ghimire/Wang et al. Scientific Reports — VIC+SMAP+GRACE published", "done": True},
    {"date": "Apr 2025",   "event": "Project End Target (ARL 7 — Integration into Partner's System)",    "done": False},
    {"date": "2026",       "event": "Colorado River Compact Renegotiation (key stakeholder milestone)",   "done": False},
]

BUDGET_DATA = {
    "periods": ["Apr 2022–Feb 2023", "Mar 2023–Feb 2024"],
    "budgeted": [1_049_993, 1_049_993],
    "obligated": [350_074, 709_524],
    "costed": [20_786, 386_040],
}

NASA_DATA = {
    "products": [
        ("MODIS NDVI, LAI, Albedo", "Surface parameters",         "MOD13Q1, 15A2H, 43A3"),
        ("MODIS LST / ECOSTRESS ET","Surface temp & ET",          "MYD11A2/ECO2LSTE; 8-d"),
        ("MODIS Snow Cover",        "Snow assimilation",          "MOD10A2; 8-d, 500m"),
        ("SMAP (SPL3SMP/SPL3SMP_E)","Soil moisture",             "1-d, 9- and 36-km"),
        ("NLCD Land Cover",         "Land classification",        "2001, 2011, 2016; 30m"),
        ("NMME",                    "Seasonal forecasts",         "6 models, 1-d, 50km"),
        ("PRISM",                   "Meteorological forcing",     "Daily, 4km"),
        ("GRACE JPL RL06 Mascons",  "Terrestrial water storage",  "Monthly, ~300km"),
        ("LOCA2 (CMIP6)",           "Long-range projections",     "214 models, 1-d, 6km"),
        ("LOCA1 (CMIP5)",           "Long-range projections",     "64 models, 1-d, 6km"),
    ]
}

# ── Project documents (summarized in-app; originals not publicly distributed) ──
# Each report is summarized as graph/info content in-app. "covers" = topic chips,
# "results" = key findings, "see" = (label, route) links to the in-app tab that
# shows it as live graphs.
DOCUMENTS = [
    {"file": "AnnualProgressReport_WR_Feb2025.pdf",
     "title": "Annual Progress Report — Feb 2025",
     "tag": "Year-3 RPPR",
     "desc": "The most complete write-up: remote-sensing evaluation, seasonal forecasts, "
             "long-range projections and the CRIA prototype.",
     "covers": ["VIC–SMAP evaluation", "NMME+VIC forecasts", "CMIP5/CMIP6 projections", "CRIA framework"],
     "results": [
         "VIC vs SMAP soil moisture: R²=0.71 (surface), 0.81 (root-zone); streamflow NSE=0.96.",
         "NMME+VIC 9-month streamflow forecasts match or beat the USBR 24-Month Study.",
         "8+8 top GCMs selected; 5 of 6 scenarios project declining runoff by 2066–2095.",
     ],
     "see": [("Seasonal Forecasts", "/nmme"), ("Climate Projections", "/cmip")],
     "size": "2.0 MB"},
    {"file": "NASA_WR_QuarterlyReview_November2024.pptx",
     "title": "Quarterly Review — Nov 2024",
     "tag": "Slides",
     "desc": "Quarterly progress review: model screening tables and the projected-change figure.",
     "covers": ["CMIP model ranking", "Projected ΔP / ΔRunoff / ΔSM", "Phase-5 VIC"],
     "results": [
         "214 CMIP6-LOCA2 + 64 CMIP5-LOCA1 projections screened to the best 8 per family.",
         "Comprehensive Error Index ranks models against PRISM (1976–2005).",
         "CMIP5 spread encompasses CMIP6; CMIP6 has the lower spread.",
     ],
     "see": [("Climate Projections", "/cmip")],
     "size": "3.8 MB"},
    {"file": "NASA_WR_AnnualReview_Feb2024.pdf",
     "title": "Annual Review — Feb 2024",
     "tag": "Year-2",
     "desc": "Year-2 review (30 pp): objectives, accomplishments and stakeholder engagement.",
     "covers": ["Objectives 1–4", "Snow–rain partitioning", "Stakeholder engagement"],
     "results": [
         "ARL advanced from 3 → 4 (development & testing phase).",
         "New precipitation-partition method tested in VIC short- and long-range runs.",
         "14 stakeholder engagements across the basin states.",
     ],
     "see": [("Project tasks", "/reports")],
     "size": "2.5 MB"},
    {"file": "NASAWaterResources2021.pdf",
     "title": "NASA Water Resources — 2021",
     "tag": "Background",
     "desc": "Program / proposal background that framed the CRIA effort.",
     "covers": ["Infrastructure-asset concept", "Program scope"],
     "results": [
         "Frames the Colorado River as an infrastructure asset (biophysical + sociopolitical).",
         "Sets the NASA Applied Sciences — Water Resources objectives the project delivers on.",
     ],
     "see": [("Project overview", "/reports")],
     "size": "7.5 MB"},
]


# ── ARL gauge ────────────────────────────────────────────────
def make_arl_gauge():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=PROJECT["arl_current"],
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Application Readiness Level", "font": {"size": 13, "color": "#1e293b"}},
        gauge={
            "axis": {"range": [1, 9], "tickwidth": 1, "tickcolor": "#475569",
                     "tickvals": list(range(1, 10)), "tickfont": {"size": 11}},
            "bar": {"color": "#8C1D40", "thickness": 0.25},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "#e2e8f0",
            "steps": [
                {"range": [1, 3],  "color": "#fce7f3", "name": "Phase I: Discovery"},
                {"range": [3, 6],  "color": "#fed7aa", "name": "Phase II: Dev/Test"},
                {"range": [6, 9],  "color": "#d1fae5", "name": "Phase III: Integration"},
            ],
            "threshold": {
                "line": {"color": "#FFC627", "width": 4},
                "thickness": 0.75,
                "value": PROJECT["arl_target"],
            },
        },
        number={"font": {"size": 36, "color": "#8C1D40"}},
    ))
    fig.update_layout(
        height=220,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        annotations=[
            dict(x=0.5, y=-0.12, xref="paper", yref="paper",
                 text="<span style='color:#8C1D40'>■ Current (4)</span>  ""<span style='color:#FFC627'>| Target (7)</span>",
                 showarrow=False, font=dict(size=11), xanchor="center"),
        ],
    )
    return fig


# ── Budget chart ──────────────────────────────────────────────
def make_budget_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Budgeted",
        x=BUDGET_DATA["periods"],
        y=BUDGET_DATA["budgeted"],
        marker_color="#e2e8f0",
        text=["$1,049,993", "$1,049,993"],
        textposition="outside",
        textfont=dict(size=10, color="#475569"),
    ))
    fig.add_trace(go.Bar(
        name="Obligated",
        x=BUDGET_DATA["periods"],
        y=BUDGET_DATA["obligated"],
        marker_color="#0D2137",
        text=["$350,074", "$709,524"],
        textposition="outside",
        textfont=dict(size=10, color="#0D2137"),
    ))
    fig.add_trace(go.Bar(
        name="Costed",
        x=BUDGET_DATA["periods"],
        y=BUDGET_DATA["costed"],
        marker_color="#8C1D40",
        text=["$20,786", "$386,040"],
        textposition="outside",
        textfont=dict(size=10, color="#8C1D40"),
    ))
    fig.update_layout(
        barmode="group",
        height=260,
        title=dict(text="Budget Status by Period (ASU)", font=dict(size=13)),
        yaxis=dict(title="USD ($)", tickformat="$,.0f", showgrid=True, gridcolor="#f0f0f0"),
        xaxis=dict(showgrid=False),
        margin=dict(l=60, r=20, t=40, b=40),
        legend=dict(orientation="h", y=1.12, x=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", size=11),
    )
    return fig


# ── Timeline chart ───────────────────────────────────────────
def make_timeline_chart():
    done = [m for m in MILESTONES if m["done"]]
    pending = [m for m in MILESTONES if not m["done"]]

    fig = go.Figure()

    # Completed milestones
    fig.add_trace(go.Scatter(
        x=list(range(len(done))),
        y=[0] * len(done),
        mode="markers+text",
        marker=dict(size=18, color="#8C1D40", symbol="circle",
                    line=dict(color="white", width=2)),
        text=[" "] * len(done),
        textfont=dict(size=9, color="white"),
        textposition="middle center",
        hovertext=[f"<b>{m['date']}</b><br>{m['event']}" for m in done],
        hoverinfo="text",
        name="Completed",
    ))

    # Pending milestones
    offset = len(done)
    fig.add_trace(go.Scatter(
        x=list(range(offset, offset + len(pending))),
        y=[0] * len(pending),
        mode="markers+text",
        marker=dict(size=18, color="#FFC627", symbol="circle",
                    line=dict(color="#8C1D40", width=2)),
        text=["⧖"] * len(pending),
        textfont=dict(size=10, color="#8C1D40"),
        textposition="middle center",
        hovertext=[f"<b>{m['date']}</b><br>{m['event']}" for m in pending],
        hoverinfo="text",
        name="Upcoming",
    ))

    all_m = done + pending
    for i, m in enumerate(all_m):
        fig.add_annotation(
            x=i, y=0.22 if i % 2 == 0 else -0.28,
            text=f"<b>{m['date']}</b><br>{m['event'][:45]}{'…' if len(m['event']) > 45 else ''}",
            showarrow=True,
            arrowhead=0,
            arrowcolor="#cbd5e1",
            arrowwidth=1,
            ax=0,
            ay=-30 if i % 2 == 0 else 30,
            font=dict(size=9, color="#1e293b"),
            align="center",
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            borderpad=3,
        )

    fig.update_layout(
        height=400,
        title=dict(text="Project Timeline & Milestones", font=dict(size=13)),
        xaxis=dict(visible=False, range=[-0.5, len(all_m) - 0.5]),
        yaxis=dict(visible=False, range=[-0.6, 0.6]),
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        legend=dict(orientation="h", y=-0.05, x=0.4),
        shapes=[
            dict(type="line", x0=-0.3, x1=len(all_m) - 0.7,
                 y0=0, y1=0, line=dict(color="#cbd5e1", width=2)),
        ],
    )
    return fig


# ── Impact tiles ─────────────────────────────────────────────
def make_impact_section():
    impacts = [
        {"v": "40M+",   "l": "People Served by CRB Water", "i": " ", "c": "tile-maroon"},
        {"v": "5.5M ac","l": "Acres of Irrigated Agriculture","i":" ","c": "tile-navy"},
        {"v": "4,180MW","l": "Hydropower Capacity",         "i": " ", "c": "tile-green"},
        {"v": "7 States","l": "Upper + Lower Basin States",  "i": "","c": "tile-gold"},
        {"v": "9 States","l": "Total CRB Jurisdiction",     "i": " ", "c": "tile-maroon"},
        {"v": "22 Tribes","l":"Indian Tribes with Water Rights","i":"","c":"tile-navy"},
        {"v": "$3.15M", "l": "NASA Investment",             "i": " ", "c": "tile-green"},
        {"v": "$40M",   "l": "Leveraged State Funding",     "i": " ", "c": "tile-gold"},
    ]
    return dbc.Row([
        dbc.Col(
            html.Div([
                html.Div(t["i"], className="info-tile-icon"),
                html.Div(t["v"], className="info-tile-value"),
                html.Div(t["l"], className="info-tile-label"),
            ], className=f"info-tile {t['c']}"),
            xs=6, sm=4, md=3
        )
        for t in impacts
    ], className="g-2 mb-3")


# ── Layout ───────────────────────────────────────────────────
def layout():
    # Task cards
    task_cards = []
    for t in TASKS:
        acc_items = [
            html.Li(a, style={"fontSize": "12px", "color": "#1e293b",
                              "marginBottom": "4px", "lineHeight": "1.45"})
            for a in t["accomplishments"]
        ]
        prod_badges = [
            html.Span(p, style={"background": "#f1f5f9", "borderRadius": "10px",
                                "padding": "2px 8px", "fontSize": "11px",
                                "color": "#0D2137", "fontWeight": "500",
                                "border": "1px solid #e2e8f0"})
            for p in t["products"]
        ]
        task_cards.append(
            html.Div([
                html.Div([
                    html.Span(t["icon"], style={"fontSize": "20px", "marginRight": "10px"}),
                    html.Span(f"Task {t['id']}: {t['name']}",
                              style={"fontSize": "14px", "fontWeight": "700",
                                     "color": "white"}),
                    html.Span(t["status"],
                              style={"marginLeft": "auto", "fontSize": "11px",
                                     "background": "rgba(255,255,255,0.25)",
                                     "padding": "2px 8px", "borderRadius": "10px",
                                     "color": "white"}),
                ], style={"display": "flex", "alignItems": "center",
                          "background": t["color"],
                          "padding": "10px 14px", "borderRadius": "8px 8px 0 0"}),
                html.Div([
                    html.Ul(acc_items, style={"paddingLeft": "18px", "marginBottom": "8px"}),
                    html.Div([
                        html.Span("Products: ", style={"fontSize": "11px", "fontWeight": "700",
                                                        "color": "#1e293b", "marginRight": "6px"}),
                        *prod_badges,
                    ], style={"display": "flex", "flexWrap": "wrap",
                              "gap": "4px", "alignItems": "center"}),
                ], style={"padding": "12px 14px", "background": "white",
                          "borderRadius": "0 0 8px 8px",
                          "border": f"1px solid {t['color']}30",
                          "borderTop": "none"}),
            ], style={"borderRadius": "8px", "overflow": "hidden",
                      "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
                      "marginBottom": "12px"})
        )

    # Team table rows
    team_rows = [
        html.Tr([
            html.Td(m["name"], style={"fontWeight": "600", "fontSize": "12px",
                                      "color": "#1e293b", "padding": "7px 10px"}),
            html.Td(m["role"], style={"fontSize": "12px", "color": "#1e293b",
                                      "padding": "7px 10px"}),
            html.Td(m["aff"], style={"fontSize": "12px", "fontWeight": "600",
                                     "color": "#8C1D40", "padding": "7px 10px"}),
            html.Td(m["expertise"], style={"fontSize": "11px", "color": "#1e293b",
                                           "padding": "7px 10px"}),
        ])
        for m in TEAM
    ]

    # Stakeholder chips
    stakeholder_chips = html.Div([
        html.Span(s, style={"background": "#f8fafc", "border": "1px solid #e2e8f0",
                            "borderRadius": "16px", "padding": "4px 12px",
                            "fontSize": "12px", "color": "#0D2137",
                            "fontWeight": "500"})
        for s in STAKEHOLDERS
    ], style={"display": "flex", "flexWrap": "wrap", "gap": "6px"})

    # Awards cards
    award_cards = dbc.Row([
        dbc.Col(
            html.Div([
                html.Div(a["icon"], style={"fontSize": "24px", "marginBottom": "6px"}),
                html.Div(a["award"],
                         style={"fontSize": "12px", "fontWeight": "700",
                                "color": "#1e293b", "marginBottom": "3px",
                                "lineHeight": "1.35"}),
                html.Div(a["awardee"],
                         style={"fontSize": "11px", "color": "#8C1D40",
                                "fontWeight": "600", "marginBottom": "3px"}),
                html.Div(a["org"],
                         style={"fontSize": "11px", "color": "#1e293b"}),
            ], style={"background": "white", "border": "1px solid #e2e8f0",
                      "borderTop": "3px solid #FFC627",
                      "borderRadius": "8px", "padding": "12px",
                      "boxShadow": "0 2px 6px rgba(0,0,0,0.06)",
                      "height": "100%", "textAlign": "center"}),
            xs=12, sm=6, md=4, className="mb-3")
        for a in AWARDS
    ], className="g-2")

    # NASA data products table
    data_rows = [
        html.Tr([
            html.Td(row[0], style={"fontWeight": "600", "fontSize": "12px",
                                   "color": "#1e293b", "padding": "6px 10px"}),
            html.Td(row[1], style={"fontSize": "12px", "color": "#1e293b",
                                   "padding": "6px 10px"}),
            html.Td(row[2], style={"fontSize": "11px", "color": "#1e293b",
                                   "fontFamily": "monospace", "padding": "6px 10px"}),
        ])
        for row in NASA_DATA["products"]
    ]

    def section_head(icon, title):
        return html.Div([
            html.Span(icon, style={"fontSize": "18px", "marginRight": "8px"}),
            html.Span(title, style={"fontSize": "15px", "fontWeight": "700",
                                    "color": "#1e293b"}),
        ], style={"borderBottom": "2px solid #8C1D40",
                  "paddingBottom": "6px", "marginBottom": "12px",
                  "display": "flex", "alignItems": "center"})

    return html.Div([
        # Header
        html.Div([
            html.H2("Project & Reports"),
            html.P(
                "NASA Earth Science Division · Applied Sciences — Water Resources  |  "
                f"Award {PROJECT['award']}  |  PI: Prof. Enrique R. Vivoni, ASU"),
        ], className="tab-header"),

        html.Div([
            # ── Row 1: Project overview tiles ──────────────────
            html.Div([
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div(PROJECT["award"], className="info-tile-value",
                             style={"fontSize": "13px"}),
                    html.Div("NASA Award Number", className="info-tile-label"),
                ], className="info-tile tile-maroon"),
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div("3 Years", className="info-tile-value"),
                    html.Div(f"{PROJECT['start']} {PROJECT['end']}", className="info-tile-label"),
                ], className="info-tile tile-navy"),
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div("~$3.15M", className="info-tile-value"),
                    html.Div("Total NASA Funding", className="info-tile-label"),
                ], className="info-tile tile-green"),
                html.Div([
                    html.Div(" ", className="info-tile-icon"),
                    html.Div("ARL 4 7", className="info-tile-value"),
                    html.Div("Application Readiness Level", className="info-tile-label"),
                ], className="info-tile tile-gold"),
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div("11 Papers", className="info-tile-value"),
                    html.Div("Published + In Prep", className="info-tile-label"),
                ], className="info-tile tile-maroon"),
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div("15 Orgs", className="info-tile-value"),
                    html.Div("Stakeholders Engaged", className="info-tile-label"),
                ], className="info-tile tile-navy"),
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div("7 Awards", className="info-tile-value"),
                    html.Div("Team Recognition", className="info-tile-label"),
                ], className="info-tile tile-green"),
                html.Div([
                    html.Div("", className="info-tile-icon"),
                    html.Div("640k km²", className="info-tile-value"),
                    html.Div("CRB Study Area", className="info-tile-label"),
                ], className="info-tile tile-gold"),
            ], style={"display": "grid",
                      "gridTemplateColumns": "repeat(auto-fill, minmax(130px, 1fr))",
                      "gap": "8px", "marginBottom": "16px"}),

            # ── Row 2: Project title card ───────────────────────
            html.Div([
                html.Div([
                    html.Img(src="/assets/img/nasa-logo.webp",
                             style={"height": "40px", "objectFit": "contain",
                                    "marginRight": "12px"}),
                    html.Div([
                        html.H5(PROJECT["title"],
                                style={"fontSize": "14px", "fontWeight": "800",
                                       "color": "#8C1D40", "marginBottom": "3px",
                                       "lineHeight": "1.35"}),
                        html.P(PROJECT["subtitle"],
                               style={"fontSize": "12px", "color": "#1e293b",
                                      "marginBottom": "4px", "fontStyle": "italic"}),
                        html.P(PROJECT["program"],
                               style={"fontSize": "11px", "color": "#1e293b",
                                      "marginBottom": "0"}),
                    ]),
                ], style={"display": "flex", "alignItems": "flex-start"}),
            ], className="crb-card", style={"marginBottom": "16px"}),

            # ── Project documents (what's inside, as graph/info) ──
            html.Div([
                section_head("", "Project Reports — What's Inside"),
                html.Div(
                    "Each NASA report is summarized below as readable info — what it covers and its "
                    "key results — with links to the in-app tabs that show that content as live, "
                    "interactive graphs. The original file is available as a download if you need it.",
                    style={"fontSize": "11.5px", "color": "#1e293b", "marginBottom": "12px",
                           "lineHeight": "1.5"}),
                dbc.Row([
                    dbc.Col(html.Div([
                        # header strip
                        html.Div([
                            html.Span(d["title"], style={"fontWeight": "700", "fontSize": "12.5px",
                                                         "color": "white"}),
                            html.Span(d["tag"], style={"marginLeft": "auto", "fontSize": "10px",
                                "background": "rgba(255,255,255,0.25)", "color": "white",
                                "padding": "1px 8px", "borderRadius": "10px"}),
                        ], style={"display": "flex", "alignItems": "center", "background": "#0D2137",
                                  "padding": "8px 12px", "borderRadius": "8px 8px 0 0"}),
                        html.Div([
                            html.Div(d["desc"], style={"fontSize": "11px", "color": "#1e293b",
                                "lineHeight": "1.45", "marginBottom": "8px"}),
                            # topic chips
                            html.Div([html.Span(c, style={"background": "#eef2f7", "border": "1px solid #e2e8f0",
                                "borderRadius": "10px", "padding": "2px 8px", "fontSize": "10px",
                                "color": "#0D2137", "marginRight": "4px", "marginBottom": "4px",
                                "display": "inline-block"}) for c in d["covers"]],
                                style={"marginBottom": "8px"}),
                            # key results
                            html.Div("Key results", style={"fontSize": "10px", "fontWeight": "700",
                                "color": "#8C1D40", "textTransform": "uppercase", "letterSpacing": "0.5px",
                                "marginBottom": "3px"}),
                            html.Ul([html.Li(r, style={"fontSize": "11px", "color": "#37474f",
                                "marginBottom": "3px", "lineHeight": "1.4"}) for r in d["results"]],
                                style={"paddingLeft": "16px", "marginBottom": "8px"}),
                            # in-app links + download
                            html.Div([
                                html.Span("See as graphs: ", style={"fontSize": "10.5px",
                                    "fontWeight": "600", "color": "#1e293b"}),
                                *[html.A(lbl, href=route, style={"fontSize": "10.5px",
                                    "fontWeight": "600", "color": "#01579B", "marginRight": "8px",
                                    "textDecoration": "underline"}) for lbl, route in d["see"]],
                            ], style={"marginBottom": "4px"}),
                            html.Div("Internal project document — summarized here; original not publicly distributed.",
                                     style={"fontSize": "10px", "color": "#94a3b8",
                                            "fontStyle": "italic"}),
                        ], style={"padding": "10px 12px", "background": "white",
                                  "border": "1px solid #e2e8f0", "borderTop": "none",
                                  "borderRadius": "0 0 8px 8px"}),
                    ], style={"height": "100%", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)",
                              "borderRadius": "8px", "overflow": "hidden"}),
                    md=6, className="mb-3")
                    for d in DOCUMENTS
                ], className="g-3"),
            ], className="crb-card", style={"marginBottom": "16px"}),

            # ── Row 3: ARL gauge + budget chart ────────────────
            dbc.Row([
                dbc.Col([
                    html.Div([
                        section_head("", "Application Readiness"),
                        dcc.Graph(figure=make_arl_gauge(), config={"displayModeBar": False}),
                        html.Div([
                            html.P("Phase I (ARL 1–3): Discovery & Feasibility",
                                   style={"fontSize": "11px", "color": "#1e293b", "marginBottom": "2px"}),
                            html.P("Phase II (ARL 4–6): Development, Testing & Validation",
                                   style={"fontSize": "11px", "color": "#1e293b", "marginBottom": "2px"}),
                            html.P("Phase III (ARL 7–9): Integration into Partner's System",
                                   style={"fontSize": "11px", "color": "#1e293b", "marginBottom": "0"}),
                        ], style={"marginTop": "8px"}),
                    ], className="crb-card"),
                ], md=5),
                dbc.Col([
                    html.Div([
                        section_head("", "Budget Status"),
                        dcc.Graph(figure=make_budget_chart(), config={"displayModeBar": False}),
                    ], className="crb-card"),
                ], md=7),
            ], className="g-3 mb-3"),

            # ── Row 4: Timeline ─────────────────────────────────
            dbc.Row([
                dbc.Col([
                    html.Div([
                        section_head("", "Milestone Timeline"),
                        dcc.Graph(figure=make_timeline_chart(), config={"displayModeBar": False}),
                    ], className="crb-card"),
                ], md=12),
            ], className="g-3 mb-3"),

            # ── Row 5: 4 Task cards ─────────────────────────────
            html.Div(section_head(" ", "Project Tasks & Accomplishments"), style={"marginBottom": "4px"}),
            dbc.Row([
                dbc.Col(task_cards[:2], md=6),
                dbc.Col(task_cards[2:], md=6),
            ], className="g-3 mb-3"),

            # ── Row 6: Impact ───────────────────────────────────
            html.Div(section_head("", "Project Impact — The Colorado River System"), style={"marginBottom": "8px"}),
            html.Div([
                html.P(
                    "The Colorado River Basin serves as the primary water source for over 40 million people ""across 7 U.S. states and Mexico, irrigates 5.5 million acres of agriculture, and generates ""4,180 MW of hydroelectric power. The 2022 Tier 1 shortage declaration — unprecedented in ""CRB history — triggered this project. By fusing NASA Earth observations with the ""Variable Infiltration Capacity (VIC) hydrologic model and the Colorado River ""Simulation System (CRSS), this project delivers actionable science to support ""water management decisions ahead of the 2026 Colorado River Compact renegotiation.",
                    style={"fontSize": "12px", "color": "#1e293b", "lineHeight": "1.6",
                           "marginBottom": "12px"}
                ),
                make_impact_section(),
            ], className="crb-card", style={"marginBottom": "16px"}),

            # ── Row 7: Awards ────────────────────────────────────
            html.Div(section_head("", "Awards & Recognition"), style={"marginBottom": "8px"}),
            html.Div([award_cards], className="crb-card", style={"marginBottom": "16px"}),

            # ── Row 8: NASA data products ────────────────────────
            html.Div(section_head(" ", "NASA Earth Observation Products Used"), style={"marginBottom": "8px"}),
            html.Div([
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("Product / Model", style={"background": "#8C1D40", "color": "white",
                                                           "padding": "8px 10px", "fontSize": "12px"}),
                        html.Th("Application",     style={"background": "#8C1D40", "color": "white",
                                                           "padding": "8px 10px", "fontSize": "12px"}),
                        html.Th("Specification",   style={"background": "#8C1D40", "color": "white",
                                                           "padding": "8px 10px", "fontSize": "12px"}),
                    ])),
                    html.Tbody(data_rows),
                ], style={"width": "100%", "borderCollapse": "collapse",
                          "fontSize": "12px"}),
            ], className="crb-card", style={"marginBottom": "16px"}),

            # ── Row 9: Stakeholders ──────────────────────────────
            html.Div(section_head("", "End-Users & Stakeholder Organizations"), style={"marginBottom": "8px"}),
            html.Div([stakeholder_chips], className="crb-card", style={"marginBottom": "16px"}),

            # ── Row 10: Team ─────────────────────────────────────
            html.Div(section_head("", "Project Team"), style={"marginBottom": "8px"}),
            html.Div([
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("Name",      style={"background": "#0D2137", "color": "white",
                                                    "padding": "8px 10px", "fontSize": "12px"}),
                        html.Th("Role",      style={"background": "#0D2137", "color": "white",
                                                    "padding": "8px 10px", "fontSize": "12px"}),
                        html.Th("Affil.",    style={"background": "#0D2137", "color": "white",
                                                    "padding": "8px 10px", "fontSize": "12px"}),
                        html.Th("Expertise", style={"background": "#0D2137", "color": "white",
                                                    "padding": "8px 10px", "fontSize": "12px"}),
                    ])),
                    html.Tbody(team_rows),
                ], style={"width": "100%", "borderCollapse": "collapse",
                          "fontSize": "12px"}),
            ], className="crb-card"),

        ], className="tab-body"),
    ])


def register_callbacks(app):
    pass  # Reports tab is static — all content from PDF data
