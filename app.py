# ============================================================
# CRB DST — app.py
# Colorado River Basin Decision Support Tool
# Python Dash + HuggingFace Spaces deployment
# ============================================================

import dash
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.io as pio
# ── App init ─────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"],
    suppress_callback_exceptions=True,
    title="CRIA — Decision Support Tool",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server  # for gunicorn

# ── Custom Plotly theme (same feel as CRB-WRDST) ────────────
import plotly.graph_objects as go

crb_template = go.layout.Template()
crb_template.layout = go.Layout(
    font=dict(family="Inter, sans-serif", size=12, color="#1e293b"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    # richer, professional colorway
    colorway=["#8C1D40","#01579B","#2E7D32","#E65100","#4527A0","#00838F","#C62828","#00695C"],
    xaxis=dict(showgrid=True, gridcolor="#eef2f6", gridwidth=1, linecolor="#e0e0e0",
               tickfont=dict(size=11), zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#eef2f6", gridwidth=1, linecolor="#e0e0e0",
               tickfont=dict(size=11), zeroline=False),
    margin=dict(l=50, r=20, t=40, b=40),
    legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#e0e0e0", borderwidth=1,
                font=dict(size=11)),
    # polished rounded bars + clean hover + smooth transitions on update
    barcornerradius=6,
    bargap=0.28,
    hovermode="closest",
    hoverlabel=dict(bgcolor="white", bordercolor="#cfd8dc", font_size=12,
                    font_family="Inter, sans-serif"),
    transition=dict(duration=450, easing="cubic-in-out"),
)
# default bar styling — no harsh outlines
crb_template.data.bar = [go.Bar(marker=dict(line=dict(width=0)))]
pio.templates["crb"] = crb_template
pio.templates.default = "crb"# ── Basin + Variable dictionaries ───────────────────────────
BASINS = {
    "CRB":        "Colorado River Basin",
    "UpperBasin": "Upper Basin",
    "LowerBasin": "Lower Basin",
    "Green":      "Green River",
    "SanJuan":    "San Juan",
    "GrandCanyon":"Grand Canyon",
    "Gila":       "Gila River",
}

VIC_VARS = {
    "OUT_PREC":      {"label": "Precipitation",        "unit": "mm/yr",   "color": "#0D2137"},
    "OUT_RUNOFF":    {"label": "Surface Runoff",        "unit": "mm/yr",   "color": "#8C1D40"},
    "OUT_BASEFLOW":  {"label": "Baseflow",              "unit": "mm/yr",   "color": "#4527A0"},
    "OUT_EVAP":      {"label": "Total ET",              "unit": "mm/yr",   "color": "#2E7D32"},
    "OUT_EVAP_CANOP":{"label": "Canopy Evaporation",   "unit": "mm/yr",   "color": "#388E3C"},
    "OUT_TRANSP_VEG":{"label": "Transpiration",         "unit": "mm/yr",   "color": "#1B5E20"},
    "OUT_EVAP_BARE": {"label": "Bare Soil Evaporation", "unit": "mm/yr",   "color": "#A5D6A7"},
    "OUT_SWE":       {"label": "Snow Water Equiv (SWE)","unit": "mm",      "color": "#01579B"},
    "OUT_SNOW_MELT": {"label": "Snowmelt",              "unit": "mm/yr",   "color": "#0288D1"},
    "OUT_SOIL_MOIST":{"label": "Soil Moisture",         "unit": "mm",      "color": "#E65100"},
    "OUT_AIR_TEMP":  {"label": "Air Temperature",       "unit": "°C",      "color": "#C62828"},
    "OUT_LATENT":    {"label": "Latent Heat Flux",      "unit": "W/m²",    "color": "#00695C"},
}

