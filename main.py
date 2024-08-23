import os
import asyncio
from dotenv import load_dotenv
from agent import WeatherAgent

load_dotenv(".env")

async def main(region):
    # Initialize the weather agent with your LLM model and OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    os.environ["OPENAI_API_KEY"] = api_key
    
    agent = WeatherAgent(api_key=api_key)
    await agent.run(region=region)

if __name__ == "__main__":
    asyncio.run(main())
