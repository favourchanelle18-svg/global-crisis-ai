def simulate_crisis(population, food, water, energy, severity):
    vulnerability = (100 - food) * 0.3 + (100 - water) * 0.3 + (100 - energy) * 0.2
    risk = (severity * 10) + vulnerability

    affected = (risk / 120) * population

    return round(risk, 2), int(affected)


def compare_strategies(population, food, water, energy, severity):
    # Strategy A: Immediate Aid
    aid_food = min(food + 20, 100)
    aid_water = min(water + 20, 100)

    risk_a, affected_a = simulate_crisis(population, aid_food, aid_water, energy, severity)

    # Strategy B: Infrastructure Investment
    infra_energy = min(energy + 30, 100)

    risk_b, affected_b = simulate_crisis(population, food, water, infra_energy, severity)

    return {
        "Aid Strategy": affected_a,
        "Infrastructure Strategy": affected_b
    }


def explain_ai(food, water, energy):
    explanation = []

    if food < 50:
        explanation.append("Low food supply is a major driver of risk.")
    if water < 50:
        explanation.append("Water scarcity significantly increases vulnerability.")
    if energy < 50:
        explanation.append("Energy instability reduces crisis response capacity.")

    if not explanation:
        explanation.append("Resource levels are stable; risk is mainly driven by severity.")

    return explanation
