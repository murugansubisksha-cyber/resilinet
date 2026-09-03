"""
ResiliNet 2.0 - Demo Vehicle Dataset for Assam Corridor
Routes: Guwahati ↔ Silchar (400 km)
Vehicle types: Medical, relief supplies, emergency
"""

import pandas as pd
import numpy as np
from datetime import datetime

class AssamVehicleGenerator:
    def __init__(self):
        self.demo_vehicles = []
    
    def generate_demo_vehicles(self):
        """
        Generate demo vehicles for Assam Corridor.
        
        Routes: Guwahati ↔ Silchar (400 km highway)
        Vehicle types: Ambulance, supply trucks, emergency vans
        
        ⚠️  ALL VEHICLES ARE SIMULATED DEMO DATA
        """
        
        print("\n" + "=" * 60)
        print("ASSAM CORRIDOR - DEMO VEHICLE GENERATION")
        print("=" * 60)
        print("\n⚠️  NOTE: All vehicles are SIMULATED DEMO DATA\n")
        
        # Assam-specific vehicle profiles
        vehicle_profiles = [
            {
                'name': 'MEDICAL_GUWAHATI_01',
                'vehicle_number': 'AS-01-MD-0001',
                'vehicle_type': 'Ambulance',
                'cargo_type': 'MEDICAL_SUPPLIES',
                'capacity_kg': 500,
                'priority': 'CRITICAL',
                'operator': 'Assam Health Services',
                'base_location': 'Guwahati',
                'destination': 'Silchar',
            },
            {
                'name': 'MEDICAL_SILCHAR_01',
                'vehicle_number': 'AS-24-MD-0002',
                'vehicle_type': 'Ambulance',
                'cargo_type': 'MEDICAL_SUPPLIES',
                'capacity_kg': 500,
                'priority': 'CRITICAL',
                'operator': 'Assam Health Services',
                'base_location': 'Silchar',
                'destination': 'Guwahati',
            },
            {
                'name': 'FOOD_RELIEF_01',
                'vehicle_number': 'AS-01-FR-0001',
                'vehicle_type': 'Truck',
                'cargo_type': 'FOOD_SUPPLIES',
                'capacity_kg': 8000,
                'priority': 'HIGH',
                'operator': 'Assam NDRF & NGOs',
                'base_location': 'Guwahati',
                'destination': 'Lumding',
            },
            {
                'name': 'RELIEF_SUPPLIES_02',
                'vehicle_number': 'AS-26-RS-0002',
                'vehicle_type': 'Truck',
                'cargo_type': 'RELIEF_SUPPLIES',
                'capacity_kg': 10000,
                'priority': 'CRITICAL',
                'operator': 'Assam Disaster Management',
                'base_location': 'Nagaon',
                'destination': 'Silchar',
            },
            {
                'name': 'SUPPLY_CHAIN_03',
                'vehicle_number': 'AS-01-SC-0003',
                'vehicle_type': 'Container Truck',
                'cargo_type': 'ESSENTIALS',
                'capacity_kg': 15000,
                'priority': 'HIGH',
                'operator': 'Assam Logistics',
                'base_location': 'Guwahati',
                'destination': 'Silchar',
            },
            {
                'name': 'EMERGENCY_RESPONSE_01',
                'vehicle_number': 'AS-22-ER-0001',
                'vehicle_type': 'Jeep',
                'cargo_type': 'EMERGENCY_EQUIPMENT',
                'capacity_kg': 1500,
                'priority': 'CRITICAL',
                'operator': 'Assam Police/NDRF',
                'base_location': 'Lumding',
                'destination': 'Silchar',
            },
        ]
        
        # Location coordinates (along corridor)
        location_coords = {
            'Guwahati': (26.18, 91.75),
            'Nagaon': (26.15, 92.72),
            'Lumding': (25.28, 92.84),
            'Silchar': (24.82, 92.80),
        }
        
        vehicles = []
        
        for vehicle in vehicle_profiles:
            base_lat, base_lon = location_coords[vehicle['base_location']]
            dest_lat, dest_lon = location_coords[vehicle['destination']]
            
            # Current position: somewhere between base and destination
            progress = np.random.uniform(0, 0.5)
            curr_lat = base_lat + progress * (dest_lat - base_lat)
            curr_lon = base_lon + progress * (dest_lon - base_lon)
            
            vehicles.append({
                'vehicle_id': vehicle['name'],
                'vehicle_number': vehicle['vehicle_number'],
                'vehicle_type': vehicle['vehicle_type'],
                'cargo_type': vehicle['cargo_type'],
                'capacity_kg': vehicle['capacity_kg'],
                'priority': vehicle['priority'],
                'operator': vehicle['operator'],
                'origin': vehicle['base_location'],
                'destination': vehicle['destination'],
                'current_latitude': curr_lat,
                'current_longitude': curr_lon,
                'destination_latitude': dest_lat,
                'destination_longitude': dest_lon,
                'status': 'IN_TRANSIT',
                'current_load_kg': np.random.randint(int(vehicle['capacity_kg'] * 0.4),
                                                      vehicle['capacity_kg']),
                'timestamp': datetime.now().isoformat(),
                'data_source': 'DEMO',
                'data_note': 'SIMULATED for hackathon demo - Assam Corridor'
            })
        
        self.demo_vehicles = pd.DataFrame(vehicles)
        
        print(f"✓ Generated {len(self.demo_vehicles)} DEMO vehicles\n")
        
        print("Vehicles Summary (DEMO DATA):")
        print("=" * 60)
        print(self.demo_vehicles[['vehicle_id', 'origin', 'destination', 'priority', 'status']])
        
        return self.demo_vehicles
    
    def save(self, output_path='data/processed/vehicles/assam_vehicles.csv'):
        """Save demo vehicles."""
        self.demo_vehicles.to_csv(output_path, index=False)
        self.demo_vehicles.to_json(output_path.replace('.csv', '.json'), orient='records', indent=2)
        
        print(f"\n✓ Saved to:")
        print(f"  - {output_path}")
        print(f"  - {output_path.replace('.csv', '.json')}")
        
        # Print summary
        print(f"\nVehicle breakdown:")
        print(f"  CRITICAL priority: {(self.demo_vehicles['priority'] == 'CRITICAL').sum()}")
        print(f"  HIGH priority: {(self.demo_vehicles['priority'] == 'HIGH').sum()}")
        print(f"  Average load: {self.demo_vehicles['current_load_kg'].mean():.0f} kg")


if __name__ == "__main__":
    generator = AssamVehicleGenerator()
    generator.generate_demo_vehicles()
    generator.save()
    print("\n✓ Vehicle dataset ready")