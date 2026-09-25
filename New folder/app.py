"""
Nassau Candy Distributor - Shipping Route Efficiency Dashboard (v2 - Polished)
Run: streamlit run app.py
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from state_codes import US_STATE_ABBR
from pathlib import path

st.set_page_config(page_title="Nassau Candy | Route Efficiency", page_icon="🍬", layout="wide")

# ===========================================================
# THEME TOKENS
# ===========================================================
BG = "#1A1523"
CARD = "#241D31"
CARD_BORDER = "#3A2E4D"
GOLD = "#E8A33D"
CHERRY = "#E4572E"
MINT = "#4ECDC4"
CREAM = "#F5EFE6"
MUTED = "#B7A9C9"

PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(family="Inter, sans-serif", color=CREAM, size=13),
        title=dict(font=dict(family="Fraunces, serif", size=18, color=CREAM)),
        colorway=[GOLD, MINT, CHERRY, "#8E7CC3", "#6FA8DC"],
        xaxis=dict(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER, linecolor=CARD_BORDER),
        yaxis=dict(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER, linecolor=CARD_BORDER),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=60, l=10, r=10, b=10),
    )
)

# ===========================================================
# CSS
# ===========================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

/* Page background */
.stApp {{ background-color: {BG}; }}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {CARD};
    border-right: 1px solid {CARD_BORDER};
}}
section[data-testid="stSidebar"] h1 {{ font-family: 'Fraunces', serif; }}

/* Headings */
h1, h2, h3 {{ font-family: 'Fraunces', serif !important; color: {CREAM} !important; letter-spacing: -0.01em; }}

/* Hero banner */
.hero {{
    background: linear-gradient(120deg, {CARD} 0%, #2E2340 100%);
    border: 1px solid {CARD_BORDER};
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 22px;
}}
.hero .eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    color: {GOLD};
    letter-spacing: 0.12em;
    font-size: 12px;
    text-transform: uppercase;
}}
.hero h1 {{ margin: 6px 0 4px 0; font-size: 34px; }}
.hero p {{ color: {MUTED}; margin: 0; font-size: 15px; }}

/* KPI wrapper cards */
.kpi-row {{ display: flex; gap: 16px; margin-bottom: 22px; flex-wrap: wrap; }}
.kpi-card {{
    flex: 1;
    min-width: 190px;
    background: {CARD};
    border: 1px solid {CARD_BORDER};
    border-left: 4px solid {GOLD};
    border-radius: 12px;
    padding: 16px 18px;
}}
.kpi-card .label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
.kpi-card .value {{
    font-family: 'Fraunces', serif;
    font-size: 30px;
    color: {CREAM};
    margin-top: 4px;
}}

/* Section divider */
.section-title {{
    display: flex; align-items: center; gap: 10px;
    margin: 8px 0 14px 0;
}}
.section-title .dot {{ width: 8px; height: 8px; border-radius: 50%; background: {GOLD}; }}
.section-title span {{ font-family: 'Fraunces', serif; font-size: 20px; color: {CREAM}; }}

/* Dataframe container polish */
[data-testid="stDataFrame"] {{ border: 1px solid {CARD_BORDER}; border-radius: 10px; overflow: hidden; }}

/* Tabs */
button[data-baseweb="tab"] {{ font-family: 'Inter', sans-serif; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)


def kpi_card(label, value):
    return f'<div class="kpi-card"><div class="label">{label}</div><div class="value">{value}</div></div>'


def section_title(text):
    st.markdown(f'<div class="section-title"><div class="dot"></div><span>{text}</span></div>', unsafe_allow_html=True)


# ===========================================================
# LOAD DATA
# ===========================================================
@st.cache_data
def load_data():
    file_path=Path(__file__).parent / "Data" / "cleaned_data.csv"
    df=pd.read_csv(file_path, parse_dates=["Order Date","Ship Date"])
    return df

df = load_data()

# ===========================================================
# HERO HEADER
# ===========================================================
st.markdown("""
<div class="hero">
    <div class="eyebrow">Logistics Intelligence &middot; Nassau Candy Distributor</div>
    <h1>🍬 Factory-to-Customer Route Efficiency</h1>
    <p>Where shipments run smooth, and where they get stuck — by route, region, and ship mode.</p>
