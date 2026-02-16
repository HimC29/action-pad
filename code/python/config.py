"""Configuration loading and state management."""

import json

def load_config(config_path="config.json"):
    """Load button configuration from JSON file."""
    with open(config_path) as f:
        return json.load(f)

def create_states(btn_configs):
    """Initialize application state from configuration."""
    current_layer = btn_configs["active_layer"]
    
    btn_toggle = {}
    for i in range(16):
        btn_toggle[f"btn{i + 1}"] = False
    
    return {
        "current_layer": current_layer,
        "btn_toggle": btn_toggle
    }
