import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function AIInsights() {
  const [riskLevel, setRiskLevel] = useState("Medium");

  const riskData = {
    Low: {
      score: 25,
      accessibility: "90%",
      weather: "Low Risk",
      landslide: "Low Risk",
      flood: "Low Risk",
      recommendation:
        "Route conditions are stable. Normal logistics operations can continue.",
    },

    Medium: {
      score: 58,
      accessibility: "70%",
      weather: "Moderate Rainfall",
      landslide: "Medium Risk",
      flood: "Low Risk",
      recommendation:
        "Monitor weather conditions and keep an alternative route ready.",
    },

    High: {
      score: 87,
      accessibility: "35%",
      weather: "Heavy Rainfall",
      landslide: "High Risk",
      flood: "High Risk",
      recommendation:
        "Avoid this route. Redirect convoys through a safer alternative route.",
    },
  };

  const currentRisk = riskData[riskLevel];

  return (
    <div className="ai-page">
      <h1>🤖 AI Smart Logistics Insights</h1>

      <p className="ai-subtitle">
        AI-powered risk analysis for safer logistics operations.
      </p>

      <div className="risk-selector">
        <label>Select Risk Scenario:</label>

        <select
          value={riskLevel}
          onChange={(e) => setRiskLevel(e.target.value)}
        >
          <option value="Low">Low Risk</option>
          <option value="Medium">Medium Risk</option>
          <option value="High">High Risk</option>
        </select>
      </div>

      <div className="ai-score-card">
        <h2>AI Risk Score</h2>

        <div className="risk-score">
          {currentRisk.score}/100
        </div>

        <h3>Risk Level: {riskLevel}</h3>
      </div>

      <div className="ai-grid">

        <div className="ai-card">
          <h3>🛣️ Road Accessibility</h3>
          <p>{currentRisk.accessibility}</p>
        </div>

        <div className="ai-card">
          <h3>🌧️ Weather Condition</h3>
          <p>{currentRisk.weather}</p>
        </div>

        <div className="ai-card">
          <h3>⛰️ Landslide Risk</h3>
          <p>{currentRisk.landslide}</p>
        </div>

        <div className="ai-card">
          <h3>🌊 Flood Risk</h3>
          <p>{currentRisk.flood}</p>
        </div>

      </div>

      <div className="recommendation-card">
        <h2>🤖 AI Recommendation</h2>

        <p>
          {currentRisk.recommendation}
        </p>
      </div>
    </div>
  );
}

export default AIInsights;