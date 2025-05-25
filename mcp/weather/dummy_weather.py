"""
Dummy functions for weather alerts and forecasts
"""
import asyncio

async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    # Return mock data based on state
    if state == "NY":
        return """
Event: Flood Watch
Area: New York City, NY
Severity: Moderate
Description: Potential flooding in low-lying areas due to heavy rainfall.
Instructions: Monitor local weather reports and avoid flood-prone areas.
"""
    elif state == "CA":
        return """
Event: Heat Advisory
Area: Southern California
Severity: Moderate
Description: Temperatures expected to reach 95-100°F in some areas.
Instructions: Stay hydrated and avoid outdoor activities during peak hours.
"""
    elif state == "FL":
        return """
Event: Tropical Storm Watch
Area: South Florida
Severity: High
Description: Tropical storm conditions possible within 48 hours.
Instructions: Review evacuation plans and secure outdoor items.
"""
    elif state == "TX":
        return """
Event: Severe Thunderstorm Warning
Area: North Texas
Severity: High
Description: Thunderstorms with damaging winds and possible hail.
Instructions: Move to an interior room on the lowest floor of a building.
"""
    else:
        return f"No active alerts for {state}."

async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # New York City
    if abs(latitude - 40.7128) < 0.1 and abs(longitude - (-74.0060)) < 0.1:
        return """
Today:
Temperature: 75°F
Wind: 10 mph NW
Forecast: Partly cloudy with a chance of showers in the afternoon.

Tonight:
Temperature: 55°F
Wind: 5 mph NW
Forecast: Clearing skies, cooler temperatures.

Tomorrow:
Temperature: 72°F
Wind: 8 mph SW
Forecast: Mostly sunny and pleasant.
"""
    # Los Angeles
    elif abs(latitude - 34.0522) < 0.1 and abs(longitude - (-118.2437)) < 0.1:
        return """
Today:
Temperature: 78°F
Wind: 8 mph W
Forecast: Sunny and warm with clear skies.

Tonight:
Temperature: 62°F
Wind: 5 mph SW
Forecast: Clear and mild.

Tomorrow:
Temperature: 80°F
Wind: 7 mph W
Forecast: Continued sunny and warm.
"""
    # Chicago
    elif abs(latitude - 41.8781) < 0.1 and abs(longitude - (-87.6298)) < 0.1:
        return """
Today:
Temperature: 65°F
Wind: 12 mph NE
Forecast: Mostly cloudy with occasional light rain.

Tonight:
Temperature: 52°F
Wind: 8 mph NE
Forecast: Cloudy with occasional showers.

Tomorrow:
Temperature: 68°F
Wind: 10 mph E
Forecast: Partly cloudy with a slight chance of showers.
"""
    # Default for any other location
    else:
        return f"""
Today:
Temperature: 70°F
Wind: 8 mph Variable
Forecast: Typical seasonal weather for coordinates {latitude}, {longitude}.

Tonight:
Temperature: 58°F
Wind: 5 mph Variable
Forecast: Clear skies.

Tomorrow:
Temperature: 72°F
Wind: 7 mph Variable
Forecast: Partly cloudy.
"""

# Test the functions if run directly
if __name__ == "__main__":
    async def test():
        print("TESTING ALERTS:")
        print(await get_alerts("NY"))
        print("\nTESTING FORECAST:")
        print(await get_forecast(40.7128, -74.0060))
    
    asyncio.run(test())
