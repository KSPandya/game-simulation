

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
import math
import random
from datetime import datetime, timedelta


st.set_page_config(
    page_title="SPACECOM | WARGAME OPS",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] { background: #0A0F1C !important; color: #FFFFFF !important; font-family: 'Rajdhani', sans-serif !important; }
[data-testid="stAppViewContainer"] { background-image: repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(47,128,237,0.04) 39px, rgba(47,128,237,0.04) 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(47,128,237,0.04) 39px, rgba(47,128,237,0.04) 40px) !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="block-container"] { padding: 0.5rem 1rem !important; max-width: 100% !important; }
.stApp { background: #0A0F1C !important; }
#MainMenu, footer, header { visibility: hidden !important; }

[data-testid="stAppViewContainer"]::before { content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 9999; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(47,128,237,0.02) 2px, rgba(47,128,237,0.02) 4px); }
[data-testid="column"] { padding: 0 6px !important; }

.panel-card { background: #0F1A2E; border: 1px solid #1A2D4F; border-radius: 4px; padding: 14px; margin-bottom: 10px; position: relative; overflow: hidden; }
.panel-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #2F80ED, transparent); }

.dash-header { background: #0D1526; border-bottom: 2px solid #1E3A6E; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; font-family: 'Share Tech Mono', monospace; }
.panel-title { font-family: 'Orbitron', monospace; font-size: 14px; font-weight: bold; letter-spacing: 3px; color: #56CCF2; text-transform: uppercase; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid #1A2D4F; }

.metric-box { background: #111E35; border: 1px solid #1A2D4F; border-left: 4px solid; padding: 10px 14px; margin-bottom: 6px; border-radius: 2px; }
.metric-label { font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #8BA3C7; letter-spacing: 1px; }
.metric-val { font-family: 'Share Tech Mono', monospace; font-size: 24px; font-weight: 700; color: #FFFFFF; }

.badge { font-family: 'Share Tech Mono', monospace; font-weight: bold; font-size: 11px; padding: 4px 10px; letter-spacing: 1px; display: inline-block; border: 1px solid; border-radius: 2px; }
.badge-red   { color: #EB5757; border-color: #EB5757; background: rgba(235,87,87,0.15); }
.badge-orange{ color: #F2994A; border-color: #F2994A; background: rgba(242,153,74,0.15); }
.badge-green { color: #27AE60; border-color: #27AE60; background: rgba(39,174,96,0.15); }
.badge-blue  { color: #56CCF2; border-color: #56CCF2; background: rgba(47,128,237,0.15); }
.badge-live  { color: #27AE60; border-color: #27AE60; animation: blink 1.5s infinite; }

.coa-card { background: #111E35; border: 1px solid #1A2D4F; border-left: 4px solid; padding: 12px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
.coa-card:hover { transform: translateX(3px); border-color: #56CCF2; }
.coa-optimal  { border-left-color: #27AE60; background: rgba(39,174,96,0.08); }
.coa-moderate { border-left-color: #F2994A; background: rgba(242,153,74,0.08); }
.coa-risky    { border-left-color: #EB5757; background: rgba(235,87,87,0.08); }
.coa-name { font-family: 'Orbitron', monospace; font-size: 12px; font-weight: bold; letter-spacing: 1px; }

.pbar-wrap { height: 4px; background: #1A2D4F; margin: 5px 0; border-radius: 2px; }
.pbar { height: 4px; border-radius: 2px; }
.stat-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(26,45,79,0.5); font-family: 'Share Tech Mono', monospace; font-size: 13px; }
.stat-label { color: #E2EAF8; font-weight: bold; }

[data-testid="stSelectbox"] label, [data-testid="stSlider"] label { font-family: 'Share Tech Mono', monospace !important; font-size: 13px !important; color: #56CCF2 !important; letter-spacing: 1px !important; }
[data-testid="stSelectbox"] > div > div { background: #111E35 !important; border: 1px solid #1A2D4F !important; color: #FFFFFF !important; border-radius: 2px !important; font-family: 'Share Tech Mono', monospace !important; font-size: 14px !important; }
.stSlider > div > div > div > div { background: #56CCF2 !important; }

.stButton > button { background: #111E35 !important; border: 1px solid #1A2D4F !important; color: #56CCF2 !important; border-radius: 2px !important; font-family: 'Share Tech Mono', monospace !important; font-size: 13px !important; transition: all 0.2s !important; padding: 6px 12px !important; font-weight: bold; }
.stButton > button:hover { border-color: #FFFFFF !important; color: #FFFFFF !important; background: rgba(47,128,237,0.2) !important; }
.stButton > button:active { background: #27AE60 !important; color: white !important; border-color: #27AE60 !important; }

.intel-feed { max-height: 200px; overflow-y: auto; background: #080D1A; border: 1px solid #1A2D4F; padding: 10px; font-family: 'Share Tech Mono', monospace; }
.intel-item { font-size: 12px; padding: 5px 0; border-bottom: 1px solid rgba(26,45,79,0.4); }
.intel-time { color: #56CCF2; display: inline; font-weight: bold; margin-right: 5px; }

@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)


def init_state():
    defaults = {
        "sim_running": False,
        "sim_time": 0.0,
        "sim_speed": 1.0,
        "scenario": "ASAT INTERCEPT",
        "time_horizon": 6,
        "selected_coa": "COA-ALPHA",
        "threat_level": "ELEVATED",
        "tick": 0,
        "intel_log": [
            ("T+00:00:00", "Simulation initialized — all assets nominal", "ok"),
            ("T+00:01:00", "ECI frame lock acquired", "ok"),
            ("T+00:04:00", "COA-ALPHA manoeuvre window OPEN", "ok"),
            ("T+00:08:00", "PROXIMITY ALERT — KOSMOS range <50km", "warn"),
        ],
        "uncert": 15,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


def advance_simulation(multiplier=1.0):
    st.session_state.sim_time += (60 * multiplier) 
    st.session_state.tick += 1
    
    if st.session_state.tick % 4 == 0:
        sim_s = st.session_state.sim_time
        h = int(sim_s // 3600); m = int((sim_s % 3600) // 60); s = int(sim_s % 60)
        curr_epoch = f"T+{h:02d}:{m:02d}:{s:02d}"
        
        horizon_s = st.session_state.time_horizon * 3600
        prog = (sim_s % horizon_s) / horizon_s
        
        if 0.55 <= prog <= 0.65:
            msg = ("INFRARED BLOOM DETECTED - ADVERSARY LAUNCH", "alert")
        elif 0.65 < prog <= 0.75:
            msg = ("ASAT KKV IN FLIGHT - TRACKING LOCK", "alert")
        elif 0.75 < prog <= 0.85:
            msg = ("COA EXECUTING - THRUST VECTOR NOMINAL", "ok")
        else:
            msgs = [("Conjunction analysis updated — covariance nominal", ""), ("Radar sweep telemetry received", "ok"), ("SDIZ boundary proximity warning", "warn")]
            msg = random.choice(msgs)
            
        st.session_state.intel_log.insert(0, (curr_epoch, msg[0], msg[1]))


def orbital_pos(semi_major, inc, raan, phase, t, speed_mult=1.0):
    omega = speed_mult / (semi_major ** 1.5)
    angle = phase + omega * t
    x = semi_major * (math.cos(raan) * math.cos(angle) - math.sin(raan) * math.sin(angle) * math.cos(inc))
    y = semi_major * (math.sin(raan) * math.cos(angle) + math.cos(raan) * math.sin(angle) * math.cos(inc))
    z = semi_major * math.sin(angle) * math.sin(inc)
    return x, y, z

SATELLITES = [
    dict(id="USA-316",     type="friendly",  a=1.05, inc=0.90, raan=0.0,  phase=0.0,  color="#2F80ED", size=7),
    dict(id="USA-317",     type="friendly",  a=1.10, inc=0.95, raan=1.1,  phase=2.1,  color="#2F80ED", size=7),
    dict(id="KOSMOS-9821", type="adversary", a=0.90, inc=1.00, raan=0.5,  phase=1.0,  color="#EB5757", size=8),
    dict(id="KOSMOS-9822", type="adversary", a=1.06, inc=0.85, raan=1.8,  phase=3.3,  color="#EB5757", size=7),
    dict(id="DEBRIS-4471", type="debris",    a=0.96, inc=1.20, raan=2.2,  phase=4.5,  color="#9CA3AF", size=5),
]

SCENARIOS = {
    "ASAT INTERCEPT":  {"threat":"CRITICAL","desc":"Anti-satellite missile approach — intercept trajectory confirmed"},
    "PROXIMITY OPS":   {"threat":"HIGH",    "desc":"Adversary rendezvous & proximity operation detected"},
}

COA_DATA = {
    "COA-ALPHA": {"label": "EVASIVE BURN", "tier": "optimal", "risk_red": 87, "success": 91, "cost": 22, "tta": "04:20", "desc": "Prograde Δv burn to raise perigee 12km — clears conjunction"},
    "COA-BRAVO": {"label": "ALTITUDE RAISE", "tier": "moderate", "risk_red": 71, "success": 74, "cost": 58, "tta": "08:15", "desc": "Hohmann transfer to +50km orbit — fuel intensive"},
    "COA-CHARLIE": {"label": "HOLD STATION", "tier": "risky", "risk_red": 12, "success": 34, "cost": 0, "tta": "N/A", "desc": "No manoeuvre — accept risk, monitor and wait"},
}

ESCALATION_EVENTS = [
    (0.00, "SIM START",      "nominal",     "#27AE60"), (0.10, "NOMINAL OPS",    "nominal",     "#27AE60"),
    (0.22, "ANOMALY DET.",   "anomalous",   "#F2C94C"), (0.38, "PROX ALERT",     "preconflict", "#F2994A"),
    (0.52, "BURN DET.",      "preconflict", "#F2994A"), (0.63, "ASAT TRACK",     "active",      "#EB5757"),
    (0.75, "COA EXEC",       "active",      "#56CCF2"), (1.00, "RESOLUTION",     "nominal",     "#27AE60"),
]


def build_orbital_figure(t, scenario, speed, horizon):
    fig = go.Figure()
    horizon_s = horizon * 3600
    prog = (t % horizon_s) / horizon_s

    u = np.linspace(0, 2*np.pi, 60); v = np.linspace(0, np.pi, 40)
    ex = 0.85 * np.outer(np.cos(u), np.sin(v)); ey = 0.85 * np.outer(np.sin(u), np.sin(v)); ez = 0.85 * np.outer(np.ones(60), np.cos(v))
    fig.add_trace(go.Surface(x=ex, y=ey, z=ez, colorscale=[[0,'#050E1F'],[0.4,'#0D2347'],[0.7,'#1A3A6B'],[1,'#2060A0']], showscale=False, opacity=1.0, lighting=dict(ambient=0.6, diffuse=0.8, specular=0.3), name='Earth'))

    theta = np.linspace(0, 2*np.pi, 200); ar = 0.92
    fig.add_trace(go.Scatter3d(x=ar*np.cos(theta), y=ar*np.sin(theta), z=np.zeros(200), mode='lines', line=dict(color='rgba(47,128,237,0.2)', width=4), name='Atmo', showlegend=False))
    
    trail_len = 60
    for sat in SATELLITES:
        px, py, pz = orbital_pos(sat['a'], sat['inc'], sat['raan'], sat['phase'], t, speed)

        trail_t = np.linspace(max(0, t - trail_len), t, trail_len)
        tx = [orbital_pos(sat['a'], sat['inc'], sat['raan'], sat['phase'], tt, speed)[0] for tt in trail_t]
        ty = [orbital_pos(sat['a'], sat['inc'], sat['raan'], sat['phase'], tt, speed)[1] for tt in trail_t]
        tz = [orbital_pos(sat['a'], sat['inc'], sat['raan'], sat['phase'], tt, speed)[2] for tt in trail_t]
        fig.add_trace(go.Scatter3d(x=tx, y=ty, z=tz, mode='lines', line=dict(color=f"rgba({int(sat['color'][1:3], 16)}, {int(sat['color'][3:5], 16)}, {int(sat['color'][5:7], 16)}, 0.6)", width=3), showlegend=False))

        sym = 'diamond' if sat['type'] == 'debris' else 'square'
        fig.add_trace(go.Scatter3d(x=[px], y=[py], z=[pz], mode='markers+text', marker=dict(size=sat['size']+2, color=sat['color'], symbol=sym, line=dict(color='#FFFFFF', width=1.5), opacity=1.0), text=[sat['id']], textposition='top center', textfont=dict(color='#FFFFFF', size=13, family='Share Tech Mono', weight='bold'), name=sat['id'], showlegend=True))


    

    sweep_phase = (t % 1200) / 1200.0  # Loops visually based on time
    sweep_r = 0.1 + (sweep_phase * 0.7)
    sweep_op = max(0, 0.4 - (sweep_phase * 0.4))
    ux, uy, uz = orbital_pos(SATELLITES[0]['a'], SATELLITES[0]['inc'], SATELLITES[0]['raan'], SATELLITES[0]['phase'], t, speed)
    u_sph = np.linspace(0, 2*np.pi, 20); v_sph = np.linspace(0, np.pi, 20); U_sph, V_sph = np.meshgrid(u_sph, v_sph)
    fig.add_trace(go.Surface(
        x=ux + sweep_r*np.cos(U_sph)*np.sin(V_sph), y=uy + sweep_r*np.sin(U_sph)*np.sin(V_sph), z=uz + sweep_r*np.cos(V_sph),
        colorscale=[[0, 'rgba(47,128,237,0)'], [1, f'rgba(47,128,237,{sweep_op})']],
        showscale=False, opacity=sweep_op, hoverinfo='skip', showlegend=False, name="Radar Sweep"
    ))

    
    if 0.55 <= prog <= 0.85:
        t_launch = horizon_s * 0.55
        t_intercept = horizon_s * 0.85
        kx, ky, kz = orbital_pos(SATELLITES[2]['a'], SATELLITES[2]['inc'], SATELLITES[2]['raan'], SATELLITES[2]['phase'], t_launch, speed)
        target_x, target_y, target_z = orbital_pos(SATELLITES[0]['a'], SATELLITES[0]['inc'], SATELLITES[0]['raan'], SATELLITES[0]['phase'], t_intercept, speed)
        
        m_prog = (t - t_launch) / (t_intercept - t_launch)
        mx = kx + (target_x - kx) * m_prog
        my = ky + (target_y - ky) * m_prog
        mz = kz + (target_z - kz) * m_prog

        fig.add_trace(go.Scatter3d(x=[mx], y=[my], z=[mz], mode='markers', marker=dict(size=8, color='#FF2020', symbol='x', line=dict(color='white', width=1)), name='ASAT KKV'))
    
        fig.add_trace(go.Scatter3d(x=[kx, mx], y=[ky, my], z=[kz, mz], mode='lines', line=dict(color='rgba(255,32,32,0.8)', width=3, dash='dot'), showlegend=False))


    if 0.75 <= prog <= 0.86:
        # Glow aura around USA-316
        fig.add_trace(go.Scatter3d(
            x=[ux], y=[uy], z=[uz], mode='markers',
            marker=dict(size=35, color='rgba(86,204,242,0.6)', line=dict(color='#00E5FF', width=2)),
            name='EVASIVE THRUST'
        ))

    fig.update_layout(
        paper_bgcolor='rgba(8,13,26,0)', plot_bgcolor='rgba(8,13,26,0)',
        scene=dict(xaxis=dict(visible=False, range=[-1.6,1.6]), yaxis=dict(visible=False, range=[-1.6,1.6]), zaxis=dict(visible=False, range=[-1.6,1.6]), bgcolor='rgba(8,13,26,0)', camera=dict(eye=dict(x=1.6, y=1.4, z=0.9)), aspectmode='cube'),
        legend=dict(x=0.01, y=0.99, font=dict(family='Share Tech Mono', size=12, color='#FFFFFF'), bgcolor='rgba(10,15,28,0.8)', bordercolor='#56CCF2', borderwidth=1),
        margin=dict(l=0, r=0, t=0, b=0), height=550,
    )
    return fig

def build_radar():
    cats = ['SUCCESS', 'RISK↓', 'COST EFF.', 'SPEED', 'STABILITY', 'SUCCESS']
    fig = go.Figure()
    coas = [('COA-ALPHA', [0.91, 0.87, 0.80, 0.75, 0.90, 0.91], '#27AE60'), ('COA-BRAVO', [0.74, 0.71, 0.50, 0.55, 0.70, 0.74], '#F2994A'), ('COA-CHARLIE',[0.34, 0.12, 0.95, 0.30, 0.20, 0.34], '#EB5757')]
    for name, vals, color in coas:
        fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill='toself', name=name, line=dict(color=color, width=2), fillcolor=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15)", marker=dict(size=6, color=color)))
    fig.update_layout(
        polar=dict(bgcolor='rgba(8,13,26,0)', radialaxis=dict(visible=True, range=[0,1], tickfont=dict(size=10,color='#FFFFFF'), gridcolor='#1A2D4F', linecolor='#1A2D4F'), angularaxis=dict(tickfont=dict(size=12,color='#56CCF2',family='Share Tech Mono', weight='bold'), gridcolor='#1A2D4F', linecolor='#1A2D4F')),
        paper_bgcolor='rgba(0,0,0,0)', legend=dict(font=dict(family='Share Tech Mono', size=11, color='#FFFFFF'), bgcolor='rgba(10,15,28,0.8)', bordercolor='#56CCF2', borderwidth=1), margin=dict(l=40, r=40, t=30, b=30), height=300,
    )
    return fig


def build_sensitivity(uncert):
    u = uncert / 100.0
    coa_data_s = [('COA-α', 0.91, '#27AE60'), ('COA-β', 0.74, '#F2994A'), ('COA-χ', 0.34, '#EB5757')]
    fig = go.Figure()
    for name, base, color in coa_data_s:
        lo = max(0, base - u)
        hi = min(1, base + u * 0.6)
        fig.add_trace(go.Scatter(x=[name, name], y=[lo*100, hi*100], mode='lines', line=dict(color=f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.6)", width=16), showlegend=False))
        fig.add_trace(go.Scatter(x=[name], y=[base*100], mode='markers+text', marker=dict(size=14, color=color, symbol='diamond', line=dict(width=1, color='white')), text=[f"{base*100:.0f}%"], textposition='top center', textfont=dict(family='Share Tech Mono', size=14, color='#FFFFFF', weight='bold'), name=name))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(8,13,26,0.5)', xaxis=dict(tickfont=dict(family='Share Tech Mono',size=14,color='#FFFFFF'), gridcolor='#1A2D4F', linecolor='#1A2D4F'),
        yaxis=dict(title=dict(text='Success %', font=dict(color='#56CCF2', size=13)), range=[0,110], tickfont=dict(family='Share Tech Mono',size=12,color='#FFFFFF'), gridcolor='rgba(26,45,79,0.5)', linecolor='#1A2D4F'),
        margin=dict(l=40, r=20, t=20, b=40), height=250,
    )
    return fig

def build_escalation_trend(sim_t, horizon_h):
    x = np.linspace(0, horizon_h, 200)
    y = 0.1 + 0.7 * np.exp(-((x - horizon_h * 0.6) ** 2) / (2 * (horizon_h * 0.15) ** 2)); y += 0.05 * np.sin(x * 3); y = np.clip(y, 0, 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y * 100, fill='tozeroy', fillcolor='rgba(235,87,87,0.15)', line=dict(color='rgba(235,87,87,0.3)', width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=x, y=y * 100, mode='lines', line=dict(color='#EB5757', width=3), name='Threat Level', showlegend=False))

    current_x = (sim_t % (horizon_h * 3600)) / 3600
    fig.add_vline(x=current_x, line=dict(color='#56CCF2', width=2, dash='dash'))
    fig.add_annotation(x=current_x, y=105, text="NOW", showarrow=False, font=dict(family='Share Tech Mono', size=12, color='#56CCF2', weight='bold'))

    for frac, label, _, color in ESCALATION_EVENTS:
        ex = frac * horizon_h
        ey = float(np.interp(ex, x, y)) * 100
        fig.add_trace(go.Scatter(x=[ex], y=[ey], mode='markers+text', marker=dict(size=12, color=color, symbol='diamond', line=dict(color='#FFFFFF', width=1)), text=[label], textposition='top center', textfont=dict(family='Share Tech Mono', size=11, color='#FFFFFF', weight='bold'), showlegend=False))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(8,13,26,0.4)',
        xaxis=dict(title=dict(text='Time (hours)', font=dict(color='#56CCF2', size=13)), range=[0, horizon_h], tickfont=dict(family='Share Tech Mono',size=12,color='#FFFFFF'), gridcolor='rgba(26,45,79,0.4)', linecolor='#1A2D4F'),
        yaxis=dict(title=dict(text='Threat %', font=dict(color='#56CCF2', size=13)), range=[0,120], tickfont=dict(family='Share Tech Mono',size=12,color='#FFFFFF'), gridcolor='rgba(26,45,79,0.3)', linecolor='#1A2D4F'), margin=dict(l=50, r=20, t=10, b=45), height=200,
    )
    return fig


def build_risk_bars():
    coas = ['COA-ALPHA', 'COA-BRAVO', 'COA-CHARLIE']; risks  = [13, 29, 88]; costs  = [22, 58, 0]; colors = ['#27AE60', '#F2994A', '#EB5757']
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Risk Score', x=coas, y=risks, marker_color=colors, marker_line_width=0, text=[f"{v}%" for v in risks], textposition='auto', textfont=dict(family='Share Tech Mono', size=14, color='#FFFFFF', weight='bold')))
    fig.add_trace(go.Bar(name='Resource Cost', x=coas, y=costs, marker_color=[f"rgba({int(c[1:3], 16)}, {int(c[3:5], 16)}, {int(c[5:7], 16)}, 0.6)" for c in colors], marker_line_width=0, text=[f"{v}%" for v in costs], textposition='auto', textfont=dict(family='Share Tech Mono', size=14, color='#FFFFFF', weight='bold')))
    fig.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(8,13,26,0.4)', legend=dict(font=dict(family='Share Tech Mono',size=12,color='#FFFFFF'), bgcolor='rgba(10,15,28,0.8)', bordercolor='#56CCF2'), xaxis=dict(tickfont=dict(family='Share Tech Mono',size=13,color='#FFFFFF'), gridcolor='#1A2D4F', linecolor='#1A2D4F'), yaxis=dict(tickfont=dict(family='Share Tech Mono',size=12,color='#FFFFFF'), gridcolor='rgba(26,45,79,0.4)', linecolor='#1A2D4F'), margin=dict(l=30, r=10, t=10, b=40), height=240,
    )
    return fig


def pbar_html(val, color, max_val=100):
    pct = val / max_val * 100
    return f"""<div class='pbar-wrap'><div class='pbar' style='width:{pct}%;background:{color}'></div></div>"""



t_now = datetime.utcnow() + timedelta(days=27 * 365.25)   # 2047
sim_s = st.session_state.sim_time
h = int(sim_s // 3600); m = int((sim_s % 3600) // 60); s = int(sim_s % 60)
epoch_str = f"T+{h:02d}:{m:02d}:{s:02d}"

threat_colors = {"CRITICAL":"#EB5757","HIGH":"#EB5757","ELEVATED":"#F2994A","MODERATE":"#F2C94C","LOW":"#27AE60"}
scen_threat = SCENARIOS[st.session_state.scenario]["threat"]
tc = threat_colors.get(scen_threat, "#EB5757")

st.markdown(f"""
<div class="dash-header">
  <div>
    <span style='font-family:Orbitron,monospace;font-size:20px;font-weight:900; color:#FFFFFF;letter-spacing:4px;text-shadow:0 0 20px rgba(47,128,237,0.8)'>SPACECOM/<span style='color:#56CCF2'>WARGAME</span> OPS CENTER</span>&nbsp;&nbsp;
    <span style='color:#8BA3C7;font-size:13px;font-weight:bold;'>SESSION: WG-2047-DELTA</span>
  </div>
  <div style='display:flex;gap:25px;align-items:center'>
    <span><span class='badge badge-live' style='font-size:13px;'>● LIVE</span></span>
    <span style='color:#FFFFFF;font-size:14px;'>UTC: {t_now.strftime('%Y-%m-%d %H:%M:%S')}</span>
    <span style='color:#FFFFFF;font-size:14px;font-weight:bold;'>EPOCH: <span style='color:#56CCF2'>{epoch_str}</span></span>
    <span style='color:{tc};border:2px solid {tc};padding:4px 10px; font-weight:bold; font-size:13px;letter-spacing:2px;font-family:Share Tech Mono,monospace'>⚠ THREAT: {scen_threat}</span>
  </div>
</div>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.2, 2.6, 1.4])

with col_left:
    st.markdown("<div class='panel-title'>◈ SCENARIO CONTROL</div>", unsafe_allow_html=True)

    scenario = st.selectbox("ACTIVE SCENARIO", list(SCENARIOS.keys()), index=list(SCENARIOS.keys()).index(st.session_state.scenario), key="scenario_sel")
    if scenario != st.session_state.scenario:
        st.session_state.scenario = scenario
        st.session_state.intel_log.insert(0, (epoch_str, f"SCENARIO LOADED: {scenario}", "warn"))

    scen_info = SCENARIOS[scenario]
    st.markdown(f"""
    <div class='panel-card' style='margin-top:6px; padding:16px;'>
      <span class='badge badge-{'red' if scen_info['threat'] in ('CRITICAL','HIGH') else 'orange' if scen_info['threat']=='ELEVATED' else 'green'}' style='font-size:12px;'>{scen_info['threat']}</span>
      <div style='font-size:14px;color:#FFFFFF;margin-top:8px;font-weight:bold;'>{scen_info['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-title'>// SIMULATION CONTROLS</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("⏮ Step Back"):
        st.session_state.sim_time = max(0, st.session_state.sim_time - 600)
    
    # ── THE NEW AUTO-PLAY TOGGLE ──
    play_label = "⏹ Pause" if st.session_state.sim_running else "▶ Auto-Play"
    if c2.button(play_label):
        st.session_state.sim_running = not st.session_state.sim_running
        
    if c3.button("⏭ Step Fwd"):
        advance_simulation(5.0)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-title'>// TRACKED OBJECTS</div>", unsafe_allow_html=True)
    asset_rows = [("USA-316", "FRIENDLY", "#56CCF2", "NOM", "#27AE60"), ("USA-317", "FRIENDLY", "#56CCF2", "NOM", "#27AE60"), ("KOSMOS-9821", "ADVERSARY","#EB5757", "THR", "#EB5757"), ("KOSMOS-9822", "ADVERSARY","#EB5757", "PRX", "#F2994A"), ("DEBRIS-4471", "DEBRIS", "#9CA3AF", "TRK", "#9CA3AF")]
    for aname, atype, acolor, astate, scolor in asset_rows:
        st.markdown(f"""
        <div class='stat-row' style='padding:8px 0;'>
          <span style='color:{acolor};font-size:16px;'>■</span>
          <span class='stat-label' style='flex:1;padding-left:8px;font-size:14px;'>{aname}</span>
          <span class='badge' style='color:{scolor};border-color:{scolor};background:rgba(0,0,0,0.4);font-size:12px;'>{astate}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-title'>// INTEL FEED</div>", unsafe_allow_html=True)
    intel_html = "<div class='intel-feed'>"
    for it, imsg, icls in st.session_state.intel_log[:10]:
        col_map = {"alert":"#EB5757","warn":"#F2994A","ok":"#27AE60","":"#FFFFFF"}
        ic = col_map.get(icls, "#FFFFFF")
        intel_html += f"<div class='intel-item'><span class='intel-time'>{it}</span> <span style='color:{ic};font-weight:bold;'>{imsg}</span></div>"
    intel_html += "</div>"
    st.markdown(intel_html, unsafe_allow_html=True)


with col_center:
    st.markdown("<div class='panel-title' style='font-size:16px;'>◈ ECI ORBITAL SIMULATION — LEO THEATRE | ALT: 550km | INC: 53°</div>", unsafe_allow_html=True)

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.markdown(f"""<div class='metric-box' style='border-left-color:#EB5757'><div class='metric-label'>CONJUNCTIONS</div><div class='metric-val' style='color:#EB5757'>2</div></div>""", unsafe_allow_html=True)
    mc2.markdown(f"""<div class='metric-box' style='border-left-color:#EB5757'><div class='metric-label'>Pc MAX</div><div class='metric-val' style='color:#EB5757'>4.7e-3</div></div>""", unsafe_allow_html=True)
    mc3.markdown(f"""<div class='metric-box' style='border-left-color:#F2994A'><div class='metric-label'>ACTIVE ALERTS</div><div class='metric-val' style='color:#F2994A'>3</div></div>""", unsafe_allow_html=True)
    mc4.markdown(f"""<div class='metric-box' style='border-left-color:#56CCF2'><div class='metric-label'>SIM TIME</div><div class='metric-val' style='color:#56CCF2'>{epoch_str}</div></div>""", unsafe_allow_html=True)

    fig_orb = build_orbital_figure(st.session_state.sim_time, st.session_state.scenario, st.session_state.sim_speed, st.session_state.time_horizon)
    st.plotly_chart(fig_orb, use_container_width=True, key=f"orbital_{st.session_state.tick}")


with col_right:
    st.markdown("<div class='panel-title'>◈ COA DECISION MATRIX</div>", unsafe_allow_html=True)

    tabs_r = st.tabs(["COA LIST", "RADAR", "RISK BARS", "SENS."])

    with tabs_r[0]:
        for coa_key, cdata in COA_DATA.items():
            tier_class = f"coa-{cdata['tier']}"
            tier_colors = {"optimal":"#27AE60","moderate":"#F2994A","risky":"#EB5757"}
            tc2 = tier_colors[cdata['tier']]
            badge_map = {"optimal":"badge-green","moderate":"badge-orange","risky":"badge-red"}
            is_selected = st.session_state.selected_coa == coa_key
            border_extra = f"box-shadow:0 0 12px {tc2}60; border-color:{tc2};" if is_selected else ""

            st.markdown(f"""
            <div class='coa-card {tier_class}' style='{border_extra}; padding:14px;'>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <span class='coa-name' style='color:{tc2};font-size:14px;'>{coa_key}: {cdata['label']}</span>
                <span class='badge {badge_map[cdata["tier"]]}' style='font-size:11px;'>{cdata['tier'].upper()}</span>
              </div>
              <div style='font-size:13px;color:#FFFFFF;margin:6px 0 10px;font-weight:bold;'>{cdata['desc']}</div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>
                <div><div class='metric-label'>RISK REDUCTION</div>{pbar_html(cdata['risk_red'], tc2)}<span style='font-family:Share Tech Mono,monospace;font-size:13px;color:{tc2};font-weight:bold;'>{cdata['risk_red']}%</span></div>
                <div><div class='metric-label'>SUCCESS PROB</div>{pbar_html(cdata['success'], tc2)}<span style='font-family:Share Tech Mono,monospace;font-size:13px;color:{tc2};font-weight:bold;'>{cdata['success']}%</span></div>
                <div><div class='metric-label'>RESOURCE COST</div>{pbar_html(cdata['cost'], '#56CCF2')}<span style='font-family:Share Tech Mono,monospace;font-size:13px;color:#56CCF2;font-weight:bold;'>{cdata['cost']}%</span></div>
                <div><div class='metric-label'>TIME-TO-ACT</div><span style='font-family:Share Tech Mono,monospace;font-size:14px;color:#FFFFFF;font-weight:bold;'>{cdata['tta']}</span></div>
              </div>
            </div>""", unsafe_allow_html=True)

            if st.button(f"SELECT {coa_key}", key=f"sel_{coa_key}"):
                st.session_state.selected_coa = coa_key
                st.session_state.intel_log.insert(0, (epoch_str, f"{coa_key} SELECTED FOR EXECUTION", "ok"))

    with tabs_r[1]: st.plotly_chart(build_radar(), use_container_width=True, key="radar")
    with tabs_r[2]: st.plotly_chart(build_risk_bars(), use_container_width=True, key="risk_bars")
    with tabs_r[3]:
        uncert = st.slider("UNCERTAINTY FACTOR ±%", 5, 50, st.session_state.uncert, 1, key="uncert_sl")
        st.session_state.uncert = uncert
        st.plotly_chart(build_sensitivity(uncert), use_container_width=True, key="sens")
        st.markdown(f"""<div style='font-family:Share Tech Mono,monospace;font-size:12px;color:#FFFFFF;text-align:center;font-weight:bold;'>COA-ALPHA optimal across ±{uncert}% uncertainty band</div>""", unsafe_allow_html=True)


st.markdown("---", unsafe_allow_html=True)
st.markdown("<div class='panel-title'>◈ ESCALATION LADDER & TEMPORAL EVOLUTION</div>", unsafe_allow_html=True)

b1, b2 = st.columns([3.5, 1])

with b1:
    fig_trend = build_escalation_trend(st.session_state.sim_time, st.session_state.time_horizon)
    st.plotly_chart(fig_trend, use_container_width=True, key="trend")

with b2:
    st.markdown("""<div style='font-family:Share Tech Mono,monospace;font-size:12px;padding:8px'><div style='color:#56CCF2;letter-spacing:1px;margin-bottom:8px;font-weight:bold;'>ESCALATION STATES</div>""", unsafe_allow_html=True)
    state_legend = [("NOMINAL","#27AE60"),("ANOMALOUS","#F2C94C"),("PRE-CONFLICT","#F2994A"),("ACTIVE THREAT","#EB5757")]
    for sname, scolor in state_legend:
        st.markdown(f"""<div style='display:flex;align-items:center;gap:10px;margin:6px 0'><div style='width:14px;height:14px;background:{scolor};flex-shrink:0'></div><span style='color:{scolor};font-family:Share Tech Mono,monospace;font-size:13px;font-weight:bold;'>{sname}</span></div>""", unsafe_allow_html=True)

    prog = (st.session_state.sim_time % (st.session_state.time_horizon * 3600)) / (st.session_state.time_horizon * 3600)
    if prog < 0.3:   cur_state, cur_col = "NOMINAL", "#27AE60"
    elif prog < 0.5: cur_state, cur_col = "ANOMALOUS", "#F2C94C"
    elif prog < 0.7: cur_state, cur_col = "PRE-CONFLICT", "#F2994A"
    else:            cur_state, cur_col = "ACTIVE THREAT", "#EB5757"

    st.markdown(f"""<div style='margin-top:12px;padding:12px;background:#111E35;border:1px solid #1A2D4F;border-left:4px solid {cur_col}'>
      <div style='font-family:Share Tech Mono,monospace;font-size:11px;color:#8BA3C7;font-weight:bold;'>CURRENT STATE</div>
      <div style='font-family:Orbitron,monospace;font-size:16px;color:{cur_col};margin-top:4px;font-weight:bold;'>{cur_state}</div>
    </div>""", unsafe_allow_html=True)



if st.session_state.sim_running:
  
    advance_simulation(4.0)
    time.sleep(0.5) 
    st.rerun()