</div>
""", unsafe_allow_html=True)

# ===========================================================
# SIDEBAR FILTERS
# ===========================================================
st.sidebar.markdown("# Filters")

min_date, max_date = df["Order Date"].min(), df["Order Date"].max()
date_range = st.sidebar.date_input("Order Date range", (min_date, max_date))

regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=list(df["Region"].unique()))
states = st.sidebar.multiselect("State/Province", sorted(df["State/Province"].unique()))
ship_modes = st.sidebar.multiselect("Ship Mode", sorted(df["Ship Mode"].unique()), default=list(df["Ship Mode"].unique()))
lead_time_threshold = st.sidebar.slider(
    "Lead-time delay threshold (days)",
    int(df["Lead Time (Days)"].min()),
    int(df["Lead Time (Days)"].max()),
    int(df["Lead Time (Days)"].median()),
)

mask = (
    (df["Order Date"] >= pd.to_datetime(date_range[0]))
    & (df["Order Date"] <= pd.to_datetime(date_range[-1]))
    & (df["Region"].isin(regions))
    & (df["Ship Mode"].isin(ship_modes))
)
if states:
    mask &= df["State/Province"].isin(states)

fdf = df[mask]
st.sidebar.caption(f"**{len(fdf):,}** shipments match filters")

# ===========================================================
# KPI ROW
# ===========================================================
delay_pct = (fdf["Lead Time (Days)"] > lead_time_threshold).mean() * 100 if len(fdf) else 0
st.markdown(
    '<div class="kpi-row">'
    + kpi_card("Total Shipments", f"{len(fdf):,}")
    + kpi_card("Avg Lead Time", f"{fdf['Lead Time (Days)'].mean():.1f} days")
    + kpi_card("Total Sales", f"${fdf['Sales'].sum():,.0f}")
    + kpi_card("Above Threshold", f"{delay_pct:.1f}%")
    + '</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊  Route Efficiency", "🗺️  Geographic Map", "🚚  Ship Mode", "🔍  Drill-Down"]
)

# ===========================================================
# TAB 1: ROUTE EFFICIENCY
# ===========================================================
with tab1:
    section_title("Route Performance Leaderboard (Factory → State)")

    route_summary = (
        fdf.groupby("Route (State)")
        .agg(
            Total_Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Lead Time (Days)", "mean"),
            Lead_Time_StdDev=("Lead Time (Days)", lambda s: s.std(ddof=0)),
        )
        .reset_index()
        .round(1)
    )
    route_summary["Lead_Time_StdDev"] = route_summary["Lead_Time_StdDev"].fillna(0)

    # Efficiency Score: routes with LOWER average lead time score higher (0-100)
    min_lt, max_lt = route_summary["Avg_Lead_Time"].min(), route_summary["Avg_Lead_Time"].max()
    lt_span = max(max_lt - min_lt, 1)
    route_summary["Efficiency Score"] = (100 * (1 - (route_summary["Avg_Lead_Time"] - min_lt) / lt_span)).round(0)

    # Consistency Score: routes with LOWER variability (std dev) score higher (0-100).
    # This is what makes a route "consistently" efficient, not just fast on average once.
    max_std = route_summary["Lead_Time_StdDev"].max()
    if max_std > 0:
        route_summary["Consistency Score"] = (100 * (1 - route_summary["Lead_Time_StdDev"] / max_std)).round(0)
    else:
        route_summary["Consistency Score"] = 100

    # Overall Score blends both: 60% how fast, 40% how consistent
    route_summary["Overall Score"] = (
        0.6 * route_summary["Efficiency Score"] + 0.4 * route_summary["Consistency Score"]
    ).round(0)

    route_summary = route_summary.sort_values("Overall Score", ascending=False)
    display_cols = [
        "Route (State)", "Total_Shipments", "Avg_Lead_Time",
        "Lead_Time_StdDev", "Consistency Score", "Overall Score",
    ]

    st.caption(
        "**Overall Score** = 60% speed (Efficiency Score) + 40% reliability (Consistency Score). "
        "A route can be fast on average but *inconsistent* (some shipments quick, others very slow) — "
        "Consistency Score penalizes that, so a route only ranks high here if it's fast **and** dependable."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Top 10 Most Consistently Efficient** &nbsp;<span style='color:{MINT}'>●</span>", unsafe_allow_html=True)
        st.dataframe(
            route_summary.head(10)[display_cols],
            use_container_width=True, hide_index=True,
            column_config={
                "Consistency Score": st.column_config.ProgressColumn(
                    "Consistency Score", min_value=0, max_value=100, format="%d"
                ),
                "Overall Score": st.column_config.ProgressColumn(
                    "Overall Score", min_value=0, max_value=100, format="%d"
                ),
                "Lead_Time_StdDev": st.column_config.NumberColumn("Lead Time Variability (± days)"),
            },
        )
    with col2:
        st.markdown(f"**Bottom 10 Least Consistent / Efficient** &nbsp;<span style='color:{CHERRY}'>●</span>", unsafe_allow_html=True)
        st.dataframe(
            route_summary.tail(10).sort_values("Overall Score")[display_cols],
            use_container_width=True, hide_index=True,
            column_config={
                "Consistency Score": st.column_config.ProgressColumn(
                    "Consistency Score", min_value=0, max_value=100, format="%d"
                ),
                "Overall Score": st.column_config.ProgressColumn(
                    "Overall Score", min_value=0, max_value=100, format="%d"
                ),
                "Lead_Time_StdDev": st.column_config.NumberColumn("Lead Time Variability (± days)"),
            },
        )

    top20 = route_summary.head(20).sort_values("Overall Score")
    fig = px.bar(
        top20,
        x="Overall Score", y="Route (State)", orientation="h",
        title="Overall Score — Top 20 Consistently Efficient Routes",
        labels={"Overall Score": "Overall Score (speed + consistency)", "Route (State)": ""},
        color="Overall Score", color_continuous_scale=[GOLD, MINT],
        hover_data=["Avg_Lead_Time", "Lead_Time_StdDev"],
    )
    fig.update_layout(template=PLOTLY_TEMPLATE, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ===========================================================
# TAB 2: GEOGRAPHIC MAP
# ===========================================================
with tab2:
    section_title("Shipping Efficiency Heatmap (US States)")

    state_summary = (
        fdf.groupby("State/Province")
        .agg(Shipments=("Order ID", "count"), Avg_Lead_Time=("Lead Time (Days)", "mean"))
        .reset_index()
    )
    state_summary["code"] = state_summary["State/Province"].map(US_STATE_ABBR)
    us_states = state_summary.dropna(subset=["code"])

    fig_map = go.Figure()
    fig_map.add_trace(go.Choropleth(
        locations=us_states["code"], z=us_states["Avg_Lead_Time"], locationmode="USA-states",
        colorscale=[[0, MINT], [0.5, GOLD], [1, CHERRY]],
        marker_line_color=BG, marker_line_width=1.2,
        colorbar_title="Avg Lead<br>Time (days)",
    ))

    factories = fdf.drop_duplicates("Factory")[["Factory", "Factory Lat", "Factory Lon"]]
    fig_map.add_trace(go.Scattergeo(
        lon=factories["Factory Lon"], lat=factories["Factory Lat"],
        text=factories["Factory"], mode="markers+text",
        marker=dict(size=13, color=CREAM, line=dict(width=2, color=BG), symbol="star"),
        textposition="top center",
        textfont=dict(size=13, color=CREAM, family="Inter, sans-serif"),
        name="Factories",
    ))

    fig_map.update_layout(
        template=PLOTLY_TEMPLATE,
        geo=dict(scope="usa", bgcolor=CARD, lakecolor=CARD, showlakes=True,
                  landcolor="#2E2340", subunitcolor=BG),
        title="Darker red = higher average lead time (bottleneck) · Stars = factories",
        height=520,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    section_title("Regional Comparison")
    region_summary = (
        fdf.groupby("Region")
        .agg(Shipments=("Order ID", "count"), Avg_Lead_Time=("Lead Time (Days)", "mean"))
        .reset_index()
        .sort_values("Avg_Lead_Time", ascending=False)
    )
    fig_region = px.bar(
        region_summary, x="Region", y="Avg_Lead_Time", color="Avg_Lead_Time",
        color_continuous_scale=[MINT, GOLD, CHERRY],
        title="Average Lead Time by Region (higher = more bottleneck)",
    )
    fig_region.update_layout(template=PLOTLY_TEMPLATE, coloraxis_showscale=False)
    st.plotly_chart(fig_region, use_container_width=True)

    with st.expander("View full state-level table"):
        st.dataframe(state_summary.sort_values("Shipments", ascending=False), use_container_width=True, hide_index=True)

# ===========================================================
# TAB 3: SHIP MODE
# ===========================================================
with tab3:
    section_title("Lead Time by Ship Mode")
    fig_mode = px.box(fdf, x="Ship Mode", y="Lead Time (Days)", color="Ship Mode",
                       title="Lead Time Distribution by Ship Mode",
                       color_discrete_sequence=[GOLD, MINT, CHERRY, "#8E7CC3"])
    fig_mode.update_layout(template=PLOTLY_TEMPLATE, showlegend=False)
    st.plotly_chart(fig_mode, use_container_width=True)

    mode_summary = (
        fdf.groupby("Ship Mode")
        .agg(Shipments=("Order ID", "count"), Avg_Lead_Time=("Lead Time (Days)", "mean"), Avg_Sales=("Sales", "mean"))
        .round(1).reset_index().sort_values("Avg_Lead_Time")
    )
    st.dataframe(mode_summary, use_container_width=True, hide_index=True)

# ===========================================================
# TAB 4: DRILL-DOWN
# ===========================================================
with tab4:
    section_title("Drill Down Into a Specific State")
    chosen_state = st.selectbox("Choose State/Province", sorted(fdf["State/Province"].unique()))
    state_df = fdf[fdf["State/Province"] == chosen_state]

    st.caption(f"**{len(state_df)}** shipments to **{chosen_state}**")
    st.dataframe(
        state_df[["Order ID", "Order Date", "Ship Date", "Lead Time (Days)", "Ship Mode", "Factory", "Product Name", "Sales"]]
        .sort_values("Order Date"),
        use_container_width=True, hide_index=True,
    )

    fig_timeline = px.scatter(
        state_df, x="Order Date", y="Lead Time (Days)", color="Ship Mode",
        title=f"Order-Level Shipment Timeline — {chosen_state}",
        color_discrete_sequence=[GOLD, MINT, CHERRY, "#8E7CC3"],
    )
    fig_timeline.update_layout(template=PLOTLY_TEMPLATE)
    st.plotly_chart(fig_timeline, use_container_width=True)
