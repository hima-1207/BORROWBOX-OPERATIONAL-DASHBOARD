
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="BorrowBox Operational Monitoring Dashboard", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

CUSTOM_CSS = '''
<style>
:root {
    --bg: #efefef;
    --card: rgba(255,255,255,0.72);
    --border: #d6d6d6;
    --blue: #5b8fe3;
    --purple: #b08be8;
    --teal: #35c1b6;
    --orange: #f39c12;
    --text: #20304a;
}

html, body, [class*="css"] {
    font-family: 'Arial', sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

/* ---------- HERO ---------- */
.hero-wrap {
    position: relative;
    width: 100%;
    min-height: 360px;
    border-radius: 28px;
    background: #ececec;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.hero-dash-left,
.hero-dash-left-2 {
    position: absolute;
    left: 34px;
    width: 12px;
    height: 62px;
    border-radius: 16px;
    background: var(--teal);
    z-index: 1;
}
.hero-dash-left { top: 14px; }
.hero-dash-left-2 { top: 128px; }

.hero-orange-box {
    position: absolute;
    left: -18px;
    top: 132px;
    width: 130px;
    height: 130px;
    border: 8px solid var(--orange);
    border-radius: 8px;
    z-index: 1;
}

.hero-orange-angle {
    position: absolute;
    top: -24px;
    left: 48%;
    width: 180px;
    height: 100px;
    border-top: 8px solid var(--orange);
    border-left: 8px solid var(--orange);
    border-right: 8px solid var(--orange);
    transform: rotate(0deg);
    background: transparent;
    z-index: 1;
}

.hero-teal-curve {
    position: absolute;
    left: 110px;
    bottom: -34px;
    width: 210px;
    height: 180px;
    border-left: 10px dashed var(--teal);
    border-top: 10px dashed var(--teal);
    border-radius: 180px 0 0 0;
    transform: rotate(-18deg);
    z-index: 1;
}

.hero-circle-purple {
    position: absolute;
    left: 140px;
    top: 40px;
    width: 295px;
    height: 295px;
    border-radius: 50%;
    background: var(--purple);
    z-index: 1;
}

.hero-circle-teal {
    position: absolute;
    right: 70px;
    top: -24px;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: var(--teal);
    z-index: 1;
}

.hero-circle-blue {
    position: absolute;
    right: -140px;
    bottom: -180px;
    width: 860px;
    height: 860px;
    border-radius: 50%;
    background: var(--blue);
    z-index: 1;
}

.hero-title {
    position: absolute;
    right: 9%;
    top: 42%;
    transform: translateY(-50%);
    z-index: 5;
    color: #ffffff;
    font-size: 2.05rem;
    font-weight: 800;
    line-height: 1.12;
    text-align: center;
    max-width: 540px;
}

.hero-subtitle {
    position: absolute;
    right: 9%;
    top: 78%;
    transform: translateY(-50%);
    z-index: 5;
    color: #ffffff;
    font-size: 0.95rem;
    font-weight: 500;
    text-align: center;
    max-width: 520px;
}

/* ---------- TITLES ---------- */
.section-title {
    font-size: 2rem;
    font-weight: 800;
    color: #1b2a41;
    margin-top: 6px;
    margin-bottom: 6px;
}

.section-note {
    font-size: 1rem;
    color: #44546a;
    margin-bottom: 18px;
}

.info-chip {
    display: inline-block;
    background: #ffffff;
    color: #20304a;
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 8px 16px;
    font-weight: 700;
    margin-bottom: 14px;
}

/* ---------- KPI CARDS ---------- */
.kpi-card {
    background: rgba(255,255,255,0.72);
    border: 1.5px solid #d6d6d6;
    border-radius: 24px;
    padding: 18px 16px;
    min-height: 120px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 0.35rem !important;
}

.kpi-title {
    font-size: 1rem;
    font-weight: 700;
    color: #455468;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: #20304a;
}

.kpi-sub {
    font-size: 0.88rem;
    color: #64748b;
    margin-top: 6px;
}

/* ---------- CHART CONTAINER ---------- */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.72);
    border: 1.5px solid #d6d6d6;
    border-radius: 24px;
    padding: 10px 12px 6px 12px;
    margin-top: 0rem !important;
    margin-bottom: 0.6rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    overflow: hidden;
}

div[data-testid="stPlotlyChart"] > div {
    border-radius: 18px !important;
    overflow: hidden !important;
}

/* ---------- INSIGHT BOX ---------- */
.insight-box {
    background: rgba(255,255,255,0.8);
    border: 1.5px solid var(--border);
    border-left: 8px solid var(--teal);
    border-radius: 22px;
    padding: 16px 18px;
    margin-top: 6px;
    margin-bottom: 12px;
    color: #26374d;
}

/* ---------- FORM ---------- */
.stForm {
    background: rgba(255,255,255,0.72);
    border: 1.5px solid var(--border);
    border-radius: 24px;
    padding: 18px;
}

/* ---------- BUTTONS ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    border-radius: 999px !important;
    border: 2px solid var(--orange) !important;
    background: white !important;
    color: #1f2d3d !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.2rem !important;
}

/* ---------- TABLE ---------- */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.72);
    border: 1.5px solid var(--border);
    border-radius: 22px;
    padding: 8px;
}

/* tighten overall spacing */
div.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* reduce random spacing between elements */
.element-container {
    margin-bottom: 0.35rem !important;
}

/* tighten column vertical spacing */
[data-testid="column"] {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* KPI text cleanup */
.kpi-title {
    font-size: 1rem;
    font-weight: 700;
    color: #455468;
    margin-bottom: 10px;
    line-height: 1.25;
    min-height: 2.3rem;
}

.kpi-sub {
    font-size: 0.92rem;
    color: #44546a;
    margin-top: 10px;
    line-height: 1.6;
    min-height: 3.2rem;
}

/* chart containers cleaner */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.72);
    border: 1.5px solid #d6d6d6;
    border-radius: 24px;
    padding: 10px 12px 6px 12px;
    margin-top: 0rem !important;
    margin-bottom: 0.6rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    overflow: hidden;
}

/* keep plotly modebar out of the way */
.modebar {
    opacity: 0 !important;
    pointer-events: none !important;
}
.modebar:hover {
    opacity: 0.9 !important;
}
</style>
'''
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

