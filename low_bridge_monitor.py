#!/usr/bin/env python3
"""
Low Bridge Alert System
Monitors vehicles approaching low clearance bridges and triggers external buzzer via Webfleet API
"""

import requests
import hashlib
import time
import json
from datetime import datetime
from typing import Dict, List, Optional


class WebfleetAPI:
    """Handle Webfleet API communications"""

    def __init__(self, account: str, username: str, password: str, api_url: str = "https://csv.webfleet.com/extern"):
        """
        Initialize Webfleet API client

        Args:
            account: Webfleet account name
            username: API username
            password: API password
            api_url: Base API URL (default: https://csv.webfleet.com/extern)
        """
        self.account = account
        self.username = username
        self.password = password
        self.api_url = api_url
        self.session = requests.Session()

    def _generate_signature(self, params: Dict) -> str:
        """Generate API signature for authentication"""
        # Sort parameters alphabetically
        sorted_params = sorted(params.items())
        param_string = ''.join([f"{k}{v}" for k, v in sorted_params])

        # Create signature: MD5(params + password)
        signature_string = param_string + self.password
        return hashlib.md5(signature_string.encode()).hexdigest()

    def _make_request(self, action: str, params: Dict) -> Dict:
        """
        Make API request to Webfleet

        Args:
            action: API action name (e.g., 'switchoutputextern')
            params: Additional parameters for the API call

        Returns:
            API response as dictionary
        """
        # Build base parameters
        request_params = {
            'account': self.account,
            'username': self.username,
            'action': action,
            'apikey': self.password,
            'lang': 'en',
            'outputformat': 'json'
        }

        # Add custom parameters
        request_params.update(params)

        try:
            response = self.session.get(self.api_url, params=request_params, timeout=30)
            response.raise_for_status()

            # Parse JSON response
            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {'error': str(e)}

    def switch_output_extern(self, object_uid: str, output_name: str, state: int, duration: int = 5) -> Dict:
        """
        Activate or deactivate an external output (buzzer)

        Args:
            object_uid: Vehicle object UID or object number
            output_name: Name of the output (e.g., 'Low Bridge')
            state: 0 = deactivate, 1 = activate
            duration: Duration in seconds (default: 5)

        Returns:
            API response
        """
        params = {
            'objectno': object_uid,
            'outputname': output_name,
            'state': state,
            'duration': duration
        }

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering output '{output_name}' on vehicle {object_uid} for {duration}s")

        response = self._make_request('switchoutput', params)
        return response

    def get_object_positions(self) -> Dict:
        """Get current positions of all vehicles"""
        response = self._make_request('showObjectReportExtern', {})
        return response

    def get_vehicles_in_geofence(self, geofence_name: str) -> Dict:
        """Get vehicles currently in a specific geofence"""
        params = {
            'geofencename': geofence_name
        }
        response = self._make_request('showVehiclesInGeofence', params)
        return response

    def create_geofence(self, name: str, lat: float, lon: float, radius: int, color: str = "red") -> Dict:
        """
        Create a circular geofence in Webfleet

        Args:
            name: Geofence name (e.g., 'Low_Bridge_Penrose')
            lat: Latitude
            lon: Longitude
            radius: Radius in meters
            color: Geofence color (default: red)

        Returns:
            API response
        """
        params = {
            'geofencename': name,
            'latitude': lat,
            'longitude': lon,
            'radius': radius,
            'color': color
        }
        print(f"Creating geofence: {name} at ({lat}, {lon}) with radius {radius}m")
        response = self._make_request('insertGeofenceExtern', params)
        return response

    def delete_geofence(self, name: str) -> Dict:
        """Delete a geofence from Webfleet"""
        params = {
            'geofencename': name
        }
        print(f"Deleting geofence: {name}")
        response = self._make_request('deleteGeofenceExtern', params)
        return response

    def list_geofences(self) -> Dict:
        """List all geofences"""
        response = self._make_request('showGeofenceReportExtern', {})
        return response


