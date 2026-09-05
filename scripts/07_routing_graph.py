"""
ResiliNet 2.0 - Routing Graph Generation
Creates node-edge graph for pathfinding algorithms

INPUT: roads.csv, roads.geojson
OUTPUT: routing_edges.csv, routing_nodes.csv
TIME: ~5 minutes
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import logging
from pathlib import Path
from shapely.geometry import Point

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_coordinates_from_linestring(geom_str):
    """Extract all coordinates from LINESTRING"""
    try:
        coords_str = geom_str.split('(')[1].split(')')[0]
        coords = []
        for coord_pair in coords_str.split(','):
            lon, lat = map(float, coord_pair.strip().split())
            coords.append((lat, lon))
        return coords
    except:
        return []

def create_routing_graph():
    """Generate routing graph (nodes and edges)"""
    
    logger.info("=" * 70)
    logger.info("ROUTING GRAPH GENERATION")
    logger.info("=" * 70)
    
    # Load roads
    logger.info("\n1️⃣ Loading roads data...")
    roads = pd.read_csv('data/processed/roads/roads.csv')
    logger.info(f"   ✓ Loaded {len(roads)} roads")
    
    # Extract all nodes
    logger.info("\n2️⃣ Extracting nodes from roads...")
    
    nodes_dict = {}
    node_id_counter = 1000
    
    for idx, road in roads.iterrows():
        coords = extract_coordinates_from_linestring(road['geometry'])
        
        if len(coords) < 2:
            continue
        
        # Add start and end nodes
        for coord in [coords[0], coords[-1]]:
            lat, lon = coord
            node_key = (round(lat, 4), round(lon, 4))  # Round to avoid duplicates
            
            if node_key not in nodes_dict:
                nodes_dict[node_key] = {
                    'node_id': f'N{node_id_counter:06d}',
                    'latitude': lat,
                    'longitude': lon
                }
                node_id_counter += 1
    
    logger.info(f"   ✓ Created {len(nodes_dict)} unique nodes")
    
    # Create nodes dataframe
    nodes_df = pd.DataFrame([
        {'node_id': v['node_id'], 'latitude': v['latitude'], 'longitude': v['longitude']}
        for v in nodes_dict.values()
    ])
    
    # Create node lookup
    node_lookup = {k: v['node_id'] for k, v in nodes_dict.items()}
    
    # Create edges
    logger.info("\n3️⃣ Creating edges from roads...")
    
    edges_list = []
    edge_id = 1
    
    for idx, road in roads.iterrows():
        coords = extract_coordinates_from_linestring(road['geometry'])
        
        if len(coords) < 2:
            continue
        
        # Get start and end nodes
        start_coord = coords[0]
        end_coord = coords[-1]
        
        start_key = (round(start_coord[0], 4), round(start_coord[1], 4))
        end_key = (round(end_coord[0], 4), round(end_coord[1], 4))
        
        if start_key not in node_lookup or end_key not in node_lookup:
            continue
        
        from_node_id = node_lookup[start_key]
        to_node_id = node_lookup[end_key]
        
        # Calculate distance
        distance_m = road['length_km'] * 1000
        
        # Create edges (bidirectional for roads)
        edge1 = {
            'edge_id': edge_id,
            'from_node_id': from_node_id,
            'to_node_id': to_node_id,
            'road_id': road['road_id'],
            'distance_m': distance_m,
            'status': 'OPEN'
        }
        
        edge2 = {
            'edge_id': edge_id + 1,
            'from_node_id': to_node_id,
            'to_node_id': from_node_id,
            'road_id': road['road_id'],
            'distance_m': distance_m,
            'status': 'OPEN'
        }
        
        edges_list.append(edge1)
        edges_list.append(edge2)
        edge_id += 2
    
    edges_df = pd.DataFrame(edges_list)
    
    logger.info(f"   ✓ Created {len(edges_df)} edges")
    logger.info(f"     (bidirectional: each road = 2 edges)")
    
    # Summary
    logger.info("\n4️⃣ Graph summary...")
    logger.info(f"   Total nodes: {len(nodes_df)}")
    logger.info(f"   Total edges: {len(edges_df)}")
    logger.info(f"   Connected roads: {edges_df['road_id'].nunique()}")
    logger.info(f"   Total distance: {edges_df['distance_m'].sum() / 1000:.0f} km")
    
    # Save outputs
    logger.info("\n5️⃣ Saving routing graph...")
    
    Path('data/processed/routing').mkdir(parents=True, exist_ok=True)
    
    nodes_path = 'data/processed/routing/routing_nodes.csv'
    edges_path = 'data/processed/routing/routing_edges.csv'
    
    nodes_df.to_csv(nodes_path, index=False)
    edges_df.to_csv(edges_path, index=False)
    
    logger.info(f"   ✓ Saved: {nodes_path}")
    logger.info(f"   ✓ Saved: {edges_path}")
    
    logger.info(f"\n" + "=" * 70)
    logger.info(f"✅ ROUTING GRAPH GENERATION COMPLETE!")
    logger.info(f"=" * 70)
    logger.info(f"\n📊 Summary:")
    logger.info(f"   Nodes: {len(nodes_df)}")
    logger.info(f"   Edges: {len(edges_df)}")
    logger.info(f"   Network: Complete bidirectional graph")
    logger.info(f"\n📁 Outputs:")
    logger.info(f"   {nodes_path}")
    logger.info(f"   {edges_path}")
    
    return nodes_df, edges_df

if __name__ == "__main__":
    create_routing_graph()
    print("\n✅ Done! Ready for database setup.")