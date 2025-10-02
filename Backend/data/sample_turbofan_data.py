"""
Sample NASA Turbofan Engine Dataset Generator
Creates realistic synthetic data for testing and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_sample_dataset(num_engines=10, cycles_per_engine=200):
    """
    Create a comprehensive sample dataset similar to NASA Turbofan data
    
    Args:
        num_engines: Number of different engines to simulate
        cycles_per_engine: Number of operational cycles per engine
    
    Returns:
        DataFrame with complete turbofan engine data
    """
    np.random.seed(42)  # For reproducibility
    
    all_data = []
    
    for engine_id in range(1, num_engines + 1):
        # Each engine has different degradation characteristics
        degradation_rate = np.random.uniform(0.8, 1.2)  # Different degradation speeds
        noise_level = np.random.uniform(0.1, 0.3)       # Different noise levels
        
        for cycle in range(1, cycles_per_engine + 1):
            # Operational settings (flight conditions)
            altitude = np.random.uniform(0, 42000)  # feet
            mach_number = np.random.uniform(0.2, 0.84)
            throttle_resolver_angle = np.random.uniform(20, 25)
            
            # Normalize settings
            setting_1 = (altitude - 21000) / 21000
            setting_2 = (mach_number - 0.52) / 0.32
            setting_3 = (throttle_resolver_angle - 22.5) / 2.5
            
            # Base sensor readings (21 sensors)
            sensors = {}
            
            # Temperature sensors (affected by degradation)
            sensors['sensor_1'] = 518.67 + np.random.normal(0, 1)  # Fan inlet temperature
            sensors['sensor_2'] = 642.35 + degradation_rate * cycle * 0.1 + np.random.normal(0, noise_level)  # LPC outlet temperature
            sensors['sensor_3'] = 1589.70 + degradation_rate * cycle * 0.2 + np.random.normal(0, noise_level)  # HPC outlet temperature
            sensors['sensor_4'] = 1400.60 + degradation_rate * cycle * 0.15 + np.random.normal(0, noise_level)  # LPT outlet temperature
            
            # Pressure sensors
            sensors['sensor_5'] = 14.62 + np.random.normal(0, 0.1)  # Fan inlet pressure
            sensors['sensor_6'] = 21.61 + degradation_rate * cycle * 0.01 + np.random.normal(0, noise_level)  # bypass-duct pressure
            sensors['sensor_7'] = 553.85 + degradation_rate * cycle * 0.5 + np.random.normal(0, noise_level)  # HPC outlet pressure
            
            # Flow and speed sensors
            sensors['sensor_8'] = 2388.02 + np.random.normal(0, 5)  # Physical fan speed
            sensors['sensor_9'] = 9046.19 + np.random.normal(0, 10)  # Physical core speed
            sensors['sensor_10'] = 1.30 + np.random.normal(0, 0.01)  # Engine pressure ratio
            sensors['sensor_11'] = 47.47 + degradation_rate * cycle * 0.02 + np.random.normal(0, noise_level)  # Static pressure at HPC outlet
            
            # Fuel and efficiency sensors
            sensors['sensor_12'] = 521.66 + degradation_rate * cycle * 0.05 + np.random.normal(0, noise_level)  # Ratio of fuel flow to Ps30
            sensors['sensor_13'] = 2388.02 + np.random.normal(0, 5)  # Corrected fan speed
            sensors['sensor_14'] = 8138.62 + np.random.normal(0, 10)  # Corrected core speed
            sensors['sensor_15'] = 8.4195 + degradation_rate * cycle * 0.001 + np.random.normal(0, noise_level)  # Bypass Ratio
            
            # Additional operational sensors
            sensors['sensor_16'] = 0.03 + np.random.normal(0, 0.001)  # Burner fuel-air ratio
            sensors['sensor_17'] = 392.0 + degradation_rate * cycle * 0.1 + np.random.normal(0, noise_level)  # Bleed Enthalpy
            sensors['sensor_18'] = 2388.0 + np.random.normal(0, 5)  # Required fan speed
            sensors['sensor_19'] = 100.0 + np.random.normal(0, 1)  # Required fan conversion speed
            sensors['sensor_20'] = 38.86 + degradation_rate * cycle * 0.02 + np.random.normal(0, noise_level)  # High-pressure turbine coolant bleed
            sensors['sensor_21'] = 23.419 + degradation_rate * cycle * 0.01 + np.random.normal(0, noise_level)  # Low-pressure turbine coolant bleed
            
            # Add operational setting influences
            for sensor_key in sensors:
                sensors[sensor_key] += 0.1 * setting_1 + 0.05 * setting_2 + 0.02 * setting_3
            
            # Calculate RUL (Remaining Useful Life)
            max_cycles = cycles_per_engine
            rul = max(1, max_cycles - cycle + np.random.normal(0, 5))
            
            # Determine failure modes based on sensor patterns
            failure_mode = 'normal'
            if sensors['sensor_2'] > 650 or sensors['sensor_3'] > 1600:
                failure_mode = 'overheating'
            elif sensors['sensor_7'] < 500 or sensors['sensor_11'] < 45:
                failure_mode = 'pressure_drop'
            elif abs(sensors['sensor_8'] - 2388) > 50 or abs(sensors['sensor_9'] - 9046) > 100:
                failure_mode = 'speed_deviation'
            
            # Create data row
            row = {
                'engine_id': f'ENGINE-{engine_id:03d}',
                'cycle': cycle,
                'setting_1': setting_1,
                'setting_2': setting_2,
                'setting_3': setting_3,
                **sensors,
                'rul': rul,
                'failure_mode': failure_mode,
                'timestamp': datetime.now() - timedelta(days=30) + timedelta(hours=cycle)
            }
            
            all_data.append(row)
    
    return pd.DataFrame(all_data)

def save_sample_datasets():
    """Save sample datasets in different formats"""
    
    # Create data directory if it doesn't exist
    os.makedirs('sample_datasets', exist_ok=True)
    
    # Generate different sized datasets
    datasets = {
        'small': {'engines': 5, 'cycles': 100},
        'medium': {'engines': 20, 'cycles': 200},
        'large': {'engines': 50, 'cycles': 300}
    }
    
    for size, params in datasets.items():
        print(f"Generating {size} dataset...")
        df = create_sample_dataset(params['engines'], params['cycles'])
        
        # Save as CSV
        csv_path = f'sample_datasets/turbofan_data_{size}.csv'
        df.to_csv(csv_path, index=False)
        print(f"Saved {csv_path} ({len(df)} rows)")
        
        # Save training/test split
        train_df = df.sample(frac=0.8, random_state=42)
        test_df = df.drop(train_df.index)
        
        train_df.to_csv(f'sample_datasets/turbofan_train_{size}.csv', index=False)
        test_df.to_csv(f'sample_datasets/turbofan_test_{size}.csv', index=False)
        
        print(f"Saved train/test split: {len(train_df)} train, {len(test_df)} test samples")

def get_data_description():
    """Get description of the dataset features"""
    return {
        'operational_settings': {
            'setting_1': 'Normalized altitude (flight condition)',
            'setting_2': 'Normalized Mach number (flight condition)', 
            'setting_3': 'Normalized throttle resolver angle (flight condition)'
        },
        'sensors': {
            'sensor_1': 'Fan inlet temperature (°R)',
            'sensor_2': 'LPC outlet temperature (°R)',
            'sensor_3': 'HPC outlet temperature (°R)',
            'sensor_4': 'LPT outlet temperature (°R)',
            'sensor_5': 'Fan inlet pressure (psia)',
            'sensor_6': 'Bypass-duct pressure (psia)',
            'sensor_7': 'HPC outlet pressure (psia)',
            'sensor_8': 'Physical fan speed (rpm)',
            'sensor_9': 'Physical core speed (rpm)',
            'sensor_10': 'Engine pressure ratio (P50/P2)',
            'sensor_11': 'Static pressure at HPC outlet (psia)',
            'sensor_12': 'Ratio of fuel flow to Ps30 (pps/psia)',
            'sensor_13': 'Corrected fan speed (rpm)',
            'sensor_14': 'Corrected core speed (rpm)',
            'sensor_15': 'Bypass Ratio',
            'sensor_16': 'Burner fuel-air ratio',
            'sensor_17': 'Bleed Enthalpy',
            'sensor_18': 'Required fan speed (rpm)',
            'sensor_19': 'Required fan conversion speed (rpm)',
            'sensor_20': 'High-pressure turbine coolant bleed (lbm/s)',
            'sensor_21': 'Low-pressure turbine coolant bleed (lbm/s)'
        },
        'targets': {
            'rul': 'Remaining Useful Life (cycles)',
            'failure_mode': 'Type of failure (normal, overheating, pressure_drop, speed_deviation)'
        },
        'metadata': {
            'engine_id': 'Unique engine identifier',
            'cycle': 'Operational cycle number',
            'timestamp': 'Data collection timestamp'
        }
    }

if __name__ == "__main__":
    print("Creating sample NASA Turbofan datasets...")
    save_sample_datasets()
    
    print("\nDataset description:")
    description = get_data_description()
    for category, features in description.items():
        print(f"\n{category.upper()}:")
        for feature, desc in features.items():
            print(f"  {feature}: {desc}")
    
    print("\nSample datasets created successfully!")