# ── Navigation structure ─────────────────────────────────────
# Per-view metadata: route key → (sub-tab label, sidebar/section icon)
VIEW_LABELS = {
    "home":          ("Basin Overview",                       "bi-water"),
    "snowpack":      ("Snowpack & Runoff",                    "bi-snow"),
    "watbal":        ("Water Balance",                        "bi-droplet"),
    "timing":        ("Snowmelt Timing & Flash Drought",      "bi-calendar3"),
    "links":         ("Soil Moisture–Streamflow Coupling",    "bi-link-45deg"),
    "elevsnow":      ("Elevation-Dependent Snow Loss",        "bi-graph-down-arrow"),
    "warming":       ("Land-Surface Warming & Energy",        "bi-thermometer-high"),
    "references":    ("References & Validation",              "bi-journal-check"),
    "tws":           ("Terrestrial Water Storage (GRACE)",    "bi-globe-americas"),
    "storage":       ("Subsurface Storage (GW + reservoir)",   "bi-bank"),
    "drought":       ("Drought & Shortage Risk",              "bi-exclamation-triangle"),
    "cascade":       ("Drought Propagation",                  "bi-diagram-3"),
    "recovery":      ("Drought Recovery (WY2023)",            "bi-arrow-repeat"),
    "aridification": ("Aridification & Runoff Loss",          "bi-thermometer-sun"),
    "asi":           ("Aridity Severity Index",               "bi-bar-chart-steps"),
    "budyko":        ("Budyko Water–Energy Balance",          "bi-vector-pen"),
    "scenario":      ("Climate-Sensitivity Scenario",         "bi-sliders"),
    "future":        ("Hydrologic Projections to 2100",       "bi-graph-up-arrow"),
    "noanalog":      ("No-Analog Future Climate",             "bi-eye"),
    "nmme":          ("Seasonal Streamflow Forecasts (NMME)", "bi-cloud-drizzle"),
    "cmip":          ("Climate-Change Projections (CMIP5/6)", "bi-thermometer-half"),
    "cria":          ("CRIA Asset Framework",                 "bi-diagram-3-fill"),
    "governance":    ("Water Governance",                     "bi-bank2"),
    "reservoirs":    ("Reservoirs & Shortage Tiers",          "bi-moisture"),
    "uncertainty":   ("Uncertainty & Confidence",             "bi-plusminus"),
    "spatial":       ("Spatial Hydrology Maps",               "bi-map"),
    "animations":    ("Seasonal & Drought Animations",        "bi-play-circle"),
    "methods":       ("Methods & Data Sources",               "bi-book"),
    "publications":  ("Publications",                         "bi-journals"),
    "reports":       ("Project & Reports",                    "bi-clipboard-data"),
}

# 7 top-level groups. Each group's first view is its landing route.
# Decision-first order for stakeholders. Every multi-view group uses a dropdown menu
# (the user picks an analysis from the menu — nothing is shown until chosen).
# ── Six clear, decision-framed sections (the questions a manager/scientist asks) ──
GROUPS = [
    {"key": "home",    "label": "Overview",            "icon": "bi-house-door",
     "question": "Start here",
     "views": ["home"],
     "desc": "Start here — the three questions this tool answers, then open any analysis."},
    {"key": "water",   "label": "Water Supply & Snow", "icon": "bi-droplet",
     "question": "How much water is there?",
     "views": ["snowpack", "watbal", "timing", "links", "elevsnow", "budyko"],
     "desc": "Where the water comes from — snowpack-to-runoff, the water balance, snowmelt "
             "timing, soil-moisture controls, and the Budyko water–energy partition."},
    {"key": "risk",    "label": "Drought & Risk",      "icon": "bi-exclamation-triangle",
     "question": "How severe is the stress?",
     "views": ["drought", "reservoirs", "tws", "storage", "recovery", "cascade",
               "aridification", "asi", "warming"],
     "desc": "Supply security and stress — drought & shortage risk, reservoir tiers, terrestrial "
             "& groundwater storage, recovery, drought propagation, and long-term aridification."},
    {"key": "future",  "label": "Scenarios & Future",  "icon": "bi-sliders",
     "question": "What happens under change?",
     "views": ["scenario", "uncertainty", "future", "cmip", "nmme", "noanalog"],
     "desc": "The decision centerpiece — dial a warming / precipitation change and see the projected "
             "streamflow response (with confidence), plus projections, climate scenarios and forecasts."},
    {"key": "spatial", "label": "Basin Maps",          "icon": "bi-map", "nav": "tabs",
     "question": "Where across the basin?",
     "views": ["spatial", "animations"],
     "desc": "Interactive side-by-side maps of every VIC variable, SNOTEL stations, watersheds "
             "and rivers across the basin — plus animated seasonal and 40-year drought cycles."},
    {"key": "about",   "label": "Governance & About",  "icon": "bi-bank2", "nav": "tabs",
     "question": "How it works & where it comes from",
     "views": ["governance", "cria", "methods", "publications", "reports", "references"],
     "desc": "Context & credibility — water governance (Law of the River), the CRIA asset "
             "framework, methods & data sources, publications, and the NASA project reports."},
]
VIEW_TO_GROUP = {v: g for g in GROUPS for v in g["views"]}


