import pandas as pd
import numpy as np
import logging
from pathlib import Path
from datetime import datetime, timedelta
from shapely import wkt
from shapely.geometry import shape
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def get_coordinates(geometry_value):
    """
    Convert road geometry into WGS84 longitude/latitude.
    Handles WKT geometry stored in the roads CSV.
    """

    try:
        # Convert string into Shapely geometry
        geom = wkt.loads(geometry_value)

        # The roads CSV was created from the GeoDataFrame.
        # Its geometry coordinates are projected coordinates.
        #
        # Assam corridor data uses UTM Zone 46N.
        # Convert from EPSG:32646 -> EPSG:4326.

        import geopandas as gpd

        temp_gdf = gpd.GeoDataFrame(
            {"geometry": [geom]},
            crs="EPSG:32646"
        )

        temp_gdf = temp_gdf.to_crs("EPSG:4326")

        point = temp_gdf.geometry.iloc[0]

        # Use the first coordinate of the road
        if hasattr(point, "coords"):
            lon, lat = list(point.coords)[0]
        else:
            lon, lat = point.representative_point().coords[0]

        return float(lon), float(lat)

    except Exception as e:
        logger.warning(f"Could not convert geometry: {e}")

        # Safe Assam fallback
        lat = 25.5 + np.random.uniform(-1, 1)
        lon = 92.0 + np.random.uniform(-1, 1)

        return float(lon), float(lat)


def create_incidents_data():

    logger.info("=" * 70)
    logger.info("INCIDENTS DATA PROCESSING")
    logger.info("=" * 70)

    # ---------------------------------------------------------
    # 1. Load roads
    # ---------------------------------------------------------

    logger.info("\n1️⃣ Loading roads data...")

    roads = pd.read_csv(
        "data/processed/roads/roads.csv"
    )

    logger.info(f"   ✓ Loaded {len(roads)} roads")

    # ---------------------------------------------------------
    # 2. Incident configuration
    # ---------------------------------------------------------

    logger.info("\n2️⃣ Setting up incident generation...")

    incident_types = [
        "LANDSLIDE",
        "FLOOD",
        "ROAD_BLOCKAGE",
        "ACCIDENT",
        "FALLEN_TREE"
    ]

    severities = [1, 2, 3, 4, 5]

    high_risk_count = max(
        1,
        len(roads) // 7
    )

    high_risk_roads = roads.sample(
        n=high_risk_count,
        random_state=42
    )["road_id"].tolist()

    logger.info(
        f"   ✓ Identified {len(high_risk_roads)} high-risk roads"
    )

    # ---------------------------------------------------------
    # 3. Generate incidents
    # ---------------------------------------------------------

    logger.info("\n3️⃣ Generating synthetic incidents (2023)...")

    np.random.seed(42)

    incidents_list = []

    incident_id_counter = 1000

    # Create a lookup dictionary
    road_geometry = dict(
        zip(
            roads["road_id"],
            roads["geometry"]
        )
    )

    for road_id in roads["road_id"]:

        # High-risk roads get more incidents
        if road_id in high_risk_roads:
            num_incidents = np.random.randint(0, 5)
        else:
            num_incidents = np.random.randint(0, 2)

        for _ in range(num_incidents):

            # Random date in 2023
            random_days = np.random.randint(0, 365)

            incident_date = (
                datetime(2023, 1, 1)
                + timedelta(days=int(random_days))
            )

            # -------------------------------------------------
            # Convert projected road coordinates
            # to longitude / latitude
            # -------------------------------------------------

            geometry_value = road_geometry.get(road_id)

            lon, lat = get_coordinates(
                geometry_value
            )

            # Small random displacement
            incident_latitude = (
                lat + np.random.uniform(-0.01, 0.01)
            )

            incident_longitude = (
                lon + np.random.uniform(-0.01, 0.01)
            )

            # -------------------------------------------------
            # Safety validation
            # -------------------------------------------------

            if not (
                20 <= incident_latitude <= 30
            ):
                logger.warning(
                    f"Invalid latitude for {road_id}: "
                    f"{incident_latitude}"
                )
                continue

            if not (
                88 <= incident_longitude <= 98
            ):
                logger.warning(
                    f"Invalid longitude for {road_id}: "
                    f"{incident_longitude}"
                )
                continue

            # -------------------------------------------------
            # Create incident
            # -------------------------------------------------

            incident = {
                "incident_id":
                    f"INC{incident_id_counter:06d}",

                "road_id":
                    road_id,

                "incident_type":
                    np.random.choice(
                        incident_types
                    ),

                "severity":
                    int(
                        np.random.choice(
                            severities
                        )
                    ),

                "date":
                    incident_date,

                "latitude":
                    round(
                        float(incident_latitude),
                        6
                    ),

                "longitude":
                    round(
                        float(incident_longitude),
                        6
                    ),

                "description":
                    "Synthetic incident record",

                "data_source":
                    "SYNTHETIC"
            }

            incidents_list.append(
                incident
            )

            incident_id_counter += 1

    # ---------------------------------------------------------
    # 4. Create DataFrame
    # ---------------------------------------------------------

    incidents_df = pd.DataFrame(
        incidents_list
    )

    logger.info(
        f"   ✓ Generated {len(incidents_df)} incidents"
    )

    # ---------------------------------------------------------
    # 5. Validate coordinates
    # ---------------------------------------------------------

    logger.info(
        "\n4️⃣ Validating incident coordinates..."
    )

    logger.info(
        f"   Latitude range: "
        f"{incidents_df['latitude'].min():.6f} "
        f"to "
        f"{incidents_df['latitude'].max():.6f}"
    )

    logger.info(
        f"   Longitude range: "
        f"{incidents_df['longitude'].min():.6f} "
        f"to "
        f"{incidents_df['longitude'].max():.6f}"
    )

    invalid_latitude = (
        (incidents_df["latitude"] < 20)
        |
        (incidents_df["latitude"] > 30)
    )

    invalid_longitude = (
        (incidents_df["longitude"] < 88)
        |
        (incidents_df["longitude"] > 98)
    )

    invalid_count = (
        invalid_latitude
        |
        invalid_longitude
    ).sum()

    if invalid_count == 0:

        logger.info(
            "   ✓ All coordinates are valid"
        )

    else:

        logger.error(
            f"   ✗ Found {invalid_count} "
            f"invalid coordinates"
        )

    # ---------------------------------------------------------
    # 6. Save
    # ---------------------------------------------------------

    logger.info(
        "\n5️⃣ Saving incidents data..."
    )

    output_directory = Path(
        "data/processed/incidents"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        output_directory /
        "incidents.csv"
    )

    incidents_df.to_csv(
        output_path,
        index=False
    )

    logger.info(
        f"   ✓ Saved: {output_path}"
    )

    logger.info("\n" + "=" * 70)
    logger.info(
        "✅ INCIDENTS DATA PROCESSING COMPLETE!"
    )
    logger.info("=" * 70)

    return incidents_df


if __name__ == "__main__":

    create_incidents_data()

    print(
        "\n✅ Done! Incident data is ready for Supabase."
    )