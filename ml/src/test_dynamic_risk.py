from predict import predict_risk


BASE_CONDITIONS = {
    "elevation": 420,
    "slope": 25,
    "road_importance": 5,
    "incident_count": 4,
}


SCENARIOS = {
    "NORMAL": {
        "rainfall": 35,
        "accumulated_rainfall_24h": 35,
        "accumulated_rainfall_72h": 35,
        "rainfall_intensity": 35,
        "weather_severity_index": 0.30,
    },

    "HEAVY_MONSOON": {
        "rainfall": 220,
        "accumulated_rainfall_24h": 220,
        "accumulated_rainfall_72h": 220,
        "rainfall_intensity": 220,
        "weather_severity_index": 0.82,
    },

    "EXTREME_MONSOON": {
        "rainfall": 320,
        "accumulated_rainfall_24h": 320,
        "accumulated_rainfall_72h": 320,
        "rainfall_intensity": 320,
        "weather_severity_index": 0.95,
    },
}


print("Dynamic Risk Test")
print("=================")

for scenario, weather in SCENARIOS.items():

    data = {
        **BASE_CONDITIONS,
        **weather,
    }

    result = predict_risk(data)

    print()
    print(f"Scenario   : {scenario}")
    print(f"Rainfall   : {data['rainfall']} mm")
    print(f"Risk Score : {result['risk_score']}")
    print(f"Risk Level : {result['risk_level']}")