# ── Sidebar (7 groups only) ──────────────────────────────────
def make_sidebar():
    items = []
    for g in GROUPS:
        first_route = "/" + g["views"][0]
        routes = ",".join("/" + v for v in g["views"])
        items.append(
            html.A(
                [html.I(className=f"bi {g['icon']}",
                        style={"fontSize": "16px", "marginRight": "10px", "width": "18px",
                               "display": "inline-block"}),
                 g["label"]],
                id=f"nav-{g['key']}",
                href=first_route,
                className="nav-link",
                **{"data-routes": routes},
            )
        )

    return html.Div([
        # Title (logo removed — it already appears in the right-hand header strip)
        html.Div([
            html.Div([
                html.Div([
                    "C", html.Span("▪", className="dst-dot"),
                    "R", html.Span("▪", className="dst-dot"),
                    "I", html.Span("▪", className="dst-dot"),
                    "A",
                ], className="sidebar-logo-text"),
                html.Div("Decision Support Tool", className="sidebar-logo-sub"),
            ], style={"width": "100%"})
        ], className="sidebar-logo"),

        # Nav
        html.Nav(items, style={"padding": "12px 0"}),

        # Bottom info
        html.Div([
            html.Div("Arizona State University", className="sidebar-bottom-text"),
            html.Div("NASA Applied Sciences",    className="sidebar-bottom-text"),
            html.Div([
                html.Div("CRIA — Decision Support Tool",
                         style={"fontWeight": "700", "color": "#8C1D40", "fontSize": "11px"}),
                html.Div("Developed by Pradeepika Kaushik (Praddy)",
                         style={"color": "#0D2137", "fontWeight": "600", "fontSize": "10.5px",
                                "marginTop": "2px"}),
                html.Div("Geospatial & Data-Visualization Scientist, ASU",
                         style={"color": "#64748b", "fontSize": "9.5px",
                                "lineHeight": "1.35", "marginTop": "1px"}),
            ], style={"borderTop": "1px solid #e2e8f0",
                      "marginTop": "10px", "paddingTop": "9px"}),
        ], className="sidebar-bottom"),
    ], className="sidebar", id="sidebar")


# ── Page layout wrapper ──────────────────────────────────────
def page_layout(title, subtitle, icon, color_class, tiles, content):
    return html.Div([
        # Header
        html.Div([
            html.H2(f"{icon}  {title}"),
            html.P(subtitle),
        ], className="tab-header"),

        # Body
        html.Div([
            # Info tiles row
            dbc.Row([
                dbc.Col(t, xs=6, md=3) for t in tiles
            ], className="mb-3 g-2") if tiles else html.Div(),

            # Main content
            content,
        ], className="tab-body"),
    ])


def info_tile(value, label, icon, color):
    return html.Div([
        html.Div(str(value), className="info-tile-value"),
        html.Div(label, className="info-tile-label"),
        html.Div(icon, className="info-tile-icon"),
    ], className=f"info-tile {color}")


# ── Import page modules (populated in later phases) ─────────
from modules.home     import layout as home_layout
from modules.snowpack import layout as snowpack_layout
from modules.watbal   import layout as watbal_layout
from modules.tws      import layout as tws_layout
from modules.drought  import layout as drought_layout
from modules.future   import layout as future_layout
from modules.spatial  import layout as spatial_layout
from modules.aridification import layout as aridification_layout
from modules.asi          import layout as asi_layout
from modules.storage      import layout as storage_layout
from modules.budyko       import layout as budyko_layout
from modules.cascade      import layout as cascade_layout
from modules.recovery     import layout as recovery_layout
from modules.noanalog     import layout as noanalog_layout
from modules.timing       import layout as timing_layout
from modules.links        import layout as links_layout
from modules.nmme         import layout as nmme_layout
from modules.cmip         import layout as cmip_layout
from modules.scenario     import layout as scenario_layout
from modules.governance   import layout as governance_layout
from modules.reservoirs   import layout as reservoirs_layout
from modules.cria         import layout as cria_layout
from modules.uncertainty  import layout as uncertainty_layout
from modules.methods      import layout as methods_layout
from modules.publications import layout as publications_layout
from modules.reports      import layout as reports_layout
from modules.elevsnow     import layout as elevsnow_layout
from modules.warming      import layout as warming_layout
from modules.references   import layout as references_layout
from modules.animations   import layout as animations_layout

