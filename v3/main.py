import board
from sensors import DHT11Sensor,SoilSensor
from relay import WaterPumpRelay
from cache import Cache
from utils import System
from db import Query
from utils import has_internet
from decouple import config
from mail.email import SendMail
import threading
import asyncio
import json


# Modules Init
relay=WaterPumpRelay(pin=4,moist_threasold=18000)
dht=DHT11Sensor(board_pin=board.D17)
soil_moist=SoilSensor()
cache=Cache(capacity=256)
system=System()

# print(relay,' ',dht,' ',soil_moist,' ',system)

async def send_data():
    await asyncio.gather(
        Query.createRasp(
            id=system.sp.get_creds()['id'],
            username=system.sp.get_creds()['name'],
            password=system.sp.get_creds()['pswd']
        ),
        Query.createDefaultTask(
            id=system.sp.get_creds()['id'],
            auto_harvest=True,
            pump_schedule_start_time='00:00:00',
            pump_schedule_end_time='00:00:00',
            system_cooling=True,
            pump_start_now=False
        )
    )
    Is_data_sending=False
    while True:
        try:
            if not has_internet():
                await asyncio.sleep(5)

            while True:
                try:
                    print("cache data ------------------------ : ",cache.get('tasks'),end="\n")
                    print("--------------------------------------")
                    moist=soil_moist.getMoisture
                    soil_mositure=moist[0]
                    voltage=moist[1]
                    curr_temp=dht.getTemp
                    curr_humdt=dht.getHumidity
                    system_data=system.get_system_status

                    if cache.get('tasks'):
                        relay.match(
                            auto_harvest=cache.get('tasks')[0]['auto_harvest'],
                            soil_moist=soil_mositure,
                            pump_start=cache.get('tasks')[0]['pump_schedule_start_time'],
                            pump_end=cache.get('tasks')[0]['pump_schedule_end_time'],
                            pump_start_now=cache.get('tasks')[0]['pump_start_now']
                        )

                    if not (moist and curr_temp and curr_humdt and system_data):
                        continue

                    
                    if not Is_data_sending:
                        Is_data_sending=True
                        print('First Time...')
                        threading.Thread(
                            target=SendMail.send_raw,
                            args=('From Your Raspi...','Your First data is sent and data flow begins','utsavchatterjee71@gmail.com')
                        ).start()
                    
                    try:
                        print('In db operation......')
                        await asyncio.gather(
                            Query.insert_system_data(
                                system_data['creds']['id'],
                                str(system_data['cpu_temperature']),
                                str(system_data['cpu_usage']),
                                json.dumps(system_data['memory_usage']),
                                json.dumps(system_data['disk_usage']),
                                json.dumps(system_data['network_stats']),
                                str(system_data['system_uptime']),
                                json.dumps(system_data['core_info'])
                            ),
                            Query.insert_sensor_data(
                                system_data['creds']['id'],
                                curr_temp,
                                curr_humdt,
                                soil_mositure
                            )
                        )
                        print("------------ data sent to db -------")
                        pass
                    except Exception as e:
                        print(f"Database operation error: {e}")

                    
                    try:
                        data=await Query.get_updated_task(
                            raspberry_id=system_data['creds']['id']
                        )
                        cache.put('tasks',data)
                        print("------------ data get from db -------")
                    except Exception as e:
                        print(f"Database fetch error: {e}")

                    
                    await asyncio.sleep(5)  # Send data every 1 second
                except Exception as e:
                    print(f"An error occurred: {e}. Reconnecting...")
                    Query.insert_error_log(
                        rasp_id=system.sp.get_creds()['id'],
                        error=str(e)
                    )
                    relay.relay.stop
                    await asyncio.sleep(5)  # Wait before attempting to reconnec
                except KeyboardInterrupt:
                    relay.relay.stop
                    exit()
        except Exception  as e:
            print(f"An error occurred: {e}. Reconnecting...")
            Query.insert_error_log(
                rasp_id=system.sp.get_creds()['id'],
                error=str(e)
            )
            relay.relay.stop
            await asyncio.sleep(5)  # Wait before attempting to reconnect
            
async def main():
    await send_data()
        
if __name__=="__main__":
    asyncio.run(main())