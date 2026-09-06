"""
ResiliNet 2.0 - Terrain Data Processing
Creates elevation and slope data for roads

INPUT: roads.csv
OUTPUT: data/processed/terrain/terrain.csv
TIME: ~2 minutes
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_terrain_data():
    """Generate synthetic terrain data based on road locations"""
    
    logger.info("=" * 70)
    logger.info("TERRAIN DATA PROCESSING")
    logger.info("=" * 70)
    
    # Load roads
    logger.info("\n1️⃣ Loading roads data...")
    roads = pd.read_csv('data/processed/roads/roads.csv')
    logger.info(f"   ✓ Loaded {len(roads)} roads")
    
    # Extract coordinates from geometry string
    logger.info("\n2️⃣ Extracting coordinates...")
    
    # Parse geometry string to get first coordinate
    def extract_first_coord(geom_str):
        try:
            # Format: "LINESTRING (lon1 lat1, lon2 lat2, ...)"
            coords_str = geom_str.split('(')[1].split(')')[0]
            first_coord = coords_str.split(',')[0].strip()
            lon, lat = map(float, first_coord.split())
            return lat, lon
        except:
            return None, None
    
    roads[['latitude', 'longitude']] = roads['geometry'].apply(
        lambda x: pd.Series(extract_first_coord(x))
    )
    
    logger.info(f"   ✓ Extracted coordinates for {len(roads)} roads")
    
    # Generate elevation based on latitude/longitude
    logger.info("\n3️⃣ Generating elevation data...")
    
    np.random.seed(42)
    
    def assign_elevation(row):
        """Assign elevation based on location and road type"""
        # Assam region baseline
        base_elevation = 100
        
        # Guwahati-Nagaon area (higher, hilly)
        if row['latitude'] > 26.10:
            base_elevation += 300
        # Nagaon-Lumding area (medium)
        elif row['latitude'] > 25.50:
            base_elevation += 150
        # Lumding-Silchar area (low, valley)
        else:
            base_elevation += 50
        
        # Add some variation
        variation = np.random.uniform(-50, 50)
        return max(0, base_elevation + variation)
    
    roads['elevation'] = roads.apply(assign_elevation, axis=1)
    roads['elevation_min'] = roads['elevation'] - np.random.uniform(10, 50, len(roads))
    roads['elevation_max'] = roads['elevation'] + np.random.uniform(10, 50, len(roads))
    
    logger.info(f"   ✓ Generated elevation data")
    logger.info(f"     Min: {roads['elevation'].min():.0f}m")
    logger.info(f"     Max: {roads['elevation'].max():.0f}m")
    logger.info(f"     Mean: {roads['elevation'].mean():.0f}m")
    
    # Calculate slope based on elevation change
    logger.info("\n4️⃣ Calculating slope...")
    
    def assign_slope(row):
        """Calculate slope as percentage"""
        # Elevation change over road length
        elev_change = row['elevation_max'] - row['elevation_min']
        road_length_m = row['length_km'] * 1000
        
        if road_length_m == 0:
            return 0
        
        # Slope % = (elevation change / distance) × 100
        slope = (elev_change / road_length_m) * 100
        return round(min(slope, 30), 2)  # Cap at 30%
    
    roads['slope'] = roads.apply(assign_slope, axis=1)
    
    logger.info(f"   ✓ Calculated slope")
    logger.info(f"     Min: {roads['slope'].min():.2f}%")
    logger.info(f"     Max: {roads['slope'].max():.2f}%")
    logger.info(f"     Mean: {roads['slope'].mean():.2f}%")
    
    # Classify terrain type based on slope
    logger.info("\n5️⃣ Classifying terrain type...")
    
    def classify_terrain(slope):
        if slope < 2:
            return 'FLAT'
        elif slope < 5:
            return 'GENTLE'
        elif slope < 10:
            return 'MODERATE'
        elif slope < 15:
            return 'STEEP'
        else:
            return 'VERY_STEEP'
    
    roads['terrain_type'] = roads['slope'].apply(classify_terrain)
    
    logger.info(f"   ✓ Classified terrain types")
    logger.info(roads['terrain_type'].value_counts())
    
    # Create terrain dataframe
    logger.info("\n6️⃣ Creating terrain dataset...")
    
    terrain = roads[[
        'road_id',
        'elevation',
        'elevation_min',
        'elevation_max',
        'slope',
        'terrain_type'
    ]].copy()
    
    logger.info(f"   ✓ Created {len(terrain)} terrain records")
    
    # Save to CSV
    logger.info("\n7️⃣ Saving terrain data...")
    
    Path('data/processed/terrain').mkdir(parents=True, exist_ok=True)
    output_path = 'data/processed/terrain/terrain.csv'
    terrain.to_csv(output_path, index=False)
    logger.info(f"   ✓ Saved: {output_path}")
    
    logger.info(f"\n" + "=" * 70)
    logger.info(f"✅ TERRAIN DATA PROCESSING COMPLETE!")
    logger.info(f"=" * 70)
    logger.info(f"\n📊 Summary:")
    logger.info(f"   Total records: {len(terrain)}")
    logger.info(f"   Elevation range: {terrain['elevation'].min():.0f}m - {terrain['elevation'].max():.0f}m")
    logger.info(f"   Slope range: {terrain['slope'].min():.2f}% - {terrain['slope'].max():.2f}%")
    logger.info(f"\n📁 Output: {output_path}")
    
    return terrain

if __name__ == "__main__":
    create_terrain_data()
    print("\n✅ Done! Ready for incidents data.")