# ── Register callbacks ───────────────────────────────────────
from modules.home         import register_callbacks as home_cb
from modules.snowpack     import register_callbacks as snowpack_cb
from modules.watbal       import register_callbacks as watbal_cb
from modules.tws          import register_callbacks as tws_cb
from modules.drought      import register_callbacks as drought_cb
from modules.future       import register_callbacks as future_cb
from modules.spatial      import register_callbacks as spatial_cb
from modules.aridification import register_callbacks as aridification_cb
from modules.asi          import register_callbacks as asi_cb
from modules.storage      import register_callbacks as storage_cb
from modules.budyko       import register_callbacks as budyko_cb
from modules.cascade      import register_callbacks as cascade_cb
from modules.recovery     import register_callbacks as recovery_cb
from modules.noanalog     import register_callbacks as noanalog_cb
from modules.timing       import register_callbacks as timing_cb
from modules.links        import register_callbacks as links_cb
from modules.nmme         import register_callbacks as nmme_cb
from modules.cmip         import register_callbacks as cmip_cb
from modules.scenario     import register_callbacks as scenario_cb
from modules.governance   import register_callbacks as governance_cb
from modules.reservoirs   import register_callbacks as reservoirs_cb
from modules.cria         import register_callbacks as cria_cb
from modules.uncertainty  import register_callbacks as uncertainty_cb
from modules.publications import register_callbacks as publications_cb
from modules.reports      import register_callbacks as reports_cb
from modules.elevsnow     import register_callbacks as elevsnow_cb
from modules.warming      import register_callbacks as warming_cb
from modules.references   import register_callbacks as references_cb
from modules.animations   import register_callbacks as animations_cb

for cb in [home_cb, snowpack_cb, watbal_cb, tws_cb, drought_cb, future_cb, spatial_cb,
           aridification_cb, asi_cb, storage_cb, budyko_cb, cascade_cb, recovery_cb,
           noanalog_cb, timing_cb, links_cb, nmme_cb, cmip_cb, scenario_cb,
           governance_cb, reservoirs_cb, cria_cb, uncertainty_cb,
           publications_cb, reports_cb, elevsnow_cb, warming_cb, references_cb,
           animations_cb]:
    cb(app)

# ── Main layout ──────────────────────────────────────────────
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    # Mobile hamburger button
    html.Button("", id="sidebar-toggle", className="sidebar-toggle",
                n_clicks=0),

    make_sidebar(),

    # ── Main content wrapper ─────────────────────────────────
    html.Div([
        # Global header band — LOGOS ONLY (same on every page)
        html.Div([
            html.Img(src="/assets/img/nasa-logo.webp", className="header-logo", title="NASA Applied Sciences"),
            html.Img(src="/assets/img/asu.jpeg",       className="header-logo", title="Arizona State University"),
            html.Img(src="/assets/img/cap.jpeg",       className="header-logo", title="Central Arizona Project"),
        ], className="app-header"),

        # Global title container — fixed title + subtitle (same on every page)
        html.Div([
            html.H1("CRIA — Colorado River Infrastructure Asset", className="app-title"),
            html.P("Decision Support Tool · Historical hydroclimatic analysis WY1984–2024 · "
                   "VIC 5.0 PRISM-calibrated (U. Washington, NASA-funded) + SNOTEL + GRACE · "
                   "For Bureau of Reclamation, ADWR, CAWCD & Basin Stakeholders",
                   className="app-subtitle"),
        ], className="app-titlebar"),

        html.Div(id="page-content"),
    ], className="main-content"),
    html.Div([
        html.Span("CRIA — Decision Support Tool",
                  className="crb-footer-left"),
        html.Span(["Full data sources & citations: ",
                   html.A("References & Validation", href="/references",
                          style={"color":"#01579B","fontWeight":"600","textDecoration":"underline"})],
                  className="crb-footer-center"),
        html.Span("© 2026 ASU | NASA Applied Sciences",
                  className="crb-footer-right"),
    ], className="crb-footer"),

])

# Mobile sidebar toggle: hamburger opens/closes; navigating closes it
app.clientside_callback(
    """function(n, path){
        var sb = document.getElementById('sidebar');
        var open = sb && sb.classList.contains('open');
        var ctx = dash_clientside.callback_context;
        if (ctx.triggered && ctx.triggered.length){
            var src = ctx.triggered[0].prop_id;
            if (src.indexOf('sidebar-toggle') !== -1) { open = !open; }
            else { open = false; }   // navigation closes the drawer
        }
        return open ? 'sidebar open' : 'sidebar';
    }""",
    Output("sidebar", "className"),
    Input("sidebar-toggle", "n_clicks"),
    Input("url", "pathname"),
    prevent_initial_call=False,
)

