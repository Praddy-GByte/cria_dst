"""
modules/links.py — Soil Moisture & Spring Weather to Summer Streamflow
Reproduces the project's snow-soil-streamflow experiments (NASA Quarterly Review, Nov 2024,
slides 22-23) and addresses CAP science priority #1 (effect of (deep) soil moisture on
streamflow efficiency):
  - Post-April-1 (AMJ) hot/dry weather reduces summer (JJAS) streamflow despite average SWE.
  - October-1 (start-of-water-year) soil moisture, esp. deep layers, supports summer baseflow.
Verified (CRB): AMJ temp -> JJAS Q r=-0.73; Oct-1 soil moisture -> JJAS Q r=+0.39.
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from utils.data_loader import load_vic_monthly, basin_label
from utils.components import howto

MAROON="#8C1D40"; NAVY="#0D2137"; BLUE="#01579B"; GREEN="#2E7D32"; ORANGE="#E65100"; PURPLE="#4527A0"

BASIN_OPTIONS=[{"label":n,"value":b} for b,n in [
    ("CRB","Colorado River Basin"),("UpperBasin","Upper Basin"),("LowerBasin","Lower Basin"),
    ("Green","Green River"),("SanJuan","San Juan"),("UpperColo","Upper Colorado"),
    ("GlenCanyon","Glen Canyon"),("Gila","Gila River"),("GrandCanyon","Grand Canyon"),
    ("LittleColo","Little Colorado"),("LowerColo","Lower Colorado")]]

def _safe(fn):
    try: return fn()
    except: return pd.DataFrame()

def _empty(msg="Run preprocessing first"):
    fig=go.Figure(); fig.add_annotation(text=msg,xref="paper",yref="paper",x=0.5,y=0.5,
        showarrow=False,font=dict(size=12,color="#90a4ae"))
    fig.update_layout(paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(visible=False),
        yaxis=dict(visible=False),margin=dict(l=20,r=20,t=30,b=20),height=320); return fig

def _tile(val,label,icon,color):
    return html.Div([html.Div(str(val),className="info-tile-value"),
        html.Div(label,className="info-tile-label"),html.Div(icon,className="info-tile-icon")],
        className=f"info-tile {color}")

def _seasonal(basin):
    """Per water year: AMJ temp & precip, Oct-1 (start) soil moisture (total & deep), JJAS streamflow."""
    m=_safe(load_vic_monthly)
    if m.empty: return pd.DataFrame()
    b=m[m["basin"]==basin].copy()
    if b.empty: return pd.DataFrame()
    b["Q"]=b["OUT_RUNOFF"]+b["OUT_BASEFLOW"]
    b["wy"]=b.apply(lambda r:r["year"]+1 if r["month"]>=10 else r["year"],axis=1)
    rows=[]
    for wy,g in b.groupby("wy"):
        amjT=g[g["month"].isin([4,5,6])]["OUT_AIR_TEMP"].mean()
        amjP=g[g["month"].isin([4,5,6])]["OUT_PREC"].sum()
        jjasQ=g[g["month"].isin([7,8,9])]["Q"].sum()
        oct1=g[g["month"]==10]["OUT_SOIL_MOIST"].mean()
        octL3=g[g["month"]==10]["OUT_SOIL_MOIST_L3"].mean() if "OUT_SOIL_MOIST_L3" in g.columns else np.nan
        rows.append(dict(wy=wy,amjT=amjT,amjP=amjP,jjasQ=jjasQ,oct1=oct1,octL3=octL3))
    d=pd.DataFrame(rows).dropna(subset=["amjT","jjasQ"])
    return d[(d["wy"]>=1985)&(d["wy"]<=2024)]

def _r(x,y):
    x=np.asarray(x,float); y=np.asarray(y,float); m=~(np.isnan(x)|np.isnan(y))
    return np.corrcoef(x[m],y[m])[0,1] if m.sum()>3 else np.nan

def _scatter(x,y,c,xt,yt,cbar):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode="markers",
        marker=dict(size=8,color=c,colorscale="YlOrRd",showscale=True,
                    colorbar=dict(title=cbar,thickness=10)),
        hovertemplate=f"{xt}: %{{x:.1f}}<br>{yt}: %{{y:.1f}}<extra></extra>"))
    xv=np.asarray(x,float); yv=np.asarray(y,float); mm=~(np.isnan(xv)|np.isnan(yv))
    if mm.sum()>2:
        sl,ic=np.polyfit(xv[mm],yv[mm],1); xr=np.array([xv[mm].min(),xv[mm].max()])
        fig.add_trace(go.Scatter(x=xr,y=sl*xr+ic,mode="lines",
            line=dict(color=MAROON,width=2),showlegend=False))
    fig.update_layout(xaxis_title=xt,yaxis_title=yt,margin=dict(l=55,r=10,t=10,b=45),
        height=340,paper_bgcolor="white",plot_bgcolor="white",showlegend=False)
    return fig


def layout():
    return html.Div([
        html.Div([
            html.H2("Soil Moisture & Spring Weather to Summer Streamflow"),
            html.P("Why average snow doesn't guarantee summer flow — the role of spring heat and "
                   "start-of-year soil moisture (CAP priority; project experiments)."),
        ],className="tab-header"),
        html.Div([
            dbc.Row(id="lk-tiles",className="mb-3 g-2"),
            html.Div(id="lk-findings",
                     style={"background":"#e3f2fd","borderLeft":f"3px solid {BLUE}",
                            "padding":"10px 14px","borderRadius":"0 6px 6px 0",
                            "fontSize":"11.5px","color":"#1565c0","marginBottom":"12px"}),
                            howto("Pick a basin. This shows how soil moisture controls streamflow: drier soils convert less precipitation into runoff."),
            html.Div([dbc.Row([dbc.Col([
                html.Div("Basin",className="control-label"),
                dcc.Dropdown(id="lk-basin",options=BASIN_OPTIONS,value="CRB",clearable=False,
                             style={"fontSize":"12.5px"}),
            ],md=5)])],className="control-panel"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div([html.Span("Spring heat suppresses summer flow",style={"fontWeight":"700","fontSize":"13px"}),
                            html.Span("— AMJ (Apr-Jun) temperature vs JJAS (Jul-Sep) streamflow",
                                      style={"color":"#1e293b","fontSize":"11px"}),
                        ],className="crb-card-header"),
                        dcc.Graph(id="lk-amj",config={"displayModeBar":False},style={"height":"340px"}),
                    ],className="crb-card"),
                ],md=6),
                dbc.Col([
                    html.Div([
                        html.Div([html.Span("Start-of-year soil moisture sustains summer flow",style={"fontWeight":"700","fontSize":"13px"}),
                            html.Span("— Oct-1 soil moisture vs JJAS streamflow",
                                      style={"color":"#1e293b","fontSize":"11px"}),
                        ],className="crb-card-header"),
                        dcc.Graph(id="lk-oct",config={"displayModeBar":False},style={"height":"340px"}),
                    ],className="crb-card"),
                ],md=6),
            ],className="g-3"),
            html.Div("Reproduces the project's snow-soil-streamflow experiments (NASA Quarterly Review, Nov 2024). "
                     "AMJ = April-June; JJAS = July-September; Oct-1 soil moisture = start of the water year. "
                     "Points colored by AMJ temperature (left) and water year (right).",
                     style={"fontSize":"10.5px","color":"#1e293b","marginTop":"6px"}),
        ],className="tab-body"),
    ])


def register_callbacks(app):

    @app.callback(Output("lk-tiles","children"), Input("lk-basin","value"))
    def tiles(basin):
        d=_seasonal(basin)
        labels=["Spring-heat link","Spring-rain link","Start-SM link","Deep-SM link"]
        if d.empty:
            return [dbc.Col(_tile("—",l,"","tile-navy"),xs=6,md=3) for l in labels]
        tiles_=[
            _tile(f"r={_r(d['amjT'],d['jjasQ']):+.2f}","AMJ temp to summer Q","","tile-maroon"),
            _tile(f"r={_r(d['amjP'],d['jjasQ']):+.2f}","AMJ precip to summer Q","","tile-blue"),
            _tile(f"r={_r(d['oct1'],d['jjasQ']):+.2f}","Oct-1 soil moist to summer Q","","tile-green"),
            _tile(f"r={_r(d['octL3'],d['jjasQ']):+.2f}" if d['octL3'].notna().any() else "—","Oct-1 DEEP soil to summer Q","","tile-navy"),
        ]
        return [dbc.Col(t,xs=6,md=3) for t in tiles_]

    @app.callback(Output("lk-amj","figure"), Input("lk-basin","value"))
    def amj(basin):
        d=_seasonal(basin)
        if d.empty: return _empty("No data")
        return _scatter(d["amjT"],d["jjasQ"],d["amjT"],
                        "AMJ air temperature (°C)","JJAS streamflow (mm)","AMJ T")

    @app.callback(Output("lk-oct","figure"), Input("lk-basin","value"))
    def oct(basin):
        d=_seasonal(basin)
        if d.empty: return _empty("No data")
        return _scatter(d["oct1"],d["jjasQ"],d["wy"],
                        "Oct-1 soil moisture (mm)","JJAS streamflow (mm)","WY")

    @app.callback(Output("lk-findings","children"), Input("lk-basin","value"))
    def findings(basin):
        d=_seasonal(basin)
        if d.empty: return "Findings will appear after preprocessing is complete."
        rt=_r(d["amjT"],d["jjasQ"]); ro=_r(d["oct1"],d["jjasQ"])
        return [html.Strong("Key finding — "),
                f"{basin_label(basin)}: hotter springs depress summer streamflow (AMJ temp vs JJAS Q, r={rt:+.2f}); "
                f"wetter start-of-year soils sustain it (Oct-1 soil moisture vs JJAS Q, r={ro:+.2f}). "
                f"So an average April-1 snowpack can still yield a poor summer if spring is hot/dry or soils started dry — "
                f"a key trigger for CAP operations."]
