from risk_service import predict_risk


TEST_CASES = {
    "LOW": {
        "rainfall": 0,
        "accumulated_rainfall_24h": 0,
        "accumulated_rainfall_72h": 0,
        "rainfall_intensity": 0,
        "weather_severity_index": 0.0,
        "elevation": 350,
        "slope": 2,
        "road_importance": 1,
        "incident_count": 0,
    },

    "MEDIUM": {
        "rainfall": 35,
        "accumulated_rainfall_24h": 35,
        "accumulated_rainfall_72h": 35,
        "rainfall_intensity": 35,
        "weather_severity_index": 0.30,
        "elevation": 380,
        "slope": 10,
        "road_importance": 2,
        "incident_count": 1,
    },

    "HIGH": {
        "rainfall": 100,
        "accumulated_rainfall_24h": 100,
        "accumulated_rainfall_72h": 100,
        "rainfall_intensity": 100,
        "weather_severity_index": 0.60,
        "elevation": 400,
        "slope": 18,
        "road_importance": 3,
        "incident_count": 2,
    },

    "CRITICAL": {
        "rainfall": 220,
        "accumulated_rainfall_24h": 220,
        "accumulated_rainfall_72h": 220,
        "rainfall_intensity": 220,
        "weather_severity_index": 0.82,
        "elevation": 420,
        "slope": 25,
        "road_importance": 5,
        "incident_count": 4,
    },

    "EXTREME": {
        "rainfall": 320,
        "accumulated_rainfall_24h": 320,
        "accumulated_rainfall_72h": 320,
        "rainfall_intensity": 320,
        "weather_severity_index": 0.95,
        "elevation": 440,
        "slope": 30,
        "road_importance": 5,
        "incident_count": 5,
    },
}


for expected_level, features in TEST_CASES.items():
    result = predict_risk(features)

    print(
        f"{expected_level:10s} -> "
        f"Score: {result['risk_score']:.4f} | "
        f"Level: {result['risk_level']}"
    )