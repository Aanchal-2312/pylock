"""Output formatting utilities.

Supports JSON and ENV-style formatting for CLI output."""
import json

def format_output(data, format_type=None):
    """Format data into JSON or ENV style output based on user preference."""
    if not format_type:
        return None

    # JSON FORMAT
    if format_type == "json":
        return json.dumps(data, indent=4)

    # ENV FORMAT
    elif format_type == "env":
        lines = []

        # Handle dictionary output
        if isinstance(data, dict):
            for k, v in data.items():
                lines.append(f"{k.upper()}={v}")
                
        # Handle list output
        elif isinstance(data, list):
            for i, v in enumerate(data, 1):
                lines.append(f"ITEM_{i}={v}")

        return "\n".join(lines)

    return None