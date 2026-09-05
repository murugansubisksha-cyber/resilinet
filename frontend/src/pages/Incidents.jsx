import { useState, useEffect } from "react";
import { fetchIncidents } from "../api/services";

function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [severityFilter, setSeverityFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");

  useEffect(() => {
    const loadIncidents = async () => {
      try {
        const data = await fetchIncidents();
        setIncidents(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    loadIncidents();
  }, []);

  const filteredIncidents = incidents.filter((incident) => {
    const severityMatch =
      severityFilter === "All" || incident.severity === severityFilter;
    const statusMatch =
      statusFilter === "All" || incident.status === statusFilter;

    return severityMatch && statusMatch;
  });

  return (
    <div>
      <h1>Incidents</h1>
      {/* You can now render loading states or filteredIncidents here */}
    </div>
  );
}

export default Incidents;