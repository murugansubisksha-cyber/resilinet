import {
  MapContainer,
  TileLayer,
  Polyline,
} from "react-leaflet";

import { useEffect, useState } from "react";

import {
  fetchRoads,
  fetchRiskAssessment,
} from "../api/services";


function NetworkMap() {

  const [roads, setRoads] =
    useState([]);

  const getRiskColor = (risk) => {

    if (risk >= 80) {
      return "#EF4444";
    }

    if (risk >= 50) {
      return "#F59E0B";
    }

    return "#10B981";
  };


  useEffect(() => {

    const loadData = async () => {

      try {

        const roadsData =
          await fetchRoads();

        setRoads(roadsData);

      } catch (error) {

        console.error(
          "Failed to load roads",
          error
        );

      }

    };

    loadData();

  }, []);


  return (

    <div>

      <h1>Network Map</h1>

      <MapContainer
        center={[11.1271, 78.6569]}
        zoom={7}
        style={{
          height: "600px",
          width: "100%",
        }}
      >

        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />


        {roads.map((road) => (

          <Polyline
            key={road.id}
            positions={road.coordinates}
            color={
              getRiskColor(
                road.risk_score
              )
            }
            weight={5}
          />

        ))}

      </MapContainer>

    </div>
  );
}

export default NetworkMap;