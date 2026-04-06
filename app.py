import streamlit as st
from model import train_model
from simulation import simulate_crisis, recommend_strategy

st.set_page_config(page_title="Global Crisis AI", layout="centered")

st.title("🌍 Global Crisis AI Simulator")
st.write("Simulating global crises and optimizing response strategies")

model = train_model()

st.header("Enter Crisis Scenario")

population = st.slider("Population (millions)", 100, 2000, 500)
food = st.slider("Food Supply (%)", 0, 100, 70)
water = st.slider("Water Supply (%)", 0, 100, 70)
energy = st.slider("Energy Supply (%)", 0, 100, 70)
severity = st.slider("Crisis Severity (1-10)", 1, 10, 5)

if st.button("Run Simulation"):

    risk, affected = simulate_crisis(population, food, water, energy, severity)
    prediction = model.predict([[population, food, water, energy, severity]])[0]
    strategies = recommend_strategy(food, water, energy)

    st.subheader("📊 Results")
    st.write(f"Risk Score: {risk}")
    st.write(f"Estimated Affected Population: {affected} million")
    st.write(f"AI Prediction: {int(prediction)} million")

    st.subheader("🧠 Recommended Strategies")
    for s in strategies:
        st.write(f"- {s}")
