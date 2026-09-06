import pandas as pd
import numpy as np
import geopandas as gpd
from sklearn.metrics import pairwise_distances


IMPORTANCE_MAP = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 4,
    "CRITICAL": 5,
}


WEATHER_LOCATIONS = {
    "Guwahati": (91.75, 26.18),
    "Nagaon": (92.72, 26.15),
    "Lumding": (92.84, 25.28),
    "Silchar": (92.80, 24.82),
}


def build_weather_features(weather):

    weather = weather.copy()

    weather["timestamp"] = pd.to_datetime(
        weather["timestamp"],
        errors="coerce",
    )

    weather = weather.sort_values(
        ["location", "timestamp"]
    )

    numeric_columns = [
        "rainfall_mm",
        "temperature_c",
        "humidity_percent",
        "wind_speed_kmh",
    ]

    for column in numeric_columns:
        weather[column] = pd.to_numeric(
            weather[column],
            errors="coerce",
        )

    # Historical rainfall accumulation
    weather["accumulated_rainfall_24h"] = (
        weather.groupby("location")["rainfall_mm"]
        .transform(
            lambda x: x.rolling(
                window=1,
                min_periods=1,
            ).sum()
        )
    )

    weather["accumulated_rainfall_72h"] = (
        weather.groupby("location")["rainfall_mm"]
        .transform(
            lambda x: x.rolling(
                window=3,
                min_periods=1,
            ).sum()
        )
    )

    weather["rainfall_intensity"] = (
        weather["rainfall_mm"]
    )

    rainfall_score = np.clip(
        weather["rainfall_mm"] / 100,
        0,
        1,
    )

    humidity_score = np.clip(
        weather["humidity_percent"] / 100,
        0,
        1,
    )

    wind_score = np.clip(
        weather["wind_speed_kmh"] / 60,
        0,
        1,
    )

    weather["weather_severity_index"] = (
        0.60 * rainfall_score
        + 0.25 * humidity_score
        + 0.15 * wind_score
    )

    return weather


def assign_weather_location(roads):

    roads = roads.copy()

    roads["centroid"] = roads.geometry.centroid

    road_points = np.array(
        [
            [point.x, point.y]
            for point in roads["centroid"]
        ]
    )

    weather_gdf = gpd.GeoDataFrame(
        {
            "location": list(
                WEATHER_LOCATIONS.keys()
            )
        },
        geometry=gpd.points_from_xy(
            [
                coord[0]
                for coord in WEATHER_LOCATIONS.values()
            ],
            [
                coord[1]
                for coord in WEATHER_LOCATIONS.values()
            ],
        ),
        crs="EPSG:4326",
    )

    weather_gdf = weather_gdf.to_crs(
        "EPSG:32646"
    )

    weather_points = np.array(
        [
            [point.x, point.y]
            for point in weather_gdf.geometry
        ]
    )

    distances = pairwise_distances(
        road_points,
        weather_points,
    )

    nearest_indices = distances.argmin(
        axis=1
    )

    roads["weather_location"] = [
        weather_gdf.iloc[index]["location"]
        for index in nearest_indices
    ]

    return roads


def build_risk_dataset():

    roads = gpd.read_file(
        "data/processed/roads/roads.geojson"
    )

    terrain = pd.read_csv(
        "data/processed/terrain/terrain.csv"
    )

    incidents = pd.read_csv(
        "data/processed/incidents/incidents.csv"
    )

    weather = pd.read_csv(
        "data/processed/weather/assam_weather.csv"
    )

    # Only historical weather is used
    # for model training.
    weather = weather[
        weather["scenario"] == "HISTORICAL"
    ].copy()

    roads = assign_weather_location(
        roads
    )

    roads = roads[
        [
            "road_id",
            "importance",
            "weather_location",
        ]
    ]

    # Road + terrain
    df = roads.merge(
        terrain[
            [
                "road_id",
                "elevation",
                "slope",
            ]
        ],
        on="road_id",
        how="left",
    )

    df["road_importance"] = (
        df["importance"]
        .map(IMPORTANCE_MAP)
        .fillna(1)
    )

    # Historical incident count
    incident_counts = (
        incidents.groupby("road_id")
        .size()
        .reset_index(
            name="incident_count"
        )
    )

    df = df.merge(
        incident_counts,
        on="road_id",
        how="left",
    )

    df["incident_count"] = (
        df["incident_count"]
        .fillna(0)
    )

    # Weather features
    weather = build_weather_features(
        weather
    )

    weather = weather[
        [
            "location",
            "timestamp",
            "rainfall_mm",
            "accumulated_rainfall_24h",
            "accumulated_rainfall_72h",
            "rainfall_intensity",
            "weather_severity_index",
        ]
    ]

    # Create one training sample for every
    # road-weather-date combination.
    df["key"] = 1
    weather["key"] = 1

    df = df.merge(
        weather,
        left_on="weather_location",
        right_on="location",
        how="inner",
    )

    df = df.drop(
        columns=[
            "key_x",
            "key_y",
            "location",
            "timestamp",
        ],
        errors="ignore",
    )

    df["rainfall"] = df["rainfall_mm"]

    numeric_columns = [
        "elevation",
        "slope",
        "road_importance",
        "incident_count",
        "rainfall",
        "accumulated_rainfall_24h",
        "accumulated_rainfall_72h",
        "rainfall_intensity",
        "weather_severity_index",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    df = df.dropna(
        subset=numeric_columns
    )

    # Risk components
    slope_score = np.clip(
        df["slope"] / 30,
        0,
        1,
    )

    elevation_score = np.clip(
        (df["elevation"] - 350) / 100,
        0,
        1,
    )

    incident_score = np.clip(
        df["incident_count"] / 5,
        0,
        1,
    )

    importance_score = (
        df["road_importance"] / 5
    )

    rainfall_score = np.clip(
        df["accumulated_rainfall_72h"] / 300,
        0,
        1,
    )

    weather_score = np.clip(
        df["weather_severity_index"],
        0,
        1,
    )

    # Training target
    df["risk_score"] = (
        0.25 * slope_score
        + 0.15 * elevation_score
        + 0.20 * incident_score
        + 0.10 * importance_score
        + 0.20 * rainfall_score
        + 0.10 * weather_score
    )

    df["risk_score"] = np.clip(
        df["risk_score"],
        0,
        1,
    )

    result = df[
        [
            "road_id",
            "rainfall",
            "accumulated_rainfall_24h",
            "accumulated_rainfall_72h",
            "rainfall_intensity",
            "weather_severity_index",
            "elevation",
            "slope",
            "road_importance",
            "incident_count",
            "risk_score",
        ]
    ].copy()

    return result


if __name__ == "__main__":

    output = "ml/data/road_risk.csv"

    dataset = build_risk_dataset()

    dataset.to_csv(
        output,
        index=False,
    )

    print(
        "Risk dataset created successfully."
    )

    print(
        f"Rows: {len(dataset)}"
    )

    print(
        f"Columns: {len(dataset.columns)}"
    )

    print("\nColumns:")

    for column in dataset.columns:
        print(f"- {column}")

    print("\nFirst 5 rows:")
    print(dataset.head())

    print("\nRisk score statistics:")
    print(
        dataset["risk_score"].describe()
    )

    print("\nRainfall statistics:")
    print(
        dataset["rainfall"].describe()
    )

    print("\nUnique rainfall values:")
    print(
        dataset["rainfall"]
        .nunique()
    )

    print("\nSample rainfall values:")
    print(
        dataset["rainfall"]
        .drop_duplicates()
        .sort_values()
        .head(20)
        .to_list()
    )