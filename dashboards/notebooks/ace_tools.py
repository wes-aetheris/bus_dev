"""
Watchtower ACE (Analysis and Computation Engine) Tools

This module provides utilities for connecting to the Watchtower API
and processing drone sensor data in Jupyter notebooks.
"""

import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

class WatchtowerAPI:
    """Client for Watchtower API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_sensor_status(self) -> Dict[str, Any]:
        """Get current sensor status"""
        response = self.session.get(f"{self.base_url}/api/sensors/status")
        return response.json()
    
    def get_dashboard_data(self, tab_id: str) -> Dict[str, Any]:
        """Get dashboard data for a specific tab"""
        response = self.session.get(f"{self.base_url}/api/dashboard/{tab_id}")
        return response.json()
    
    def upload_sensor_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Upload sensor data"""
        response = self.session.post(f"{self.base_url}/api/sensors/upload", json=data)
        return response.json()
    
    def get_anomalies(self, threshold: float = 2.0) -> Dict[str, Any]:
        """Get detected anomalies"""
        response = self.session.get(f"{self.base_url}/api/sensors/anomalies", params={"threshold": threshold})
        return response.json()
    
    def get_physics_metrics(self) -> Dict[str, Any]:
        """Get physics-based metrics"""
        response = self.session.get(f"{self.base_url}/api/sensors/physics-metrics")
        return response.json()

class SensorDataProcessor:
    """Process and analyze sensor data"""
    
    def __init__(self):
        self.data = None
        self.processed_data = None
    
    def load_data(self, data: pd.DataFrame):
        """Load sensor data"""
        self.data = data
        self.processed_data = data.copy()
    
    def detect_anomalies(self, columns: List[str], threshold: float = 3.0) -> Dict[str, pd.DataFrame]:
        """Detect anomalies using z-score method"""
        anomalies = {}
        
        for col in columns:
            if col in self.data.columns:
                z_scores = np.abs(stats.zscore(self.data[col].dropna()))
                anomaly_indices = z_scores > threshold
                anomalies[col] = self.data[anomaly_indices]
        
        return anomalies
    
    def calculate_velocity(self, lat_col: str = 'latitude', lon_col: str = 'longitude', 
                          time_col: str = 'timestamp') -> pd.Series:
        """Calculate velocity from GPS coordinates"""
        if not all(col in self.data.columns for col in [lat_col, lon_col, time_col]):
            raise ValueError("Required columns not found in data")
        
        # Convert lat/lon to meters (approximate)
        lat_meters = (self.data[lat_col] - self.data[lat_col].iloc[0]) * 111000
        lon_meters = (self.data[lon_col] - self.data[lon_col].iloc[0]) * 111000 * np.cos(np.radians(self.data[lat_col].iloc[0]))
        
        # Calculate velocity
        time_diff = (self.data[time_col] - self.data[time_col].iloc[0]).dt.total_seconds()
        velocity = np.sqrt(lat_meters.diff()**2 + lon_meters.diff()**2) / time_diff.diff()
        
        return velocity
    
    def calculate_acceleration(self, velocity: pd.Series) -> pd.Series:
        """Calculate acceleration from velocity"""
        return velocity.diff()
    
    def calculate_flight_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive flight metrics"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        # Basic metrics
        flight_duration = (self.data['timestamp'].max() - self.data['timestamp'].min()).total_seconds() / 60
        
        # Calculate velocity if possible
        try:
            velocity = self.calculate_velocity()
            avg_speed = velocity.mean()
            max_speed = velocity.max()
            total_distance = velocity.sum() * 10  # Approximate
        except:
            avg_speed = max_speed = total_distance = 0
        
        # Battery metrics
        if 'battery_level' in self.data.columns:
            battery_efficiency = (self.data['battery_level'].iloc[0] - self.data['battery_level'].iloc[-1]) / flight_duration
        else:
            battery_efficiency = 0
        
        # Stability metrics
        if 'roll' in self.data.columns and 'pitch' in self.data.columns:
            stability_score = 1 - (self.data['roll'].std() + self.data['pitch'].std()) / 10
        else:
            stability_score = 0
        
        return {
            'flight_duration_minutes': flight_duration,
            'total_distance_meters': total_distance,
            'average_speed_mps': avg_speed,
            'max_speed_mps': max_speed,
            'max_altitude_meters': self.data['altitude'].max() if 'altitude' in self.data.columns else 0,
            'battery_efficiency_percent_per_minute': battery_efficiency,
            'stability_score': stability_score
        }
    
    def create_flight_path_plot(self, lat_col: str = 'latitude', lon_col: str = 'longitude',
                               color_col: str = 'altitude', size_col: str = 'battery_level') -> go.Figure:
        """Create interactive flight path visualization"""
        fig = px.scatter_mapbox(
            self.data,
            lat=lat_col,
            lon=lon_col,
            color=color_col,
            size=size_col,
            hover_data=['timestamp', 'roll', 'pitch', 'yaw'],
            title='Drone Flight Path',
            mapbox_style='open-street-map'
        )
        
        fig.update_layout(
            mapbox=dict(
                center=dict(lat=self.data[lat_col].mean(), lon=self.data[lon_col].mean()),
                zoom=15
            ),
            height=600
        )
        
        return fig
    
    def create_time_series_plots(self, columns: List[str]) -> go.Figure:
        """Create time series plots for multiple columns"""
        fig = go.Figure()
        
        for col in columns:
            if col in self.data.columns:
                fig.add_trace(go.Scatter(
                    x=self.data['timestamp'],
                    y=self.data[col],
                    name=col.title(),
                    mode='lines'
                ))
        
        fig.update_layout(
            title='Sensor Data Time Series',
            xaxis_title='Time',
            yaxis_title='Value',
            height=500
        )
        
        return fig

