import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulation import simulate_crisis, compare_strategies, explain_ai

st.set_page_config(page_title="Global Crisis AI", layout="wide")

data = pd.read_csv("data.csv")

# SIDEBAR
st.sidebar.title("🌍 Global Crisis AI")
page = st.sidebar.radio("Navigation", ["Global Dashboard", "Simulation Lab", "Strategy Engine"])

# ---------------- DASHBOARD ----------------
if page == "Global Dashboard":

    st.title("🌍 Global Crisis Intelligence System")
    st.markdown("### Monitoring high-risk regions and humanitarian stress levels")

    st.image("https://images.unsplash.com/photo-1521295121783-8a321d551ad2", use_container_width=True)

    st.markdown("## 🚨 High Risk Countries")

    high_risk = data.sort_values(by="crisis_severity", ascending=False).head(5)

    cols = st.columns(5)

    for i, row in high_risk.iterrows():
        with cols[i % 5]:
            st.metric(row["country"], f"Severity {row['crisis_severity']}")
            st.caption(f"Affected: {row['affected_population']}M")

    st.markdown("## 🌐 Crisis Distribution")

    fig, ax = plt.subplots()
    ax.bar(data["country"], data["crisis_severity"])
    plt.xticks(rotation=45)

    st.pyplot(fig)

# ---------------- SIMULATION ----------------
elif page == "Simulation Lab":

    st.title("🧪 Advanced Crisis Simulation")

    col1, col2 = st.columns(2)

    with col1:
        population = st.slider("Population (millions)", 10, 1500, 300)
        severity = st.slider("Crisis Severity", 1, 10, 6)

    with col2:
        food = st.slider("Food Supply (%)", 0, 100, 50)
        water = st.slider("Water Supply (%)", 0, 100, 50)
        energy = st.slider("Energy Supply (%)", 0, 100, 50)

    if st.button("Run Simulation"):

        risk, affected = simulate_crisis(population, food, water, energy, severity)

        st.subheader("📊 Results")

        c1, c2 = st.columns(2)
        c1.metric("Risk Score", risk)
        c2.metric("Affected Population", f"{affected}M")

        st.subheader("📈 Resource Breakdown")

        fig, ax = plt.subplots()
        ax.bar(["Food", "Water", "Energy"], [food, water, energy])
        st.pyplot(fig)

        st.subheader("🧠 AI Explanation")

        explanations = explain_ai(food, water, energy)

        for e in explanations:
            st.info(e)

# ---------------- STRATEGY ----------------
elif page == "Strategy Engine":

    st.title("⚖️ Strategy Comparison Engine")

    population = st.slider("Population", 10, 1500, 300)
    severity = st.slider("Severity", 1, 10, 6)
    food = st.slider("Food", 0, 100, 40)
    water = st.slider("Water", 0, 100, 40)
    energy = st.slider("Energy", 0, 100, 40)

    results = compare_strategies(population, food, water, energy, severity)

    st.subheader("📊 Strategy Outcomes")

    st.write(results)

    fig, ax = plt.subplots()
    ax.bar(results.keys(), results.values())
    ax.set_ylabel("Affected Population (millions)")

    st.pyplot(fig)

    best = min(results, key=results.get)

    st.success(f"✅ Best Strategy: {best}")
