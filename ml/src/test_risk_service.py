import unittest

from risk_service import (
    FEATURES,
    get_risk_level,
    predict_risk,
    validate_features,
)


class TestRiskService(unittest.TestCase):

    def setUp(self):
        self.low_features = {
            "rainfall": 0,
            "accumulated_rainfall_24h": 0,
            "accumulated_rainfall_72h": 0,
            "rainfall_intensity": 0,
            "weather_severity_index": 0.0,
            "elevation": 350,
            "slope": 2,
            "road_importance": 1,
            "incident_count": 0,
        }

        self.medium_features = {
            "rainfall": 35,
            "accumulated_rainfall_24h": 35,
            "accumulated_rainfall_72h": 35,
            "rainfall_intensity": 35,
            "weather_severity_index": 0.30,
            "elevation": 380,
            "slope": 10,
            "road_importance": 2,
            "incident_count": 1,
        }

        self.high_features = {
            "rainfall": 150,
            "accumulated_rainfall_24h": 150,
            "accumulated_rainfall_72h": 150,
            "rainfall_intensity": 150,
            "weather_severity_index": 0.70,
            "elevation": 420,
            "slope": 25,
            "road_importance": 4,
            "incident_count": 4,
        }

        self.critical_features = {
            "rainfall": 220,
            "accumulated_rainfall_24h": 220,
            "accumulated_rainfall_72h": 220,
            "rainfall_intensity": 220,
            "weather_severity_index": 0.82,
            "elevation": 420,
            "slope": 25,
            "road_importance": 5,
            "incident_count": 4,
        }

        self.extreme_features = {
            "rainfall": 320,
            "accumulated_rainfall_24h": 320,
            "accumulated_rainfall_72h": 320,
            "rainfall_intensity": 320,
            "weather_severity_index": 0.95,
            "elevation": 440,
            "slope": 30,
            "road_importance": 5,
            "incident_count": 5,
        }

    def test_required_features(self):
        self.assertEqual(len(FEATURES), 9)

        expected_features = {
            "rainfall",
            "accumulated_rainfall_24h",
            "accumulated_rainfall_72h",
            "rainfall_intensity",
            "weather_severity_index",
            "elevation",
            "slope",
            "road_importance",
            "incident_count",
        }

        self.assertEqual(set(FEATURES), expected_features)

    def test_low_risk(self):
        result = predict_risk(self.low_features)

        self.assertIn("risk_score", result)
        self.assertIn("risk_level", result)

        self.assertGreaterEqual(result["risk_score"], 0.0)
        self.assertLessEqual(result["risk_score"], 1.0)

        self.assertEqual(result["risk_level"], "LOW")

    def test_medium_risk(self):
        result = predict_risk(self.medium_features)

        self.assertGreaterEqual(result["risk_score"], 0.0)
        self.assertLessEqual(result["risk_score"], 1.0)

        self.assertEqual(result["risk_level"], "MEDIUM")

    def test_high_risk(self):
        result = predict_risk(self.high_features)

        self.assertGreaterEqual(result["risk_score"], 0.0)
        self.assertLessEqual(result["risk_score"], 1.0)

        self.assertEqual(result["risk_level"], "HIGH")

    def test_critical_risk(self):
        result = predict_risk(self.critical_features)

        self.assertGreaterEqual(result["risk_score"], 0.0)
        self.assertLessEqual(result["risk_score"], 1.0)

        self.assertEqual(result["risk_level"], "CRITICAL")

        self.assertAlmostEqual(
            result["risk_score"],
            0.8059,
            places=3,
        )

    def test_extreme_risk(self):
        result = predict_risk(self.extreme_features)

        self.assertGreaterEqual(result["risk_score"], 0.0)
        self.assertLessEqual(result["risk_score"], 1.0)

        self.assertEqual(result["risk_level"], "CRITICAL")

    def test_missing_feature(self):
        incomplete_features = self.critical_features.copy()

        del incomplete_features["rainfall"]

        with self.assertRaises(ValueError):
            predict_risk(incomplete_features)

    def test_multiple_missing_features(self):
        incomplete_features = self.critical_features.copy()

        del incomplete_features["rainfall"]
        del incomplete_features["slope"]
        del incomplete_features["incident_count"]

        with self.assertRaises(ValueError):
            predict_risk(incomplete_features)

    def test_non_numeric_feature(self):
        invalid_features = self.critical_features.copy()

        invalid_features["rainfall"] = "heavy"

        with self.assertRaises(ValueError):
            predict_risk(invalid_features)

    def test_none_feature(self):
        invalid_features = self.critical_features.copy()

        invalid_features["rainfall"] = None

        with self.assertRaises(ValueError):
            predict_risk(invalid_features)

    def test_invalid_input_type(self):
        with self.assertRaises(TypeError):
            predict_risk("invalid input")

    def test_none_input(self):
        with self.assertRaises(TypeError):
            predict_risk(None)

    def test_validation_success(self):
        validate_features(self.critical_features)

    def test_risk_level_boundaries(self):
        self.assertEqual(
            get_risk_level(0.0),
            "LOW",
        )

        self.assertEqual(
            get_risk_level(0.24),
            "LOW",
        )

        self.assertEqual(
            get_risk_level(0.25),
            "MEDIUM",
        )

        self.assertEqual(
            get_risk_level(0.49),
            "MEDIUM",
        )

        self.assertEqual(
            get_risk_level(0.50),
            "HIGH",
        )

        self.assertEqual(
            get_risk_level(0.74),
            "HIGH",
        )

        self.assertEqual(
            get_risk_level(0.75),
            "CRITICAL",
        )

        self.assertEqual(
            get_risk_level(1.0),
            "CRITICAL",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)