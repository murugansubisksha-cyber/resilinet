import { createContext, useContext, useEffect, useState } from "react";
import { authLogin } from "../api/services";

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    const token = localStorage.getItem("access_token");

    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    }

    setLoading(false);
  }, []);

  const login = async (credentials) => {
  // Temporary demo login for frontend development

  const DEMO_EMAIL = "admin@resilinet.com";
  const DEMO_PASSWORD = "admin123";

  if (
    credentials.email === DEMO_EMAIL &&
    credentials.password === DEMO_PASSWORD
  ) {
    const demoToken = "resilinet-demo-token";

    const userData = {
      email: credentials.email,
      role: credentials.role,
    };

    localStorage.setItem(
      "access_token",
      demoToken
    );

    localStorage.setItem(
      "user",
      JSON.stringify(userData)
    );

    setUser(userData);

    return {
      access_token: demoToken,
    };
  }

  // Try real FastAPI backend login for other users
  const data = await authLogin(credentials);

  const token =
    data.access_token ||
    data.token;

  if (!token) {
    throw new Error("Access token not received");
  }

  const userData = {
    email: credentials.email,
    role: credentials.role,
  };

  localStorage.setItem(
    "access_token",
    token
  );

  localStorage.setItem(
    "user",
    JSON.stringify(userData)
  );

  setUser(userData);

  return data;
};

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};