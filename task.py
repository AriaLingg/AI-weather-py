import python_weather
import asyncio

class WeatherTask:
    def __init__(self):
        # Initialize the client without format argument
        self.client = python_weather.Client()

    async def fetch_weather(self, location):
        try:
            # Fetch weather data for the specified location
            weather = await self.client.get(location)
            return weather
        except Exception as e:
            print(f"An error occurred while fetching the weather for {location}: {e}")
            return None

    async def close_client(self):
        try:
            # Properly close the client
            await self.client.close()
        except Exception as e:
            print(f"An error occurred while closing the client: {e}")
