import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import asyncio
from typing import Any
from agents import Agent, ItemHelpers, MessageOutputItem, Runner, TResponseInputItem, ToolCallItem, ToolCallOutputItem, function_tool, trace
from agents.mcp import MCPServer, MCPServerStdio
from datetime import datetime
import logging

# Import both real and dummy weather functions
# from weather import get_alerts, get_forecast
from dummy_weather import get_alerts as dummy_get_alerts, get_forecast as dummy_get_forecast

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

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
    logging.info(f"Called get_weather_alerts with state={state}")
    try:
        result = await dummy_get_alerts(state)
        logging.info(f"get_weather_alerts result: {result.strip()[:100]}...")
        return result
    except Exception as e:
        logging.error(f"Error with real get_alerts: {e}")
        return await dummy_get_alerts(state)

@function_tool
async def get_weather_forecast(latitude: float, longitude: float) -> str:
    logging.info(f"Called get_weather_forecast with latitude={latitude}, longitude={longitude}")
    try:
        result = await dummy_get_forecast(latitude, longitude)
        logging.info(f"get_weather_forecast result: {result.strip()[:100]}...")
        return result
    except Exception as e:
        logging.error(f"Error with real get_forecast: {e}")
        return await dummy_get_forecast(latitude, longitude)

# For now, the agent is constructed without mcp_servers, just with tools.
async def main():
    # If you want to use MCPServerStdio, set it up here with async context
    # Example (uncomment and adjust if needed):
    # async with MCPServerStdio(...) as server:
    #     agent = Agent(..., mcp_servers=[server])
    #     ...
    # For now, just instantiate the agent as befor
    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "uv",
            "args": [
              "--directory",
              "/workspaces/ai-launchpad/mcp/weather",
              "run",
              "/workspaces/ai-launchpad/mcp/weather/weather.py"
            ]
        },
    ) as server:
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
          # tools=[get_weather_alerts, get_weather_forecast],
          mcp_servers=[server],
      )
      await chat_loop(weather_agent)


# Main function to run the chat loop
async def chat_loop(agent: Agent):
    chat_history: list[TResponseInputItem] = []
    logging.info("Weather Assistant chat loop started.")
    # """Run the main chat loop for the weather assistant."""
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
        logging.info(f"User input: {user_input}")
        with trace("Weather Service", group_id=conversation_id):
            chat_history.append({"content": user_input, "role": "user"})
            result = await Runner.run(agent, chat_history)
            logging.info(f"Agent result: {result.final_output}")
            for new_item in result.new_items:
                agent_name = new_item.agent.name
                logging.debug(f"Processing new item of type {new_item.__class__.__name__} from {agent_name}")
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

            if user_input.lower() in ["exit", "quit"]:
                break


# Run the chat loop when the script is executed
if __name__ == "__main__":
    logging.info("Starting Weather Assistant main entry point.")
    asyncio.run(main())