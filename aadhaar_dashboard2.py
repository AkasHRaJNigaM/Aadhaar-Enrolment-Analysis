"""
Aadhaar Enrollment Analysis Dashboard
======================================
Run with:  streamlit run aadhaar_dashboard.py
Requires:  pip install streamlit plotly pandas numpy
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aadhaar Enrollment Dashboard",
    page_icon="🪪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  — dark editorial theme with saffron accents
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --saffron : #FF6B00;
    --deep    : #090912;
    --surface : #111120;
    --card    : #181828;
    --border  : #252540;
    --text    : #E4E4F0;
    --muted   : #7878A0;
    --green   : #00D4AA;
    --blue    : #4F8EF7;
    --rose    : #FF4F82;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--deep);
    color: var(--text);
}

/* ── header ── */
.dash-header {
    background: linear-gradient(135deg, #FF6B00 0%, #FF4F82 55%, #4F8EF7 100%);
    padding: 2px;
    border-radius: 14px;
    margin-bottom: 1.6rem;
}
.dash-header-inner {
    background: var(--deep);
    border-radius: 12px;
    padding: 1.6rem 2rem 1.3rem;
}
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -1px;
    line-height: 1.1;
}
.dash-sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-top: 0.35rem;
    letter-spacing: 0.04em;
}
.badge {
    display: inline-block;
    background: rgba(255,107,0,0.12);
    border: 1px solid var(--saffron);
    color: var(--saffron);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    padding: 2px 10px;
    border-radius: 99px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* ── metric cards ── */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FF6B00, #FF4F82);
}
.metric-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}
.metric-delta { font-size: 0.77rem; margin-top: 0.3rem; color: var(--green); }
.metric-delta-warn { font-size: 0.77rem; margin-top: 0.3rem; color: var(--rose); }

/* ── section headings ── */
.sec-head {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #fff;
    margin: 1.8rem 0 0.15rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}
.sec-sub { font-size: 0.8rem; color: var(--muted); margin-bottom: 0.9rem; }

/* ── insight boxes ── */
.insight { background: rgba(79,142,247,0.07); border-left: 3px solid var(--blue);
           border-radius: 0 8px 8px 0; padding: 0.9rem 1.1rem;
           font-size: 0.84rem; color: var(--text); line-height: 1.65; margin-top: 0.8rem; }
.insight b { color: var(--blue); }
.warn    { background: rgba(255,107,0,0.07); border-left: 3px solid var(--saffron);
           border-radius: 0 8px 8px 0; padding: 0.9rem 1.1rem;
           font-size: 0.84rem; color: var(--text); line-height: 1.65; margin-top: 0.8rem; }
.warn b { color: var(--saffron); }

/* ── sidebar ── */
section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border); }
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── tabs ── */
.stTabs [data-baseweb="tab-list"] { background: var(--surface); border-radius: 10px; padding: 4px; gap: 3px; }
.stTabs [data-baseweb="tab"]      { background: transparent; border-radius: 7px; font-family:'DM Sans',sans-serif;
                                    font-size:0.86rem; font-weight:500; color:var(--muted)!important; padding:7px 16px; }
.stTabs [aria-selected="true"]    { background: var(--card)!important; color:#fff!important; }

.block-container { padding-top: 0.8rem; padding-bottom: 2rem; }
div[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SYNTHETIC DATA  (mirrors notebook structure & real analytical findings)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    rng = np.random.default_rng(42)

    states = [
        "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Maharashtra", "West Bengal",
        "Rajasthan", "Andhra Pradesh", "Tamil Nadu", "Karnataka", "Gujarat",
        "Odisha", "Telangana", "Assam", "Meghalaya", "Nagaland", "Mizoram",
        "Manipur", "Arunachal Pradesh", "Tripura", "Sikkim", "Kerala",
        "Punjab", "Haryana", "Himachal Pradesh", "Uttarakhand", "Jharkhand",
        "Chhattisgarh", "Goa", "Delhi", "Jammu and Kashmir", "Ladakh",
        "Puducherry", "Andaman and Nicobar Islands", "Lakshadweep",
        "Dadra and Nagar Haveli and Daman and Diu", "Chandigarh",
    ]

    pop_map = {
        "Uttar Pradesh": 252_000_000, "Bihar": 130_000_000, "Madhya Pradesh": 90_000_000,
        "Maharashtra": 131_000_000, "West Bengal": 103_000_000, "Rajasthan": 83_000_000,
        "Andhra Pradesh": 54_000_000, "Tamil Nadu": 81_000_000, "Karnataka": 72_000_000,
        "Gujarat": 74_000_000, "Odisha": 48_000_000, "Telangana": 40_000_000,
        "Assam": 36_000_000, "Meghalaya": 4_000_000, "Nagaland": 2_200_000,
        "Mizoram": 1_300_000, "Manipur": 3_200_000, "Arunachal Pradesh": 1_600_000,
        "Tripura": 4_200_000, "Sikkim": 700_000, "Kerala": 36_000_000,
        "Punjab": 31_000_000, "Haryana": 30_000_000, "Himachal Pradesh": 7_500_000,
        "Uttarakhand": 11_500_000, "Jharkhand": 40_000_000, "Chhattisgarh": 32_000_000,
        "Goa": 1_600_000, "Delhi": 35_000_000, "Jammu and Kashmir": 14_000_000,
        "Ladakh": 300_000, "Puducherry": 1_600_000,
        "Andaman and Nicobar Islands": 430_000, "Lakshadweep": 70_000,
        "Dadra and Nagar Haveli and Daman and Diu": 640_000, "Chandigarh": 1_200_000,
    }

    ne_states = {
        "Meghalaya", "Nagaland", "Assam", "Mizoram", "Manipur",
        "Tripura", "Arunachal Pradesh", "Sikkim",
    }

    months = pd.date_range("2025-01-01", "2025-12-01", freq="MS")
    records = []

    for state in states:
        pop = pop_map.get(state, 5_000_000)
        base = int(pop * rng.uniform(0.0008, 0.0035))
        ne = state in ne_states

        for m in months:
            if m.month == 8:
                total = 0
            else:
                seasonal = 1 + 0.4 * np.sin((m.month - 3) * np.pi / 6)
                spike    = rng.uniform(1.8, 3.2) if m.month in (9, 10) else 1.0
                noise    = rng.uniform(0.7, 1.4) * (rng.uniform(1.3, 2.6) if ne else 1.0)
                total    = max(0, int(base * seasonal * spike * noise))

            adult_frac = rng.uniform(0.22, 0.46) if ne else rng.uniform(0.02, 0.06)
            age18  = int(total * adult_frac)
            rem    = total - age18
            frac05 = rng.uniform(0.58, 0.72)
            age05  = int(rem * frac05)
            age517 = rem - age05

            # 4 pincode sub-rows per state/month
            for _ in range(4):
                frac = rng.uniform(0.05, 0.40)
                pt   = max(0, int(total * frac))
                records.append({
                    "date":             m,
                    "state_clean":      state,
                    "pincode":          int(rng.integers(100_000, 999_999)),
                    "age_0_5":          int(pt * frac05),
                    "age_5_17":         int(pt * (1 - frac05) * (1 - adult_frac)),
                    "age_18_greater":   int(pt * adult_frac),
                    "total_enrollment": pt,
                })

    df  = pd.DataFrame(records)
    df["Month"] = df["date"].dt.strftime("%b")
    pop_df = pd.DataFrame(list(pop_map.items()), columns=["state_clean", "population"])
    return df, pop_df

df, pop_df = get_data()


# ─────────────────────────────────────────────────────────────────────────────
# PRE-COMPUTE AGGREGATES
# ─────────────────────────────────────────────────────────────────────────────
COLS = ["age_0_5", "age_5_17", "age_18_greater", "total_enrollment"]

state_agg = (
    df.groupby("state_clean")[COLS].sum().reset_index()
      .merge(pop_df, on="state_clean", how="left")
)
state_agg["per_1k"]       = (state_agg["total_enrollment"] / state_agg["population"] * 1000).round(1)
state_agg["adult_share"]  = (state_agg["age_18_greater"]  / state_agg["total_enrollment"]).round(4)

monthly_agg = df.groupby("date")[COLS].sum().reset_index()
monthly_agg["Month"] = monthly_agg["date"].dt.strftime("%b")

state_monthly = df.groupby(["state_clean", "date"])["total_enrollment"].sum().reset_index()
cv_table = (
    state_monthly.groupby("state_clean")
    .agg(mean_e=("total_enrollment", "mean"), std_e=("total_enrollment", "std"))
    .assign(cv=lambda x: x["std_e"] / x["mean_e"])
    .replace([np.inf, -np.inf], np.nan).dropna(subset=["cv"])
    .reset_index()
    .sort_values("cv", ascending=False)
)

quadrant = (
    state_agg[["state_clean", "adult_share"]]
    .merge(cv_table[["state_clean", "cv"]], on="state_clean")
)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME  (dark, transparent background)
# ─────────────────────────────────────────────────────────────────────────────
PAL = {
    "saffron": "#FF6B00", "green": "#00D4AA",
    "blue":    "#4F8EF7", "rose":  "#FF4F82",
    "card":    "#181828", "border":"#252540",
    "text":    "#E4E4F0", "muted": "#7878A0",
}

T = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=PAL["text"], size=12),
    xaxis=dict(gridcolor=PAL["border"], linecolor=PAL["border"], zerolinecolor=PAL["border"]),
    yaxis=dict(gridcolor=PAL["border"], linecolor=PAL["border"], zerolinecolor=PAL["border"]),
    margin=dict(l=10, r=10, t=36, b=10),
)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem;'>
        <div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:#FF6B00;'>🪪 Aadhaar</div>
        <div style='font-size:0.77rem;color:#7878A0;'>Enrollment Analytics · 2025</div>
    </div>
    <hr style='border-color:#252540;margin:0.4rem 0 1rem;'>
    """, unsafe_allow_html=True)

    all_states = sorted(df["state_clean"].unique())
    selected_states = st.multiselect(
        "Filter States",
        options=all_states,
        default=all_states[:14],
        help="States shown in state-level charts",
    )
    if not selected_states:
        selected_states = all_states

    age_filter = st.multiselect(
        "Age Groups",
        options=["Age 0–5", "Age 5–17", "Age 18+"],
        default=["Age 0–5", "Age 5–17", "Age 18+"],
    )
    if not age_filter:
        age_filter = ["Age 0–5", "Age 5–17", "Age 18+"]

    chart_style = st.radio("Bar Orientation", ["Vertical", "Horizontal"], index=0)

    st.markdown("""
    <hr style='border-color:#252540;'>
    <div style='font-size:0.74rem;color:#7878A0;line-height:1.65;'>
    <b style='color:#E4E4F0;'>Data Note</b><br>
    Synthetic data generated to mirror UIDAI Aadhaar enrollment structure.
    Patterns reflect real analytical findings from the source notebook.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="dash-header-inner">
    <div class="badge">India · UIDAI · 2025</div>
    <div class="dash-title">Aadhaar Enrollment<br>Analysis Dashboard</div>
    <div class="dash-sub">State-wise · Age-wise · Temporal · Per-Capita — Full-year enrollment intelligence</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
total_e   = int(df.total_enrollment.sum())
total_05  = int(df.age_0_5.sum())
total_517 = int(df.age_5_17.sum())
total_18  = int(df.age_18_greater.sum())
pct_05    = round(total_05  / total_e * 100, 1)
pct_517   = round(total_517 / total_e * 100, 1)
pct_18    = round(total_18  / total_e * 100, 1)

def kpi_card(label, value, delta, warn=False):
    delta_cls = "metric-delta-warn" if warn else "metric-delta"
    return f"""<div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="{delta_cls}">{delta}</div>
    </div>"""

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(kpi_card("Total Enrollments",  f"{total_e/1e6:.1f}M",   "All states · FY 2025"), unsafe_allow_html=True)
with c2: st.markdown(kpi_card("Age 0–5 Share",      f"{pct_05}%",            f"{total_05/1e6:.1f}M enrollments"), unsafe_allow_html=True)
with c3: st.markdown(kpi_card("Age 5–17 Share",     f"{pct_517}%",           f"{total_517/1e6:.1f}M enrollments"), unsafe_allow_html=True)
with c4: st.markdown(kpi_card("Age 18+ Share",      f"{pct_18}%",            f"{total_18/1e6:.1f}M enrollments", warn=True), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  State Overview",
    "📅  Time Trends",
    "🧮  Age Analysis",
    "📈  Volatility & Quadrant",
    "🗺️  Per-Capita Intensity",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — STATE OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">State-wise Total Enrollments</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Sorted by absolute enrollment volume across all age groups</div>', unsafe_allow_html=True)

    filt = state_agg[state_agg.state_clean.isin(selected_states)]

    col_chart, col_top = st.columns([3, 1])
    with col_chart:
        if chart_style == "Horizontal":
            fig = px.bar(
                filt.sort_values("total_enrollment"),
                x="total_enrollment", y="state_clean", orientation="h",
                color="total_enrollment",
                color_continuous_scale=["#4F8EF7", "#FF6B00", "#FF4F82"],
            )
        else:
            fig = px.bar(
                filt.sort_values("total_enrollment", ascending=False),
                x="state_clean", y="total_enrollment",
                color="total_enrollment",
                color_continuous_scale=["#4F8EF7", "#FF6B00", "#FF4F82"],
            )
        fig.update_layout(**T, coloraxis_showscale=False,
                          xaxis_tickangle=-50 if chart_style == "Vertical" else 0,
                          yaxis_title="Enrollments", xaxis_title="")
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col_top:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:0.88rem;font-weight:700;color:#fff;margin-bottom:0.7rem;">Top 5 States</div>', unsafe_allow_html=True)
        top5 = state_agg.sort_values("total_enrollment", ascending=False).head(5)
        max_e = top5.total_enrollment.max()
        for _, row in top5.iterrows():
            pct = row.total_enrollment / max_e
            st.markdown(f"""
            <div style='margin-bottom:0.8rem;'>
              <div style='display:flex;justify-content:space-between;font-size:0.77rem;margin-bottom:3px;'>
                <span style='color:#E4E4F0;font-weight:500;'>{row.state_clean}</span>
                <span style='color:#FF6B00;font-weight:700;'>{row.total_enrollment/1e6:.1f}M</span>
              </div>
              <div style='background:#252540;border-radius:99px;height:5px;'>
                <div style='background:linear-gradient(90deg,#FF6B00,#FF4F82);width:{pct*100:.0f}%;height:5px;border-radius:99px;'></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="insight">
    <b>Key Finding:</b> Uttar Pradesh dominates absolute volumes as India's most populous state.
    Bihar and Madhya Pradesh follow. Meanwhile North-Eastern states like Meghalaya and Assam show
    disproportionately high activity relative to population — a signature of policy-driven enrollment campaigns.
    </div>""", unsafe_allow_html=True)

    # Stacked age bar
    st.markdown('<div class="sec-head" style="margin-top:1.6rem;">Age-wise Distribution by State</div>', unsafe_allow_html=True)
    filt2 = state_agg[state_agg.state_clean.isin(selected_states)].sort_values("total_enrollment", ascending=False)
    fig2 = go.Figure()
    age_cols = [
        ("age_0_5",        "Age 0–5",  PAL["blue"]),
        ("age_5_17",       "Age 5–17", PAL["green"]),
        ("age_18_greater", "Age 18+",  PAL["rose"]),
    ]
    for col, lbl, color in age_cols:
        if lbl in age_filter:
            fig2.add_trace(go.Bar(x=filt2.state_clean, y=filt2[col],
                                  name=lbl, marker_color=color, marker_line_width=0))
    fig2.update_layout(**T, barmode="stack", xaxis_tickangle=-55,
                       legend=dict(orientation="h", y=1.07, bgcolor="rgba(0,0,0,0)"),
                       yaxis_title="Enrollments")
    st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — TIME TRENDS
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">Monthly Enrollment Trend — All India</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">August 2025 shows the UIDAI regulatory halt</div>', unsafe_allow_html=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=monthly_agg["date"], y=monthly_agg["total_enrollment"],
        mode="lines+markers", name="Total Enrollments",
        line=dict(color=PAL["saffron"], width=2.5),
        marker=dict(size=7, color=PAL["saffron"]),
        fill="tozeroy", fillcolor="rgba(255,107,0,0.07)",
    ))
    ymax = monthly_agg.total_enrollment.max()
    fig3.add_vline(x="2025-08-01", line_dash="dot", line_color=PAL["rose"], line_width=1.5)
    fig3.add_annotation(
        x="2025-08-01", y=ymax * 0.80,
        text="⚠ UIDAI Regulatory Halt<br>August 2025",
        showarrow=False, font=dict(color=PAL["rose"], size=10.5),
        bgcolor="rgba(255,79,130,0.08)", bordercolor=PAL["rose"],
        borderwidth=1, borderpad=6,
    )
    fig3.update_layout(**T, hovermode="x unified", yaxis_title="Total Enrollments", xaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

    # Age group lines
    st.markdown('<div class="sec-head">Age-Group Monthly Trends</div>', unsafe_allow_html=True)
    fig4 = go.Figure()
    for col, lbl, color in age_cols:
        if lbl in age_filter:
            fig4.add_trace(go.Scatter(
                x=monthly_agg["date"], y=monthly_agg[col],
                mode="lines+markers", name=lbl,
                line=dict(color=color, width=2), marker=dict(size=6),
            ))
    fig4.update_layout(**T, hovermode="x unified",
                       legend=dict(orientation="h", y=1.07, bgcolor="rgba(0,0,0,0)"),
                       yaxis_title="Enrollments", xaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)

    # Percentage table
    st.markdown('<div class="sec-head">Monthly Age-Share Table</div>', unsafe_allow_html=True)
    pct_tbl = monthly_agg.copy()
    pct_tbl["Age 0–5 %"]  = (pct_tbl.age_0_5          / pct_tbl.total_enrollment * 100).round(1)
    pct_tbl["Age 5–17 %"] = (pct_tbl.age_5_17          / pct_tbl.total_enrollment * 100).round(1)
    pct_tbl["Age 18+ %"]  = (pct_tbl.age_18_greater    / pct_tbl.total_enrollment * 100).round(1)
    pct_tbl["Month"]      = pct_tbl["date"].dt.strftime("%b %Y")
    display_tbl = pct_tbl[pct_tbl.date.dt.month != 8][
        ["Month", "total_enrollment", "Age 0–5 %", "Age 5–17 %", "Age 18+ %"]
    ].copy()
    display_tbl.columns = ["Month", "Total Enrollments", "Age 0–5 %", "Age 5–17 %", "Age 18+ %"]
    st.dataframe(
        display_tbl.style
            .format({"Total Enrollments": "{:,.0f}"})
            .background_gradient(subset=["Age 0–5 %"],  cmap="Blues")
            .background_gradient(subset=["Age 18+ %"],  cmap="Reds"),
        use_container_width=True, hide_index=True,
    )

    st.markdown("""<div class="warn">
    <b>August 2025 — Zero Enrollments:</b> UIDAI announced major regulatory changes on August 28 2025,
    causing a complete halt in processing. The September–October rebound reflects deferred enrollments
    clearing the backlog post-update.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — AGE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">National Age-Group Share</div>', unsafe_allow_html=True)

    col_pie, col_txt = st.columns([1, 2])
    with col_pie:
        fig_pie = go.Figure(go.Pie(
            labels=["Age 0–5", "Age 5–17", "Age 18+"],
            values=[pct_05, pct_517, pct_18],
            hole=0.55,
            marker=dict(
                colors=[PAL["blue"], PAL["green"], PAL["rose"]],
                line=dict(color=PAL["card"], width=3),
            ),
            textinfo="label+percent",
            textfont=dict(size=12, color=PAL["text"]),
        ))
        fig_pie.update_layout(
            **T, showlegend=False,
            annotations=[dict(
                text=f"<b>{total_e/1e6:.1f}M</b><br>Total",
                showarrow=False, font=dict(size=13, color=PAL["text"]),
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_txt:
        st.markdown(f"""<div class="insight" style="margin-top:1.5rem;">
        <b>~{pct_05 + pct_517:.0f}% of all enrollments are under age 18.</b><br><br>
        This aligns with India's <b>APAAR Yojana</b> (Ministry of Education), which mandates
        Aadhaar-linked academic IDs for school children.
        Early-life documentation is now a prerequisite for school admission, driving the dominant
        0–5 and 5–17 share.<br><br>
        The 18+ share is minimal nationally, suggesting adult enrollment has reached saturation.
        The strategic focus has clearly shifted toward ensuring children are registered at birth or
        school entry — a maturing identity infrastructure.
        </div>""", unsafe_allow_html=True)

    # Adult share bar
    st.markdown('<div class="sec-head">Adult Share (18+) by State</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Proportion of 18+ enrollments in each state\'s total</div>', unsafe_allow_html=True)

    adult_df = state_agg[state_agg.state_clean.isin(selected_states)].sort_values("adult_share", ascending=False)
    fig_a = px.bar(
        adult_df, x="state_clean", y="adult_share",
        color="adult_share",
        color_continuous_scale=["#4F8EF7", "#FF4F82", "#FF6B00"],
        labels={"adult_share": "Adult Share", "state_clean": ""},
    )
    fig_a.update_layout(**T, coloraxis_showscale=False,
                        xaxis_tickangle=-55, yaxis_tickformat=".0%")
    fig_a.update_traces(marker_line_width=0)
    st.plotly_chart(fig_a, use_container_width=True)

    st.markdown("""<div class="insight">
    <b>North-Eastern outliers:</b> States like Meghalaya, Nagaland, and Assam show adult shares of 25–40%,
    far above the national average. This reflects government-led corrective inclusion drives,
    high migration churn, and historically low prior Aadhaar coverage in these regions.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — VOLATILITY & QUADRANT
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">Enrollment Volatility (CV) by State</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Coefficient of Variation — higher = more erratic / campaign-driven enrollment</div>', unsafe_allow_html=True)

    cv_filt  = cv_table[cv_table.state_clean.isin(selected_states)].sort_values("cv", ascending=False)
    mean_cv  = cv_filt.cv.mean()

    fig_cv = px.bar(
        cv_filt, x="state_clean", y="cv",
        color="cv",
        color_continuous_scale=["#00D4AA", "#4F8EF7", "#FF4F82"],
        labels={"cv": "CV", "state_clean": ""},
    )
    fig_cv.add_hline(
        y=mean_cv, line_dash="dot", line_color=PAL["rose"],
        annotation_text=f"Mean CV: {mean_cv:.2f}",
        annotation_font_color=PAL["rose"],
    )
    fig_cv.update_layout(**T, coloraxis_showscale=False, xaxis_tickangle=-55)
    fig_cv.update_traces(marker_line_width=0)
    st.plotly_chart(fig_cv, use_container_width=True)

    # Quadrant scatter
    st.markdown('<div class="sec-head">Adult Share × Enrollment Volatility — Quadrant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Median lines divide the four strategic enrollment archetypes</div>', unsafe_allow_html=True)

    med_as = quadrant.adult_share.median()
    med_cv = quadrant.cv.median()

    fig_q = px.scatter(
        quadrant, x="adult_share", y="cv",
        text="state_clean", color="cv",
        color_continuous_scale=["#4F8EF7", "#00D4AA", "#FF6B00", "#FF4F82"],
        size=[14] * len(quadrant),
    )
    fig_q.add_vline(x=med_as, line_dash="dash", line_color=PAL["rose"], line_width=1)
    fig_q.add_hline(y=med_cv, line_dash="dash", line_color=PAL["rose"], line_width=1)
    fig_q.update_traces(
        textposition="top center",
        textfont=dict(size=8.5, color=PAL["muted"]),
        marker_line_width=0,
    )

    quadrant_labels = [
        (med_as * 0.25, med_cv * 1.45, "Low Adult · High Volatility\nInstitutional pressure", PAL["blue"]),
        (med_as * 1.55, med_cv * 1.45, "High Adult · High Volatility\nCorrective inclusion",   PAL["rose"]),
        (med_as * 0.25, med_cv * 0.45, "Low Adult · Low Volatility\nSteady child enrollment",  PAL["green"]),
        (med_as * 1.55, med_cv * 0.45, "High Adult · Low Volatility\nStable adult onboarding", PAL["saffron"]),
    ]
    for x, y, txt, color in quadrant_labels:
        fig_q.add_annotation(
            x=x, y=y, text=txt, showarrow=False,
            font=dict(size=8.8, color=color),
            bgcolor="rgba(24,24,40,0.85)", bordercolor=color,
            borderwidth=1, borderpad=5,
        )

    fig_q.update_layout(
        **T, coloraxis_showscale=False,
        xaxis_title="Adult Share (18+ / Total)",
        yaxis_title="Enrollment Volatility (CV)",
        xaxis_tickformat=".0%",
        height=520,
    )
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("""<div class="insight">
    <b>Quadrant Insights:</b><br>
    • <b style='color:#FF4F82;'>High Adult / High CV (top-right)</b> — Meghalaya & NE states: government-led corrective drives.<br>
    • <b style='color:#4F8EF7;'>Low Adult / High CV (top-left)</b> — Tamil Nadu: child-focused institutional enrollment with periodic bursts.<br>
    • <b style='color:#00D4AA;'>Low Adult / Low CV (bottom-left)</b> — Most large states: routine, steady child enrollment.<br>
    • High overall CVs across all states indicate enrollment is predominantly campaign-driven rather than organic.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — PER-CAPITA INTENSITY
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-head">Enrollment Rate per 1,000 Population</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Population-normalised using 2025 state estimates</div>', unsafe_allow_html=True)

    pc_filt = state_agg[state_agg.state_clean.isin(selected_states)].sort_values("per_1k", ascending=True)

    fig_pc = px.bar(
        pc_filt, x="per_1k", y="state_clean", orientation="h",
        color="per_1k",
        color_continuous_scale=["#4F8EF7", "#00D4AA", "#FF6B00", "#FF4F82"],
        labels={"per_1k": "Enrollments per 1,000", "state_clean": ""},
    )
    fig_pc.update_layout(
        **T, coloraxis_showscale=False,
        xaxis_title="Enrollments per 1,000 residents",
        height=max(420, len(pc_filt) * 22),
    )
    fig_pc.update_traces(marker_line_width=0)
    st.plotly_chart(fig_pc, use_container_width=True)

    # Age-wise grouped per-capita
    st.markdown('<div class="sec-head">Age-wise Per-Capita Intensity</div>', unsafe_allow_html=True)
    apc = state_agg[state_agg.state_clean.isin(selected_states)].copy()
    apc["0–5 /1k"]  = (apc.age_0_5          / apc.population * 1000).round(1)
    apc["5–17 /1k"] = (apc.age_5_17          / apc.population * 1000).round(1)
    apc["18+ /1k"]  = (apc.age_18_greater    / apc.population * 1000).round(1)
    apc = apc.sort_values("per_1k", ascending=False)

    fig_pc2 = go.Figure()
    age_pc_cols = [
        ("0–5 /1k",  "Age 0–5",  PAL["blue"]),
        ("5–17 /1k", "Age 5–17", PAL["green"]),
        ("18+ /1k",  "Age 18+",  PAL["rose"]),
    ]
    for col, lbl, color in age_pc_cols:
        if lbl in age_filter:
            fig_pc2.add_trace(go.Bar(
                x=apc.state_clean, y=apc[col],
                name=lbl, marker_color=color, marker_line_width=0,
            ))
    fig_pc2.update_layout(
        **T, barmode="group", xaxis_tickangle=-55,
        legend=dict(orientation="h", y=1.07, bgcolor="rgba(0,0,0,0)"),
        yaxis_title="Enrollments per 1,000",
    )
    st.plotly_chart(fig_pc2, use_container_width=True)

    # Summary table
    st.markdown('<div class="sec-head">State Summary Table</div>', unsafe_allow_html=True)
    summary = state_agg[["state_clean", "total_enrollment", "adult_share", "per_1k", "population"]].copy()
    summary.columns = ["State", "Total Enrollments", "Adult Share", "Enr / 1k Pop", "Population (2025)"]
    summary["Adult Share"] = (summary["Adult Share"] * 100).round(1).astype(str) + "%"
    summary = summary.sort_values("Enr / 1k Pop", ascending=False).reset_index(drop=True)
    st.dataframe(
        summary.style
            .format({"Total Enrollments": "{:,.0f}", "Enr / 1k Pop": "{:.1f}", "Population (2025)": "{:,.0f}"})
            .background_gradient(subset=["Enr / 1k Pop"], cmap="YlOrRd"),
        use_container_width=True, hide_index=True,
    )

    st.markdown("""<div class="insight">
    <b>Per-Capita Insight:</b> Small North-Eastern states dominate population-normalised rates,
    with figures 3–8× the national average — a direct result of administrative enrollment drives.
    Large states like Uttar Pradesh and Bihar record high absolute volumes but modest per-capita rates,
    reflecting a mature, population-proportional enrollment regime.
    The 5–17 band contributes the most per-capita intensity in nearly every state — the <b>APAAR effect</b>.
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='border-top:1px solid #252540;padding-top:0.9rem;display:flex;
            justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;'>
  <div style='font-size:0.76rem;color:#7878A0;'>
    Built from <b style='color:#FF6B00;'>Aadhaar Enrollment Analysis Notebook</b> ·
    Synthetic data mirroring UIDAI structure
  </div>
  <div style='font-size:0.76rem;color:#7878A0;'>Streamlit · Plotly · DM Sans · Syne</div>
</div>
""", unsafe_allow_html=True)
