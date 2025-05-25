
import asyncio
from typing import Any
from agents import Agent, ItemHelpers, MessageOutputItem, Runner, TResponseInputItem, ToolCallItem, ToolCallOutputItem, function_tool, trace
from datetime import datetime

# Import both real and dummy weather functions
# from weather import get_alerts, get_forecast
from dummy_weather import get_alerts as dummy_get_alerts, get_forecast as dummy_get_forecast

# Get today's date
today = datetime.now().strftime("%d %B, %Y")

# City coordinates dictionary
CITIES = {
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "houston": (29.7604, -95.3698),
    "phoenix": (33.4484, -112.0740),
    "philadelphia": (39.9526, -75.1652),
    "san antonio": (29.4241, -98.4936),
    "san diego": (32.7157, -117.1611),
    "dallas": (32.7767, -96.7970),
    "san jose": (37.3382, -121.8863)
}

# Function tools for the agent
@function_tool
async def get_weather_alerts(state: str) -> str:
    """Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    try:
        return await dummy_get_alerts(state)
    except Exception as e:
        print(f"Error with real get_alerts: {e}")
        return await dummy_get_alerts(state)

@function_tool
async def get_weather_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    try:
        return await dummy_get_forecast(latitude, longitude)
    except Exception as e:
        print(f"Error with real get_forecast: {e}")
        return await dummy_get_forecast(latitude, longitude)

# Create a weather assistant agent
weather_agent = Agent(
    name="Weather Assistant",
    instructions=f"""You are a helpful weather assistant that can provide weather forecasts and alerts.
You have access to the following tools:
1. get_weather_alerts(state): Get weather alerts for a US state (use two-letter state code)
2. get_weather_forecast(latitude, longitude): Get weather forecast for a location

When users ask about weather in a specific location, try to determine the approximate coordinates.
Here are some common city coordinates:
- New York City: 40.7128, -74.0060
- Los Angeles: 34.0522, -118.2437
- Chicago: 41.8781, -87.6298
- Houston: 29.7604, -95.3698
- Phoenix: 33.4484, -112.0740
- Philadelphia: 39.9526, -75.1652
- San Antonio: 29.4241, -98.4936
- San Diego: 32.7157, -117.1611
- Dallas: 32.7767, -96.7970
- San Jose: 37.3382, -121.8863

Today's date is {today}.
Always be helpful, concise, and accurate with weather information.
""",
    tools=[get_weather_alerts, get_weather_forecast],
)

# Function to extract city coordinates if mentioned in the query
def extract_city_coordinates(query: str) -> tuple[float, float] | None:
    """Extract coordinates if a known city is mentioned in the query."""
    query_lower = query.lower()
    for city, coords in CITIES.items():
        if city in query_lower:
            return coords
    return None

# Main function to run the chat loop
async def chat_loop():
    agent: Agent = weather_agent
    chat_history: list[TResponseInputItem] = []


    """Run the main chat loop for the weather assistant."""
    print("🌤️  Welcome to the Weather Assistant! 🌤️")
    print("You can ask about weather forecasts and alerts.")
    print("Examples:")
    print("  - What's the weather like in New York?")
    print("  - Are there any weather alerts in CA?")
    print("  - Get the forecast for Chicago")
    print("\nType 'exit' or 'quit' to end the conversation.")
    
    # Generate a unique conversation ID
    conversation_id = f"weather-convo-{datetime.now().strftime('%Y%m%d%H%M%S')}"


    # Configure max turns per interaction
    max_turns = 5
    
    while True:
        user_input = input("Enter your message: ")
        with trace("Weather Service", group_id=conversation_id):
            chat_history.append({"content": user_input, "role": "user"})
            result = await Runner.run(agent, chat_history)

            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, ToolCallItem):
                    print(f"{agent_name}: Calling a tool: {new_item.raw_item}")
                elif isinstance(new_item, ToolCallOutputItem):
                    print(f"{agent_name}: Tool call output: {new_item.output}")
                else:
                    print(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")
            chat_history = result.to_input_list()

            # # Update chat history with the original user input (not enriched)
            # chat_history.append({"role": "user", "content": user_input})
            # chat_history.append({"role": "assistant", "content": result.final_output})
            
            # # Use result.to_input_list() for the next turn to maintain proper context
            # # But limit history size to keep context manageable
            # if len(result.to_input_list()) > 10:
            #     # Keep only the most recent exchanges
            #     chat_history = result.to_input_list()[-10:]

            # Print the agent's response
            print("" + "-" * 40)
            print(f"\nAssistant: {result.final_output}")


# Run the chat loop when the script is executed
if __name__ == "__main__":
    asyncio.run(chat_loop())