import asyncio
import websockets
import json

uri = "ws://192.168.0.108:8000/ws"

async def send_weather_data():
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    weather_data = {
                        "temperature": 22.5,
                        "humidity": 60,
                        "pressure": 1012
                    }
                    await websocket.send(json.dumps(weather_data))
                    response = await websocket.recv()
                    print(f"Response from server: {response}")
                    await asyncio.sleep(5)  # Send data every 5 seconds
        except websockets.ConnectionClosed as e:
            print(f"Connection closed: {e}. Reconnecting...")
            await asyncio.sleep(5)  # Wait before attempting to reconnect
        except Exception as e:
            print(f"An error occurred: {e}. Reconnecting...")
            await asyncio.sleep(5)  # Wait before attempting to reconnect

asyncio.run(send_weather_data())