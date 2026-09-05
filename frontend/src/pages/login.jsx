import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import toast from "react-hot-toast";
import {
  Activity,
  ShieldCheck,
  Truck,
  AlertTriangle,
} from "lucide-react";

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
    role: "Dispatcher",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await login(formData);

      toast.success("Login successful");

      navigate("/");
    } catch (error) {
      console.error(error);

      toast.error(
        error.response?.data?.detail ||
          "Login failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">

      <div className="login-brand-panel">

        <div>
          <h1>🚚 ResiliNet</h1>

          <p>
            Dynamic Route & Hazard
            Management Platform
          </p>
        </div>

        <div className="telemetry-grid">

          <div className="telemetry-card">
            <Activity />
            <span>Network Status</span>
            <strong>Operational</strong>
          </div>

          <div className="telemetry-card">
            <Truck />
            <span>Active Convoys</span>
            <strong>12</strong>
          </div>

          <div className="telemetry-card">
            <AlertTriangle />
            <span>Active Hazards</span>
            <strong>8</strong>
          </div>

          <div className="telemetry-card">
            <ShieldCheck />
            <span>System Safety</span>
            <strong>85%</strong>
          </div>

        </div>

      </div>


      <div className="login-form-panel">

        <form
          className="login-card"
          onSubmit={handleSubmit}
        >

          <h2>Command Center Login</h2>

          <p>
            Sign in to access ResiliNet.
          </p>


          <label>Email</label>

          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            value={formData.email}
            onChange={handleChange}
            required
          />


          <label>Password</label>

          <input
            type="password"
            name="password"
            placeholder="Enter password"
            value={formData.password}
            onChange={handleChange}
            required
          />


          <label>Role</label>

          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
          >
            <option>Dispatcher</option>
            <option>Field Worker</option>
            <option>Admin</option>
          </select>


          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Signing In..."
              : "Login to Command Center"}
          </button>

        </form>

      </div>

    </div>
  );
}

export default Login;