DEFAULT_PATHS = ["BorrowBox_Dataset1.csv", r"C:\ASSIGNMENTS\MRP\BorrowBox_Dataset1.csv"]

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        found = None
        for p in DEFAULT_PATHS:
            if Path(p).exists():
                found = p
                break
        if found is None:
            raise FileNotFoundError("BorrowBox_Dataset1.csv not found. Upload it from the sidebar.")
        df = pd.read_csv(found)
    for col in ["reservation_date","pickup_scheduled_datetime","pickup_actual_datetime","return_due_datetime","return_actual_datetime"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    flag_cols = ["missing_parts_flag","damage_flag","inventory_available_at_reserve","notifications_enabled_flag","report_issue_in_app_flag","support_ticket_flag","cancellation_flag","cleaning_required_flag","cleaning_done_flag"]
    for col in flag_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    num_cols = ["late_hours","parts_expected","parts_returned","staff_checkout_minutes","staff_checkin_minutes","hub_queue_length","reminders_sent_count","staff_notes_length","penalty_amount_usd","borrow_days"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["month_name"] = df["reservation_date"].dt.strftime("%B")
    df["month_sort"] = df["reservation_date"].dt.month
    df["missing_parts_rate_row"] = np.where(df["parts_expected"] > 0, (df["parts_expected"] - df["parts_returned"]).clip(lower=0) / df["parts_expected"], 0)
    df["risk_score_row"] = (df["missing_parts_rate_row"] + df["damage_flag"].fillna(0)) / 2
    df["late_flag"] = (df["return_status"] == "Late").astype(int)
    df["no_show_flag"] = (df["pickup_status"] == "No-show").astype(int)
    df["cancel_flag"] = (df["pickup_status"] == "Cancelled").astype(int)
    return df

def filter_data(df, hubs, months, members):
    data = df.copy()
    if hubs:
        data = data[data["hub_name"].isin(hubs)]
    if months:
        data = data[data["month_name"].isin(months)]
    if members:
        data = data[data["member_status"].isin(members)]
    return data

def pct(n):
    return f"{n:.2%}"

def avg_num(n):
    return f"{n:.2f}"

def make_kpi_card(label, value, help_text=None):
    help_html = f"<div class='kpi-sub'>{help_text}</div>" if help_text else ""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{label}</div>
        <div class="kpi-value">{value}</div>
        {help_html}
    </div>
    """, unsafe_allow_html=True)

def style_plotly(fig, height=380, legend_position="bottom", top_margin=80, bottom_margin=70):
    legend_cfg = dict(
        orientation="h",
        bgcolor="rgba(255,255,255,0)",
        font=dict(size=10),
        title=None
    )

    if legend_position == "bottom":
        legend_cfg.update(
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5
        )
    elif legend_position == "right":
        legend_cfg.update(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    else:  # top
        legend_cfg.update(
            yanchor="bottom",
            y=1.08,
            xanchor="center",
            x=0.5
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.92)",
        height=height,
        margin=dict(l=30, r=20, t=top_margin, b=bottom_margin),
        font=dict(color="#30445f", size=13),
        title_font=dict(size=18, color="#1f2d3d"),
        legend=legend_cfg,
        uniformtext_minsize=9,
        uniformtext_mode="hide"
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(180,190,205,0.38)",
        zeroline=False,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=12),
        title_font=dict(size=12),
        automargin=True
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(180,190,205,0.38)",
        zeroline=False,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=12),
        title_font=dict(size=12),
        automargin=True
    )

    return fig

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------------- LOGIN SYSTEM ----------------
def show_login():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">Prototype login to simulate user and staff access.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Login</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This screen simulates how different people would enter the system based on their role.</div>", unsafe_allow_html=True)

    with st.form("login_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Name")
        with c2:
            role = st.selectbox("Login as", ["User", "Staff"])

        login_btn = st.form_submit_button("Sign In")

        if login_btn:
            if name.strip() == "":
                st.warning("Please enter a name.")
            else:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.user_name = name
                st.success(f"Signed in as {role}.")
                st.rerun()
if not st.session_state.logged_in:
    show_login()
    st.stop()                

# ---------------- SIDE BAR ----------------
st.sidebar.markdown("## BorrowBox Prototype")
st.sidebar.markdown(f"**Signed in as:** {st.session_state.user_name}")
st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_name = ""
    st.rerun()

upload = st.sidebar.file_uploader("Upload BorrowBox CSV if needed", type=["csv"])
df = load_data(upload)

all_hubs = sorted(df["hub_name"].dropna().unique().tolist())
month_order = df[["month_name","month_sort"]].dropna().drop_duplicates().sort_values("month_sort")["month_name"].tolist()
all_members = sorted(df["member_status"].dropna().unique().tolist())

selected_hubs = st.sidebar.multiselect("Filter by hub", all_hubs, default=[])
selected_months = st.sidebar.multiselect("Filter by month", month_order, default=[])
selected_members = st.sidebar.multiselect("Filter by member status", all_members, default=[])

if st.session_state.user_role == "User":
    available_pages = ["Home", "Book New Reservation"]
else:
    available_pages = ["Home", "User Behavior", "Inventory & Damage Risk", "Hub Operations", "Log Return Issue"]

page = st.sidebar.radio("Go to page", available_pages)
filtered = filter_data(df, selected_hubs, selected_months, selected_members)
if filtered.empty:
    st.warning("No rows match the current filters. Please change the sidebar selections.")
    st.stop()

no_show_rate = filtered["no_show_flag"].mean()
late_return_rate = filtered["late_flag"].mean()
missing_parts_rate = filtered["missing_parts_flag"].mean()
avg_checkin = filtered["staff_checkin_minutes"].mean()
damage_rate = filtered["damage_flag"].mean()
risk_score = filtered["risk_score_row"].mean()

# ---------------- PAGES ----------------
if page == "Home":
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">A prototype for tracking user behavior, inventory risk, and hub operations.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='info-chip'>Prototype MVP</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Landing Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This page gives a quick view of the current system and lets the user understand the product idea right away.</div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1: make_kpi_card("No-Show Rate", pct(no_show_rate), "Users who booked but did not come")
    with k2: make_kpi_card("Late Return Rate", pct(late_return_rate), "Reservations returned late")
    with k3: make_kpi_card("Missing Parts Rate", pct(missing_parts_rate), "Returns with incomplete item sets")
    with k4: make_kpi_card("Avg Check-in Time", avg_num(avg_checkin), "Minutes staff spend checking items")

    left, right = st.columns([1.2, 1])
    with left:
        monthly = filtered.groupby(["month_name","month_sort"], as_index=False).agg(requests=("reservation_id","count")).sort_values("month_sort")
        fig = px.line(
            monthly,
            x="month_name",
            y="requests",
            markers=True,
            text="requests",
            title="Borrow Requests Over Time"
        )
        fig.update_traces(textposition="top center", line=dict(width=3), marker=dict(size=8))
        fig = style_plotly(fig, height=360)
        fig.update_xaxes(title="Month")
        fig.update_yaxes(title="Request Count")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        member_dist = filtered["member_status"].value_counts().reset_index()
        member_dist.columns = ["member_status","count"]
        fig2 = px.pie(
            member_dist,
            names="member_status",
            values="count",
            title="User Mix",
            hole=0.45,
            color_discrete_sequence=["#5b8fe3", "#35c1b6", "#b08be8"]
        )
        fig2.update_traces(textposition="inside", textinfo="percent")
        fig2 = style_plotly(fig2, height=360)
        fig2.update_layout(
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.0,
                xanchor="left",
                x=1.02,
                font=dict(size=11)
            )
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='insight-box'><b>What this prototype shows:</b> BorrowBox can monitor the system through one landing page, then move into deeper views for user behavior, inventory risk, hub strain, and issue logging.</div>", unsafe_allow_html=True)

elif page == "User Behavior":
    if st.session_state.user_role != "Staff":
        st.warning("Only staff can access this page.")
        st.stop()
    
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">A prototype for tracking user behavior, inventory risk, and hub operations.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>User Behavior Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This page helps staff and managers understand whether users are following the expected borrowing process.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        make_kpi_card("No-Show Rate", pct(no_show_rate))
    with c2:
        make_kpi_card("Cancellation Rate", pct(filtered["cancel_flag"].mean()))
    with c3:
        make_kpi_card("Late Return Rate", pct(late_return_rate))

    # -------------------------------
    # Full-width No-show & Cancellation
    # -------------------------------
    ns = (
        filtered[filtered["pickup_status"].isin(["No-show", "Cancelled"])]
        .groupby(["hub_name", "month_name", "month_sort", "pickup_status"], as_index=False)
        .agg(count=("reservation_id", "count"))
        .sort_values(["month_sort", "hub_name"])
    )

    if not ns.empty:
        month_order = (
            ns[["month_name", "month_sort"]]
            .drop_duplicates()
            .sort_values("month_sort")["month_name"]
            .tolist()
        )

        hub_order = (
            ns.groupby("hub_name")["count"]
            .sum()
            .sort_values(ascending=False)
            .index.tolist()
        )

        dynamic_height = max(650, 90 + len(hub_order) * 44)

        fig2 = px.bar(
            ns,
            x="count",
            y="hub_name",
            color="pickup_status",
            facet_col="month_name",
            facet_col_spacing=0.015,
            orientation="h",
            title="No-Show & Cancellation",
            text="count",
            category_orders={
                "month_name": month_order,
                "hub_name": hub_order
            },
            color_discrete_map={
                "No-show": "#9ad0d6",
                "Cancelled": "#ee6a6a"
            }
        )

        fig2.update_layout(
            barmode="group",
            bargap=0.18,
            bargroupgap=0.08
        )

        fig2.update_traces(
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11, color="#1f2d3d"),
            cliponaxis=False
        )

        fig2.for_each_annotation(
            lambda a: a.update(
                text=a.text.split("=")[-1],
                font=dict(size=13, color="#55657a")
            )
        )

        fig2.update_xaxes(
            title=" ",
            showticklabels=False,
            range=[0, max(ns["count"].max() + 1, 6)],
            automargin=True
        )
        fig2.update_yaxes(
            title=" ",
            categoryorder="array",
            categoryarray=hub_order,
            tickfont=dict(size=11),
            automargin=True
        )

        fig2 = style_plotly(
            fig2,
            height=dynamic_height,
            legend_position="top",
            top_margin=80,
            bottom_margin=20
        )

        fig2.update_layout(
            margin=dict(l=125, r=20, t=80, b=15),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=1,
                font=dict(size=10)
            )
        )

        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # -------------------------------
    # Row 2: Late Return + Behavior Impact
    # -------------------------------
    left, right = st.columns([1.25, 0.75], gap="small")

    with left:
        late_month = (
            filtered[filtered["return_status"] == "Late"]
            .groupby(["month_name", "month_sort", "item_category"], as_index=False)
            .agg(late_returns=("reservation_id", "count"))
            .sort_values("month_sort")
        )

        fig = px.bar(
            late_month,
            x="month_name",
            y="late_returns",
            color="item_category",
            title="Late Return Distribution",
            text_auto=True,
            color_discrete_sequence=["#e9c46a", "#b0c45a", "#8bc0c3", "#b5b0e0", "#e7e043", "#d3a6c7"]
        )

        fig.update_layout(barmode="stack")
        fig.update_traces(textposition="inside", cliponaxis=False)
        fig = style_plotly(fig, height=440, legend_position="bottom", top_margin=80, bottom_margin=95)
        fig.update_xaxes(title="Month")
        fig.update_yaxes(title="Late Return Count")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        notif_df = filtered.groupby("notifications_enabled_flag", as_index=False).agg(
            no_show_rate=("no_show_flag", "mean"),
            late_return_rate=("late_flag", "mean")
        )
        notif_df["notifications_status"] = notif_df["notifications_enabled_flag"].map({1: "Enabled", 0: "Disabled"})

        notif_long = pd.DataFrame({
            "notifications_status": list(notif_df["notifications_status"]) * 2,
            "metric": ["No-Show %"] * len(notif_df) + ["Late Return %"] * len(notif_df),
            "rate": list(notif_df["no_show_rate"]) + list(notif_df["late_return_rate"])
        })

        fig3 = px.bar(
            notif_long,
            x="notifications_status",
            y="rate",
            color="metric",
            barmode="group",
            text=notif_long["rate"].map(lambda x: f"{x:.2%}"),
            title="Behavior Impact (Notifications Effect)",
            color_discrete_map={
                "No-Show %": "#6dc9c4",
                "Late Return %": "#e8b563"
            }
        )

        fig3.update_traces(
            textposition="outside",
            textfont=dict(size=10),
            cliponaxis=False
        )

        fig3 = style_plotly(fig3, height=440, legend_position="bottom", top_margin=80, bottom_margin=90)
        fig3.update_xaxes(title="Notifications Status")
        fig3.update_yaxes(title="Rate", tickformat=".0%")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='insight-box'><b>Main insight:</b> This view shows the full behavior story. Staff can see how many users miss pickups, how late returns change across months, and whether reminders help reduce behavior problems.</div>", unsafe_allow_html=True)

elif page == "Inventory & Damage Risk":
    if st.session_state.user_role != "Staff":
        st.warning("Only staff can access this page.")
        st.stop()
    
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">A prototype for tracking user behavior, inventory risk, and hub operations.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Inventory Management & Damage Risk</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This page focuses on item condition, missing parts, penalties, and the extra staff time created by incomplete returns.</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        make_kpi_card("Missing Parts Rate", pct(missing_parts_rate))
    with c2:
        make_kpi_card("Damage Rate", pct(damage_rate))
    with c3:
        make_kpi_card("Overall Risk Score", avg_num(risk_score))

    row1_left, row1_right = st.columns(2)

    with row1_left:
        risk_by_cat = filtered.groupby("item_category", as_index=False).agg(
            missing_parts_rate=("missing_parts_flag", "mean"),
            damage_rate=("damage_flag", "mean"),
            reservations=("reservation_id", "count")
        )

        fig = px.scatter(
            risk_by_cat,
            x="missing_parts_rate",
            y="damage_rate",
            size="reservations",
            color="item_category",
            text="item_category",
            title="Item Risk (Damage vs Missing Parts)",
            color_discrete_sequence=["#d3a6c7", "#e7e043", "#b0c45a", "#8bc0c3", "#b5b0e0", "#e9c46a"]
        )
        fig.update_traces(
            textposition="top center",
            textfont=dict(size=11, color="#1f2d3d"),
            marker=dict(line=dict(color="white", width=2), opacity=0.92)
        )

        fig.add_vline(
            x=risk_by_cat["missing_parts_rate"].mean(),
            line_dash="dash",
            line_color="#f39c12",
            annotation_text="Avg Missing",
            annotation_position="top left",
            annotation_font=dict(size=10, color="#b36a00")
        )
        fig.add_hline(
            y=risk_by_cat["damage_rate"].mean(),
            line_dash="dash",
            line_color="#35c1b6",
            annotation_text="Avg Damage",
            annotation_position="bottom right",
            annotation_font=dict(size=10, color="#1b8f86")
        )

        fig = style_plotly(fig, height=430, legend_position="bottom", top_margin=80, bottom_margin=95)
        fig.update_xaxes(title="Missing Parts Rate", tickformat=".0%")
        fig.update_yaxes(title="Damage Rate", tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with row1_right:
        penalty = filtered[filtered["penalty_amount_usd"] > 0].copy()
        if penalty.empty:
            st.info("No positive penalties under the current filters.")
        else:
            sev_order = ["Minor", "Moderate", "Severe"]
            penalty["damage_severity"] = pd.Categorical(penalty["damage_severity"], categories=sev_order, ordered=True)
            agg_penalty = penalty.groupby("damage_severity", as_index=False).agg(
                avg_late_hours=("late_hours", "mean"),
                avg_penalty=("penalty_amount_usd", "mean"),
                count=("reservation_id", "count")
            )

            fig2 = px.scatter(
                agg_penalty,
                x="avg_late_hours",
                y="avg_penalty",
                size="count",
                color="damage_severity",
                text="damage_severity",
                title="Penalty vs Behavior Relationship",
                color_discrete_map={"Minor": "#f39c34", "Moderate": "#d85b6a", "Severe": "#7dc7c0"}
            )
            fig2.update_traces(
                textposition="top right",
                textfont_size=11,
                marker=dict(line=dict(color="white", width=2), opacity=0.95)
            )

            fig2.add_vline(
                x=agg_penalty["avg_late_hours"].mean(),
                line_dash="dash",
                line_color="#f39c12",
                annotation_text="Avg Late Hours",
                annotation_position="top left",
                annotation_font_size=10,
                annotation_font_color="#7a7a7a"
            )
            fig2.add_hline(
                y=agg_penalty["avg_penalty"].mean(),
                line_dash="dash",
                line_color="#35c1b6",
                annotation_text="Avg Penalty",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="#7a7a7a"
            )

            fig2 = style_plotly(fig2, height=430, legend_position="bottom", top_margin=80, bottom_margin=95)
            fig2.update_xaxes(title="Avg Late Hours")
            fig2.update_yaxes(title="Avg Penalty Amount (USD)")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    impact = filtered.groupby(["missing_parts_flag", "item_category"], as_index=False).agg(
        avg_checkin=("staff_checkin_minutes", "mean")
    )
    impact["missing_parts_status"] = impact["missing_parts_flag"].map({0: "No", 1: "Yes"})

    fig3 = px.bar(
        impact,
        x="missing_parts_status",
        y="avg_checkin",
        color="item_category",
        barmode="group",
        text_auto=".2f",
        title="Incomplete Return Impact on Staff Time",
        color_discrete_sequence=["#d3a6c7", "#e7e043", "#b0c45a", "#8bc0c3", "#b5b0e0", "#e9c46a"]
    )
    fig3.update_traces(textposition="outside", cliponaxis=False)
    fig3 = style_plotly(fig3, height=380, legend_position="bottom", top_margin=80, bottom_margin=95)
    fig3.update_xaxes(title="Missing Parts Status")
    fig3.update_yaxes(title="Avg Staff Check-in Minutes")
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='insight-box'><b>Main insight:</b> This page makes the risk story easy to follow. Higher missing parts and damage are linked to more staff effort, and the penalty logic stays small because BorrowBox was designed to remain accessible.</div>", unsafe_allow_html=True)

elif page == "Hub Operations":
    if st.session_state.user_role != "Staff":
        st.warning("Only staff can access this page.")
        st.stop()
    
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">A prototype for tracking user behavior, inventory risk, and hub operations.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Hub Operations & Reporting</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This page shows hub workload, inventory pressure, and reporting quality across locations.</div>", unsafe_allow_html=True)

    inconsistency_rate = 1 - (filtered["data_entry_method"].eq("Electronic log").mean())

    c1, c2, c3 = st.columns(3)
    with c1:
        make_kpi_card("Avg Check-in Time", avg_num(avg_checkin))
    with c2:
        make_kpi_card("Avg Queue Length", avg_num(filtered["hub_queue_length"].mean()))
    with c3:
        make_kpi_card("Data Inconsistency Rate", pct(inconsistency_rate))

    h1, h2 = st.columns([1.05, 1.25])

    with h1:
        hub_strain = filtered.groupby(["hub_name", "hub_type"], as_index=False).agg(
            avg_queue=("hub_queue_length", "mean"),
            avg_checkin=("staff_checkin_minutes", "mean"),
            reservations=("reservation_id", "count")
        )

        fig = px.scatter(
            hub_strain,
            x="avg_queue",
            y="avg_checkin",
            color="hub_type",
            size="reservations",
            hover_name="hub_name",
            title="Hub Operational Strain",
            color_discrete_map={"Staffed": "#1da1b5", "Staffed+Volunteers": "#f2a9cc", "Volunteer-heavy": "#f1b264"}
        )
        fig.update_traces(
            marker=dict(line=dict(color="white", width=2), opacity=0.94)
        )

        fig.add_vline(
            x=hub_strain["avg_queue"].mean(),
            line_dash="dash",
            line_color="#f39c12",
            annotation_text="Avg Queue",
            annotation_position="top left",
            annotation_font_size=10,
            annotation_font_color="#7a7a7a"
        )
        fig.add_hline(
            y=hub_strain["avg_checkin"].mean(),
            line_dash="dash",
            line_color="#35c1b6",
            annotation_text="Avg Check-in",
            annotation_position="bottom right",
            annotation_font_size=10,
            annotation_font_color="#7a7a7a"
        )

        fig = style_plotly(fig, height=430, legend_position="bottom", top_margin=80, bottom_margin=90)
        fig.update_xaxes(title="Avg Hub Queue Length")
        fig.update_yaxes(title="Avg Staff Check-in Minutes")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with h2:
        dq = filtered.groupby(["hub_name", "data_entry_method"], as_index=False).agg(records=("reservation_id", "count"))
        dq["share"] = dq.groupby("hub_name")["records"].transform(lambda s: s / s.sum())

        hub_order = dq.groupby("hub_name")["share"].sum().sort_values(ascending=True).index.tolist()

        fig2 = px.bar(
            dq,
            x="share",
            y="hub_name",
            color="data_entry_method",
            orientation="h",
            title="Data Quality (Reporting Inconsistency)",
            text=dq["share"].map(lambda x: f"{x:.1%}"),
            category_orders={"hub_name": hub_order},
            color_discrete_map={"Mixed": "#f29594", "Handwritten notes": "#9ec3dd", "Electronic log": "#e6c54a"}
        )
        fig2.update_layout(barmode="stack")
        fig2.update_traces(textposition="inside", textfont_size=10, cliponaxis=False)
        fig2 = style_plotly(fig2, height=430, legend_position="bottom", top_margin=80, bottom_margin=90)
        fig2.update_xaxes(title="Share of Records", tickformat=".0%")
        fig2.update_yaxes(title="Hub Name")
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    availability = filtered.groupby(["demand_level", "hub_name"], as_index=False).agg(
        inventory_available_rate=("inventory_available_at_reserve", "mean")
    )
    pivot = availability.pivot(index="hub_name", columns="demand_level", values="inventory_available_rate")

    demand_order = [x for x in ["High", "Medium", "Low"] if x in pivot.columns]
    pivot = pivot[demand_order]

    heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=[[0, "#f29594"], [0.5, "#f6f2e7"], [1, "#4da86c"]],
        text=np.vectorize(lambda v: f"{v:.1%}")(pivot.values),
        texttemplate="%{text}",
        colorbar_title="Availability"
    ))
    heat.update_layout(
        title="Demand vs Inventory Availability Matrix",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.92)",
        height=420,
        margin=dict(l=30, r=20, t=70, b=20),
        font=dict(color="#30445f", size=13),
        title_font=dict(size=17, color="#1f2d3d")
    )
    heat.update_xaxes(title="Demand Level")
    heat.update_yaxes(title="Hub Name")

    st.plotly_chart(heat, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='insight-box'><b>Main insight:</b> This page helps the user see that the system can compare hubs, surface manual reporting gaps, and show where demand and inventory are not lining up.</div>", unsafe_allow_html=True)

elif page == "Book New Reservation":
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">Prototype page for creating a new reservation.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Book New Reservation</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This page simulates how a user would create a new reservation in the BorrowBox system.</div>", unsafe_allow_html=True)

    if "user_reservations" not in st.session_state:
        st.session_state.user_reservations = []

    with st.form("reservation_form"):
        c1, c2 = st.columns(2)

        with c1:
            full_name = st.text_input("Full Name", value=st.session_state.user_name)
            hub_name = st.selectbox("Pickup Hub", all_hubs)
            item_category = st.selectbox("Item Category", sorted(df["item_category"].dropna().unique().tolist()))
            borrow_days = st.number_input("Borrow Duration (Days)", min_value=1, max_value=30, value=3)

        with c2:
            member_status = st.selectbox("Member Type", sorted(df["member_status"].dropna().unique().tolist()))
            notifications = st.selectbox("Enable Notifications?", ["Yes", "No"])
            pickup_date = st.date_input("Pickup Date")
            notes = st.text_area("Reservation Notes", placeholder="Example: Need camping kit for weekend trip")

        submit_reservation = st.form_submit_button("Book Reservation")

        if submit_reservation:
            reservation_data = {
                "full_name": full_name,
                "hub_name": hub_name,
                "item_category": item_category,
                "borrow_days": borrow_days,
                "member_status": member_status,
                "notifications": notifications,
                "pickup_date": str(pickup_date),
                "notes": notes
            }
            st.session_state.user_reservations.append(reservation_data)
            st.success("Reservation submitted in the prototype. This simulates a user creating a new booking.")

    if st.session_state.user_reservations:
        st.markdown("### Recent reservation requests")
        reservation_df = pd.DataFrame(st.session_state.user_reservations)
        st.dataframe(reservation_df, use_container_width=True)

        csv = reservation_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download reservation requests as CSV",
            data=csv,
            file_name="borrowbox_user_reservations.csv",
            mime="text/csv"
        )

    st.markdown(
        "<div class='insight-box'><b>Why this matters:</b> This page shows that the prototype supports a real user action. It is not only a reporting tool. It also simulates how a user would place a reservation, which then becomes part of the operational workflow.</div>",
        unsafe_allow_html=True
    )

elif page == "Log Return Issue":
    if st.session_state.user_role != "Staff":
        st.warning("Only staff can access this page.")
        st.stop()
    
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-orange-angle"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-teal"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">BorrowBox Operational<br>Monitoring Dashboard</div>
        <div class="hero-subtitle">A prototype for tracking user behavior, inventory risk, and hub operations.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>Log Return Issue</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-note'>This page simulates one of the most important staff actions: recording a problem when an item is returned.</div>", unsafe_allow_html=True)
    if "logged_issues" not in st.session_state:
        st.session_state.logged_issues = []
    with st.form("issue_form"):
        c1, c2 = st.columns(2)
        with c1:
            reservation_id = st.selectbox("Reservation ID", sorted(filtered["reservation_id"].dropna().unique().tolist())[:200])
            hub_name = st.selectbox("Hub Name", all_hubs)
            item_category = st.selectbox("Item Category", sorted(df["item_category"].dropna().unique().tolist()))
            missing_parts = st.selectbox("Missing Parts?", ["No","Yes"])
        with c2:
            damage_severity = st.selectbox("Damage Severity", ["None","Minor","Moderate","Severe"])
            support_ticket = st.selectbox("Create Support Ticket?", ["No","Yes"])
            notes = st.text_area("Staff Notes", placeholder="Example: Power cord missing from item set")
            submitted = st.form_submit_button("Submit Issue")
        if submitted:
            st.session_state.logged_issues.append({"reservation_id":reservation_id, "hub_name":hub_name, "item_category":item_category, "missing_parts":missing_parts, "damage_severity":damage_severity, "support_ticket":support_ticket, "notes":notes})
            st.success("Issue saved in the prototype. This simulates data entry from staff to the monitoring system.")
    if st.session_state.logged_issues:
        st.markdown("### Recent issue entries")
        issue_df = pd.DataFrame(st.session_state.logged_issues)
        st.dataframe(issue_df, use_container_width=True)
        csv = issue_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download logged issues as CSV", data=csv, file_name="borrowbox_logged_issues.csv", mime="text/csv")
    st.markdown("<div class='insight-box'><b>Why this matters:</b> This form proves the prototype is not just for viewing charts. It also shows how staff would enter issue data and how that information can be captured for reporting.</div>", unsafe_allow_html=True)
