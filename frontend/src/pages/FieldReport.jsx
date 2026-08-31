import { useState } from "react";

function FieldReport() {
  const [incidentType, setIncidentType] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const [location, setLocation] = useState(null);
  const [locationStatus, setLocationStatus] = useState("");

  const [syncStatus, setSyncStatus] = useState("Not Saved");

  const timestamp = new Date().toLocaleString();

  // Handle image selection
  const handleImageChange = (event) => {
    const selectedImage = event.target.files[0];

    if (selectedImage) {
      setImage(selectedImage);

      const previewURL = URL.createObjectURL(selectedImage);

      setImagePreview(previewURL);
    }
  };

  // Capture GPS location
  const captureLocation = () => {
    setLocationStatus("Getting GPS location...");

    if (!navigator.geolocation) {
      setLocationStatus("Geolocation is not supported.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        setLocation({
          latitude,
          longitude,
        });

        setLocationStatus("Location captured successfully.");
      },

      (error) => {
        setLocationStatus("Unable to get location.");
      }
    );
  };

  // Save report to IndexedDB
  const saveReport = () => {
    const report = {
      id: Date.now(),
      incidentType,
      description,
      location,
      timestamp,
      imageName: image ? image.name : "No image",
      syncStatus: "Saved Offline",
    };

    const request = indexedDB.open("ResiliNetDB", 1);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      if (!db.objectStoreNames.contains("reports")) {
        db.createObjectStore("reports", {
          keyPath: "id",
        });
      }
    };

    request.onsuccess = (event) => {
      const db = event.target.result;

      const transaction = db.transaction(
        "reports",
        "readwrite"
      );

      const store = transaction.objectStore("reports");

      store.add(report);

      transaction.oncomplete = () => {
        setSyncStatus("Saved Offline");

        alert("Field report saved successfully!");
      };
    };

    request.onerror = () => {
      alert("Error saving report.");
    };
  };

  return (
    <div className="page">
      <h1>📋 Field Report</h1>

      <p className="page-description">
        Report road damage, landslides, blockages, or other incidents from the field.
      </p>

      <div className="field-report-container">

        {/* Incident Type */}

        <div className="form-group">
          <label>⚠️ Incident Type</label>

          <select
            value={incidentType}
            onChange={(event) =>
              setIncidentType(event.target.value)
            }
          >
            <option value="">Select Incident</option>

            <option value="Landslide">
              Landslide
            </option>

            <option value="Road Blockage">
              Road Blockage
            </option>

            <option value="Flood">
              Flood
            </option>

            <option value="Bridge Damage">
              Bridge Damage
            </option>

            <option value="Other">
              Other
            </option>
          </select>
        </div>

        {/* Camera / Image */}

        <div className="form-group">
          <label>📷 Capture / Upload Image</label>

          <input
            type="file"
            accept="image/*"
            capture="environment"
            onChange={handleImageChange}
          />

          {imagePreview && (
            <img
              src={imagePreview}
              alt="Incident preview"
              className="image-preview"
            />
          )}
        </div>

        {/* GPS */}

        <div className="form-group">
          <label>📍 GPS Location</label>

          <button
            className="gps-button"
            onClick={captureLocation}
          >
            Capture Location
          </button>

          <p>{locationStatus}</p>

          {location && (
            <div className="location-box">
              <p>
                <strong>Latitude:</strong>{" "}
                {location.latitude}
              </p>

              <p>
                <strong>Longitude:</strong>{" "}
                {location.longitude}
              </p>
            </div>
          )}
        </div>

        {/* Timestamp */}

        <div className="form-group">
          <label>🕒 Report Timestamp</label>

          <p className="timestamp">
            {timestamp}
          </p>
        </div>

        {/* Description */}

        <div className="form-group">
          <label>📝 Description</label>

          <textarea
            placeholder="Describe the incident..."
            value={description}
            onChange={(event) =>
              setDescription(event.target.value)
            }
          />
        </div>

        {/* Sync Status */}

        <div className="sync-status">
          🔄 Sync Status: <strong>{syncStatus}</strong>
        </div>

        {/* Save */}

        <button
          className="submit-report-button"
          onClick={saveReport}
        >
          💾 Save Field Report
        </button>

      </div>
    </div>
  );
}

export default FieldReport;