# Low Bridge Alert System

Automated alert system for Webfleet Link 740 devices to warn drivers when approaching low clearance bridges.

## Overview

This system monitors vehicle positions via the Webfleet API and automatically triggers an external buzzer (connected to Digital Output 5) when vehicles enter geofenced zones around low clearance bridges.

## Hardware Requirements

- **Webfleet Link 740** device installed in vehicle
- **External buzzer** connected to Digital Output 5
- Active Webfleet subscription with API access

## Features

- ✅ Real-time geofence monitoring
- ✅ Automatic buzzer activation via `switchoutputextern` API
- ✅ Configurable alert duration and polling intervals
- ✅ Multiple bridge monitoring
- ✅ Alert logging and history
- ✅ Severity-based bridge classification (CRITICAL/HIGH/MEDIUM)

## Installation

### 1. Clone or Download

```bash
cd /path/to/project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Edit `low_bridge_monitor.py` and add your Webfleet credentials:

```python
ACCOUNT = "Phoenix"      # Your Webfleet account name
USERNAME = "francisw"    # Your API username
PASSWORD = "your_password_here"  # Your API password
```

### 4. Configure Bridges

Edit `low_bridge_config.json` to add or modify bridge locations:

```json
{
  "buzzer_output_name": "Low Bridge",
  "buzzer_duration": 5,
  "poll_interval": 2,
  "bridges": [
    {
      "name": "Penrose Bridge",
      "geofence_name": "Low_Bridge_Penrose",
      "latitude": -36.9166,
      "longitude": 174.8333,
      "severity": "HIGH"
    }
  ]
}
```

## Usage

### Run the Monitor

```bash
python low_bridge_monitor.py
```

### Menu Options

1. **Test buzzer activation** - Manually trigger the buzzer on a specific vehicle
2. **Start monitoring geofences** - Begin continuous monitoring
3. **View configuration** - Display current settings
4. **Exit** - Stop the program

### Test the Buzzer

Before deploying, test the buzzer activation:

1. Run the script: `python low_bridge_monitor.py`
2. Select option 1: "Test buzzer activation"
3. Enter your vehicle object number (e.g., "006")
4. Verify the buzzer activates on the vehicle

## API Details

### Webfleet API Endpoint

- **Base URL**: `https://csv.webfleet.com/extern`
- **Action**: `switchoutputextern`

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `objectno` | Vehicle object UID/number | "006" |
| `outputname` | Name of the digital output | "Low Bridge" |
| `state` | 0 = deactivate, 1 = activate | 1 |
| `duration` | Duration in seconds | 5 |

### Example API Call

```python
api.switch_output_extern(
    object_uid="006",
    output_name="Low Bridge",
    state=1,
    duration=5
)
```

## Configuration Options

### low_bridge_config.json

| Setting | Description | Default |
|---------|-------------|---------|
| `buzzer_output_name` | Name of the digital output | "Low Bridge" |
| `buzzer_duration` | Buzzer duration in seconds | 5 |
| `poll_interval` | Polling frequency in seconds | 2 |
| `require_ignition` | Only trigger if ignition is ON | true |

### Bridge Properties

| Property | Description | Required |
|----------|-------------|----------|
| `name` | Bridge name | Yes |
| `geofence_name` | Webfleet geofence name | Yes |
| `latitude` | GPS latitude | Yes |
| `longitude` | GPS longitude | Yes |
| `clearance_height` | Height clearance | No |
| `severity` | CRITICAL/HIGH/MEDIUM | No |
| `radius_meters` | Geofence radius | No |

## Workflow

### Event-Based Monitoring (Message Queue)

1. **Setup**: Create geofences in Webfleet with "Alarm 1" trigger on entry
2. **Queue**: Script creates message queue for status messages (msgclass 7)
3. **Monitor**: Polls queue every 2 seconds for Alarm 1 notifications
4. **Detect**: When vehicle enters "Low Bridge" or "Low Roof" geofence
5. **Alert**: Buzzer activates via Digital Output 5 using `switchoutput` API
6. **Cooldown**: 5-minute debounce prevents repeated alerts
7. **Log**: Event recorded in `alert_log.json`

### How It Works

```
Vehicle enters geofence
    ↓
Webfleet triggers Alarm 1
    ↓
Notification posted to message queue
    ↓
Script polls queue (every 2s)
    ↓
Detects "Low Bridge" + "Alarm 1" in message
    ↓
Checks cooldown (5 min since last alert)
    ↓
Triggers buzzer via switchoutput API
    ↓
Logs alert to alert_log.json
```

## Geofence Setup

### Requirements

Geofences must be configured in Webfleet with specific settings:

1. **Name prefix**: Must start with "Low Bridge" or "Low Roof"
   - Example: "Low Bridge - Penrose"
   - Example: "Low Roof - Rust Avenue"

2. **Alarm configuration**: Set to trigger **Alarm 1** on geofence entry

3. **Setup steps**:
   - Log into Webfleet web interface
   - Go to **Configuration > Geofences**
   - Create circular geofence at bridge location
   - Set radius (recommended: 100m)
   - Configure **Alarm 1** to trigger on entry
   - Name with "Low Bridge" or "Low Roof" prefix

## Troubleshooting

### Buzzer Not Activating

- Verify Digital Output 5 is connected and configured in Webfleet
- Check output name matches configuration ("Low Bridge")
- Ensure vehicle is within geofence radius
- Verify API credentials are correct

### API Errors

- Check internet connection
- Verify Webfleet API is enabled for your account
- Confirm API password is correct
- Review API response in console output

### No Vehicles Detected

- Ensure geofences are created in Webfleet
- Verify geofence names match configuration
- Check vehicles have active GPS signal
- Confirm polling interval is appropriate

## Alert Log

All alerts are saved to `alert_log.json`:

```json
[
  {
    "timestamp": "2025-11-21T10:30:15",
    "vehicle": "006",
    "bridge": "Penrose Bridge",
    "reason": "Low bridge approach",
    "response": {...}
  }
]
```

## Safety Notes

- Test thoroughly before deploying to production vehicles
- Set appropriate geofence radius to give drivers adequate warning
- Ensure buzzer volume is noticeable but not startling
- Consider local regulations regarding in-vehicle alerts

## Support

For issues or questions:
- Email: francis@directt.co.nz
- Check Webfleet API documentation
- Review `alert_log.json` for error details

## License

Internal use - UCCL Dashboard Project
