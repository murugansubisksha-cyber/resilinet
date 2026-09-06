"""
ResiliNet 2.0 - Weather Data Processing for Assam Corridor
Locations: Guwahati, Nagaon, Lumding, Silchar
Monsoon pattern: Jun-Sep peak rainfall
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AssamWeatherProcessor:
    def __init__(self):
        self.historical = None
        self.demo = None
    
    def create_historical_weather(self):
        """
        Historical weather for Assam Corridor.
        
        Key characteristics:
        - Pre-monsoon (Mar-May): Hot, dry, occasional showers
        - Monsoon (Jun-Sep): Heavy rainfall (200-400mm/month), HIGHEST RISK
        - Post-monsoon (Oct-Nov): Moderate rainfall, declining
        - Winter (Dec-Feb): Cold, dry
        """
        
        print("Creating Assam Corridor historical weather...")
        print("Generating 1 year of data (2023) for 4 locations\n")
        
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        
        # Multiple locations along corridor
        locations = [
            {
                'name': 'Guwahati',
                'lat': 26.18,
                'lon': 91.75,
                'base_rainfall_monsoon': 180,
                'base_rainfall_dry': 15
            },
            {
                'name': 'Nagaon',
                'lat': 26.15,
                'lon': 92.72,
                'base_rainfall_monsoon': 200,
                'base_rainfall_dry': 20
            },
            {
                'name': 'Lumding',
                'lat': 25.28,
                'lon': 92.84,
                'base_rainfall_monsoon': 220,
                'base_rainfall_dry': 25
            },
            {
                'name': 'Silchar',
                'lat': 24.82,
                'lon': 92.80,
                'base_rainfall_monsoon': 250,
                'base_rainfall_dry': 30
            }
        ]
        
        weather_data = []
        
        for date in dates:
            month = date.month
            
            # Assam monsoon pattern
            if month in [6, 7, 8, 9]:
                rainfall_type = 'HEAVY_MONSOON'
                temp_base = 25
            elif month in [5, 10]:
                rainfall_type = 'MODERATE'
                temp_base = 28
            elif month in [3, 4]:
                rainfall_type = 'PRE_MONSOON'
                temp_base = 32
            else:
                rainfall_type = 'DRY'
                temp_base = 20
            
            for loc in locations:
                if rainfall_type == 'HEAVY_MONSOON':
                    rainfall = loc['base_rainfall_monsoon'] + np.random.normal(0, 40)
                elif rainfall_type == 'MODERATE':
                    rainfall = 80 + np.random.normal(0, 20)
                elif rainfall_type == 'PRE_MONSOON':
                    rainfall = 50 + np.random.normal(0, 20)
                else:
                    rainfall = loc['base_rainfall_dry'] + np.random.normal(0, 10)
                
                rainfall = max(0, rainfall)
                
                weather_data.append({
                    'timestamp': date.isoformat(),
                    'location': loc['name'],
                    'latitude': loc['lat'],
                    'longitude': loc['lon'],
                    'rainfall_mm': rainfall,
                    'temperature_c': temp_base + np.random.normal(0, 2),
                    'humidity_percent': np.random.uniform(65, 95),
                    'wind_speed_kmh': np.random.uniform(8, 30),
                    'season': rainfall_type,
                    'data_source': 'HISTORICAL'
                })
        
        self.historical = pd.DataFrame(weather_data)
        print(f"✓ Created {len(self.historical)} historical weather records")
        print(f"  Locations: {len(locations)} weather stations")
        print(f"  Period: Jan 2023 - Dec 2023")
        print(f"  ⚠️  Monsoon months (Jun-Sep): High rainfall + landslide risk\n")
        
        return self.historical
    
    def create_demo_weather(self):
        """
        Demo scenarios for Assam Corridor.
        
        Three baseline scenarios:
        1. NORMAL (winter/dry season) - 88% accessibility
        2. HEAVY_MONSOON (peak monsoon) - 62% accessibility
        3. EXTREME_MONSOON (catastrophic event) - 38% accessibility
        """
        
        print("Creating Assam Corridor demo weather scenarios...")
        
        demo_scenarios = [
            {
                'scenario': 'NORMAL',
                'timestamp': '2024-02-15T12:00:00',
                'rainfall_mm': 35,
                'temperature_c': 24,
                'season': 'DRY',
                'note': 'Clear weather, dry season conditions'
            },
            {
                'scenario': 'HEAVY_MONSOON',
                'timestamp': '2024-08-15T14:00:00',
                'rainfall_mm': 220,
                'temperature_c': 25,
                'season': 'MONSOON',
                'note': 'Peak monsoon (Aug), sustained heavy rainfall'
            },
            {
                'scenario': 'EXTREME_MONSOON',
                'timestamp': '2024-07-20T10:00:00',
                'rainfall_mm': 320,
                'temperature_c': 24,
                'season': 'MONSOON',
                'note': 'Extreme event: catastrophic rainfall + landslides'
            }
        ]
        
        locations = ['Guwahati', 'Nagaon', 'Lumding', 'Silchar']
        
        demo_data = []
        
        for scenario in demo_scenarios:
            for loc in locations:
                demo_data.append({
                    'scenario': scenario['scenario'],
                    'timestamp': scenario['timestamp'],
                    'location': loc,
                    'rainfall_mm': scenario['rainfall_mm'],
                    'temperature_c': scenario['temperature_c'],
                    'season': scenario['season'],
                    'data_source': 'DEMO',
                    'note': scenario['note']
                })
        
        self.demo = pd.DataFrame(demo_data)
        print(f"✓ Created {len(self.demo)} demo scenario records")
        print(f"  Scenarios: NORMAL, HEAVY_MONSOON, EXTREME_MONSOON")
        print(f"  Locations: {len(locations)} stations\n")
        
        return self.demo
    
    def combine_and_save(self):
        """Combine both sources, keeping them clearly separated."""
        
        # Add missing columns to match
        hist = self.historical.copy()
        hist['scenario'] = 'HISTORICAL'
        hist['note'] = 'Historical data'
        
        demo = self.demo.copy()
        demo['humidity_percent'] = np.random.uniform(60, 85, len(demo))
        demo['wind_speed_kmh'] = np.random.uniform(8, 20, len(demo))
        
        # Combine
        combined = pd.concat([hist, demo], ignore_index=True)
        
        # Save
        combined.to_csv('data/processed/weather/assam_weather.csv', index=False)
        print(f"✓ Saved combined weather data ({len(combined)} records)")
        
        # Summary
        print(f"\nWeather data summary:")
        print(combined['data_source'].value_counts())
        print(f"\nSeason breakdown:")
        print(combined['season'].value_counts())
        
        return combined


if __name__ == "__main__":
    processor = AssamWeatherProcessor()
    processor.create_historical_weather()
    processor.create_demo_weather()
    processor.combine_and_save()
    print("\n✓ Weather data ready for next step")