import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import random
import string

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="BorrowBox Solution App",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CSS theme
# ------------------------------------------------------------
CUSTOM_CSS = """
<style>
:root {
    --bg: #f1f2f4;
    --card: rgba(255,255,255,0.86);
    --border: #d8dbe0;
    --blue: #5b8fe3;
    --purple: #b08be8;
    --teal: #35c1b6;
    --orange: #ff980f;
    --red: #e15659;
    --green: #7bc96f;
    --text: #17324d;
}

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1.5rem;
}

/* ---------- HERO ---------- */
.hero-wrap {
    position: relative;
    width: 100%;
    min-height: 300px;
    border-radius: 30px;
    background: #eeeeee;
    overflow: hidden;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.hero-dash-left,
.hero-dash-left-2 {
    position: absolute;
    left: 34px;
    width: 13px;
    height: 58px;
    border-radius: 16px;
    background: var(--teal);
    z-index: 1;
}
.hero-dash-left { top: 14px; }
.hero-dash-left-2 { top: 110px; }
.hero-orange-box {
    position: absolute;
    left: -18px;
    top: 110px;
    width: 128px;
    height: 120px;
    border: 8px solid var(--orange);
    border-radius: 8px;
    z-index: 1;
}
.hero-teal-curve {
    position: absolute;
    left: 110px;
    bottom: -42px;
    width: 220px;
    height: 170px;
    border-left: 10px dashed var(--teal);
    border-top: 10px dashed var(--teal);
    border-radius: 180px 0 0 0;
    transform: rotate(-18deg);
    z-index: 1;
}
.hero-circle-purple {
    position: absolute;
    left: 155px;
    top: 38px;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: var(--purple);
    z-index: 1;
}
.hero-circle-blue {
    position: absolute;
    right: -120px;
    bottom: -220px;
    width: 760px;
    height: 760px;
    border-radius: 50%;
    background: var(--blue);
    z-index: 1;
}
.hero-title {
    position: absolute;
    right: 8%;
    top: 38%;
    transform: translateY(-50%);
    z-index: 5;
    color: #fff;
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1.15;
    text-align: center;
    max-width: 560px;
}
.hero-subtitle {
    position: absolute;
    right: 8%;
    top: 66%;
    transform: translateY(-50%);
    z-index: 5;
    color: #fff;
    font-size: 1rem;
    font-weight: 500;
    text-align: center;
    max-width: 560px;
}

/* ---------- CONTENT ---------- */
.section-title {
    font-size: 1.95rem;
    font-weight: 800;
    color: #142a43;
    margin-top: 8px;
    margin-bottom: 4px;
}
.section-note {
    font-size: 1rem;
    color: #4f6075;
    margin-bottom: 18px;
}
.role-chip {
    display: inline-block;
    padding: 8px 15px;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 999px;
    font-size: .9rem;
    font-weight: 700;
    margin: 0 6px 12px 0;
}
.role-user { border-left: 7px solid var(--blue); }
.role-staff { border-left: 7px solid var(--teal); }

.kpi-card {
    background: var(--card);
    border: 1.4px solid var(--border);
    border-radius: 24px;
    padding: 18px 18px;
    min-height: 124px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: .35rem;
}
.kpi-title {
    font-size: .95rem;
    font-weight: 700;
    color: #4c5b70;
    margin-bottom: 10px;
    min-height: 22px;
}
.kpi-value {
    font-size: 2.15rem;
    font-weight: 800;
    color: #15304d;
    line-height: 1.1;
}
.kpi-sub {
    font-size: .86rem;
    color: #64748b;
    line-height: 1.4;
    margin-top: 8px;
}

.insight-box {
    background: rgba(255,255,255,0.86);
    border: 1.4px solid var(--border);
    border-left: 8px solid var(--teal);
    border-radius: 20px;
    padding: 14px 16px;
    margin-top: 8px;
    margin-bottom: 16px;
    color: #26374d;
}
.warning-box {
    background: rgba(255,255,255,0.86);
    border: 1.4px solid var(--border);
    border-left: 8px solid var(--orange);
    border-radius: 20px;
    padding: 14px 16px;
    margin-top: 8px;
    margin-bottom: 16px;
    color: #26374d;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin: 10px 0 20px 0;
}
.step-card {
    background: rgba(255,255,255,0.86);
    border: 1.4px solid var(--border);
    border-radius: 22px;
    padding: 18px;
    min-height: 150px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.step-card h4 {
    margin: 0 0 10px 0;
    color: #15304d;
}
.step-card p {
    margin: 0;
    color: #4f6075;
    line-height: 1.45;
}

/* chart card */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.86);
    border: 1.4px solid var(--border);
    border-radius: 24px;
    padding: 12px 14px 8px 14px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    overflow: hidden;
}
.modebar { display: none !important; }

.stForm {
    background: rgba(255,255,255,0.86);
    border: 1.4px solid var(--border);
    border-radius: 24px;
    padding: 18px;
}
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    border-radius: 999px !important;
    border: 2px solid var(--orange) !important;
    background: white !important;
    color: #1f2d3d !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.2rem !important;
}
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.86);
    border: 1.4px solid var(--border);
    border-radius: 22px;
    padding: 8px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------------------------------------------
# Data loading and prep
# ------------------------------------------------------------
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

    for col in ["reservation_date", "pickup_scheduled_datetime", "pickup_actual_datetime", "return_due_datetime", "return_actual_datetime"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    flag_cols = ["missing_parts_flag", "damage_flag", "inventory_available_at_reserve", "notifications_enabled_flag", "report_issue_in_app_flag", "support_ticket_flag", "cancellation_flag", "cleaning_required_flag", "cleaning_done_flag"]
    for col in flag_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    num_cols = ["late_hours", "parts_expected", "parts_returned", "staff_checkout_minutes", "staff_checkin_minutes", "hub_queue_length", "reminders_sent_count", "staff_notes_length", "penalty_amount_usd", "borrow_days"]
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

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def pct(n):
    if pd.isna(n):
        return "0.00%"
    return f"{n:.2%}"


def avg_num(n):
    if pd.isna(n):
        return "0.00"
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


def style_plotly(fig, height=380, legend_position="bottom", top_margin=65, bottom_margin=75):
    legend_cfg = dict(orientation="h", bgcolor="rgba(255,255,255,0)", font=dict(size=10), title=None)
    if legend_position == "bottom":
        legend_cfg.update(yanchor="top", y=-0.22, xanchor="center", x=0.5)
    elif legend_position == "right":
        legend_cfg.update(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
    elif legend_position == "hide":
        fig.update_layout(showlegend=False)
    else:
        legend_cfg.update(yanchor="bottom", y=1.05, xanchor="center", x=0.5)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.92)",
        height=height,
        margin=dict(l=40, r=22, t=top_margin, b=bottom_margin),
        font=dict(color="#30445f", size=13),
        title_font=dict(size=18, color="#1f2d3d"),
        legend=legend_cfg,
        uniformtext_minsize=9,
        uniformtext_mode="hide"
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(180,190,205,0.35)", zeroline=False, linecolor="rgba(0,0,0,0)", tickfont=dict(size=12), title_font=dict(size=12), automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(180,190,205,0.35)", zeroline=False, linecolor="rgba(0,0,0,0)", tickfont=dict(size=12), title_font=dict(size=12), automargin=True)
    return fig


def hero(title="BorrowBox Control Center", subtitle="A centralized system to monitor user behavior, inventory condition, and hub performance in real time"):
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-dash-left"></div>
        <div class="hero-dash-left-2"></div>
        <div class="hero-orange-box"></div>
        <div class="hero-teal-curve"></div>
        <div class="hero-circle-purple"></div>
        <div class="hero-circle-blue"></div>
        <div class="hero-title">{title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def page_header(title, note, role):
    role_class = "role-user" if role == "User" else "role-staff" if role == "Staff" else ""
    st.markdown(f"<span class='role-chip {role_class}'>Designed for: {role}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-note'>{note}</div>", unsafe_allow_html=True)


def generate_reservation_id(existing_ids):
    while True:
        new_id = "R" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if new_id not in existing_ids:
            return new_id


def generate_issue_id(existing_ids):
    while True:
        new_id = "ISSUE-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if new_id not in existing_ids:
            return new_id

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
st.sidebar.markdown("## BorrowBox Control Center")
st.sidebar.caption("Operational Monitoring System")

upload = st.sidebar.file_uploader("Upload BorrowBox CSV if needed", type=["csv"])
df = load_data(upload)

all_hubs = sorted(df["hub_name"].dropna().unique().tolist())
month_order = df[["month_name", "month_sort"]].dropna().drop_duplicates().sort_values("month_sort")["month_name"].tolist()
all_members = sorted(df["member_status"].dropna().unique().tolist())

view_mode = st.sidebar.radio("Choose user type", ["Staff view", "User view"], help="This replaces login. It simply shows which pages belong to staff and which belong to regular users.")

if view_mode == "Staff view":
    pages = ["Home", "Staff Dashboard", "Inventory Lookup", "Log Return Issue", "Decision Guide"]
else:
    pages = ["Home", "Inventory Lookup", "Book New Reservation", "My Reservation Summary", "Decision Guide"]

page = st.sidebar.radio("Go to page", pages)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")
selected_hubs = st.sidebar.multiselect("Filter by hub", all_hubs, default=[])
selected_months = st.sidebar.multiselect("Filter by month", month_order, default=[])
selected_members = st.sidebar.multiselect("Filter by member status", all_members, default=[])

filtered = filter_data(df, selected_hubs, selected_months, selected_members)
if filtered.empty:
    st.warning("No rows match the current filters. Please change the sidebar selections.")
    st.stop()

# KPI variables
no_show_rate = filtered["no_show_flag"].mean()
late_return_rate = filtered["late_flag"].mean()
cancel_rate = filtered["cancel_flag"].mean()
missing_parts_rate = filtered["missing_parts_flag"].mean()
damage_rate = filtered["damage_flag"].mean()
risk_score = filtered["risk_score_row"].mean()
avg_checkin = filtered["staff_checkin_minutes"].mean()
avg_queue = filtered["hub_queue_length"].mean()

# ------------------------------------------------------------
# Pages
# ------------------------------------------------------------
if page == "Home":
    hero()
    page_header("Overview", "This system helps BorrowBox staff identify operational problems early, reduce user misuse, and improve inventory handling across all hubs. It combines real-time monitoring with actionable insights to support faster and better decision-making.\n See what’s going wrong. Act before it becomes a bigger problem.", "User + Staff")

    k1, k2, k3, k4 = st.columns(4, gap="small")
    with k1:
        make_kpi_card("No-Show Rate", pct(no_show_rate), "Booked items not picked up")
    with k2:
        make_kpi_card("Late Return Rate", pct(late_return_rate), "Items returned after due time")
    with k3:
        make_kpi_card("Missing Parts Rate", pct(missing_parts_rate), "Returned items missing pieces")
    with k4:
        make_kpi_card("Avg Check-in Time", avg_num(avg_checkin), "Minutes staff spend on return check-in")

    st.markdown("""
    <div class="card-grid">
        <div class="step-card">
            <h4>👤 User pages</h4>
            <p>Users can create a new reservation and see a simple reservation summary. This shows how BorrowBox supports the borrower side of the system.</p>
        </div>
        <div class="step-card">
            <h4>🧑‍💼 Staff pages</h4>
            <p>Staff can monitor problem areas, review user behavior, track inventory risk, and log return issues when something comes back late, damaged, or incomplete.</p>
        </div>
        <div class="step-card">
            <h4>📊 Decision support</h4>
            <p>The app turns the dashboard into action. It helps staff decide which hubs need attention, which items are risky, and where user reminders matter most.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.25, 1], gap="small")
    with left:
        monthly = filtered.groupby(["month_name", "month_sort"], as_index=False).agg(requests=("reservation_id", "count")).sort_values("month_sort")
        fig = px.line(monthly, x="month_name", y="requests", markers=True, text="requests", title="Borrow Requests Over Time")
        fig.update_traces(textposition="top center", line=dict(width=3, color="#5b8fe3"), marker=dict(size=8, color="#5b8fe3"))
        fig = style_plotly(fig, height=350, legend_position="hide", top_margin=55, bottom_margin=55)
        fig.update_xaxes(title="Month")
        fig.update_yaxes(title="Borrow Requests")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with right:
        member_dist = filtered["member_status"].value_counts().reset_index()
        member_dist.columns = ["member_status", "count"]
        fig2 = px.pie(member_dist, names="member_status", values="count", title="User Mix", hole=0.5, color_discrete_sequence=["#5b8fe3", "#35c1b6", "#b08be8"])
        fig2.update_traces(textinfo="percent+label", textfont_size=12)
        fig2 = style_plotly(fig2, height=350, legend_position="hide", top_margin=55, bottom_margin=25)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='insight-box'><b>Main idea:</b> The app is split by user type. Regular users make reservations. Staff use the app to monitor problems and record return issues. This keeps the system simple and easier to understand.</div>", unsafe_allow_html=True)

