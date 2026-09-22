import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Inputs
relevance = ctrl.Antecedent(
    np.arange(0, 101, 1),
    "relevance"
)

difficulty = ctrl.Antecedent(
    np.arange(0, 101, 1),
    "difficulty"
)

availability = ctrl.Antecedent(
    np.arange(0, 101, 1),
    "availability"
)


# Output
suitability = ctrl.Consequent(
    np.arange(0, 101, 1),
    "suitability"
)


# Membership Functions

relevance["low"] = fuzz.trimf(
    relevance.universe,
    [0, 0, 50]
)

relevance["medium"] = fuzz.trimf(
    relevance.universe,
    [25, 50, 75]
)

relevance["high"] = fuzz.trimf(
    relevance.universe,
    [50, 100, 100]
)


difficulty["easy"] = fuzz.trimf(
    difficulty.universe,
    [0, 0, 50]
)

difficulty["medium"] = fuzz.trimf(
    difficulty.universe,
    [25, 50, 75]
)

difficulty["hard"] = fuzz.trimf(
    difficulty.universe,
    [50, 100, 100]
)


availability["low"] = fuzz.trimf(
    availability.universe,
    [0, 0, 50]
)

availability["medium"] = fuzz.trimf(
    availability.universe,
    [25, 50, 75]
)

availability["high"] = fuzz.trimf(
    availability.universe,
    [50, 100, 100]
)


suitability["poor"] = fuzz.trimf(
    suitability.universe,
    [0, 0, 40]
)

suitability["average"] = fuzz.trimf(
    suitability.universe,
    [25, 50, 75]
)

suitability["good"] = fuzz.trimf(
    suitability.universe,
    [60, 80, 100]
)

suitability["excellent"] = fuzz.trimf(
    suitability.universe,
    [80, 100, 100]
)


# Fuzzy Rules

rule1 = ctrl.Rule(
    relevance["high"]
    & difficulty["easy"]
    & availability["high"],
    suitability["excellent"]
)

rule2 = ctrl.Rule(
    relevance["high"]
    & difficulty["medium"]
    & availability["high"],
    suitability["good"]
)

rule3 = ctrl.Rule(
    relevance["medium"]
    & difficulty["easy"]
    & availability["high"],
    suitability["good"]
)

rule4 = ctrl.Rule(
    relevance["low"]
    & availability["low"],
    suitability["poor"]
)

rule5 = ctrl.Rule(
    difficulty["hard"]
    & relevance["high"],
    suitability["average"]
)

rule6 = ctrl.Rule(
    relevance["medium"] & difficulty["medium"],
    suitability["average"]
)

rule7 = ctrl.Rule(
    relevance["low"] & difficulty["easy"],
    suitability["poor"]
)

rule8 = ctrl.Rule(
    relevance["low"] & difficulty["medium"],
    suitability["poor"]
)

# Control System

suitability_control = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]
)


# Function used by the Streamlit app

def calculate_suitability(
    relevance_value,
    difficulty_value,
    availability_value
):

    system = ctrl.ControlSystemSimulation(
        suitability_control
    )

    system.input["relevance"] = relevance_value
    system.input["difficulty"] = difficulty_value
    system.input["availability"] = availability_value

    system.compute()

    return round(
        system.output["suitability"],
        2
    )