import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function NetworkMap() {
  const center = [26.2006, 92.9376];

  const incidents = [
    {
      id: 1,
      position: [26.25, 92.95],
      title: "Road Obstruction",
      description: "Possible landslide reported",
    },
    {
      id: 2,
      position: [26.15, 92.85],
      title: "Flood Risk",
      description: "Heavy rainfall affecting road",
    },
  ];

  return (
    <div>
      <h1>Network Map</h1>

      <p className="subtitle">
        Live accessibility and logistics monitoring
      </p>

      <div className="map-container">
        <MapContainer
          center={center}
          zoom={8}
          style={{ height: "600px", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {incidents.map((incident) => (
            <Marker
              key={incident.id}
              position={incident.position}
            >
              <Popup>
                <strong>{incident.title}</strong>
                <br />
                {incident.description}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default NetworkMap;