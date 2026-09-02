import geopandas as gpd
import osmnx as ox
import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURATION
# ============================================================

# Assam Corridor Bounding Box
NORTH = 26.20
SOUTH = 24.80
EAST = 93.00
WEST = 91.30

CORRIDOR_NAME = "Assam Corridor (Guwahati-Silchar)"

# Road types to download
ROAD_TYPES = [
    'motorway',
    'trunk',
    'primary',
    'secondary',
    'tertiary',
]

# ============================================================
# MAIN FUNCTION
# ============================================================

def download_roads():
    """Download road network from OpenStreetMap"""
    
    logger.info("=" * 70)
    logger.info("ROAD NETWORK DOWNLOAD - ASSAM CORRIDOR")
    logger.info("=" * 70)
    
    logger.info(f"\nBounding Box:")
    logger.info(f"  North: {NORTH}°")
    logger.info(f"  South: {SOUTH}°")
    logger.info(f"  East: {EAST}°")
    logger.info(f"  West: {WEST}°")
    logger.info(f"  Region: {CORRIDOR_NAME}")
    
    # Step 1: Download roads
    logger.info(f"\n1️⃣  DOWNLOADING ROADS FROM OPENSTREETMAP...")
    logger.info(f"   Requesting road types: {', '.join(ROAD_TYPES)}")
    
    try:
        # Create bounding box
        bbox = (WEST, SOUTH, EAST, NORTH)
        
        # Download all roads in bbox
        logger.info("   ⏳ This may take 10-15 minutes...")
        roads = ox.features_from_bbox(
            bbox=bbox,
            tags={'highway': ROAD_TYPES}
        )
        
        logger.info(f"   ✓ Downloaded {len(roads)} road features")
        
    except Exception as e:
        logger.error(f"   ✗ Error downloading roads: {e}")
        logger.error("   Tip: Check internet connection and try again")
        return False
    
    # Step 2: Process roads data
    logger.info(f"\n2️⃣  PROCESSING ROAD DATA...")
    
    # Convert to GeoDataFrame if not already
    if not isinstance(roads, gpd.GeoDataFrame):
        roads = gpd.GeoDataFrame(roads)
    
    # Keep only LineString geometries (actual roads)
    logger.info(f"   Filtering for road geometries (LineString only)...")
    roads = roads[roads.geometry.type == 'LineString'].copy()
    logger.info(f"   ✓ {len(roads)} LineString roads")
    
    # Step 3: Generate road_ids
    logger.info(f"\n3️⃣  GENERATING ROAD IDS...")
    roads['road_id'] = ['R' + str(i+1).zfill(4) for i in range(len(roads))]
    logger.info(f"   ✓ Generated road_ids from R0001 to R{len(roads):04d}")
    
    # Step 4: Extract and clean key fields
    logger.info(f"\n4️⃣  EXTRACTING KEY FIELDS...")
    
    roads['name'] = roads.get('name', 'Unknown Road')
    roads['highway'] = roads.get('highway', 'unclassified')
    
    # Calculate road length in km
    roads= roads.to_crs(epsg=32646)
    roads['length_km'] = roads.geometry.length / 1000
    
    # Determine importance level
    def assign_importance(road_type):
        if road_type in ['motorway', 'trunk']:
            return 'CRITICAL'
        elif road_type == 'primary':
            return 'HIGH'
        elif road_type == 'secondary':
            return 'MEDIUM'
        else:
            return 'LOW'
    
    roads['importance'] = roads['highway'].apply(assign_importance)
    roads['status'] = 'OPEN'  # Default status
    
    logger.info(f"   ✓ Extracted fields:")
    logger.info(f"     - name")
    logger.info(f"     - highway (road type)")
    logger.info(f"     - length_km")
    logger.info(f"     - importance (CRITICAL/HIGH/MEDIUM/LOW)")
    logger.info(f"     - status (OPEN/DEGRADED/BLOCKED)")
    
    # Step 5: Select and organize columns
    logger.info(f"\n5️⃣  SELECTING FINAL COLUMNS...")
    
    roads = roads[[
        'road_id',
        'name',
        'highway',
        'length_km',
        'importance',
        'status',
        'geometry'
    ]].copy()
    
    roads = roads.reset_index(drop=True)
    logger.info(f"   ✓ Final dataset: {len(roads)} rows × {len(roads.columns)} columns")
    
    # Step 6: Summary statistics
    logger.info(f"\n6️⃣  DATA SUMMARY...")
    logger.info(f"\n   Road Type Distribution:")
    logger.info(roads['highway'].value_counts())
    
    logger.info(f"\n   Importance Distribution:")
    logger.info(roads['importance'].value_counts())
    
    logger.info(f"\n   Length Statistics (km):")
    logger.info(f"     Min: {roads['length_km'].min():.2f}")
    logger.info(f"     Max: {roads['length_km'].max():.2f}")
    logger.info(f"     Mean: {roads['length_km'].mean():.2f}")
    logger.info(f"     Total: {roads['length_km'].sum():.2f}")
    
    # Step 7: Save outputs
    logger.info(f"\n7️⃣  SAVING OUTPUTS...")
    
    # Create output folders
    Path('data/raw/osm').mkdir(parents=True, exist_ok=True)
    Path('data/processed/roads').mkdir(parents=True, exist_ok=True)
    
    # Save as GeoJSON (for mapping)
    geojson_path = 'data/raw/osm/assam_corridor_roads.geojson'
    roads.to_file(geojson_path, driver='GeoJSON')
    logger.info(f"   ✓ Saved: {geojson_path}")
    
    # Save as CSV (for database)
    csv_path = 'data/processed/roads/roads.csv'
    roads_csv = roads.copy()
    roads_csv['geometry'] = roads_csv['geometry'].astype(str)  # Convert geometry to string
    roads_csv.to_csv(csv_path, index=False)
    logger.info(f"   ✓ Saved: {csv_path}")
    
    # Save processed GeoJSON
    processed_geojson_path = 'data/processed/roads/roads.geojson'
    roads.to_file(processed_geojson_path, driver='GeoJSON')
    logger.info(f"   ✓ Saved: {processed_geojson_path}")
    
    # Step 8: Verify
    logger.info(f"\n8️⃣  VERIFICATION...")
    
    # Check file sizes
    import os
    geojson_size = os.path.getsize(geojson_path) / (1024 * 1024)  # MB
    csv_size = os.path.getsize(csv_path) / (1024 * 1024)  # MB
    
    logger.info(f"   File Sizes:")
    logger.info(f"     {geojson_path}: {geojson_size:.2f} MB")
    logger.info(f"     {csv_path}: {csv_size:.2f} MB")
    
    # Check for duplicates
    duplicates = roads['road_id'].duplicated().sum()
    logger.info(f"   Duplicate road_ids: {duplicates}")
    
    if duplicates > 0:
        logger.warning(f"   ⚠️  Found {duplicates} duplicate road_ids!")
    else:
        logger.info(f"   ✓ All road_ids are unique")
    
    # Check for missing geometries
    missing_geom = roads['geometry'].isna().sum()
    logger.info(f"   Missing geometries: {missing_geom}")
    
    if missing_geom > 0:
        logger.warning(f"   ⚠️  Found {missing_geom} roads with missing geometries!")
    else:
        logger.info(f"   ✓ All roads have valid geometries")
    
    logger.info(f"\n" + "=" * 70)
    logger.info(f"✅ ROAD NETWORK DOWNLOAD COMPLETE!")
    logger.info(f"=" * 70)
    
    logger.info(f"\n📊 Summary:")
    logger.info(f"   Total roads downloaded: {len(roads)}")
    logger.info(f"   Total road length: {roads['length_km'].sum():.0f} km")
    logger.info(f"   Road_id format: R0001 to R{len(roads):04d}")
    logger.info(f"\n📁 Output files:")
    logger.info(f"   1. {geojson_path}")
    logger.info(f"   2. {csv_path}")
    logger.info(f"   3. {processed_geojson_path}")
    
    logger.info(f"\n✨ Next steps:")
    logger.info(f"   1. Ask for weather data code")
    logger.info(f"   2. Ask for terrain data code")
    logger.info(f"   3. Ask for incidents data code")
    logger.info(f"   4. Load everything to Supabase")
    
    return True


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    success = download_roads()
    if success:
        print("\n✅ All done! Ready for next step.")
    else:
        print("\n❌ Failed. Check errors above.")