class LowBridgeMonitor:
    """Monitor vehicles and trigger alerts when approaching low bridges"""

    def __init__(self, api: WebfleetAPI, config_file: str = 'low_bridge_config.json'):
        """
        Initialize low bridge monitoring system

        Args:
            api: WebfleetAPI instance
            config_file: Path to configuration file
        """
        self.api = api
        self.config_file = config_file
        self.config = self.load_config()
        self.alert_log = []

    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Creating default config...")
            default_config = {
                'buzzer_output_name': 'Low Bridge',
                'buzzer_duration': 5,
                'poll_interval': 2,
                'require_ignition': True,
                'bridges': []
            }
            self.save_config(default_config)
            return default_config

    def save_config(self, config: Dict):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, indent=2, fp=f)

    def trigger_buzzer(self, vehicle_id: str, bridge_name: str, reason: str = "Low bridge approach") -> bool:
        """
        Trigger the external buzzer for a specific vehicle

        Args:
            vehicle_id: Vehicle object UID/number
            bridge_name: Name of the bridge being approached
            reason: Reason for alert

        Returns:
            True if successful, False otherwise
        """
        output_name = self.config.get('buzzer_output_name', 'Low Bridge')
        duration = self.config.get('buzzer_duration', 5)

        response = self.api.switch_output_extern(
            object_uid=vehicle_id,
            output_name=output_name,
            state=1,  # Activate
            duration=duration
        )

        # Log the alert
        alert = {
            'timestamp': datetime.now().isoformat(),
            'vehicle': vehicle_id,
            'bridge': bridge_name,
            'reason': reason,
            'response': response
        }
        self.alert_log.append(alert)

        # Check if successful
        if 'error' not in response:
            print(f"✓ Buzzer activated for vehicle {vehicle_id} - {bridge_name}")
            return True
        else:
            print(f"✗ Failed to activate buzzer: {response.get('error')}")
            return False

    def save_alert_log(self, filename: str = 'alert_log.json'):
        """Save alert log to file"""
        with open(filename, 'w') as f:
            json.dump(self.alert_log, indent=2, fp=f)
        print(f"Alert log saved to {filename}")

    def create_all_geofences(self):
        """Create geofences for all bridges in configuration"""
        print("\n" + "="*60)
        print("CREATING GEOFENCES FOR ALL BRIDGES")
        print("="*60 + "\n")

        bridges = self.config.get('bridges', [])
        if not bridges:
            print("No bridges configured!")
            return

        success_count = 0
        fail_count = 0

        for bridge in bridges:
            name = bridge.get('geofence_name')
            lat = bridge.get('latitude')
            lon = bridge.get('longitude')
            radius = bridge.get('radius_meters', 100)

            if not all([name, lat, lon]):
                print(f"⚠ Skipping {bridge.get('name', 'Unknown')} - missing data")
                fail_count += 1
                continue

            result = self.api.create_geofence(name, lat, lon, radius, color='red')

            if 'error' in result:
                print(f"✗ Failed: {name} - {result.get('error')}")
                fail_count += 1
            else:
                print(f"✓ Created: {name}")
                success_count += 1

        print(f"\n{'='*60}")
        print(f"Summary: {success_count} created, {fail_count} failed")
        print(f"{'='*60}\n")

    def delete_all_geofences(self):
        """Delete all bridge geofences"""
        print("\n" + "="*60)
        print("DELETING ALL BRIDGE GEOFENCES")
        print("="*60 + "\n")

        bridges = self.config.get('bridges', [])
        if not bridges:
            print("No bridges configured!")
            return

        confirm = input(f"Are you sure you want to delete {len(bridges)} geofences? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled")
            return

        success_count = 0
        fail_count = 0

        for bridge in bridges:
            name = bridge.get('geofence_name')
            if not name:
                continue

            result = self.api.delete_geofence(name)

            if 'error' in result:
                print(f"✗ Failed: {name}")
                fail_count += 1
            else:
                print(f"✓ Deleted: {name}")
                success_count += 1

        print(f"\n{'='*60}")
        print(f"Summary: {success_count} deleted, {fail_count} failed")
        print(f"{'='*60}\n")

    def list_all_geofences(self):
        """List all geofences in Webfleet"""
        print("\n" + "="*60)
        print("ALL GEOFENCES IN WEBFLEET")
        print("="*60 + "\n")

        result = self.api.list_geofences()

        if 'error' in result:
            print(f"✗ Error: {result.get('error')}")
        else:
            print(json.dumps(result, indent=2))

    def monitor_geofences(self):
        """Main monitoring loop - checks geofences and triggers alerts"""
        print("\n" + "="*60)
        print("LOW BRIDGE ALERT SYSTEM - MONITORING ACTIVE")
        print("="*60)
        print(f"Buzzer Output: {self.config.get('buzzer_output_name')}")
        print(f"Duration: {self.config.get('buzzer_duration')}s")
        print(f"Poll Interval: {self.config.get('poll_interval')}s")
        print(f"Bridges Monitored: {len(self.config.get('bridges', []))}")
        print("="*60 + "\n")

        try:
            while True:
                # Monitor each configured bridge
                for bridge in self.config.get('bridges', []):
                    geofence_name = bridge.get('geofence_name')
                    bridge_name = bridge.get('name')

                    if not geofence_name:
                        continue

                    # Check for vehicles in this geofence
                    result = self.api.get_vehicles_in_geofence(geofence_name)

                    # Process vehicles in geofence
                    # This will depend on the actual API response format
                    # You may need to adjust based on real API responses

                    if 'vehicles' in result:
                        for vehicle in result['vehicles']:
                            vehicle_id = vehicle.get('objectno')
                            if vehicle_id:
                                self.trigger_buzzer(vehicle_id, bridge_name)

                # Wait before next poll
                time.sleep(self.config.get('poll_interval', 2))

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            self.save_alert_log()


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("LOW BRIDGE ALERT SYSTEM")
    print("="*60 + "\n")

    # Configuration
    ACCOUNT = "Phoenix"
    USERNAME = "francisw"
    PASSWORD = "@wynn5Fr4nc1s"  # Webfleet API password

    if not PASSWORD:
        print("ERROR: Please set your Webfleet API password in the script")
        print("Edit low_bridge_monitor.py and update the PASSWORD variable")
        return

    # Initialize API
    print("Initializing Webfleet API...")
    api = WebfleetAPI(ACCOUNT, USERNAME, PASSWORD)

    # Initialize monitor
    monitor = LowBridgeMonitor(api)

    # Menu
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Test buzzer activation")
        print("2. Create all geofences")
        print("3. Delete all geofences")
        print("4. List all geofences")
        print("5. Start monitoring geofences")
        print("6. View configuration")
        print("7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            vehicle_id = input("Enter vehicle object number: ").strip()
            if vehicle_id:
                monitor.trigger_buzzer(vehicle_id, "Test Bridge", "Manual test")

        elif choice == "2":
            monitor.create_all_geofences()

        elif choice == "3":
            monitor.delete_all_geofences()

        elif choice == "4":
            monitor.list_all_geofences()

        elif choice == "5":
            monitor.monitor_geofences()

        elif choice == "6":
            print("\nCurrent Configuration:")
            print(json.dumps(monitor.config, indent=2))

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
