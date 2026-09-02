import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulation import simulate_crisis, compare_strategies, explain_ai

# 1. Page Configuration (MUST BE FIRST STREAMLIT COMMAND)
st.set_page_config(
    page_title="Global Crisis Command Center AI",
    page_icon="🌍",
    layout="wide"
)

# 2. Load Local CSS
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("`style.css` not found. Please upload it to your repository.")

load_css("style.css")

# Helper function to style Matplotlib dark theme
def set_dark_chart_theme(fig, ax):
    fig.patch.set_facecolor('#0b0f19')
    ax.set_facecolor('#0b0f19')
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
        return f'<span class="badge-yellow">MODERATE ({severity})</span>'
    elif severity <= 7:
        return f'<span class="badge-orange">HIGH ({severity})</span>'
    else:
        return f'<span class="badge-red">CRITICAL ({severity})</span>'

# Load Dataset
try:
    data = pd.read_csv("data.csv")
except FileNotFoundError:
    data = pd.DataFrame({
        "country": ["Nigeria", "India", "Yemen", "Brazil"],
        "crisis_severity": [8, 6, 9, 4],
        "affected_population": [45, 120, 18, 12],
        "lat": [9.0820, 20.5937, 15.5527, -14.2350],
        "lon": [8.6753, 78.9629, 48.5164, -51.9253]
    })

# SIDEBAR NAVIGATION
st.sidebar.title("🛸 COMMAND CENTER")
page = st.sidebar.radio(
    "Navigation",
    ["Global Dashboard", "Simulation Lab", "Strategy Engine", "How Can I Help?"]
)

# ---------------- DASHBOARD ----------------
if page == "Global Dashboard":

    st.title("🌍 GLOBAL CRISIS COMMAND CENTER")
    st.caption("Real-time monitoring of high-risk regions, resource stress levels, and humanitarian alerts.")

    # Global Map Setup
    st.markdown("### 🗺️ Live Global Stress Map")
    map_data = data[["lat", "lon"]].dropna() if "lat" in data.columns else pd.DataFrame({
        "lat": [9.0820, 20.5937, 15.5527, -14.2350],
        "lon": [8.6753, 78.9629, 48.5164, -51.9253]
    })
    st.map(map_data, zoom=1)

    st.markdown("---")

    # High Risk Cards Section
    st.markdown("### 🚨 Critical Risk Focus Zones")
    high_risk = data.sort_values(by="crisis_severity", ascending=False).head(5)

    cols = st.columns(min(len(high_risk), 5))

    for idx, (_, row) in enumerate(high_risk.iterrows()):
        with cols[idx]:
            badge = get_severity_badge(row["crisis_severity"])
            st.markdown(f"**{row['country']}**", unsafe_allow_html=True)
            st.markdown(badge, unsafe_allow_html=True)
            st.metric("Affected", f"{row['affected_population']}M")

    st.markdown("---")

    # Crisis Distribution Chart
    st.markdown("### 🌐 Regional Severity Overview")
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(data["country"], data["crisis_severity"], color='#00f2fe', edgecolor='#0072ff', alpha=0.85)
    
    # Highlight highest bar
    max_val = data["crisis_severity"].max()
    for bar, val in zip(bars, data["crisis_severity"]):
        if val == max_val:
            bar.set_color('#ef4444')

    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Severity Level (1-10)")
    set_dark_chart_theme(fig, ax)
    
    st.pyplot(fig)

# ---------------- SIMULATION ----------------
elif page == "Simulation Lab":

    st.title("🧪 CRISIS SIMULATION LAB")
    st.markdown("Adjust environmental and resource parameters to forecast crisis outcomes.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👥 Demographics & Threat")
        population = st.slider("Population (millions)", 10, 1500, 300)
        severity = st.slider("Crisis Severity", 1, 10, 6)

    with col2:
        st.markdown("#### 📦 Resource Reserves")
        food = st.slider("Food Supply (%)", 0, 100, 50)
        water = st.slider("Water Supply (%)", 0, 100, 50)
        energy = st.slider("Energy Supply (%)", 0, 100, 50)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("RUN ADVANCED SIMULATION"):

        risk, affected = simulate_crisis(population, food, water, energy, severity)

        st.markdown("### 📊 Simulation Results")

        c1, c2 = st.columns(2)
        c1.metric("Predicted Risk Score", f"{risk:.1f}")
        c2.metric("Estimated Affected Population", f"{affected}M")

        st.markdown("### 📈 Resource Vulnerability Spectrum")

        fig, ax = plt.subplots(figsize=(8, 3))
        resources = ["Food", "Water", "Energy"]
        values = [food, water, energy]
        colors = ['#f87171' if v < 40 else '#facc15' if v < 70 else '#00f2fe' for v in values]
        
        ax.barh(resources, values, color=colors)
        ax.set_xlim(0, 100)
        ax.set_xlabel("Reserve Level (%)")
        set_dark_chart_theme(fig, ax)

        st.pyplot(fig)

        st.markdown("### 🧠 AI Tactical Assessment")

        explanations = explain_ai(food, water, energy)

        for e in explanations:
            st.info(f"⚡ {e}")

# ---------------- STRATEGY ----------------
elif page == "Strategy Engine":

    st.title("⚖️ STRATEGY OPTIMIZATION ENGINE")
    st.markdown("Compare intervention models to minimize total human impact.")

    c1, c2 = st.columns(2)
    with c1:
        population = st.slider("Target Population (M)", 10, 1500, 300, key="strat_pop")
        severity = st.slider("Severity Baseline", 1, 10, 6, key="strat_sev")
    with c2:
        food = st.slider("Food Deployment (%)", 0, 100, 40, key="strat_food")
        water = st.slider("Water Deployment (%)", 0, 100, 40, key="strat_water")
        energy = st.slider("Energy Deployment (%)", 0, 100, 40, key="strat_energy")

    results = compare_strategies(population, food, water, energy, severity)

    st.markdown("### 📊 Strategy Outcomes Comparison")

    fig, ax = plt.subplots(figsize=(8, 4))
    strategies = list(results.keys())
    outcomes = list(results.values())
    
    ax.bar(strategies, outcomes, color='#00c6ff', edgecolor='#0072ff')
    ax.set_ylabel("Affected Population (millions)")
    set_dark_chart_theme(fig, ax)

    st.pyplot(fig)

    best = min(results, key=results.get)
    st.success(f"🎯 **OPTIMAL STRATEGY:** {best.upper()} minimizes population impact.")

# ---------------- HOW TO HELP ----------------
elif page == "How Can I Help?":

    st.title("🤝 ACTION CENTER")
    st.markdown("Discover direct paths to aid humanitarian initiatives and crisis relief.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 💳 Donate")
        st.write("Direct financial support to verified international emergency response funds.")
        st.button("Explore Relief Funds")

    with col2:
        st.markdown("### 🙋 Volunteer")
        st.write("Offer skills in data mapping, logistics, supply routing, or field support.")
        st.button("Join Volunteer Network")

    with col3:
        st.markdown("### 📢 Advocate")
        st.write("Amplify high-priority updates and educate communities on risk trends.")
        st.button("Share Campaign Assets")
