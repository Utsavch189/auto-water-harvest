import board
from sensors import DHT11Sensor,SoilSensor
from relay import WaterPumpRelay
from cache import Cache
import asyncio
import websockets
from utils import System
from db import Query
from utils import decompress,compress,has_internet
from decouple import config
from mail.email import SendMail
import threading

URI=config('URI')


# Modules Init
relay=WaterPumpRelay(pin=4)
dht=DHT11Sensor(board_pin=board.D17)
soil_moist=SoilSensor()
cache=Cache(capacity=256)
system=System()

print(relay,' ',dht,' ',soil_moist,' ',system)

async def send_data():
    Query.createRasp(
        id=system.sp.get_creds['id'],
        username=system.sp.get_creds['name'],
        password=system.sp.get_creds['pswd']
    )
    Is_data_sending=False
    while True:
        try:
            if not has_internet():
                await asyncio.sleep(5)

            async with websockets.connect(URI) as websocket:
                    while True:
                        try:
                            print("cache data : ",cache.get('tasks'))
                            moist=soil_moist.getMoisture
                            soil_mositure=moist[0]
                            voltage=moist[1]
                            curr_temp=dht.getTemp
                            curr_humdt=dht.getHumidity
                            print("soil moist : ",soil_mositure)
                            print("voltage : ",voltage)
                            if cache.get('tasks'):
                                relay.match(
                                    auto_harvest=cache.get('tasks')[0]['auto_harvest'],
                                    soil_moist=soil_mositure
                                )
                            if not (moist and curr_temp and curr_humdt):
                                await asyncio.sleep(2)
                                continue
     
                            data={
                                "system":system.get_system_status,
                                "sensor":{
                                    "curr_temp":curr_temp,
                                    "curr_humdity":curr_humdt,
                                    "soil_moist":soil_mositure,
                                }
                            }
                            compressed_data=compress(data) # converts into bytes
                            await websocket.send(compressed_data)
                            print("------------ data sent to server -------")

                            if not Is_data_sending:
                                Is_data_sending=True
                                print('First Time...')
                                threading.Thread(
                                    target=SendMail.send_raw,
                                    args=('From Your Raspi...','Your First data is sent and data flow begins','utsavchatterjee71@gmail.com')
                                ).start()

                            response = await websocket.recv()
                            print("------------ data received from server -------")
                            decompressed_data=decompress(response) # converts into python dict
                            cache.put('tasks',decompressed_data)
                            await asyncio.sleep(1)  # Send data every 1 seconds
                        except websockets.ConnectionClosed as e:
                            print(f"Connection closed: {e}. Reconnecting...")
                            # Query.insert_error_log(
                            #     rasp_id=system.sp.get_creds['id'],
                            #     error=str(e)
                            # )
                            relay.relay.stop
                            await asyncio.sleep(5)  # Wait before attempting to reconnect
                        except Exception as e:
                            print(f"An error occurred: {e}. Reconnecting...")
                            # Query.insert_error_log(
                            #     rasp_id=system.sp.get_creds['id'],
                            #     error=str(e)
                            # )
                            relay.relay.stop
                            await asyncio.sleep(5)  # Wait before attempting to reconnect

                        except KeyboardInterrupt:
                            relay.relay.stop
                            exit()
        except Exception  as e:
            print(f"An error occurred: {e}. Reconnecting...")
            # Query.insert_error_log(
            #     rasp_id=system.sp.get_creds['id'],
            #     error=str(e)
            # )
            relay.relay.stop
            await asyncio.sleep(5)  # Wait before attempting to reconnect
            
        
        
if __name__=="__main__":
    asyncio.get_event_loop().run_until_complete(send_data())