def simulate_crisis(population, food, water, energy, severity):
    risk = (severity * 10) + (100 - food) + (100 - water) + (100 - energy)
    affected = (risk / 100) * population
    return risk, int(affected)


def recommend_strategy(food, water, energy):
    strategies = []

    if food < 60:
        strategies.append("Increase food distribution")
    if water < 60:
        strategies.append("Deploy water aid systems")
    if energy < 60:
        strategies.append("Stabilize energy supply")

    if not strategies:
        strategies.append("Maintain current strategy")

    return strategies
