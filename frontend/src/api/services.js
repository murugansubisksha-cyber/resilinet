import client from "./client";

// Authentication
export const authLogin = async (credentials) => {
  const response = await client.post("/auth/login", credentials);
  return response.data;
};


// Roads
export const fetchRoads = async () => {
  const response = await client.get("/roads");
  return response.data;
};


// Incidents
export const fetchIncidents = async () => {
  const response = await client.get("/incidents");
  return response.data;
};

export const submitIncident = async (data) => {
  const response = await client.post("/incidents", data);
  return response.data;
};


// Risk
export const fetchRiskAssessment = async (params = {}) => {
  const response = await client.get("/risk", {
    params,
  });

  return response.data;
};


// Convoys / Vehicles
export const fetchConvoys = async () => {
  const response = await client.get("/vehicles");
  return response.data;
};