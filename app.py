import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import train_model
from simulation import simulate_crisis, recommend_strategy

st.set_page_config(page_title="Global Crisis AI", layout="wide")

# -------------------------
# LOAD DATA
# -------------------------
data = pd.read_csv("data.csv")
model = train_model()

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("🌍 Global Crisis AI")
page = st.sidebar.radio("Navigate", ["Dashboard", "Simulation Lab", "Insights"])

# -------------------------
# DASHBOARD
# -------------------------
if page == "Dashboard":

    st.title("🌍 Global Crisis Overview")
    st.markdown("### Real-time inspired simulation of global crisis conditions")

    st.image("https://images.unsplash.com/photo-1509099836639-18ba1795216d", use_container_width=True)

    st.markdown("## 🌐 Regions at Risk")

    cols = st.columns(3)

    for i, row in data.iterrows():
        with cols[i % 3]:
            st.metric(label=row["region"], value=f"Severity {row['crisis_severity']}")
            st.write(f"Affected: {row['affected_population']}M")

# -------------------------
# SIMULATION LAB
# -------------------------
elif page == "Simulation Lab":

    st.title("🧪 Crisis Simulation Lab")
    st.markdown("Adjust parameters to simulate a real-world crisis scenario.")

    col1, col2 = st.columns(2)

    with col1:
        population = st.slider("Population (millions)", 100, 2000, 500)
        severity = st.slider("Crisis Severity", 1, 10, 5)

    with col2:
        food = st.slider("Food Supply (%)", 0, 100, 70)
        water = st.slider("Water Supply (%)", 0, 100, 70)
        energy = st.slider("Energy Supply (%)", 0, 100, 70)

    st.markdown("---")

    if st.button("🚀 Run Advanced Simulation"):

        risk, affected = simulate_crisis(population, food, water, energy, severity)
        prediction = model.predict([[population, food, water, energy, severity]])[0]
        strategies = recommend_strategy(food, water, energy)

        st.subheader("📊 Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Risk Score", risk)
        col2.metric("Simulated Affected", f"{affected}M")
        col3.metric("AI Prediction", f"{int(prediction)}M")

        # Graph
        st.subheader("📈 Impact Visualization")

        labels = ["Food", "Water", "Energy"]
        values = [food, water, energy]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Supply %")

        st.pyplot(fig)

# -------------------------
# INSIGHTS
# -------------------------
elif page == "Insights":

    st.title("🧠 AI Strategy Insights")

    st.markdown("This section explains how AI recommends crisis response strategies.")

    food = st.slider("Food Supply", 0, 100, 50)
    water = st.slider("Water Supply", 0, 100, 50)
    energy = st.slider("Energy Supply", 0, 100, 50)

    strategies = recommend_strategy(food, water, energy)

    st.subheader("📌 Recommended Actions")

    for s in strategies:
        st.success(s)

    st.markdown("## ⚖️ Decision Impact")
    st.write(
        "AI evaluates trade-offs between resource allocation strategies to maximize lives saved."
    )
