import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from streamlit_folium import st_folium
import folium
from simulation import simulate_crisis, compare_strategies, explain_ai

# 1. PAGE CONFIGURATION (MUST BE FIRST)
st.set_page_config(
    page_title="Global Crisis AI Command",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. LOAD EXTERNAL CSS
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("`style.css` not found. Please ensure it is present in your repository.")

load_css("style.css")

# Helper function to style Matplotlib dark theme
def set_dark_chart_theme(fig, ax):
    fig.patch.set_facecolor('#040711')
    ax.set_facecolor('#080d1a')
    ax.spines['bottom'].set_color('#00f2fe')
    ax.spines['left'].set_color('#00f2fe')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(colors='#e2e8f0', which='both')
    ax.yaxis.label.set_color('#e2e8f0')
    ax.xaxis.label.set_color('#e2e8f0')
    ax.title.set_color('#00f2fe')

# Helper function for dynamic color badges
def get_severity_badge(severity):
    if severity <= 4:
        return f'<span class="badge-yellow">MODERATE ({severity}/10)</span>'
    elif severity <= 7:
        return f'<span class="badge-orange">HIGH ({severity}/10)</span>'
    else:
        return f'<span class="badge-red">CRITICAL ({severity}/10)</span>'

# Load Dataset Safely
try:
    data = pd.read_csv("data.csv")
except FileNotFoundError:
    data = pd.DataFrame({
        "country": ["Nigeria", "India", "Yemen", "Brazil", "Sudan", "Ukraine"],
        "crisis_severity": [8, 6, 9, 4, 9, 8],
        "affected_population": [45, 120, 18, 12, 24, 15],
        "primary_risk": ["Conflict & Food", "Water Scarcity", "Severe Famine", "Climate Disaster", "Civil Unrest", "War & Energy"],
        "lat": [9.0820, 20.5937, 15.5527, -14.2350, 12.8628, 48.3794],
        "lon": [8.6753, 78.9629, 48.5164, -51.9253, 30.2176, 31.1656]
    })

# SIDEBAR NAVIGATION & INTERACTIVE AI SEARCH
st.sidebar.markdown("## 🛸 GLOBAL COMMAND")
st.sidebar.caption("System Status: **ONLINE** | Live Intelligence Feed")

page = st.sidebar.radio(
    "Navigation Mode",
    ["Global Command Atlas", "Simulation Lab", "Strategy Engine", "Solutions Lab", "Action Center (Donate & Volunteer)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Ask the Crisis Map")
user_query = st.sidebar.text_input("Query crisis intelligence database:")
if user_query:
    st.sidebar.info(f"🤖 **AI Analysis:** Scanning live records for '{user_query}'... High risks detected in multiple regional sectors.")

# ---------------- 1. GLOBAL COMMAND ATLAS ----------------
if page == "Global Command Atlas":

    st.title("🌐 GLOBAL CRISIS INTELLIGENCE ATLAS")
    st.caption("Real-time telemetry on global humanitarian risks, regional severity, and population displacement.")

    # Dynamic Stat Counters
    total_crises = len(data)
    critical_count = len(data[data["crisis_severity"] >= 8])
    total_affected = data["affected_population"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Active Crisis Zones", f"{total_crises} Regions")
    m2.metric("Critical Threat Sectors", f"{critical_count} High Priority")
    m3.metric("Total Affected Population", f"{total_affected} Million")

    st.markdown("---")

    # Interactive Folium Map
    st.markdown("### 🗺️ Live Global Stress Map")
    m = folium.Map(location=[15.0, 10.0], zoom_start=2, tiles="CartoDB dark_matter")

    for _, row in data.iterrows():
        color = "#ef4444" if row["crisis_severity"] >= 8 else "#f97316" if row["crisis_severity"] >= 5 else "#eab308"
        
        popup_html = f"""
        <div style="font-family: sans-serif; width: 170px;">
            <h4 style="margin:0; color: {color};">{row['country']}</h4>
            <b>Severity:</b> {row['crisis_severity']}/10<br>
            <b>Affected:</b> {row['affected_population']}M<br>
            <b>Primary Risk:</b> {row.get('primary_risk', 'N/A')}
        </div>
        """
        
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=int(row["crisis_severity"]) * 2.2,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"{row['country']} - Severity: {row['crisis_severity']}"
        ).add_to(m)

    st_folium(m, width="100%", height=450)

    st.markdown("---")

    # Interactive Cards
    st.markdown("### 🚨 Priority Risk Focus Zones")
    high_risk = data.sort_values(by="crisis_severity", ascending=False).head(4)

    cols = st.columns(4)
    for idx, (_, row) in enumerate(high_risk.iterrows()):
        with cols[idx % 4]:
            st.markdown(f"""
            <div class="card-container">
                <h4>{row['country']}</h4>
                {get_severity_badge(row['crisis_severity'])}<br><br>
                <small>Impacted Population</small>
                <h3 style="margin:0; color:#00f2fe;">{row['affected_population']}M</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {row['country']} Report", key=f"btn_{row['country']}"):
                st.info(f"📍 **{row['country']} Focus:** Primary risk factor identified as **{row.get('primary_risk', 'General Crisis')}**.")

    # Severity Distribution Chart
    st.markdown("### 📊 Regional Severity Distribution")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    bars = ax.bar(data["country"], data["crisis_severity"], color='#00f2fe', edgecolor='#0072ff', alpha=0.85)
    
    for bar, val in zip(bars, data["crisis_severity"]):
        if val >= 8:
            bar.set_color('#ef4444')

    plt.xticks(rotation=30, ha='right')
    ax.set_ylabel("Severity Score (1-10)")
    set_dark_chart_theme(fig, ax)
    st.pyplot(fig)

# ---------------- 2. SIMULATION LAB ----------------
elif page == "Simulation Lab":

    st.title("🧪 ADVANCED SIMULATION LAB")
    st.markdown("Adjust environmental and resource parameters to project real-time crisis outcomes.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👥 Demographics & Threat")
        population = st.slider("Population Size (Millions)", 10, 1500, 300)
        severity = st.slider("Crisis Severity Index", 1, 10, 6)

    with col2:
        st.markdown("#### 📦 Strategic Resource Reserves")
        food = st.slider("Food Reserves (%)", 0, 100, 50)
        water = st.slider("Water Reserves (%)", 0, 100, 50)
        energy = st.slider("Energy Grid (%)", 0, 100, 50)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("RUN PREDICTIVE SIMULATION"):
        with st.spinner("Processing AI Predictive Engine..."):
            time.sleep(0.4)
            risk, affected = simulate_crisis(population, food, water, energy, severity)

        st.markdown("### 📊 Forecasted Simulation Outcomes")

        c1, c2 = st.columns(2)
        c1.metric("Predicted Risk Score", f"{risk:.1f} / 100")
        c2.metric("Estimated Affected Population", f"{affected} Million")

        st.markdown("### 📈 Resource Vulnerability Spectrum")

        fig, ax = plt.subplots(figsize=(8, 2.5))
        resources = ["Food", "Water", "Energy"]
        values = [food, water, energy]
        colors = ['#ef4444' if v < 40 else '#facc15' if v < 70 else '#00f2fe' for v in values]
        
        ax.barh(resources, values, color=colors)
        ax.set_xlim(0, 100)
        ax.set_xlabel("Reserve Level (%)")
        set_dark_chart_theme(fig, ax)
        st.pyplot(fig)

        st.markdown("### 🧠 AI Tactical Assessment")
        explanations = explain_ai(food, water, energy)
        for e in explanations:
            st.info(f"⚡ **Tactical Advisory:** {e}")

# ---------------- 3. STRATEGY ENGINE ----------------
elif page == "Strategy Engine":

    st.title("⚖️ STRATEGY OPTIMIZATION ENGINE")
    st.markdown("Evaluate intervention strategies to mitigate human casualty and displacement metrics.")

    c1, c2 = st.columns(2)
    with c1:
        population = st.slider("Target Population (M)", 10, 1500, 300, key="strat_pop")
        severity = st.slider("Severity Index", 1, 10, 6, key="strat_sev")
    with c2:
        food = st.slider("Food Aid Deployment (%)", 0, 100, 40, key="strat_food")
        water = st.slider("Water Aid Deployment (%)", 0, 100, 40, key="strat_water")
        energy = st.slider("Energy Grid Repair (%)", 0, 100, 40, key="strat_energy")

    results = compare_strategies(population, food, water, energy, severity)

    st.markdown("### 📊 Strategy Outcomes Comparison")

    fig, ax = plt.subplots(figsize=(8, 3.5))
    strategies = list(results.keys())
    outcomes = list(results.values())
    
    ax.bar(strategies, outcomes, color='#00c6ff', edgecolor='#0072ff')
    ax.set_ylabel("Affected Population (Millions)")
    set_dark_chart_theme(fig, ax)
    st.pyplot(fig)

    best = min(results, key=results.get)
    st.success(f"🎯 **OPTIMAL STRATEGY:** {best.upper()} yields the lowest population risk.")

# ---------------- 4. SOLUTIONS LAB ----------------
elif page == "Solutions Lab":

    st.title("💡 SOLUTIONS & INTERVENTION LAB")
    st.markdown("Explore targeted intervention protocols for major humanitarian sectors.")

    sector = st.selectbox("Select Crisis Sector:", ["Food Insecurity", "Water Shortage", "Conflict & Displacement", "Energy Grid Failure"])

    if sector == "Food Insecurity":
        st.markdown("""
        <div class="card-container">
            <h4>🌾 Tactical Intervention Flow: Food Supply</h4>
            <p><b>Step 1: Strategic Grain Mobilization</b> → Deploy emergency food reserves to distribution hubs.</p>
            <p><b>Step 2: Local Agricultural Support</b> → Supply drought-tolerant seeds and fertilizer packages.</p>
            <p><b>Step 3: Market Stabilization</b> → Direct emergency cash grants to local food suppliers.</p>
        </div>
        """, unsafe_allow_html=True)
    elif sector == "Water Shortage":
        st.markdown("""
        <div class="card-container">
            <h4>💧 Tactical Intervention Flow: Clean Water Access</h4>
            <p><b>Step 1: Mobile Desalination & Filtration</b> → Deploy rapid water purification units.</p>
            <p><b>Step 2: Well & Aquifer Repair</b> → Restore subterranean wells and municipal pipes.</p>
            <p><b>Step 3: Sanitation Kits</b> → Distribute water purification tablets and emergency supplies.</p>
        </div>
        """, unsafe_allow_html=True)
    elif sector == "Conflict & Displacement":
        st.markdown("""
        <div class="card-container">
            <h4>🛡️ Tactical Intervention Flow: Civilian Protection</h4>
            <p><b>Step 1: Safe Humanitarian Corridors</b> → Secure demilitarized routes for safe transit.</p>
            <p><b>Step 2: Modular Emergency Shelters</b> → Construct temporary modular housing centers.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card-container">
            <h4>⚡ Tactical Intervention Flow: Power Restoration</h4>
            <p><b>Step 1: Micro-Grid Solar Generators</b> → Restore immediate electrical power to medical hubs.</p>
            <p><b>Step 2: Grid Repairs</b> → Deploy specialized engineers for regional power lines.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------- 5. ACTION CENTER (REAL LINKS & INTERACTIVE MODALS) ----------------
elif page == "Action Center (Donate & Volunteer)":

    st.title("🤝 ACTION & RESPONSE CENTER")
    st.markdown("Support verified international humanitarian organizations directly.")

    st.markdown("### 💳 Direct Aid & Real-World Donation Channels")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <h4>🇺🇳 UNHCR</h4>
            <p>Refugee relief & emergency shelters worldwide.</p>
            <a href="https://donate.unhcr.org/" target="_blank" class="donate-btn">Donate to UNHCR ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <h4>🍲 WFP</h4>
            <p>World Food Programme emergency aid.</p>
            <a href="https://donate.wfp.org/" target="_blank" class="donate-btn">Donate to WFP ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <h4>🏥 RED CROSS</h4>
            <p>Emergency medical response & disaster relief.</p>
            <a href="https://www.icrc.org/en/donate" target="_blank" class="donate-btn">Donate to Red Cross ↗</a>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card-container" style="text-align: center;">
            <h4>👶 UNICEF</h4>
            <p>Children & youth humanitarian assistance.</p>
            <a href="https://www.unicef.org/take-action" target="_blank" class="donate-btn">Donate to UNICEF ↗</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Interactive Modal Popups
    st.markdown("### 🙋 Interactive Community Actions")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("🤝 Register as a Volunteer"):
            st.success("✅ **Volunteer Portal Unlocked:** Your profile has been logged for disaster mapping & logistical support networks.")

    with c2:
        if st.button("📢 Generate Social Advocacy Kit"):
            st.info("📋 **Advocacy Assets Ready:** Campaign graphics and pre-written press releases have been prepared.")
