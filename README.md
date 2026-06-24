# cisco_restconf_mcp

A Model Context Protocol (MCP) server for querying Cisco IOS-XE devices using RESTCONF APIs.

## Overview

This MCP server provides **read-only** access to Cisco network devices via RESTCONF. It allows you to query device configuration and operational data using YANG data models.

## Features

- **Read-only operations**: Uses HTTP GET requests only - no configuration changes are made to devices
- **YANG data model support**: Query both native Cisco IOS-XE and IETF standard YANG models
- **Multi-device inventory**: Support for multiple devices with flexible configuration
- **Environment variable support**: Secure credential management via environment variables
- **SSL verification options**: Configurable SSL verification for lab environments

## cisco_restconf_mcp.py

The main server file `cisco_restconf_mcp.py` implements a FastMCP server with the following characteristics:

### Read-Only Design

The server uses **HTTP GET requests only** to query device data. No PUT, POST, PATCH, or DELETE operations are implemented, ensuring:
- No accidental configuration changes
- Safe for production environments
- Suitable for monitoring and auditing use cases

### Available Tool

**`get_restconf_data(device_name: str, yang_path: str)`**
- Queries RESTCONF data from a specific device
- Returns JSON-formatted YANG data
- Examples of `yang_path`:
  - `Cisco-IOS-XE-native:native/interface`
  - `ietf-interfaces:interfaces`
  - `Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization`

## Inventory Configuration

### Default Inventory

The inventory is defined in the `INVENTORY` dictionary and includes:
- `leaf1`, `leaf2`: Leaf switches
- `spine1`: Spine switch
- `router1`: Edge router

### Customizing for Your Environment

You can modify the inventory in two ways:

#### 1. Direct Code Modification

Edit the `INVENTORY` dictionary in `cisco_restconf_mcp.py`:

```python
INVENTORY = {
    "my-device": {
        "ip": "192.168.1.100",
        "port": 443,
        "auth": ("username", "password"),
        "device_type": "router",  # or "switch"
        "location": "site-name",
    },
}
```

#### 2. Environment Variables (Recommended)

Set environment variables before running the server:

```bash
# For leaf1
export LEAF1_IP="10.0.1.10"
export LEAF1_PORT="443"
export LEAF1_USERNAME="admin"
export LEAF1_PASSWORD="your-password"

# For router1
export ROUTER1_IP="10.0.2.1"
export ROUTER1_PORT="443"
export ROUTER1_USERNAME="admin"
export ROUTER1_PASSWORD="your-password"

# Global configuration
export RESTCONF_TIMEOUT="30"
export RESTCONF_VERIFY_SSL="false"  # Set to "true" for production
```

### Adding New Devices

To add a new device to the inventory:

1. Add an entry to the `INVENTORY` dictionary:
```python
"my-new-device": {
    "ip": os.getenv("MYNEWDEVICE_IP", "192.168.1.50"),
    "port": int(os.getenv("MYNEWDEVICE_PORT", "443")),
    "auth": (
        os.getenv("MYNEWDEVICE_USERNAME", "admin"),
        os.getenv("MYNEWDEVICE_PASSWORD", "password")
    ),
    "device_type": "router",
    "location": "datacenter2",
},
```

2. Set corresponding environment variables if desired

## Usage Example

Once connected via MCP, you can query devices:

```python
# Get interface configuration from leaf1
get_restconf_data(
    device_name="leaf1",
    yang_path="Cisco-IOS-XE-native:native/interface"
)

# Get CPU utilization from router1
get_restconf_data(
    device_name="router1", 
    yang_path="Cisco-IOS-XE-process-cpu-oper:cpu-usage/cpu-utilization"
)
```

## Security Notes

- Credentials can be stored in environment variables to avoid hardcoding
- SSL verification is disabled by default for lab environments with self-signed certificates
- Set `RESTCONF_VERIFY_SSL=true` for production environments with valid certificates
- Read-only operations minimize security risk

## Requirements

- Python 3.7+
- `requests` library
- `urllib3` library
- `mcp` (FastMCP) library
