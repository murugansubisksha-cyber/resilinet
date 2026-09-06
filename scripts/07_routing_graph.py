"""
ResiliNet 2.0 - Routing Graph Generation
Creates node-edge graph for pathfinding algorithms

INPUT: roads.csv, roads.geojson
OUTPUT: routing_edges.csv, routing_nodes.csv
TIME: ~5 minutes
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def fix_routing_nodes():

    logger.info("=" * 70)
    logger.info("ROUTING NODE COORDINATE PROCESSING")
    logger.info("=" * 70)

    input_path = Path(
        "data/processed/routing/routing_nodes.csv"
    )

    output_path = Path(
        "data/processed/routing/routing_nodes.csv"
    )

    # ---------------------------------------------------------
    # 1. Load routing nodes
    # ---------------------------------------------------------

    logger.info("\n1️⃣ Loading routing nodes...")

    nodes = pd.read_csv(input_path)

    logger.info(
        f"   ✓ Loaded {len(nodes)} routing nodes"
    )

    logger.info(
        f"   Original latitude range: "
        f"{nodes['latitude'].min():.2f} "
        f"to "
        f"{nodes['latitude'].max():.2f}"
    )

    logger.info(
        f"   Original longitude range: "
        f"{nodes['longitude'].min():.2f} "
        f"to "
        f"{nodes['longitude'].max():.2f}"
    )

    # ---------------------------------------------------------
    # 2. Create geometry from projected coordinates
    # ---------------------------------------------------------

    logger.info(
        "\n2️⃣ Converting projected coordinates..."
    )

    geometry = [
        Point(lon, lat)
        for lon, lat in zip(
            nodes["longitude"],
            nodes["latitude"]
        )
    ]

    gdf = gpd.GeoDataFrame(
        nodes,
        geometry=geometry,
        crs="EPSG:32646"
    )

    # ---------------------------------------------------------
    # 3. Convert UTM Zone 46N → WGS84
    # ---------------------------------------------------------

    logger.info(
        "   Converting EPSG:32646 → EPSG:4326..."
    )

    gdf = gdf.to_crs("EPSG:4326")

    # Extract converted coordinates
    gdf["longitude"] = gdf.geometry.x
    gdf["latitude"] = gdf.geometry.y

    # Remove geometry column before saving CSV
    nodes_fixed = gdf.drop(
        columns=["geometry"]
    )

    # Round coordinates
    nodes_fixed["latitude"] = nodes_fixed[
        "latitude"
    ].round(6)

    nodes_fixed["longitude"] = nodes_fixed[
        "longitude"
    ].round(6)

    # ---------------------------------------------------------
    # 4. Validate
    # ---------------------------------------------------------

    logger.info(
        "\n3️⃣ Validating converted coordinates..."
    )

    invalid_latitude = (
        (nodes_fixed["latitude"] < 20)
        |
        (nodes_fixed["latitude"] > 30)
    )

    invalid_longitude = (
        (nodes_fixed["longitude"] < 88)
        |
        (nodes_fixed["longitude"] > 98)
    )

    invalid_count = (
        invalid_latitude
        |
        invalid_longitude
    ).sum()

    logger.info(
        f"   Latitude range: "
        f"{nodes_fixed['latitude'].min():.6f} "
        f"to "
        f"{nodes_fixed['latitude'].max():.6f}"
    )

    logger.info(
        f"   Longitude range: "
        f"{nodes_fixed['longitude'].min():.6f} "
        f"to "
        f"{nodes_fixed['longitude'].max():.6f}"
    )

    if invalid_count == 0:
        logger.info(
            "   ✓ All routing node coordinates are valid"
        )
    else:
        logger.error(
            f"   ✗ Found {invalid_count} invalid coordinates"
        )

    # ---------------------------------------------------------
    # 5. Save corrected CSV
    # ---------------------------------------------------------

    logger.info(
        "\n4️⃣ Saving corrected routing nodes..."
    )

    nodes_fixed.to_csv(
        output_path,
        index=False
    )

    logger.info(
        f"   ✓ Saved: {output_path}"
    )

    logger.info("\n" + "=" * 70)
    logger.info(
        "✅ ROUTING NODE PROCESSING COMPLETE!"
    )
    logger.info("=" * 70)


if __name__ == "__main__":

    fix_routing_nodes()

    print(
        "\n✅ Routing node coordinates fixed successfully!"
    )