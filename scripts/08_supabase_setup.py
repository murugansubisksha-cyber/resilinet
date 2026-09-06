"""
ResiliNet 2.0 - Supabase Database Setup & Loading
Creates tables and loads all CSV data

TIME: ~15 minutes
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class SupabaseLoader:
    def __init__(self):
        """Initialize database connection"""
        self.host = os.getenv('DB_HOST')
        self.database = os.getenv('DB_DATABASE', 'postgres')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD')
        self.port = int(os.getenv('DB_PORT', 5432))
        
        self.conn = None
        
        logger.info("=" * 70)
        logger.info("SUPABASE DATABASE SETUP & LOADING")
        logger.info("=" * 70)
    
    def connect(self):
        """Connect to database"""
        logger.info("\n1️⃣ Connecting to Supabase...")
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = self.conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            cursor.close()
            logger.info(f"   ✓ Connected successfully")
            logger.info(f"   PostgreSQL: {version}")
            return True
        except Exception as e:
            logger.error(f"   ✗ Connection failed: {e}")
            logger.error(f"   Check your .env file:")
            logger.error(f"     DB_HOST={self.host}")
            logger.error(f"     DB_USER={self.user}")
            return False
    
    def create_tables(self):
        """Create all required tables"""
        logger.info("\n2️⃣ Creating database tables...")
        
        sql = """
        -- Enable PostGIS
        CREATE EXTENSION IF NOT EXISTS postgis;

        -- Road Segments
        CREATE TABLE IF NOT EXISTS road_segments (
            road_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(255),
            highway VARCHAR(50),
            length_km NUMERIC(10, 3),
            importance VARCHAR(20),
            status VARCHAR(20) DEFAULT 'OPEN',
            geometry GEOMETRY(LineString, 4326),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Terrain
        CREATE TABLE IF NOT EXISTS terrain (
            terrain_id SERIAL PRIMARY KEY,
            road_id VARCHAR(10) NOT NULL REFERENCES road_segments(road_id) ON DELETE CASCADE,
            elevation NUMERIC(8, 2),
            elevation_min NUMERIC(8, 2),
            elevation_max NUMERIC(8, 2),
            slope NUMERIC(6, 2),
            terrain_type VARCHAR(50)
        );

        -- Weather
        CREATE TABLE IF NOT EXISTS weather (
            weather_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            location VARCHAR(100),
            latitude NUMERIC(9, 6),
            longitude NUMERIC(9, 6),
            rainfall_mm NUMERIC(8, 2),
            temperature_c NUMERIC(5, 2),
            humidity_percent NUMERIC(5, 2),
            wind_speed_kmh NUMERIC(5, 2),
            data_source VARCHAR(50)
        );

        -- Incidents
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id VARCHAR(20) PRIMARY KEY,
            road_id VARCHAR(10) NOT NULL REFERENCES road_segments(road_id) ON DELETE CASCADE,
            incident_type VARCHAR(50),
            severity INT,
            date TIMESTAMP,
            latitude NUMERIC(9, 6),
            longitude NUMERIC(9, 6),
            description TEXT,
            data_source VARCHAR(50)
        );

        -- Vehicles
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id VARCHAR(50) PRIMARY KEY,
            vehicle_number VARCHAR(50),
            vehicle_type VARCHAR(50),
            cargo_type VARCHAR(100),
            capacity_kg INT,
            priority VARCHAR(20),
            operator VARCHAR(100),
            origin VARCHAR(100),
            destination VARCHAR(100),
            current_latitude NUMERIC(9, 6),
            current_longitude NUMERIC(9, 6),
            destination_latitude NUMERIC(9, 6),
            destination_longitude NUMERIC(9, 6),
            status VARCHAR(50),
            current_load_kg INT,
            timestamp TIMESTAMP,
            data_source VARCHAR(50)
        );

        -- Routing Nodes
        CREATE TABLE IF NOT EXISTS routing_nodes (
            node_id VARCHAR(20) PRIMARY KEY,
            latitude NUMERIC(9, 6),
            longitude NUMERIC(9, 6),
            geometry GEOMETRY(Point, 4326)
        );

        -- Routing Edges
        CREATE TABLE IF NOT EXISTS routing_edges (
            edge_id SERIAL PRIMARY KEY,
            from_node_id VARCHAR(20) NOT NULL REFERENCES routing_nodes(node_id),
            to_node_id VARCHAR(20) NOT NULL REFERENCES routing_nodes(node_id),
            road_id VARCHAR(10) NOT NULL REFERENCES road_segments(road_id) ON DELETE CASCADE,
            distance_m NUMERIC(10, 2),
            status VARCHAR(20) DEFAULT 'OPEN'
        );

        -- Demo Scenarios
        CREATE TABLE IF NOT EXISTS demo_scenarios (
            scenario_id VARCHAR(50) PRIMARY KEY,
            scenario_name VARCHAR(255),
            scenario_type VARCHAR(50),
            rainfall_mm NUMERIC(8, 2),
            network_accessibility_percent NUMERIC(5, 2),
            risk_level VARCHAR(50),
            timestamp TIMESTAMP,
            data_source VARCHAR(50)
        );

        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_road_geometry ON road_segments USING GIST(geometry);
        CREATE INDEX IF NOT EXISTS idx_terrain_road ON terrain(road_id);
        CREATE INDEX IF NOT EXISTS idx_incident_road ON incidents(road_id);
        CREATE INDEX IF NOT EXISTS idx_weather_location ON weather(location);
        CREATE INDEX IF NOT EXISTS idx_edge_from ON routing_edges(from_node_id);
        CREATE INDEX IF NOT EXISTS idx_edge_to ON routing_edges(to_node_id);
        """
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ All tables created successfully")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error creating tables: {e}")
            self.conn.rollback()
            return False
    
    def load_roads(self):
        """Load roads data"""
        logger.info("\n3️⃣ Loading roads data...")
        
        try:
            roads = pd.read_csv('data/processed/roads/roads.csv')
            cursor = self.conn.cursor()
            
            for idx, row in roads.iterrows():
                cursor.execute("""
                    INSERT INTO road_segments 
                    (road_id, name, highway, length_km, importance, status, geometry)
                    VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
                    ON CONFLICT (road_id) DO NOTHING
                """, (
                    row['road_id'],
                    row['name'],
                    row['highway'],
                    row['length_km'],
                    row['importance'],
                    row['status'],
                    row['geometry']
                ))
            
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ Loaded {len(roads)} roads")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error loading roads: {e}")
            self.conn.rollback()
            return False
    
    def load_terrain(self):
        """Load terrain data"""
        logger.info("\n4️⃣ Loading terrain data...")
        
        try:
            terrain = pd.read_csv('data/processed/terrain/terrain.csv')
            cursor = self.conn.cursor()
            
            for idx, row in terrain.iterrows():
                cursor.execute("""
                    INSERT INTO terrain 
                    (road_id, elevation, elevation_min, elevation_max, slope, terrain_type)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['road_id'],
                    row['elevation'],
                    row['elevation_min'],
                    row['elevation_max'],
                    row['slope'],
                    row['terrain_type']
                ))
            
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ Loaded {len(terrain)} terrain records")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error loading terrain: {e}")
            self.conn.rollback()
            return False
    
    def load_weather(self):
        """Load weather data"""
        logger.info("\n5️⃣ Loading weather data...")
        
        try:
            weather = pd.read_csv('data/processed/weather/assam_weather.csv')
            cursor = self.conn.cursor()
            
            for idx, row in weather.iterrows():
                cursor.execute("""
                    INSERT INTO weather 
                    (timestamp, location, latitude, longitude, rainfall_mm, 
                     temperature_c, humidity_percent, wind_speed_kmh, data_source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row.get('timestamp'),
                    row.get('location'),
                    row.get('latitude'),
                    row.get('longitude'),
                    row.get('rainfall_mm'),
                    row.get('temperature_c'),
                    row.get('humidity_percent'),
                    row.get('wind_speed_kmh'),
                    row.get('data_source', 'DEMO')
                ))
            
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ Loaded {len(weather)} weather records")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error loading weather: {e}")
            self.conn.rollback()
            return False
    
    def load_incidents(self):
        """Load incidents data"""
        logger.info("\n6️⃣ Loading incidents data...")
        
        try:
            incidents = pd.read_csv('data/processed/incidents/incidents.csv')
            cursor = self.conn.cursor()
            
            for idx, row in incidents.iterrows():
                cursor.execute("""
                    INSERT INTO incidents 
                    (incident_id, road_id, incident_type, severity, date, 
                     latitude, longitude, description, data_source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (incident_id) DO NOTHING
                """, (
                    row['incident_id'],
                    row['road_id'],
                    row['incident_type'],
                    row['severity'],
                    row['date'],
                    row['latitude'],
                    row['longitude'],
                    row.get('description'),
                    row.get('data_source', 'HISTORICAL')
                ))
            
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ Loaded {len(incidents)} incidents")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error loading incidents: {e}")
            self.conn.rollback()
            return False
    
    def load_vehicles(self):
        """Load vehicles data"""
        logger.info("\n7️⃣ Loading vehicles data...")
        
        try:
            vehicles = pd.read_csv('data/processed/vehicles/assam_vehicles.csv')
            cursor = self.conn.cursor()
            
            for idx, row in vehicles.iterrows():
                cursor.execute("""
                    INSERT INTO vehicles 
                    (vehicle_id, vehicle_number, vehicle_type, cargo_type, capacity_kg, 
                     priority, operator, origin, destination, current_latitude, current_longitude,
                     destination_latitude, destination_longitude, status, current_load_kg, 
                     timestamp, data_source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vehicle_id) DO NOTHING
                """, (
                    row['vehicle_id'],
                    row.get('vehicle_number'),
                    row.get('vehicle_type'),
                    row.get('cargo_type'),
                    row.get('capacity_kg'),
                    row.get('priority'),
                    row.get('operator'),
                    row.get('origin'),
                    row.get('destination'),
                    row.get('current_latitude'),
                    row.get('current_longitude'),
                    row.get('destination_latitude'),
                    row.get('destination_longitude'),
                    row.get('status'),
                    row.get('current_load_kg'),
                    row.get('timestamp'),
                    row.get('data_source', 'DEMO')
                ))
            
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ Loaded {len(vehicles)} vehicles")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error loading vehicles: {e}")
            self.conn.rollback()
            return False
    
    def load_routing(self):
        """Load routing data"""
        logger.info("\n8️⃣ Loading routing data...")
        
        try:
            # Load nodes
            nodes = pd.read_csv('data/processed/routing/routing_nodes.csv')
            cursor = self.conn.cursor()
            
            for idx, row in nodes.iterrows():
                cursor.execute("""
                    INSERT INTO routing_nodes 
                    (node_id, latitude, longitude, geometry)
                    VALUES (%s, %s, %s, ST_GeomFromText(%s, 4326))
                    ON CONFLICT (node_id) DO NOTHING
                """, (
                    row['node_id'],
                    row['latitude'],
                    row['longitude'],
                    f"POINT({row['longitude']} {row['latitude']})"
                ))
            
            self.conn.commit()
            logger.info(f"   ✓ Loaded {len(nodes)} nodes")
            
            # Load edges
            edges = pd.read_csv('data/processed/routing/routing_edges.csv')
            
            for idx, row in edges.iterrows():
                cursor.execute("""
                    INSERT INTO routing_edges 
                    (from_node_id, to_node_id, road_id, distance_m, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    row['from_node_id'],
                    row['to_node_id'],
                    row['road_id'],
                    row['distance_m'],
                    row.get('status', 'OPEN')
                ))
            
            self.conn.commit()
            cursor.close()
            logger.info(f"   ✓ Loaded {len(edges)} edges")
            return True
        except Exception as e:
            logger.error(f"   ✗ Error loading routing: {e}")
            self.conn.rollback()
            return False
    
    def validate_data(self):
        """Validate loaded data"""
        logger.info("\n9️⃣ Validating data...")
        
        try:
            cursor = self.conn.cursor()
            
            # Count records in each table
            tables = ['road_segments', 'terrain', 'weather', 'incidents', 'vehicles', 
                     'routing_nodes', 'routing_edges']
            
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                logger.info(f"   {table}: {count} records")
            
            # Check for orphans
            cursor.execute("""
                SELECT COUNT(*) FROM terrain 
                WHERE road_id NOT IN (SELECT road_id FROM road_segments);
            """)
            orphans = cursor.fetchone()[0]
            if orphans > 0:
                logger.warning(f"   ⚠️ Found {orphans} orphan terrain records")
            else:
                logger.info(f"   ✓ No orphan terrain records")
            
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"   ✗ Validation error: {e}")
            return False
    
    def run(self):
        """Run complete setup and loading"""
        if not self.connect():
            return False
        
        if not self.create_tables():
            return False
        
        if not self.load_roads():
            return False
        
        if not self.load_terrain():
            return False
        
        if not self.load_weather():
            return False
        
        if not self.load_incidents():
            return False
        
        if not self.load_vehicles():
            return False
        
        if not self.load_routing():
            return False
        
        if not self.validate_data():
            return False
        
        logger.info(f"\n" + "=" * 70)
        logger.info(f"✅ DATABASE SETUP & LOADING COMPLETE!")
        logger.info(f"=" * 70)
        
        self.conn.close()
        return True

if __name__ == "__main__":
    loader = SupabaseLoader()
    success = loader.run()
    if success:
        print("\n✅ All data loaded successfully!")
    else:
        print("\n❌ Some errors occurred. Check above.")