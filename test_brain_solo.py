import asyncio
from src.services.brain import Brain

async def test():
    print("Initializing Brain...")
    brain = Brain()
    print("Asking Gemini a question...")
    try:
        response = await brain.think("Hello, are you working?")
        print(f"SUCCESS! Gemini replied: {response}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test())