elif page == "Staff Dashboard":
    hero("Staff Decision Dashboard", "A simpler staff view focused on the original problems: user behavior, item condition, and hub pressure.")
    page_header("Staff Dashboard", "This page is for staff and managers. It gives a clean view of the main problem areas and tells where action is needed.", "Staff")

    tab1, tab2, tab3 = st.tabs(["1. User Behavior", "2. Inventory Risk", "3. Hub Operations"])

    with tab1:
        st.markdown("<div class='warning-box'><b>Question:</b> Are users following the borrowing rules?</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            make_kpi_card("Cancellation Rate", pct(cancel_rate), "Users canceling before pickup")
        with c2:
            make_kpi_card("No-Show Rate", pct(no_show_rate), "Users booking but not picking up")
        with c3:
            make_kpi_card("Late Return Rate", pct(late_return_rate), "Returns after due time")

        hub_problem = filtered.groupby("hub_name", as_index=False).agg(
            no_show_rate=("no_show_flag", "mean"),
            cancel_rate=("cancel_flag", "mean"),
            late_return_rate=("late_flag", "mean")
        )
        hub_long = hub_problem.melt(id_vars="hub_name", value_vars=["late_return_rate", "cancel_rate", "no_show_rate"], var_name="metric", value_name="rate")
        metric_labels = {"late_return_rate": "Late Return", "cancel_rate": "Cancellation", "no_show_rate": "No-Show"}
        hub_long["metric"] = hub_long["metric"].map(metric_labels)
        fig = px.bar(hub_long, x="hub_name", y="rate", color="metric", barmode="group", text=hub_long["rate"].map(lambda x: f"{x:.1%}"), title="Problem Rates by Hub", color_discrete_map={"Late Return": "#e15659", "Cancellation": "#ffad5a", "No-Show": "#7bc96f"})
        fig.update_traces(textposition="outside", textfont_size=10, cliponaxis=False)
        fig = style_plotly(fig, height=430, legend_position="bottom", top_margin=60, bottom_margin=100)
        fig.update_xaxes(title="Hub")
        fig.update_yaxes(title="Problem Rate", tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        left, right = st.columns([1.1, 0.9], gap="small")
        with left:
            trend = filtered.groupby(["month_name", "month_sort"], as_index=False).agg(late_return=("late_flag", "mean"), cancel=("cancel_flag", "mean"), no_show=("no_show_flag", "mean")).sort_values("month_sort")
            trend_long = trend.melt(id_vars=["month_name", "month_sort"], value_vars=["late_return", "cancel", "no_show"], var_name="metric", value_name="rate")
            trend_long["metric"] = trend_long["metric"].map({"late_return": "Late Return", "cancel": "Cancellation", "no_show": "No-Show"})
            fig2 = px.line(trend_long, x="month_name", y="rate", color="metric", markers=True, text=trend_long["rate"].map(lambda x: f"{x:.1%}"), title="Problem Rates Over Time", color_discrete_map={"Late Return": "#e15659", "Cancellation": "#ffad5a", "No-Show": "#7bc96f"})
            fig2.update_traces(textposition="top center")
            fig2 = style_plotly(fig2, height=350, legend_position="bottom", top_margin=55, bottom_margin=95)
            fig2.update_yaxes(title="Rate", tickformat=".0%")
            fig2.update_xaxes(title="Month")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        with right:
            notif = filtered.groupby("notifications_enabled_flag", as_index=False).agg(no_show_rate=("no_show_flag", "mean"), late_return_rate=("late_flag", "mean"))
            notif["Notifications"] = notif["notifications_enabled_flag"].map({1: "ON", 0: "OFF"})
            notif_long = notif.melt(id_vars="Notifications", value_vars=["no_show_rate", "late_return_rate"], var_name="metric", value_name="rate")
            notif_long["metric"] = notif_long["metric"].map({"no_show_rate": "No-Show", "late_return_rate": "Late Return"})
            fig3 = px.bar(notif_long, x="Notifications", y="rate", color="metric", barmode="group", text=notif_long["rate"].map(lambda x: f"{x:.1%}"), title="Notifications ON vs OFF", color_discrete_map={"No-Show": "#35c1b6", "Late Return": "#f2bd60"})
            fig3.update_traces(textposition="outside", textfont_size=10, cliponaxis=False)
            fig3 = style_plotly(fig3, height=350, legend_position="bottom", top_margin=55, bottom_margin=95)
            fig3.update_yaxes(title="Rate", tickformat=".0%")
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<div class='insight-box'><b>Staff takeaway:</b> User behavior is the first issue to monitor. Late returns are the strongest warning sign because they directly block the next user from borrowing the same item.</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='warning-box'><b>Question:</b> Are items being returned properly?</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            make_kpi_card("Missing Parts Rate", pct(missing_parts_rate), "Returns with incomplete item sets")
        with c2:
            make_kpi_card("Damage Rate", pct(damage_rate), "Items returned with damage")
        with c3:
            make_kpi_card("Risk Score", avg_num(risk_score), "Combined missing parts and damage risk")

        left, right = st.columns(2, gap="small")
        with left:
            cat_missing = filtered.groupby("item_category", as_index=False).agg(missing_rate=("missing_parts_flag", "mean")).sort_values("missing_rate", ascending=False)
            fig = px.bar(cat_missing, x="item_category", y="missing_rate", text=cat_missing["missing_rate"].map(lambda x: f"{x:.1%}"), title="Missing Parts % by Item Category", color_discrete_sequence=["#f2cf63"])
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig = style_plotly(fig, height=360, legend_position="hide", top_margin=55, bottom_margin=55)
            fig.update_yaxes(title="Missing Parts Rate", tickformat=".0%")
            fig.update_xaxes(title="Item Category")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with right:
            cat_damage = filtered.groupby("item_category", as_index=False).agg(damage_rate=("damage_flag", "mean")).sort_values("damage_rate", ascending=False)
            fig2 = px.bar(cat_damage, x="item_category", y="damage_rate", text=cat_damage["damage_rate"].map(lambda x: f"{x:.1%}"), title="Damage Rate by Item Category", color_discrete_sequence=["#a77f68"])
            fig2.update_traces(textposition="outside", cliponaxis=False)
            fig2 = style_plotly(fig2, height=360, legend_position="hide", top_margin=55, bottom_margin=55)
            fig2.update_yaxes(title="Damage Rate", tickformat=".0%")
            fig2.update_xaxes(title="Item Category")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        impact = filtered.groupby("missing_parts_flag", as_index=False).agg(avg_checkin=("staff_checkin_minutes", "mean"))
        impact["Missing Parts Status"] = impact["missing_parts_flag"].map({0: "No missing parts", 1: "Missing parts"})
        fig3 = px.bar(impact, x="Missing Parts Status", y="avg_checkin", text=impact["avg_checkin"].map(lambda x: f"{x:.2f}"), title="Average Check-in Time: Missing vs Not Missing", color_discrete_sequence=["#78b9b3"])
        fig3.update_traces(textposition="outside", cliponaxis=False)
        fig3 = style_plotly(fig3, height=330, legend_position="hide", top_margin=55, bottom_margin=55)
        fig3.update_yaxes(title="Avg Check-in Minutes")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<div class='insight-box'><b>Staff takeaway:</b> Inventory issues create extra work. Missing parts and damage do not just affect the item. They also slow down the check-in process and reduce readiness for the next borrower.</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='warning-box'><b>Question:</b> Are hubs running efficiently?</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            make_kpi_card("Avg Check-in Time", avg_num(avg_checkin), "Staff time spent on returns")
        with c2:
            make_kpi_card("Avg Queue Length", avg_num(avg_queue), "Average hub queue pressure")
        with c3:
            make_kpi_card("Inventory Availability", pct(filtered["inventory_available_at_reserve"].mean()), "Items available when users reserve")

        left, right = st.columns(2, gap="small")
        with left:
            checkin = filtered.groupby("hub_name", as_index=False).agg(avg_checkin=("staff_checkin_minutes", "mean")).sort_values("avg_checkin", ascending=False)
            fig = px.bar(checkin, x="hub_name", y="avg_checkin", text=checkin["avg_checkin"].map(lambda x: f"{x:.2f}"), title="Avg Check-in Time by Hub", color_discrete_sequence=["#78b9b3"])
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig = style_plotly(fig, height=360, legend_position="hide", top_margin=55, bottom_margin=65)
            fig.update_xaxes(title="Hub")
            fig.update_yaxes(title="Minutes")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with right:
            queue = filtered.groupby("hub_name", as_index=False).agg(avg_queue=("hub_queue_length", "mean")).sort_values("avg_queue", ascending=False)
            fig2 = px.bar(queue, x="hub_name", y="avg_queue", text=queue["avg_queue"].map(lambda x: f"{x:.2f}"), title="Avg Queue Length by Hub", color_discrete_sequence=["#9ec7e2"])
            fig2.update_traces(textposition="outside", cliponaxis=False)
            fig2 = style_plotly(fig2, height=360, legend_position="hide", top_margin=55, bottom_margin=65)
            fig2.update_xaxes(title="Hub")
            fig2.update_yaxes(title="Queue Length")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        demand = filtered.groupby("demand_level", as_index=False).agg(availability=("inventory_available_at_reserve", "mean"))
        fig3 = px.bar(demand, x="demand_level", y="availability", text=demand["availability"].map(lambda x: f"{x:.1%}"), title="Inventory Availability by Demand Level", color_discrete_sequence=["#6c7884"])
        fig3.update_traces(textposition="outside", cliponaxis=False)
        fig3 = style_plotly(fig3, height=330, legend_position="hide", top_margin=55, bottom_margin=55)
        fig3.update_xaxes(title="Demand Level")
        fig3.update_yaxes(title="Availability Rate", tickformat=".0%")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        st.markdown("<div class='insight-box'><b>Staff takeaway:</b> Hub pressure is visible through queue length and check-in time. Staff can use this page to decide where to add support, inspect inventory, or improve return handling.</div>", unsafe_allow_html=True)

elif page == "Book New Reservation":
    hero("BorrowBox Reservation Page", "A user-facing page that simulates how a borrower would request an item.")
    page_header("Book New Reservation", "This page is for regular users. It shows how a user would book an item and create a new reservation request.", "User")

    if "user_reservations" not in st.session_state:
        st.session_state.user_reservations = []

    with st.form("reservation_form"):
        c1, c2 = st.columns(2, gap="small")
        with c1:
            full_name = st.text_input("Full Name", value="Sample BorrowBox User")
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
            existing_ids = set(df["reservation_id"].dropna().astype(str).tolist())
            existing_ids.update([str(x["reservation_id"]) for x in st.session_state.user_reservations])
            new_reservation_id = generate_reservation_id(existing_ids)
            reservation_data = {
                "reservation_id": new_reservation_id,
                "full_name": full_name,
                "hub_name": hub_name,
                "item_category": item_category,
                "borrow_days": borrow_days,
                "member_status": member_status,
                "notifications": notifications,
                "pickup_date": str(pickup_date),
                "pickup_status": "Scheduled",
                "return_status": "Not Returned Yet",
                "notes": notes,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.user_reservations.append(reservation_data)
            st.success(f"Reservation submitted. New Reservation ID: {new_reservation_id}")

    if st.session_state.user_reservations:
        st.markdown("### Recent reservation requests")
        reservation_df = pd.DataFrame(st.session_state.user_reservations)
        st.dataframe(reservation_df, use_container_width=True)
        st.download_button("Download reservation requests as CSV", data=reservation_df.to_csv(index=False).encode("utf-8"), file_name="borrowbox_user_reservations.csv", mime="text/csv")

    st.markdown("<div class='insight-box'><b>Why this matters:</b> This page shows the borrower side of the solution. It also shows how notification choice, item type, pickup hub, and duration can become useful data for staff decisions later.</div>", unsafe_allow_html=True)

elif page == "My Reservation Summary":
    hero("My BorrowBox Summary", "A simple user-facing page that shows what a borrower has requested in the prototype.")
    page_header("My Reservation Summary", "This page is for regular users. It gives a simple summary of the reservations created during the prototype demo.", "User")

    if "user_reservations" not in st.session_state or not st.session_state.user_reservations:
        st.info("No new reservation has been created yet. Go to 'Book New Reservation' first.")
    else:
        reservation_df = pd.DataFrame(st.session_state.user_reservations)
        c1, c2, c3 = st.columns(3, gap="small")
        with c1:
            make_kpi_card("Reservations Created", str(len(reservation_df)), "Requests submitted in this prototype session")
        with c2:
            make_kpi_card("Notifications ON", str((reservation_df["notifications"] == "Yes").sum()), "Reservations with reminders enabled")
        with c3:
            make_kpi_card("Unique Hubs Used", str(reservation_df["hub_name"].nunique()), "Different pickup hubs selected")
        st.dataframe(reservation_df, use_container_width=True)

    st.markdown("<div class='insight-box'><b>User takeaway:</b> Users get a simple way to confirm their reservation details. In the full system, this page could also show reminders, return due dates, and current reservation status.</div>", unsafe_allow_html=True)

elif page == "Log Return Issue":
    hero("Staff Return Issue Form", "A staff-facing page for recording damaged items, missing parts, and support tickets.")
    page_header("Log Return Issue", "This page is for staff. It simulates how staff would record problems during the return process.", "Staff")

    if "logged_issues" not in st.session_state:
        st.session_state.logged_issues = []

    with st.form("issue_form"):
        c1, c2 = st.columns(2, gap="small")
        with c1:
            reservation_id = st.selectbox("Reservation ID", sorted(filtered["reservation_id"].dropna().unique().tolist())[:300])
            hub_name = st.selectbox("Hub Name", all_hubs)
            item_category = st.selectbox("Item Category", sorted(df["item_category"].dropna().unique().tolist()))
            missing_parts = st.selectbox("Missing Parts?", ["No", "Yes"])
        with c2:
            damage_severity = st.selectbox("Damage Severity", ["None", "Minor", "Moderate", "Severe"])
            support_ticket = st.selectbox("Create Support Ticket?", ["No", "Yes"])
            notes = st.text_area("Staff Notes", placeholder="Example: Power cord missing from item set")
            submitted = st.form_submit_button("Submit Issue")

        if submitted:
            existing_issue_ids = {str(x["issue_id"]) for x in st.session_state.logged_issues} if st.session_state.logged_issues else set()
            new_issue_id = generate_issue_id(existing_issue_ids)
            issue_record = {
                "issue_id": new_issue_id,
                "reservation_id": reservation_id,
                "hub_name": hub_name,
                "item_category": item_category,
                "missing_parts": missing_parts,
                "damage_severity": damage_severity,
                "support_ticket": support_ticket,
                "notes": notes,
                "logged_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.logged_issues.append(issue_record)
            st.success(f"Issue saved. New Issue ID: {new_issue_id}")

    if st.session_state.logged_issues:
        st.markdown("### Recent issue entries")
        issue_df = pd.DataFrame(st.session_state.logged_issues)
        st.dataframe(issue_df, use_container_width=True)
        st.download_button("Download logged issues as CSV", data=issue_df.to_csv(index=False).encode("utf-8"), file_name="borrowbox_logged_issues.csv", mime="text/csv")

    st.markdown("<div class='insight-box'><b>Staff takeaway:</b> This form turns observations into usable data. Instead of only seeing problems after the fact, staff can record issues as they happen and use them for future reporting.</div>", unsafe_allow_html=True)

elif page == "Decision Guide":
    hero("Decision Guide", "A simple explanation of how each user type can use the prototype to make better decisions.")
    page_header("How This Supports Decision-Making", "This page connects the app features to real decisions for users and staff.", "User + Staff")

    st.markdown("""
    <div class="card-grid">
        <div class="step-card">
            <h4>1. User decisions</h4>
            <p>Users can choose a hub, item type, borrow duration, and notification option. This helps users make clearer reservations and reduces confusion before pickup.</p>
        </div>
        <div class="step-card">
            <h4>2. Staff decisions</h4>
            <p>Staff can see which hubs, months, or item categories have more problems. They can use this to decide where to focus training, reminders, or inventory checks.</p>
        </div>
        <div class="step-card">
            <h4>3. Manager decisions</h4>
            <p>Managers can use KPIs like late returns, missing parts, damage rate, queue length, and check-in time to understand whether BorrowBox operations are improving.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='insight-box'><b>Final decision story:</b> The proposed app supports both action and analysis. Users can create reservations, staff can log problems, and managers can monitor what needs attention. This connects the solution directly to the dashboard problems.</div>", unsafe_allow_html=True)

elif page == "Inventory Lookup":

    hero(
        "Inventory Explorer",
        "Search items like a library and see availability, condition, and the best hub to book from."
    )

    page_header(
        "Inventory Lookup",
        "This page helps users and staff understand what items are available, where they are, and what condition they are in.",
        "User + Staff"
    )

    # ---------------------------
    # Search and filters
    # ---------------------------
    c1, c2, c3 = st.columns([1.3, 1, 1], gap="small")

    with c1:
        search_text = st.text_input(
            "Search by Item Name",
            placeholder="Example: Projector, Speaker, Tent, Drill"
        )

    with c2:
        selected_category = st.selectbox(
            "Select Item Category",
            ["All"] + sorted(df["item_category"].dropna().unique().tolist())
        )

    with c3:
        selected_hub = st.selectbox(
            "Select Hub",
            ["All"] + sorted(df["hub_name"].dropna().unique().tolist())
        )

    data = df.copy()

    if search_text.strip():
        data = data[data["item_name"].str.contains(search_text.strip(), case=False, na=False)]

    if selected_category != "All":
        data = data[data["item_category"] == selected_category]

    if selected_hub != "All":
        data = data[data["hub_name"] == selected_hub]

    if data.empty:
        st.warning("No matching inventory found. Try another item name, category, or hub.")
        st.stop()

    # ---------------------------
    # Inventory logic
    # ---------------------------
    data["is_missing"] = data["missing_parts_flag"].fillna(0).astype(int) == 1
    data["is_damaged"] = data["damage_flag"].fillna(0).astype(int) == 1
    data["needs_cleaning"] = (
        (data["cleaning_required_flag"].fillna(0).astype(int) == 1)
        & (data["cleaning_done_flag"].fillna(0).astype(int) == 0)
    )

    data["is_booked"] = data["pickup_status"].isin(["Picked up", "Scheduled"])

    data["ready_to_book"] = (
        (~data["is_booked"])
        & (~data["is_missing"])
        & (~data["is_damaged"])
        & (~data["needs_cleaning"])
        & (data["inventory_available_at_reserve"].fillna(0).astype(int) == 1)
    )

    # ---------------------------
    # Top inventory cards
    # ---------------------------
    total_items = len(data)
    ready_items = int(data["ready_to_book"].sum())
    booked_items = int(data["is_booked"].sum())
    missing_items = int(data["is_missing"].sum())
    damaged_items = int(data["is_damaged"].sum())
    cleaning_items = int(data["needs_cleaning"].sum())

    ready_rate = ready_items / total_items if total_items > 0 else 0

    k1, k2, k3, k4, k5 = st.columns(5, gap="small")

    with k1:
        make_kpi_card("Total Matching Items", str(total_items), "Items matching your search")
    with k2:
        make_kpi_card("Ready to Book", str(ready_items), "Available and usable now")
    with k3:
        make_kpi_card("Already Booked", str(booked_items), "Currently picked up or scheduled")
    with k4:
        make_kpi_card("Missing/Damaged", str(missing_items + damaged_items), "Needs staff attention")
    with k5:
        make_kpi_card("Needs Cleaning", str(cleaning_items), "Not ready until cleaned")

    # ---------------------------
    # Best hub recommendation
    # ---------------------------
    hub_summary = data.groupby("hub_name", as_index=False).agg(
        total_items=("reservation_id", "count"),
        ready_to_book=("ready_to_book", "sum"),
        booked_items=("is_booked", "sum"),
        missing_items=("is_missing", "sum"),
        damaged_items=("is_damaged", "sum"),
        cleaning_needed=("needs_cleaning", "sum"),
        avg_queue=("hub_queue_length", "mean")
    )

    hub_summary["ready_rate"] = hub_summary["ready_to_book"] / hub_summary["total_items"]

    hub_summary["issue_count"] = (
        hub_summary["missing_items"]
        + hub_summary["damaged_items"]
        + hub_summary["cleaning_needed"]
    )

    hub_summary["hub_score"] = (
        hub_summary["ready_to_book"] * 3
        + hub_summary["ready_rate"] * 10
        - hub_summary["avg_queue"].fillna(0) * 0.5
        - hub_summary["issue_count"] * 0.7
    )

    hub_summary = hub_summary.sort_values("hub_score", ascending=False)

    best_hub = hub_summary.iloc[0]

    # ---------------------------
    # Availability prediction
    # ---------------------------
    if ready_rate >= 0.60:
        prediction = "High availability"
        prediction_message = "There are enough ready items, so booking should be easy."
        border_color = "#7bc96f"
    elif ready_rate >= 0.30:
        prediction = "Medium availability"
        prediction_message = "Some items are ready, but users should book soon or use the recommended hub."
        border_color = "#f2bd60"
    else:
        prediction = "Low availability"
        prediction_message = "Very few items are ready. Staff may need to clean, repair, or restock items."
        border_color = "#e15659"

    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.86);
            border: 1.4px solid #d8dbe0;
            border-left: 8px solid {border_color};
            border-radius: 20px;
            padding: 16px 18px;
            margin-top: 12px;
            margin-bottom: 14px;
            color: #26374d;">
            <b>Availability prediction:</b> {prediction}. {prediction_message}<br>
            <b>Best hub recommendation:</b> {best_hub["hub_name"]} 
            has <b>{int(best_hub["ready_to_book"])}</b> ready item(s), 
            a ready rate of <b>{best_hub["ready_rate"]:.1%}</b>, 
            and average queue length of <b>{best_hub["avg_queue"]:.2f}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------
    # Inventory overview table
    # ---------------------------
    st.markdown("### Inventory Overview")

    summary = data.groupby(["hub_name", "item_category"], as_index=False).agg(
        total_items=("reservation_id", "count"),
        ready_to_book=("ready_to_book", "sum"),
        booked_items=("is_booked", "sum"),
        missing_items=("is_missing", "sum"),
        damaged_items=("is_damaged", "sum"),
        cleaning_needed=("needs_cleaning", "sum")
    )

    st.dataframe(summary, use_container_width=True)

    # ---------------------------
    # Simple chart
    # ---------------------------
    st.markdown("### Inventory Status by Hub")

    chart_data = hub_summary.copy()

    fig = px.bar(
        chart_data,
        x="hub_name",
        y=["ready_to_book", "booked_items", "missing_items", "damaged_items", "cleaning_needed"],
        barmode="stack",
        title="Ready, Booked, Missing, Damaged, and Cleaning Items by Hub",
        labels={
            "hub_name": "Hub",
            "value": "Item Count",
            "variable": "Inventory Status"
        },
        color_discrete_map={
            "ready_to_book": "#7bc96f",
            "booked_items": "#5b8fe3",
            "missing_items": "#e15659",
            "damaged_items": "#a77f68",
            "cleaning_needed": "#f2bd60"
        }
    )

    fig = style_plotly(fig, height=430, legend_position="bottom", top_margin=60, bottom_margin=95)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ---------------------------
    # Detail table
    # ---------------------------
    st.markdown("### Item Detail Table")

    detail_cols = [
        "item_name",
        "item_category",
        "hub_name",
        "pickup_status",
        "return_status",
        "missing_parts_flag",
        "damage_flag",
        "cleaning_required_flag",
        "cleaning_done_flag",
        "inventory_available_at_reserve",
        "hub_queue_length"
    ]

    detail_cols = [col for col in detail_cols if col in data.columns]

    detail_table = data[detail_cols].copy()
    detail_table["ready_to_book"] = data["ready_to_book"].map({True: "Yes", False: "No"})
    detail_table["already_booked"] = data["is_booked"].map({True: "Yes", False: "No"})
    detail_table["needs_cleaning_now"] = data["needs_cleaning"].map({True: "Yes", False: "No"})

    st.dataframe(detail_table, use_container_width=True)

    st.download_button(
        "Download inventory lookup results",
        data=detail_table.to_csv(index=False).encode("utf-8"),
        file_name="borrowbox_inventory_lookup.csv",
        mime="text/csv"
    )

    st.markdown(
        """
        <div class='insight-box'>
        <b>Why this matters:</b> This page works like a library search system.
        Users can search for items before booking, and staff can quickly see which hubs have
        ready items, booked items, missing parts, damages, or cleaning needs.
        </div>
        """,
        unsafe_allow_html=True
    )
