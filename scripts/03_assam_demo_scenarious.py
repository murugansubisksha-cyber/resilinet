"""
ResiliNet 2.0 - Demo Scenarios for Assam Corridor
Three baseline scenarios:
1. NORMAL (88% accessibility)
2. HEAVY_MONSOON (62% accessibility)
3. EXTREME_LANDSLIDE (38% accessibility)
"""

import json
from datetime import datetime

class AssamDemoScenarioGenerator:
    """
    Demo scenarios for Assam Corridor (Guwahati–Silchar).
    """
    
    def scenario_normal(self):
        """SCENARIO 1: NORMAL CONDITIONS"""
        
        print("\n[SCENARIO 1] NORMAL - Winter/Dry Season")
        print("=" * 50)
        
        scenario = {
            'scenario_id': 'ASSAM_NORMAL_001',
            'scenario_name': 'Normal Conditions - Dry Season',
            'corridor': 'Guwahati–Silchar (400 km)',
            'timestamp': datetime.now().isoformat(),
            'season': 'Winter/Dry (Feb-Mar or Nov)',
            'weather': {
                'rainfall_mm': 35,
                'temperature_c': 24,
                'humidity_percent': 65,
                'wind_speed_kmh': 10,
                'condition': 'Clear to partly cloudy',
            },
            'road_conditions': {
                'total_roads': 12500,
                'roads_open': 12500,
                'roads_blocked': 0,
                'roads_degraded': 0,
                'status': {
                    'OPEN': 12500,
                    'DEGRADED': 0,
                    'BLOCKED': 0
                }
            },
            'accessibility': {
                'network_accessibility_percent': 88,
                'avg_delay_multiplier': 1.0,
                'note': 'Full network operational, normal travel times'
            },
            'vehicles': {
                'all_operational': True,
                'restrictions': None
            },
            'risk': {
                'overall': 'LOW',
                'landslide': 'LOW',
                'flood': 'LOW',
            },
            'data_source': 'DEMO',
            'data_note': 'SIMULATED for hackathon demo'
        }
        
        print(f"✓ Accessibility: {scenario['accessibility']['network_accessibility_percent']}%")
        print(f"✓ Rainfall: {scenario['weather']['rainfall_mm']} mm")
        print(f"✓ Risk: {scenario['risk']['overall']}")
        
        return scenario
    
    def scenario_heavy_monsoon(self):
        """SCENARIO 2: HEAVY MONSOON"""
        
        print("\n[SCENARIO 2] HEAVY MONSOON - Peak Season")
        print("=" * 50)
        
        scenario = {
            'scenario_id': 'ASSAM_MONSOON_001',
            'scenario_name': 'Heavy Monsoon Rainfall',
            'corridor': 'Guwahati–Silchar (400 km)',
            'timestamp': datetime.now().isoformat(),
            'season': 'Peak Monsoon (Jul-Aug)',
            'weather': {
                'rainfall_mm': 230,
                'temperature_c': 25,
                'humidity_percent': 92,
                'wind_speed_kmh': 40,
                'condition': 'Heavy rain, strong wind, poor visibility',
                'advisory': 'Extreme weather alert'
            },
            'affected_segments': {
                'guwahati_nagaon': {
                    'distance_km': 120,
                    'status': 'DEGRADED',
                    'reason': 'Hill terrain, landslide risk',
                    'affected_roads': '~1200 roads (10%)',
                    'speed_reduction': '35%'
                },
                'nagaon_lumding': {
                    'distance_km': 100,
                    'status': 'DEGRADED',
                    'reason': 'River flooding, waterlogging',
                    'affected_roads': '~800 roads (6%)',
                    'speed_reduction': '40%'
                },
                'lumding_silchar': {
                    'distance_km': 180,
                    'status': 'OPEN',
                    'reason': 'Relatively higher terrain',
                    'affected_roads': '~500 roads (4%)',
                    'speed_reduction': '25%'
                }
            },
            'road_conditions': {
                'total_roads': 12500,
                'roads_open': 10000,
                'roads_blocked': 0,
                'roads_degraded': 2500,
                'status': {
                    'OPEN': 10000,
                    'DEGRADED': 2500,
                    'BLOCKED': 0
                }
            },
            'accessibility': {
                'network_accessibility_percent': 62,
                'avg_delay_multiplier': 1.35,
                'note': 'Major routes open, hill/flood-prone routes degraded',
                'bottlenecks': ['Guwahati–Nagaon transition', 'River crossings near Lumding']
            },
            'vehicles': {
                'all_operational': True,
                'speed_reduction_percent': 30,
                'priority_routing': 'Medical + Emergency vehicles prioritized',
                'restrictions': 'Avoid degraded hill routes where possible'
            },
            'risk': {
                'overall': 'HIGH',
                'landslide': 'MEDIUM',
                'flood': 'HIGH',
                'cascading_risk': 'Secondary landslides possible in steep terrain'
            },
            'critical_routes': [
                'NH37 Guwahati–Nagaon (landslide-prone)',
                'NH6 bridge crossings (flood-prone)',
                'Silchar approach roads'
            ],
            'data_source': 'DEMO',
            'data_note': 'SIMULATED for hackathon demo'
        }
        
        print(f"✓ Accessibility: {scenario['accessibility']['network_accessibility_percent']}%")
        print(f"✓ Rainfall: {scenario['weather']['rainfall_mm']} mm")
        print(f"✓ Degraded roads: {scenario['road_conditions']['roads_degraded']}")
        print(f"✓ Risk: {scenario['risk']['overall']}")
        
        return scenario
    
    def scenario_extreme_monsoon_landslide(self):
        """SCENARIO 3: EXTREME MONSOON + CRITICAL LANDSLIDE"""
        
        print("\n[SCENARIO 3] EXTREME MONSOON + LANDSLIDE EVENT")
        print("=" * 50)
        
        scenario = {
            'scenario_id': 'ASSAM_EXTREME_001',
            'scenario_name': 'Critical Landslide Event During Monsoon',
            'corridor': 'Guwahati–Silchar (400 km)',
            'timestamp': datetime.now().isoformat(),
            'season': 'Extreme Monsoon (Jul)',
            'weather': {
                'rainfall_mm': 320,
                'temperature_c': 24,
                'humidity_percent': 98,
                'wind_speed_kmh': 55,
                'condition': 'Catastrophic rainfall, extreme conditions',
                'advisory': 'CRITICAL WEATHER ALERT - Cascading landslide risk'
            },
            'critical_event': {
                'event_type': 'MAJOR_LANDSLIDE',
                'location': 'NH37 near Karbi Anglong (between Guwahati–Nagaon)',
                'blocked_road_id': 'R3847',
                'blocked_road_name': 'NH37 - Karbi Anglong Section',
                'impact': 'Complete network bifurcation',
                'duration_estimated': '4–8 hours (initial) + recovery'
            },
            'cascading_impacts': {
                'primary_blockage': {
                    'road': 'NH37 (R3847)',
                    'impact': 'North-South corridor severed',
                    'accessibility_loss': '45%'
                },
                'secondary_impacts': {
                    'guwahati_zone': 'Accessible via alternative routes (~20 km detour)',
                    'silchar_zone': 'Accessible via alternative routes (~50 km detour)',
                    'critical_gap': 'No direct NH37 access between zones'
                },
                'tertiary_risks': {
                    'description': 'Secondary slides likely in adjacent areas',
                    'probability': 'HIGH',
                    'additional_closures_expected': '3–5 more roads'
                }
            },
            'road_conditions': {
                'total_roads': 12500,
                'roads_open': 4750,
                'roads_blocked': 1,
                'roads_degraded': 7750,
                'status': {
                    'OPEN': 4750,
                    'DEGRADED': 7750,
                    'BLOCKED': 1
                },
                'critical_blockage': {
                    'road_id': 'R3847',
                    'name': 'NH37 Karbi Anglong',
                    'length_km': 15,
                    'importance': 'CRITICAL'
                }
            },
            'connectivity_analysis': {
                'network_segments': 2,
                'segment_1': {
                    'name': 'Guwahati Zone',
                    'roads': 5200,
                    'accessibility': '41%'
                },
                'segment_2': {
                    'name': 'Silchar Zone',
                    'roads': 3100,
                    'accessibility': '24%'
                },
                'disconnected_roads': 2500,
                'critical_note': 'Two previously-connected zones now isolated'
            },
            'accessibility': {
                'network_accessibility_percent': 38,
                'avg_delay_multiplier': 2.8,
                'note': 'Network fragmented; major blockage requires dynamic rerouting',
                'impact': 'Some routes require 50+ km detours'
            },
            'vehicles': {
                'all_operational': False,
                'vehicles_stranded': 'Vehicles in blocked zone unable to cross',
                'emergency_response': 'Emergency vehicles routed via alternative paths',
                'priority_access': 'Only critical medical/emergency vehicles authorized'
            },
            'routing_impact': {
                'shortest_path': 'Unavailable (NH37 blocked)',
                'detour_distance': '+50–75 km',
                'detour_time': '+2–3 hours',
                'alternative_routes': [
                    'Guwahati → Lumding → Silchar (via Lumding Junction)',
                    'Guwahati → Nagaon → Kaboi → Silchar (longer, steep)'
                ]
            },
            'risk': {
                'overall': 'CRITICAL',
                'landslide': 'CRITICAL',
                'flood': 'HIGH',
                'cascading': 'HIGH',
                'emergency_response': 'Immediate multi-agency coordination required'
            },
            'mitigation_actions': [
                'Block R3847 from all routing algorithms',
                'Activate emergency response protocols (NDRF, district admin)',
                'Deploy rescue teams to NH37 landslide site',
                'Monitor secondary slide zones (Karbi Anglong, Dima Hasao)',
                'Divert traffic via alternative routes',
                'Establish emergency rest stops on detour routes',
                'Coordinate with medical facilities for rerouting ambulances'
            ],
            'recovery_timeline': {
                'phase_1': '0–2 hours: Emergency response deployment',
                'phase_2': '2–6 hours: Debris clearance',
                'phase_3': '6–24 hours: Stabilization + partial clearance',
                'phase_4': '1–3 days: Full restoration if no major damage',
                'worst_case': '1–2 weeks: Road reconstruction (major damage)'
            },
            'data_source': 'DEMO',
            'data_note': 'SIMULATED for hackathon demo - Based on realistic monsoon scenarios'
        }
        
        print(f"✓ Accessibility: {scenario['accessibility']['network_accessibility_percent']}%")
        print(f"✓ Blocked Road: {scenario['critical_event']['blocked_road_id']}")
        print(f"✓ Degraded Roads: {scenario['road_conditions']['roads_degraded']}")
        print(f"✓ Risk: {scenario['risk']['overall']}")
        
        return scenario
    
    def save_all_scenarios(self):
        """Generate and save all three scenarios."""
        
        print("\n" + "=" * 60)
        print("ASSAM CORRIDOR - DEMO SCENARIO GENERATION")
        print("=" * 60)
        print("\n⚠️  IMPORTANT NOTE:")
        print("All scenarios below are SIMULATED for hackathon demo.")
        print("They are NOT real-world data.\n")
        
        normal = self.scenario_normal()
        heavy_monsoon = self.scenario_heavy_monsoon()
        extreme = self.scenario_extreme_monsoon_landslide()
        
        scenarios = {
            'NORMAL': normal,
            'HEAVY_MONSOON': heavy_monsoon,
            'EXTREME_LANDSLIDE': extreme
        }
        
        for name, scenario in scenarios.items():
            filename = f'data/scenarios/assam_{name.lower()}.json'
            with open(filename, 'w') as f:
                json.dump(scenario, f, indent=2)
            print(f"✓ Saved: {filename}")
        
        return scenarios


if __name__ == "__main__":
    generator = AssamDemoScenarioGenerator()
    generator.save_all_scenarios()
    print("\n✓ All demo scenarios created")