import asyncio
from task import WeatherTask
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Optional
import pytemperature

class WeatherAgent(Agent):
    weather_task: Optional[WeatherTask] = None
    def __init__(self, api_key):
        super().__init__(
            role="Weather Agent",
            goal="Provide accurate weather information",
            backstory=(
                "You are a knowledgeable agent tasked with fetching and relaying "
                "weather information for any location the user inquires about."
            )
        )
        self.llm = ChatOpenAI()
        self.weather_task = WeatherTask()

    async def run(self, region):
        print("Welcome to the Weather Agent!")
        try:
            user_input = region
            response = await self.handle_input(user_input)
            print(f"Agent: {response}")
            return response
        finally:
            await self.close()

    async def handle_input(self, user_input):
        llm_response = await self.llm.apredict(
            f"User asked about weather. Extract the location from this query: '{user_input}'."
        )
        location = llm_response.strip()  # Assuming the LLM extracts the location correctly

        # Check if a location was extracted
        if not location:
            return "Sorry, I couldn't extract a location from your query."
        
        print(location)

        weather_data = await self.weather_task.fetch_weather(location)
        
        # Check if weather data was fetched successfully
        if not weather_data:
            return f"Sorry, I couldn't fetch the weather data for '{location}'."

        weather_report = self.process_weather(weather_data, location)
        return weather_report

    def process_weather(self, weather_data, location):
        # Start constructing the forecast
        forecast = f"Here is the weather forecast for {location}:\n\n"
    
        # Current conditions
        forecast += "**Current Conditions:**\n"
        forecast += f"- Current Temperature: **{weather_data.temperature}°C**\n"
        forecast += f"- Sky: **{weather_data.kind}**\n"
        forecast += f"- Humidity: **{weather_data.humidity}%**\n"
        forecast += f"- Wind Speed: **{weather_data.wind_speed} km/h**\n"
        forecast += f"- Wind Direction: **{weather_data.wind_direction}**\n"
        forecast += f"- Precipitation: **{weather_data.precipitation} mm**\n"
        forecast += f"- UV Index: **{weather_data.ultraviolet}**\n\n"
    
        # Daily forecast
        forecast += "**Daily Forecast:**\n"
        for day in weather_data.daily_forecasts:
            forecast += (
                f"- **{day.date}**\n"
                f"  - High Temperature: **{day.highest_temperature}°C**\n"
                f"  - Low Temperature: **{day.lowest_temperature}°C**\n"
                f"  - Average Temperature: **{day.temperature}°C**\n"
                # f"  - Sky: **{day.kind}**\n"
                f"  - Snowfall: **{day.snowfall} cm**\n"
                f"  - Moon Phase: **{day.moon_phase.emoji} ({day.moon_phase.name})**\n"
                f"  - Hours of Sunlight: **{day.sunlight} hours**\n"
                f"  - Moon Illumination: **{day.moon_illumination}%**\n"
            )
    
            # Only add moonrise, moonset, sunrise, and sunset if they exist
            if day.moonrise:
                forecast += f"  - Moonrise: **{day.moonrise}**\n"
            if day.moonset:
                forecast += f"  - Moonset: **{day.moonset}**\n"
            if day.sunrise:
                forecast += f"  - Sunrise: **{day.sunrise}**\n"
            if day.sunset:
                forecast += f"  - Sunset: **{day.sunset}**\n"
    
            forecast += "\n"
    
        # Generate overall summary
        #summary = "Overall, the weather for the day is expected to be: The day is expected to be clear and sunny, ideal for outdoor activities."
        # avg_temp = sum(day.highest_temperature + day.lowest_temperature for day in weather_data.daily_forecasts) / (2 * len(weather_data.daily_forecasts))
    
        # if any(day.snowfall > 0 for day in weather_data.daily_forecasts):
        #     summary += "Expect some snow, so dress warmly."
        # elif all(day.kind == 'clear' for day in weather_data.daily_forecasts):
        #     summary += "The day is expected to be clear and sunny, ideal for outdoor activities."
        # else:
        #     summary += "Expect variable weather conditions. Stay prepared for changes."
    
        # forecast += summary
        return forecast
    



    async def close(self):
        try:
            await self.weather_task.close_client()
        except Exception as e:
            print(f"An error occurred while closing the client: {e}")

# To actually run this agent, you'd do something like this:
# if __name__ == "__main__":
#     agent = WeatherAgent(api_key="YOUR_API_KEY")
#     asyncio.run(agent.run())