class DataVisualizer:
    """Create visualizations for sensor data"""
    
    @staticmethod
    def create_performance_dashboard(metrics: Dict[str, float]) -> go.Figure:
        """Create performance metrics dashboard"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(metrics.keys()),
                y=list(metrics.values()),
                marker_color=['green' if v > np.mean(list(metrics.values())) else 'orange' 
                            for v in metrics.values()]
            )
        ])
        
        fig.update_layout(
            title='Flight Performance Metrics',
            xaxis_title='Metric',
            yaxis_title='Value',
            height=500
        )
        
        return fig
    
    @staticmethod
    def create_anomaly_plot(data: pd.DataFrame, anomalies: Dict[str, pd.DataFrame]) -> go.Figure:
        """Create anomaly visualization"""
        fig = go.Figure()
        
        for col, anomaly_data in anomalies.items():
            if col in data.columns:
                # Normal data
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[col],
                    name=f'{col} (Normal)',
                    mode='markers',
                    marker=dict(size=3, opacity=0.6)
                ))
                
                # Anomaly data
                if len(anomaly_data) > 0:
                    fig.add_trace(go.Scatter(
                        x=anomaly_data.index,
                        y=anomaly_data[col],
                        name=f'{col} (Anomaly)',
                        mode='markers',
                        marker=dict(size=8, color='red')
                    ))
        
        fig.update_layout(
            title='Anomaly Detection Results',
            xaxis_title='Time Index',
            yaxis_title='Value',
            height=600
        )
        
        return fig

# Utility functions
def generate_sample_data(n_points: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Generate sample sensor data for testing"""
    np.random.seed(seed)
    
    # Time series
    start_time = datetime.now() - timedelta(hours=2)
    timestamps = pd.date_range(start=start_time, periods=n_points, freq='10S')
    
    # GPS data
    base_lat, base_lon = 40.7128, -74.0060
    latitudes = base_lat + np.cumsum(np.random.normal(0, 0.0001, n_points))
    longitudes = base_lon + np.cumsum(np.random.normal(0, 0.0001, n_points))
    altitudes = 100 + np.cumsum(np.random.normal(0, 2, n_points))
    
    # IMU data
    roll = np.random.normal(0, 5, n_points)
    pitch = np.random.normal(0, 5, n_points)
    yaw = np.random.normal(180, 10, n_points)
    
    # Battery data
    battery_level = np.linspace(100, 75, n_points) + np.random.normal(0, 1, n_points)
    voltage = 12.6 - (100 - battery_level) * 0.01 + np.random.normal(0, 0.1, n_points)
    
    return pd.DataFrame({
        'timestamp': timestamps,
        'latitude': latitudes,
        'longitude': longitudes,
        'altitude': altitudes,
        'roll': roll,
        'pitch': pitch,
        'yaw': yaw,
        'battery_level': battery_level,
        'voltage': voltage
    })

def export_analysis_results(processor: SensorDataProcessor, filename: str = "analysis_results.json"):
    """Export analysis results to JSON"""
    metrics = processor.calculate_flight_metrics()
    
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'data_summary': {
            'total_records': len(processor.data),
            'time_range': {
                'start': processor.data['timestamp'].min().isoformat(),
                'end': processor.data['timestamp'].max().isoformat()
            }
        },
        'flight_metrics': metrics,
        'anomalies_summary': {
            'total_anomalies': sum(len(processor.detect_anomalies(['altitude', 'roll', 'pitch', 'yaw', 'battery_level', 'voltage'])[col]) 
                                  for col in ['altitude', 'roll', 'pitch', 'yaw', 'battery_level', 'voltage'])
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis results exported to {filename}")
    return results
