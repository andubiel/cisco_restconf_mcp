import requests
import urllib3
from mcp.server.fastmcp import FastMCP

# Suppress SSL warnings for lab environments using self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize FastMCP Server
mcp = FastMCP("Cisco RESTCONF Inventory Server")

# Define your network inventory here
INVENTORY = {
    "leaf1": {
        "ip": "192.168.0.10",  # Example placeholder for scaling
        "port": 443,
        "auth": ("admin", "admin")
    },
    "leaf2": {
        "ip": "192.168.0.20",  # Example placeholder for scaling
        "port": 443,
        "auth": ("admin", "admin")
    }
}

@mcp.tool()
async def get_restconf_data(device_name: str, yang_path: str) -> dict:
    """
    Query Cisco IOS-XE data using RESTCONF data models for a specific device in the inventory.
    
    Args:
        device_name: The name of the device to query (e.g., 'leaf1', 'leaf2').
        yang_path: The native or IETF YANG data model path (e.g., 'Cisco-IOS-XE-native:native/interface').
    """
    # Normalize the input string
    target = device_name.lower().strip()
    
    # Inventory lookup safety check
    if target not in INVENTORY:
        return {
            "error": f"Device '{device_name}' not found in inventory.", 
            "available_devices": list(INVENTORY.keys())
        }
    
    device = INVENTORY[target]
    clean_path = yang_path.lstrip("/")
    url = f"https://{device['ip']}:{device['port']}/restconf/data/{clean_path}"
    
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }
    
    try:
        response = requests.get(
            url,
            auth=device["auth"],
            headers=headers,
            verify=False
        )
        if response.status_code in [200, 201, 204]:
            return response.json()
        return {"error": f"HTTP {response.status_code}", "details": response.text}
    except requests.exceptions.RequestException as e:
        return {"error": "Connection Failed", "details": str(e)}

if __name__ == "__main__":
    mcp.run()
