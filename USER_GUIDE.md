# Northland Geofence Monitoring System
## User Guide & Reference Manual

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [Dashboard Features](#dashboard-features)
5. [Vehicle Policy Groups](#vehicle-policy-groups)
6. [Geofence Management](#geofence-management)
7. [Policy Monitoring](#policy-monitoring)
8. [Compliance Checking](#compliance-checking)
9. [Map Viewing](#map-viewing)
10. [Alert Management](#alert-management)
11. [Configuration](#configuration)
12. [Troubleshooting](#troubleshooting)

---

## Overview

The **Northland Geofence Monitoring System** is a comprehensive vehicle policy enforcement platform that monitors vehicle locations in real-time against defined geographic boundaries and time-based restrictions.

### Key Features

- **Real-time vehicle tracking** - Monitor 50+ vehicles simultaneously
- **Policy enforcement** - Enforce geographic boundaries and time-based vehicle usage restrictions
- **Interactive maps** - View vehicle locations and geofence boundaries on Leaflet maps
- **Policy violations** - Receive alerts for boundary and time-based violations
- **Geofence management** - Create, edit, and import custom geofences
- **Compliance reporting** - View detailed compliance statistics and vehicle status

### Supported Policies

The system enforces 6 vehicle policy groups across the Northland region:

1. **Full Use** - Unrestricted vehicle access
2. **Northland Region Only** - Limited to Northland boundaries
3. **Whangarei District + 30km** - Limited to Whangarei area
4. **Hawkes Bay Region** - Limited to Hawkes Bay area
5. **Napier District + 30km** - Limited to Napier area
6. **Time-Restricted Trade Staff** - Restricted hours usage (after 6pm, before 4am weekdays + all weekends)

---

## Getting Started

### System Requirements

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Geotab account with API access
- JavaScript enabled
- Internet connection for Geotab API connectivity

### Accessing the Dashboard

The dashboard is available as a Geotab add-in. Access it through:
1. Log into your Geotab account
2. Navigate to Add-Ins
3. Select "Northland Geofence Monitoring System"

---

## Authentication

### Logging In

The dashboard requires Geotab API credentials to access vehicle data.

1. **Fill in authentication fields:**
   - **Server**: `my.geotab.com` (or your Geotab server)
   - **Database**: Your Geotab database name (e.g., `uccnz`)
   - **Username**: Your Geotab username
   - **Password**: Your Geotab password

2. **Click "🔐 Authenticate"** button

3. **Wait for confirmation** - You should see a success message

### Session Management

- Your credentials are stored only in the browser session
- Credentials are not saved after browser refresh
- You can log out anytime by clicking the **"🚪 Logout"** button
- Logging out clears all data and resets the dashboard

---

## Dashboard Features

### Main Sections

#### 1. Authentication Card
- Login with Geotab credentials
- Displays authentication status
- Required before accessing monitoring features

#### 2. Vehicle Policy Enforcement Card
- View all 6 vehicle policy groups
- See which vehicles belong to each group
- Understand policy restrictions for each group

#### 3. Geofence Manager
- View all policy geofences
- Load predefined policy geofences
- Create new custom geofences
- Import/Export geofences
- Delete geofences

#### 4. Monitoring Configuration
- Select active geofence to monitor
- Set monitoring timeout (minutes)
- Set check interval (seconds)
- Set asset results limit
- Enable/disable real-time monitoring
- Enable/disable audio alerts
- Enable/disable time-based restrictions

#### 5. Control Buttons
- **🚀 Start Policy Monitoring** - Begin continuous monitoring
- **⏹️ Stop Monitoring** - Stop monitoring session
- **🔍 Check Policy Compliance** - Manual compliance check
- **🗺️ Show Policy Map** - Display interactive map
- **🚪 Logout** - End session and clear data

#### 6. Statistics Panel
- **Total Monitored** - Number of vehicles being monitored
- **Inside Boundary** - Vehicles within policy boundaries
- **Outside Boundary** - Vehicles outside policy boundaries
- **Policy Violations** - Number of current violations

---

## Vehicle Policy Groups

### Group 1: Full Use (No Restrictions)
**Vehicles**: 520, 529, 541, 543, 544, 546

Full access to vehicle across North Island or NZ-wide as needed.

### Group 2: Northland Region Only
**Vehicles**: 490, 517, 518, 519, 530, 534, 535, 542, 552, 553

Vehicles restricted to Northland Region boundaries.

### Group 3: Whangarei District + 30km Radius
**Vehicles**: 471, 502, 508, 510, 513, 515, 516, 522, 526, 527, 533, 537, 538, 539, 540, 545, 549, 550

Vehicles limited to Whangarei District or 30km from residence.

### Group 4: Hawkes Bay Region
**Vehicle**: 536

Tony Abiad - restricted to Hawkes Bay Region.

### Group 5: Napier District + 30km Radius
**Vehicles**: 521, 523, 551

Vehicles limited to Napier District or 30km from residence.

### Group 6: Time-Restricted Trade Staff
**Vehicles**: 465, 470, 476, 487, 488, 489, 491, 492, 493, 494, 495, 496, 500, 501, 503, 505, 511, 512, 514, 524, 525, 528, 531, 532

Time restrictions:
- **Weekdays**: After 6pm AND before 4am
- **Weekends**: All hours permitted
- **Violations**: Usage outside permitted hours triggers violation alert

---

## Geofence Management

### Available Policy Geofences

The system includes 5 pre-configured policy geofences:

1. **Northland Region** - Full regional boundary
2. **Whangarei District** - Whangarei city area
3. **Hawkes Bay Region** - Hawkes Bay regional area
4. **Napier District** - Napier city area
5. **Far North Boundary Line** - Northern boundary line

### Loading Policy Geofences

1. Click **"🚗 Load Policy Geofences"** button
2. All 5 policy geofences load automatically
3. Geofences appear in the list below
4. Select geofence from dropdown to monitor

### Creating Custom Geofences

#### Method 1: Draw on Map

1. Click **"➕ Create New Geofence"**
2. Enter geofence name
3. Click **"🖊️ Draw on Map"**
4. Use map tools to draw polygon/rectangle
5. Click **"💾 Save Geofence"**

#### Method 2: Enter Coordinates

1. Click **"➕ Create New Geofence"**
2. Enter geofence name
3. Click **"📍 Enter Coordinates"**
4. Enter coordinates as: `latitude, longitude` (one per line)
5. Click **"💾 Save Geofence"**

**Coordinate Format Example:**
```
-35.525, 174.255
-35.525, 174.355
-35.625, 174.355
-35.625, 174.255
```

Minimum 3 points required to create polygon.

### Managing Geofences

Each geofence has three action buttons:

- **👁️ View** - Zoom to geofence on map
- **📤 Export** - Download geofence as JSON file
- **🗑️ Delete** - Remove geofence (requires confirmation)

### Importing Geofences

1. Click **"📥 Import"**
2. Paste geofence JSON in text area
3. Click **"Import"** to add to system

**JSON Format:**
```json
{
  "name": "My Geofence",
  "coordinates": [
    [-35.5, 174.2],
    [-35.5, 174.4],
    [-35.6, 174.4],
    [-35.6, 174.2]
  ],
  "color": "#1e3c72"
}
```

---

## Policy Monitoring

### Starting Monitoring

1. **Select geofence** from "Active Geofence" dropdown
2. **Configure settings:**
   - Timeout: Minutes before vehicle removed from violation (default: 30)
   - Check Interval: Seconds between checks (default: 30)
   - Results Limit: Max vehicles to monitor (default: 50)
3. **Enable options:**
   - ✓ Enable Real-time Monitoring
   - ✓ Enable Audio Alerts
   - ✓ Enforce Time-Based Restrictions
4. **Click "🚀 Start Policy Monitoring"**

### Monitoring in Progress

- **Status indicator**: Button changes to "⏹️ Stop Monitoring"
- **Real-time checks**: System checks every 30 seconds (configurable)
- **Statistics update**: Live statistics display updates
- **Results table**: Shows current vehicle status

### Stopping Monitoring

Click **"⏹️ Stop Monitoring"** button to stop the monitoring session.

---

## Compliance Checking

### Manual Compliance Check

Click **"🔍 Check Policy Compliance"** to manually check vehicle compliance against active geofence.

### Results Table

The compliance results table displays:

| Column | Description |
|--------|-------------|
| **Vehicle** | Device name and vehicle number |
| **Location** | GPS coordinates (latitude, longitude) |
| **Compliance Status** | Inside Boundary ✓ / Outside Boundary / Policy Violation 🚨 |
| **Last Update** | Timestamp of last location update |

### Status Indicators

- **✓ Inside Boundary** (Green) - Vehicle within policy boundary
- **⚠️ Outside Boundary** (Orange) - Vehicle outside boundary (but allowed by time rules)
- **🚨 Policy Violation** (Red) - Vehicle violates policy (boundary + time violation)

---

## Map Viewing

### Opening the Map

Click **"🗺️ Show Policy Map"** button to display the policy map.

### Map Features

The interactive map displays:
- **Geofence boundaries** - Colored polygons showing policy boundaries
- **Vehicle markers** - Colored circles showing vehicle locations
- **Vehicle information** - Click markers to view vehicle details
- **Google Maps links** - Fallback view with clickable map links

### Map Markers

**Marker Colors:**
- 🟢 **Green** - Vehicle inside boundary (compliant)
- 🟠 **Orange** - Vehicle outside boundary
- 🔴 **Red** - Policy violation (boundary + time)

### Vehicle Marker Details

Click any marker to view:
- Device name and vehicle number
- Compliance status
- Exact GPS coordinates
- Last update time
- Monitoring timeout

### Fallback Map Mode

If interactive map is unavailable:
- Geofences display as clickable cards
- Vehicle locations shown as list items
- All items link to Google Maps for viewing

---

## Alert Management

### Violation Alerts

When policy violations occur, an **alert panel** appears on the right side showing:

- **Vehicle name** - Device identifier
- **Violation type** - Boundary / Time & Boundary
- **Duration** - How long violation has been active
- **Location** - GPS coordinates

### Alert Actions

- **✅ Acknowledge All** - Clear all active violations
- **✖️ Close Panel** - Hide alert panel

### Audio Alerts

If enabled:
- Sound plays when violation occurs
- One alert per violation
- Can be disabled in configuration

---

## Configuration

### Monitoring Settings

#### Timeout (minutes)
- **Default**: 30 minutes
- **Purpose**: How long a vehicle stays in violation list before removal
- **Adjustable**: 1 - 1000 minutes

#### Check Interval (seconds)
- **Default**: 30 seconds
- **Purpose**: How often system checks vehicle locations
- **Adjustable**: 5 - 3600 seconds
- **Note**: Lower values = more frequent checks but higher API usage

#### Assets Limit
- **Default**: 50 vehicles
- **Purpose**: Maximum vehicles to monitor per check
- **Adjustable**: 1 - 1000
- **Note**: Larger limits may increase response time

### Feature Toggles

#### ☑️ Enable Real-time Monitoring
When checked, system continuously monitors selected geofence.

#### ☑️ Enable Audio Alerts for Violations
When checked, sound plays when violation occurs.

#### ☑️ Enforce Time-Based Restrictions
When checked, time-based policies enforced. Uncheck to disable time rules.

---

## Troubleshooting

### Map Not Showing

**Problem**: Map container displays but no map visible.

**Solutions**:
1. Check browser console (F12) for errors
2. Ensure Leaflet files loaded: Check "js/leaflet/" directory exists
3. Try fallback mode: Refresh page and use Google Maps links
4. Clear browser cache and reload

### No Vehicles Displaying

**Problem**: Map shows but no vehicle markers appear.

**Solutions**:
1. Click "Check Policy Compliance" first to fetch locations
2. Check geofence is selected in dropdown
3. Verify Geotab API credentials are correct
4. Check devices have recent location data (< 24 hours)
5. Increase "Results Limit" in configuration

### Authentication Fails

**Problem**: Cannot authenticate with Geotab credentials.

**Solutions**:
1. Verify username and password are correct
2. Check database name matches your Geotab database
3. Confirm Geotab account has API access enabled
4. Try authenticating in Geotab web app first
5. Check network connection is stable

### Alerts Not Triggering

**Problem**: Violations not detected when vehicles outside boundary.

**Solutions**:
1. Check "Enable Real-time Monitoring" is enabled
2. Click "Start Policy Monitoring" button
3. Verify correct geofence selected
4. Check vehicle assignment to policy group
5. Verify time restrictions not preventing violation (if time is allowed, no violation)

### Slow Performance

**Problem**: Dashboard responds slowly.

**Solutions**:
1. Reduce "Assets Limit" to fewer vehicles
2. Increase "Check Interval" to 60+ seconds
3. Close other browser tabs
4. Clear browser cache
5. Use Firefox instead of Chrome for better performance in Geotab

### Map Drawing Not Working

**Problem**: Cannot draw geofences on map.

**Solutions**:
1. Check Leaflet.draw library loaded
2. Use "Enter Coordinates" method instead
3. Refresh page and try again
4. Clear browser cache and cookies

---

## Technical Details

### API Requirements

The dashboard uses Geotab API endpoints:

- **Get** - Retrieve devices and location data
- **Authenticate** - Authenticate user credentials
- **DeviceStatusInfo** - Get current vehicle locations
- **LogRecord** - Get historical location data

### Data Refresh

- Vehicle locations update every 30 seconds (configurable)
- Statistics update after each compliance check
- Map markers update in real-time during monitoring

### Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Supported | Recommended |
| Firefox | ✅ Supported | Good Geotab compatibility |
| Edge | ✅ Supported | Works well |
| Safari | ✅ Supported | May have some restrictions |

### Storage

- Credentials stored in browser session only
- No data persisted after logout
- Geofences stored in session (lost on refresh)
- Device mapping cached for performance

---

## Best Practices

### Security

1. Never share credentials with others
2. Log out when done using dashboard
3. Don't leave dashboard unattended
4. Use strong passwords for Geotab account

### Monitoring

1. Test with small vehicle set first (Results Limit = 10)
2. Start monitoring during business hours for testing
3. Use appropriate check interval (30-60 seconds recommended)
4. Monitor compliance regularly (at least daily)

### Geofence Design

1. Create geofences that match policy boundaries exactly
2. Test geofences with known vehicle locations
3. Export important geofences for backup
4. Review geofence coordinates with operations team

### Alert Management

1. Acknowledge violations promptly
2. Investigate root causes of violations
3. Update policies if geofences are incorrect
4. Archive violation logs for compliance records

---

## Support & Contact

For technical issues or feature requests:

1. Check browser console (F12) for error messages
2. Review this user guide's troubleshooting section
3. Contact IT support with:
   - Browser type and version
   - Steps to reproduce issue
   - Console error messages
   - Screenshots

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Nov 2024 | Bundled Leaflet locally, improved Geotab compatibility |
| 1.5 | Nov 2024 | Device-to-vehicle mapping, async marker updates |
| 1.0 | Oct 2024 | Initial release |

---

**Last Updated**: November 19, 2024

**For the latest version, visit**: https://github.com/Kikorangee/UCCL-Dashboard/

