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

    def switch_output_extern(self, object_uid: str, output_name: str, status: int) -> Dict:
        """
        Activate or deactivate an external output (buzzer)

        Args:
            object_uid: Vehicle object UID or object number
            output_name: Name of the output (e.g., 'Low Bridge')
            status: 0 = deactivate, 1 = activate

        Returns:
            API response
        """
        params = {
            'objectno': object_uid,
            'outputname': output_name,
            'status': status
        }

        status_text = "ON" if status == 1 else "OFF"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Setting output '{output_name}' on vehicle {object_uid} to {status_text}")

        response = self._make_request('switchoutput', params)
        return response

    def get_object_positions(self) -> Dict:
        """Get current positions of all vehicles"""
        response = self._make_request('showObjectReportExtern', {})
        return response

    def create_queue(self, msgclass: int = 7) -> Dict:
        """
        Create a message queue to receive notifications

        Args:
            msgclass: Message class to receive
                0 - All messages
                2 - All except position messages
                4 - Order related messages
                5 - Driver related messages
                7 - Status messages (includes geofence alerts)
                8 - Text messages
                15 - Third party messages

        Returns:
            API response with queue ID
        """
        params = {
            'msgclass': msgclass
        }
        print(f"Creating message queue for message class {msgclass}...")
        response = self._make_request('createQueueExtern', params)
        return response

    def pop_queue_messages(self, queue_uid: str) -> Dict:
        """
        Retrieve messages from the queue

        Args:
            queue_uid: Queue ID returned from createQueueExtern

        Returns:
            API response with messages
        """
        params = {
            'queueuid': queue_uid
        }
        response = self._make_request('popQueueMessagesExtern', params)
        return response

    def delete_queue(self, queue_uid: str) -> Dict:
        """
        Delete a message queue

        Args:
            queue_uid: Queue ID to delete

        Returns:
            API response
        """
        params = {
            'queueuid': queue_uid
        }
        print(f"Deleting message queue {queue_uid}...")
        response = self._make_request('deleteQueueExtern', params)
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

    def get_event_report(self, range_pattern: str = "d0", event_level: int = None) -> Dict:
        """
        Get event report for geofence entries and other events

        Args:
            range_pattern: Time range for events
                - "d0" - today (default)
                - "d1" - yesterday
                - Can also use date range with rangefrom/rangeto params
            event_level: Filter by event level (optional)
                - 0: Message
                - 1: Notice/Information
                - 2: Warning
                - 3: Alarm 1
                - 4: Alarm 2
                - 5: Alarm 3

        Returns:
            API response with events
        """
        params = {
            'range_pattern': range_pattern
        }

        if event_level is not None:
            params['eventlevel'] = event_level

        response = self._make_request('showEventReportExtern', params)
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
                'poll_interval': 2
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

        # Turn buzzer ON
        response_on = self.api.switch_output_extern(
            object_uid=vehicle_id,
            output_name=output_name,
            status=1  # Activate
        )

        # Check if ON command successful
        if 'error' in response_on:
            print(f"✗ Failed to activate buzzer: {response_on.get('error')}")
            # Log the failed attempt
            alert = {
                'timestamp': datetime.now().isoformat(),
                'vehicle': vehicle_id,
                'bridge': bridge_name,
                'reason': reason,
                'response': response_on,
                'success': False
            }
            self.alert_log.append(alert)
            return False

        print(f"✓ Buzzer ON for vehicle {vehicle_id} - {bridge_name} (duration: {duration}s)")

        # Wait for duration
        time.sleep(duration)

        # Turn buzzer OFF
        response_off = self.api.switch_output_extern(
            object_uid=vehicle_id,
            output_name=output_name,
            status=0  # Deactivate
        )

        print(f"✓ Buzzer OFF for vehicle {vehicle_id}")

        # Log the alert
        alert = {
            'timestamp': datetime.now().isoformat(),
            'vehicle': vehicle_id,
            'bridge': bridge_name,
            'reason': reason,
            'duration': duration,
            'response_on': response_on,
            'response_off': response_off,
            'success': True
        }
        self.alert_log.append(alert)

        return True

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
        """Main monitoring loop - polls event report for Warning level geofence events"""
        print("\n" + "="*60)
        print("LOW BRIDGE ALERT SYSTEM - MONITORING ACTIVE")
        print("="*60)
        print(f"Buzzer Output: {self.config.get('buzzer_output_name')}")
        print(f"Duration: {self.config.get('buzzer_duration')}s")
        print(f"Poll Interval: {self.config.get('poll_interval')}s")
        print(f"Event Level: WARNING (level 2)")
        print("="*60 + "\n")

        print("Monitoring for WARNING level geofence entry events...")
        print("Configure geofences with 'Warning' severity in Webfleet\n")

        # Track processed events to avoid duplicates
        processed_events = set()  # Set of event IDs we've already handled

        # Track vehicles we've already alerted (debouncing)
        alerted_vehicles = {}  # {vehicle_id: timestamp}
        cooldown_minutes = 5

        try:
            while True:
                # Get today's event report - filter for WARNING level events only
                events_result = self.api.get_event_report(range_pattern='d0', event_level=2)

                # Debug: Print raw API response
                print(f"[DEBUG] API Response: {json.dumps(events_result, indent=2)}")

                if 'error' not in events_result:
                    # Parse events - the structure may vary, adjust based on actual response
                    events = []

                    # Try different possible response structures
                    if isinstance(events_result, list):
                        events = events_result
                    elif isinstance(events_result, dict):
                        events = events_result.get('events', [])
                        if not events:
                            events = events_result.get('data', [])

                    for event in events:
                        # Extract event details
                        event_id = event.get('eventid', '')
                        event_time = event.get('eventtime', '')
                        msg_time = event.get('msgtime', '')
                        vehicle_id = event.get('objectno', '')
                        msg_text = event.get('msgtext', '')
                        pos_text = event.get('postext', '')
                        event_level_cur = event.get('eventlevel_cur', '')

                        # Skip if we've already processed this event
                        if event_id in processed_events:
                            continue

                        # Verify this is a Warning level event
                        if event_level_cur != 'W':
                            continue

                        # Filter for geofence entry events only - ignore output status changes
                        if 'Output' in msg_text or 'output' in msg_text:
                            continue

                        # Only process geofence entry events
                        if 'Entering area' not in msg_text and 'entering area' not in msg_text:
                            continue

                        # Mark as processed
                        processed_events.add(event_id)

                        # Check cooldown - don't re-alert same vehicle within X minutes
                        now = datetime.now()
                        last_alert = alerted_vehicles.get(vehicle_id)

                        if last_alert:
                            time_diff = (now - last_alert).total_seconds() / 60
                            if time_diff < cooldown_minutes:
                                print(f"⏸️  Skipping {vehicle_id} - alerted {time_diff:.1f}min ago (cooldown: {cooldown_minutes}min)")
                                continue

                        # Extract bridge/location name from message or position text
                        bridge_name = pos_text if pos_text else msg_text
                        if not bridge_name:
                            bridge_name = "Unknown Location"

                        print(f"\n🚨 WARNING EVENT DETECTED!")
                        print(f"   Event ID: {event_id}")
                        print(f"   Time: {event_time or msg_time}")
                        print(f"   Vehicle: {vehicle_id}")
                        print(f"   Location: {bridge_name}")
                        print(f"   Message: {msg_text}")
                        print(f"   Level: {event_level_cur} (Warning)")

                        # Trigger buzzer
                        self.trigger_buzzer(vehicle_id, bridge_name, reason="Warning event - Geofence entry")

                        # Record alert time for cooldown
                        alerted_vehicles[vehicle_id] = now

                # Clean up old processed events (keep last 1000)
                if len(processed_events) > 1000:
                    # Convert to list, keep last 500
                    processed_events = set(list(processed_events)[-500:])

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
    APIKEY = "752a57e4-877d-4dbf-bc99-b2c356f774f1"  # Webfleet API key

    if not APIKEY:
        print("ERROR: Please set your Webfleet API key in the script")
        print("Edit low_bridge_monitor.py and update the APIKEY variable")
        return

    # Initialize API
    print("Initializing Webfleet API...")
    api = WebfleetAPI(ACCOUNT, USERNAME, APIKEY)

    # Initialize monitor
    monitor = LowBridgeMonitor(api)

    # Menu
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Test buzzer activation")
        print("2. Start monitoring warnings")
        print("3. View configuration")
        print("4. Configure buzzer duration")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            vehicle_id = input("Enter vehicle object number: ").strip()
            if vehicle_id:
                monitor.trigger_buzzer(vehicle_id, "Test Location", "Manual test")

        elif choice == "2":
            monitor.monitor_geofences()

        elif choice == "3":
            print("\nCurrent Configuration:")
            print(json.dumps(monitor.config, indent=2))

        elif choice == "4":
            current_duration = monitor.config.get('buzzer_duration', 5)
            print(f"\nCurrent buzzer duration: {current_duration} seconds")
            try:
                new_duration = int(input("Enter new duration (seconds): ").strip())
                if new_duration > 0 and new_duration <= 60:
                    monitor.config['buzzer_duration'] = new_duration
                    monitor.save_config(monitor.config)
                    print(f"✓ Buzzer duration updated to {new_duration} seconds")
                else:
                    print("✗ Duration must be between 1 and 60 seconds")
            except ValueError:
                print("✗ Invalid input - must be a number")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