# ── URL routing ──────────────────────────────────────────────
# Every view keeps its own route (so deep-links + in-app links work),
# but views are rendered inside their parent group with a sub-tab bar.
VIEW_LAYOUTS = {
    "home": home_layout, "snowpack": snowpack_layout, "watbal": watbal_layout,
    "timing": timing_layout, "links": links_layout, "tws": tws_layout,
    "storage": storage_layout, "drought": drought_layout, "cascade": cascade_layout,
    "recovery": recovery_layout, "aridification": aridification_layout, "asi": asi_layout,
    "budyko": budyko_layout, "future": future_layout, "noanalog": noanalog_layout,
    "nmme": nmme_layout, "cmip": cmip_layout, "scenario": scenario_layout,
    "cria": cria_layout, "governance": governance_layout, "reservoirs": reservoirs_layout,
    "uncertainty": uncertainty_layout, "spatial": spatial_layout,
    "methods": methods_layout, "publications": publications_layout, "reports": reports_layout,
    "elevsnow": elevsnow_layout, "warming": warming_layout,
    "references": references_layout,
    "animations": animations_layout,
}
PAGE_MAP = {f"/{k}": v for k, v in VIEW_LAYOUTS.items()}
PAGE_MAP["/"] = home_layout


def _subtab_bar(group, active_view):
    """Section intro + a view switcher. Style per group:
       nav='tabs'  → horizontal sub-tabs (like Kristen's tool)
       default     → dropdown (decision-support style)."""
    q = group.get("question")
    intro = html.Div([
        html.Div([
            html.I(className=f"bi {group['icon']}",
                   style={"color": "#8C1D40", "marginRight": "8px", "fontSize": "15px"}),
            html.Span(q or group["label"], style={"fontWeight": "800", "color": "#8C1D40",
                                                  "fontSize": "14px", "marginRight": "10px"}),
            html.Span(group["label"], style={"fontWeight": "700", "color": "#0D2137",
                                             "fontSize": "11.5px"}) if q else None,
        ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"}),
        html.Span(group.get("desc", ""), style={"color": "#64748b", "fontSize": "11.5px"}),
    ], className="subtab-intro")

    if group.get("nav") == "tabs":
        tabs = []
        for v in group["views"]:
            label, icon = VIEW_LABELS.get(v, (v, ""))
            cls = "subtab-tab active" if v == active_view else "subtab-tab"
            tabs.append(html.A(
                [html.I(className=f"bi {icon}", style={"marginRight": "7px", "fontSize": "13px"}), label],
                href=f"/{v}", className=cls))
        switcher = html.Div(tabs, className="subtab-tabs")
    else:
        options = [{"label": VIEW_LABELS.get(v, (v, ""))[0], "value": v} for v in group["views"]]
        switcher = html.Div([
            html.Span("Select analysis", className="subnav-label"),
            dcc.Dropdown(id="subnav-dropdown", options=options, value=active_view,
                         clearable=False, searchable=False, className="subnav-dropdown"),
        ], className="subnav-row")

    return html.Div([intro, switcher], className="subtab-bar")


# Dropdown view selector → navigate (decision-support style)
@app.callback(
    Output("url", "pathname"),
    Input("subnav-dropdown", "value"),
    State("url", "pathname"),
    prevent_initial_call=True,
)
def _nav_from_dropdown(view, current):
    if not view:
        raise PreventUpdate
    target = f"/{view}"
    if target == current:          # avoids loop when dropdown is rebuilt on navigation
        raise PreventUpdate
    return target


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname):
    if not pathname or pathname == "/":
        pathname = "/home"
    view = pathname.strip("/")
    group = VIEW_TO_GROUP.get(view)
    if group is None:                      # unknown route → home
        view, group = "home", VIEW_TO_GROUP["home"]
    layout_fn = VIEW_LAYOUTS.get(view, home_layout)
    # Single-view groups need no sub-tab bar
    if len(group["views"]) <= 1:
        return html.Div([layout_fn()])
    return html.Div([_subtab_bar(group, view), layout_fn()])


# Highlight active group in sidebar (by matching pathname to the group's routes)
app.clientside_callback(
    """function(pathname) {
        setTimeout(function() {
            var path = (pathname === '/' || !pathname) ? '/home' : pathname;
            document.querySelectorAll('.nav-link').forEach(function(el) {
                var routes = (el.getAttribute('data-routes') || '').split(',');
                el.classList.toggle('active', routes.indexOf(path) !== -1);
            });
        }, 50);
        return window.dash_clientside.no_update;
    }
    """,
    Output("url", "search"),
    Input("url", "pathname"),
    prevent_initial_call=False,
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
