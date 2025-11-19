"""
IoT Sensor Manager for Real-time Predictive Maintenance
Manages factory sensors with real-time data simulation
"""

import numpy as np
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import threading
import time
import random

class Sensor:
    """Represents an industrial IoT sensor"""
    
    def __init__(
        self,
        sensor_id: str,
        name: str,
        sensor_type: str,
        location: str,
        description: str,
        machine_id: str = "MACHINE-001",
        is_active: bool = True
    ):
        self.sensor_id = sensor_id
        self.name = name
        self.sensor_type = sensor_type
        self.location = location
        self.description = description
        self.machine_id = machine_id
        self.is_active = is_active
        self.current_value = 0.0
        self.status = "normal"  # normal, warning, critical
        self.last_updated = datetime.now(timezone.utc)
        self.history = []
        self.age_percentage = 0  # 0-100, represents sensor degradation/age
        
    def generate_realistic_value(self) -> float:
        """Generate realistic sensor value based on sensor type and age"""
        base_values = {
            'temperature': (50, 90, 5),  # (min, max, std_dev)
            'vibration': (0, 10, 1),
            'pressure': (100, 200, 10),
            'rpm': (1000, 5000, 200),
            'flow_rate': (10, 100, 5),
            'current': (5, 50, 3),
            'voltage': (200, 250, 5),
            'torque': (50, 200, 15)
        }
        
        if self.sensor_type in base_values:
            min_val, max_val, std = base_values[self.sensor_type]
            base_value = (min_val + max_val) / 2
            noise = np.random.normal(0, std)
            
            # Apply age-based degradation (0-100%)
            age_factor = self.age_percentage / 100.0
            degradation = (max_val - min_val) * 0.3 * age_factor  # Up to 30% degradation at 100% age
            
            value = base_value + noise + degradation
            return max(min_val, min(max_val, value))
        return np.random.uniform(0, 100)
    
    def update_reading(self):
        """Update sensor reading"""
        if self.is_active:
            self.current_value = self.generate_realistic_value()
            self.last_updated = datetime.now(timezone.utc)
            
            # Update status based on value and age
            if self.sensor_type == 'temperature':
                if self.current_value > 85 or self.age_percentage > 80:
                    self.status = "critical"
                elif self.current_value > 75 or self.age_percentage > 60:
                    self.status = "warning"
                else:
                    self.status = "normal"
            elif self.sensor_type == 'vibration':
                if self.current_value > 8 or self.age_percentage > 80:
                    self.status = "critical"
                elif self.current_value > 6 or self.age_percentage > 60:
                    self.status = "warning"
                else:
                    self.status = "normal"
            else:
                # Generic status for other sensor types
                if self.age_percentage > 80:
                    self.status = "critical"
                elif self.age_percentage > 60:
                    self.status = "warning"
                else:
                    self.status = "normal"
            
            # Keep last 100 readings
            self.history.append({
                'value': self.current_value,
                'timestamp': self.last_updated.isoformat(),
                'status': self.status
            })
            if len(self.history) > 100:
                self.history.pop(0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sensor to dictionary"""
        return {
            'sensor_id': self.sensor_id,
            'name': self.name,
            'type': self.sensor_type,
            'location': self.location,
            'description': self.description,
            'machine_id': self.machine_id,
            'is_active': self.is_active,
            'current_value': round(self.current_value, 2),
            'status': self.status,
            'age_percentage': self.age_percentage,
            'last_updated': self.last_updated.isoformat(),
            'history': self.history[-20:]  # Last 20 readings
        }


class SensorManager:
    """Manages all factory sensors"""
    
    def __init__(self):
        self.sensors: Dict[str, Sensor] = {}
        self.is_running = False
        self.update_thread = None
        self._initialize_factory_sensors()
        
    def _initialize_factory_sensors(self):
        """Initialize a realistic factory sensor network"""
        
        # Turbofan Engine Sensors - Production Line A
        factory_sensors = [
            {
                'name': 'Core Temperature Sensor',
                'type': 'temperature',
                'location': 'Production Line A - Turbofan Engine #1 - Core Section',
                'description': 'Monitors core engine temperature to prevent overheating and optimize combustion efficiency. Critical for engine safety.',
                'machine_id': 'TURBOFAN-ENGINE-001'
            },
            {
                'name': 'Fan Vibration Monitor',
                'type': 'vibration',
                'location': 'Production Line A - Turbofan Engine #1 - Fan Section',
                'description': 'Detects abnormal vibrations in fan blades indicating bearing wear or imbalance. Early warning system for mechanical failure.',
                'machine_id': 'TURBOFAN-ENGINE-001'
            },
            {
                'name': 'Compressor Pressure Gauge',
                'type': 'pressure',
                'location': 'Production Line A - Turbofan Engine #1 - Compressor',
                'description': 'Measures air pressure in compressor stages. Essential for monitoring engine performance and efficiency.',
                'machine_id': 'TURBOFAN-ENGINE-001'
            },
            {
                'name': 'Turbine RPM Sensor',
                'type': 'rpm',
                'location': 'Production Line A - Turbofan Engine #1 - Turbine Section',
                'description': 'Tracks turbine rotational speed. Critical parameter for power output and operational safety.',
                'machine_id': 'TURBOFAN-ENGINE-001'
            },
            
            # Turbofan Engine #2 - Production Line A
            {
                'name': 'Exhaust Temperature Probe',
                'type': 'temperature',
                'location': 'Production Line A - Turbofan Engine #2 - Exhaust Section',
                'description': 'Monitors exhaust gas temperature for combustion efficiency and turbine health assessment.',
                'machine_id': 'TURBOFAN-ENGINE-002'
            },
            {
                'name': 'Bearing Vibration Sensor',
                'type': 'vibration',
                'location': 'Production Line A - Turbofan Engine #2 - Main Bearings',
                'description': 'Continuous monitoring of bearing vibrations to predict lubrication issues and bearing wear.',
                'machine_id': 'TURBOFAN-ENGINE-002'
            },
            
            # Production Line B - Hydraulic Systems
            {
                'name': 'Hydraulic Pump Temperature',
                'type': 'temperature',
                'location': 'Production Line B - Hydraulic Station #1',
                'description': 'Monitors hydraulic fluid temperature. High temperatures indicate pump stress or cooling system issues.',
                'machine_id': 'HYDRAULIC-PUMP-001'
            },
            {
                'name': 'Hydraulic Pressure Sensor',
                'type': 'pressure',
                'location': 'Production Line B - Hydraulic Station #1',
                'description': 'Measures system pressure to ensure proper operation and detect leaks or pump degradation.',
                'machine_id': 'HYDRAULIC-PUMP-001'
            },
            {
                'name': 'Flow Rate Meter',
                'type': 'flow_rate',
                'location': 'Production Line B - Hydraulic Station #2',
                'description': 'Tracks hydraulic fluid flow rate. Deviations indicate blockages or pump efficiency loss.',
                'machine_id': 'HYDRAULIC-PUMP-002'
            },
            
            # Production Line C - Electric Motors
            {
                'name': 'Motor Current Sensor',
                'type': 'current',
                'location': 'Production Line C - Assembly Motor #1',
                'description': 'Monitors electrical current draw. Abnormal current indicates mechanical load issues or electrical faults.',
                'machine_id': 'MOTOR-001'
            },
            {
                'name': 'Motor Voltage Monitor',
                'type': 'voltage',
                'location': 'Production Line C - Assembly Motor #1',
                'description': 'Tracks supply voltage stability. Voltage fluctuations can damage motor windings.',
                'machine_id': 'MOTOR-001'
            },
            {
                'name': 'Motor Torque Sensor',
                'type': 'torque',
                'location': 'Production Line C - Assembly Motor #2',
                'description': 'Measures output torque for performance monitoring and load analysis.',
                'machine_id': 'MOTOR-002'
            },
            
            # Quality Control Station
            {
                'name': 'Spindle Temperature',
                'type': 'temperature',
                'location': 'Quality Control - CNC Machine #1',
                'description': 'Monitors spindle temperature during precision machining operations. Overheating affects part quality.',
                'machine_id': 'CNC-001'
            },
            {
                'name': 'Spindle Vibration',
                'type': 'vibration',
                'location': 'Quality Control - CNC Machine #1',
                'description': 'Detects tool wear and spindle bearing condition. Critical for maintaining machining precision.',
                'machine_id': 'CNC-001'
            },
            
            # Cooling System
            {
                'name': 'Coolant Temperature',
                'type': 'temperature',
                'location': 'Central Cooling System - Chiller Unit #1',
                'description': 'Monitors coolant temperature for entire production facility. Essential for process stability.',
                'machine_id': 'CHILLER-001'
            },
            {
                'name': 'Coolant Flow Meter',
                'type': 'flow_rate',
                'location': 'Central Cooling System - Distribution Network',
                'description': 'Tracks coolant circulation rate. Low flow indicates pump issues or blockages.',
                'machine_id': 'CHILLER-001'
            },
        ]
        
        # Create sensor objects
        for sensor_config in factory_sensors:
            sensor_id = str(uuid.uuid4())[:8]
            sensor = Sensor(
                sensor_id=sensor_id,
                name=sensor_config['name'],
                sensor_type=sensor_config['type'],
                location=sensor_config['location'],
                description=sensor_config['description'],
                machine_id=sensor_config['machine_id'],
                is_active=random.choice([True, True, True, False])  # Most sensors active
            )
            sensor.update_reading()
            self.sensors[sensor_id] = sensor
    
    def start_real_time_updates(self, interval: float = 2.0):
        """Start real-time sensor data updates"""
        if self.is_running:
            return
        
        self.is_running = True
        
        def update_loop():
            while self.is_running:
                for sensor in self.sensors.values():
                    if sensor.is_active:
                        sensor.update_reading()
                time.sleep(interval)
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def stop_real_time_updates(self):
        """Stop real-time sensor updates"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=5)
    
    def get_all_sensors(self) -> List[Dict[str, Any]]:
        """Get all sensors"""
        return [sensor.to_dict() for sensor in self.sensors.values()]
    
    def get_sensor(self, sensor_id: str) -> Optional[Dict[str, Any]]:
        """Get specific sensor"""
        sensor = self.sensors.get(sensor_id)
        return sensor.to_dict() if sensor else None
    
    def toggle_sensor(self, sensor_id: str, is_active: bool) -> bool:
        """Toggle sensor active state"""
        if sensor_id in self.sensors:
            self.sensors[sensor_id].is_active = is_active
            if not is_active:
                self.sensors[sensor_id].status = "offline"
            return True
        return False
    
    def set_sensor_age(self, sensor_id: str, age_percentage: int) -> bool:
        """Set sensor age/degradation percentage (0-100)"""
        if sensor_id in self.sensors and 0 <= age_percentage <= 100:
            self.sensors[sensor_id].age_percentage = age_percentage
            # Force update to reflect new age
            if self.sensors[sensor_id].is_active:
                self.sensors[sensor_id].update_reading()
            return True
        return False
    
    def get_active_sensors(self) -> List[Dict[str, Any]]:
        """Get only active sensors"""
        return [s.to_dict() for s in self.sensors.values() if s.is_active]
    
    def get_sensor_data_for_prediction(self) -> np.ndarray:
        """
        Get aggregated sensor data formatted for AI prediction
        Returns 24-dimensional feature vector based on ACTUAL sensor readings
        Critical sensors produce HIGH values that indicate imminent failure
        """
        active_sensors = [s for s in self.sensors.values() if s.is_active]
        
        if not active_sensors:
            # Return default values if no sensors active
            return np.random.normal(0, 1, 24)
        
        # Aggregate REAL sensor readings into 24 features
        # This simulates the turbofan dataset structure (3 settings + 21 sensors)
        features = []
        
        # Operational settings (3) - derived from sensor states
        avg_age = np.mean([s.age_percentage for s in active_sensors])
        critical_count = len([s for s in active_sensors if s.status == 'critical'])
        warning_count = len([s for s in active_sensors if s.status == 'warning'])
        avg_value = np.mean([s.current_value for s in active_sensors])
        
        # More aggressive normalization for critical states
        # Critical sensors should produce values that trigger low RUL predictions
        critical_factor = critical_count / max(len(active_sensors), 1)
        warning_factor = warning_count / max(len(active_sensors), 1)
        
        # Normalize settings to emphasize critical conditions
        features.extend([
            (avg_age - 50) / 50 + critical_factor * 2,  # Age setting - boost with critical count
            (critical_count - 2) / 2 + critical_factor * 3,  # Risk setting - heavily weighted
            (avg_value - 100) / 100 + (critical_factor + warning_factor) * 1.5  # Performance setting
        ])
        
        # Sensor values (21) - use ACTUAL sensor readings with critical amplification
        sensor_values = []
        for sensor in active_sensors:
            # Base normalization
            if sensor.sensor_type == 'temperature':
                normalized = (sensor.current_value - 70) / 20  # Center at 70°C
            elif sensor.sensor_type == 'vibration':
                normalized = (sensor.current_value - 5) / 5  # Center at 5
            elif sensor.sensor_type == 'pressure':
                normalized = (sensor.current_value - 150) / 50  # Center at 150
            elif sensor.sensor_type == 'rpm':
                normalized = (sensor.current_value - 3000) / 2000  # Center at 3000
            elif sensor.sensor_type == 'flow_rate':
                normalized = (sensor.current_value - 55) / 45  # Center at 55
            elif sensor.sensor_type == 'current':
                normalized = (sensor.current_value - 27.5) / 22.5  # Center at 27.5
            elif sensor.sensor_type == 'voltage':
                normalized = (sensor.current_value - 225) / 25  # Center at 225
            elif sensor.sensor_type == 'torque':
                normalized = (sensor.current_value - 125) / 75  # Center at 125
            else:
                normalized = (sensor.current_value - 50) / 50
            
            # Amplify critical and warning sensors to trigger model predictions
            if sensor.status == 'critical':
                normalized = normalized * 2.5 + 1.5  # Strong signal for failure
            elif sensor.status == 'warning':
                normalized = normalized * 1.5 + 0.5  # Moderate signal for degradation
            
            sensor_values.append(normalized)
        
        # Pad or trim to exactly 21 values
        while len(sensor_values) < 21:
            # If mostly critical, add high variance noise
            if critical_factor > 0.5:
                sensor_values.append(np.random.normal(1.0, 0.5))
            else:
                sensor_values.append(np.random.normal(0, 0.1))
        
        features.extend(sensor_values[:21])
        
        return np.array(features[:24])
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get sensor network statistics"""
        total = len(self.sensors)
        active = len([s for s in self.sensors.values() if s.is_active])
        critical = len([s for s in self.sensors.values() if s.status == "critical"])
        warning = len([s for s in self.sensors.values() if s.status == "warning"])
        
        return {
            'total_sensors': total,
            'active_sensors': active,
            'inactive_sensors': total - active,
            'critical_sensors': critical,
            'warning_sensors': warning,
            'normal_sensors': total - critical - warning,
            'health_score': round((active / total) * 100, 1) if total > 0 else 0
        }


# Global sensor manager instance
_sensor_manager_instance = None

def get_sensor_manager() -> SensorManager:
    """Get or create global sensor manager instance"""
    global _sensor_manager_instance
    if _sensor_manager_instance is None:
        _sensor_manager_instance = SensorManager()
        _sensor_manager_instance.start_real_time_updates(interval=2.0)
    return _sensor_manager_instance
