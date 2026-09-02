function RouteComparison() {
  const routes = [
    {
      name: "Route A",
      distance: "120 km",
      time: "4 hours",
      risk: "High",
      accessibility: "60%",
      score: 65,
      description: "Shorter route but has high landslide risk.",
    },
    {
      name: "Route B",
      distance: "145 km",
      time: "5 hours",
      risk: "Low",
      accessibility: "90%",
      score: 90,
      description: "Longer route but safer and more accessible.",
    },
  ];

  return (
    <div className="page">
      <h1>🛣️ Route Comparison</h1>

      <p className="page-description">
        Compare available routes and select the safest option.
      </p>

      <div className="route-container">
        {routes.map((route, index) => (
          <div className="route-card" key={index}>
            <h2>{route.name}</h2>

            <p>
              <strong>📏 Distance:</strong> {route.distance}
            </p>

            <p>
              <strong>⏱️ Travel Time:</strong> {route.time}
            </p>

            <p>
              <strong>⚠️ Risk Level:</strong>{" "}
              <span
                className={
                  route.risk === "High"
                    ? "risk-high"
                    : "risk-low"
                }
              >
                {route.risk}
              </span>
            </p>

            <p>
              <strong>🛣️ Accessibility:</strong>{" "}
              {route.accessibility}
            </p>
            <p>
              <strong>📊 Route Score:</strong> {route.score}/100
            </p>

            <p>{route.description}</p>
          </div>
        ))}
      </div>

      <div className="recommendation">
        <h2>⭐ Recommended Route</h2>

        <p>
          <strong>Route B</strong> is recommended because it has lower
          risk and higher accessibility.
        </p>
      </div>
    </div>
  );
}

export default RouteComparison;