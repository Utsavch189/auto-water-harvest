import psutil
import socket
import requests
import platform
from decouple import config
from typing import Union
import multiprocessing

class SystemParameters:

    def __init__(self) -> None:
        pass
    
    def get_creds(self):
        try:
            return {
                "id":config('ID'),
                "name":config("NAME"),
                "pswd":config("PASSWORD")
            }
        except Exception as e:
            return None

    def get_cpu_temperature(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
                temp_str = file.readline().strip()
                temp_c = int(temp_str) / 1000.0  # Convert from millidegree Celsius to degree Celsius
                return temp_c
        except FileNotFoundError:
            return None
        except Exception as e:
            return None
    
    def get_system_info(self):
        try:
            uname = platform.uname()
            return {
                "system": uname.system,
                "node_name": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
                "processor": uname.processor
            }
        except Exception as e:
            return None
    
    def get_cpu_usage(self):
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            return None

    def get_memory_usage(self):
        try:
            mem = psutil.virtual_memory()
            return {
                "total": f"{mem.total / (1024 ** 3):.2f} GB",  # Convert bytes to GB
                "available": f"{mem.available / (1024 ** 3):.2f} GB",
                "used": f"{mem.used / (1024 ** 3):.2f} GB",
                "percentage": mem.percent
            }
        except Exception as e:
            return None

    def get_disk_usage(self):
        try:
            path='/'
            disk = psutil.disk_usage(path)
            return {
                "total": f"{disk.total / (1024 ** 3):.2f} GB",  # Convert bytes to GB
                "used": f"{disk.used / (1024 ** 3):.2f} GB",
                "free": f"{disk.free / (1024 ** 3):.2f} GB",
                "percentage": disk.percent
            }
        except Exception as e:
            return None

    def get_network_stats(self):
        try:
            net = psutil.net_io_counters()
            return {
                "bytes_sent": net.bytes_sent ,  # In bytes
                "bytes_recv": net.bytes_recv ,
                "packets_sent": net.packets_sent,
                "packets_recv": net.packets_recv,
                "public_ip":self.getPublicIp,
                "private_ip":self.getLocalIp
            }
        except Exception as e:
            return None

    def get_system_uptime(self):
        try:
            return psutil.boot_time()
        except Exception as e:
            return None

    @property    
    def getLocalIp(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception as e:
            return None

    @property
    def getPublicIp(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            ip_data = response.json()
            return ip_data['ip']
        except Exception as e:
            print(f"Unable to get public IP address: {e}")
            return None


class System:

    def __init__(self) -> None:
        self.sp=SystemParameters()
    
    def _worker_function(self,item):
        key, func = item
        result = func()
        return (key, result)

    @property
    def get_system_status(self)->Union[dict,None]:

        _data={
            "cpu_temperature": self.sp.get_cpu_temperature,
            "cpu_usage": self.sp.get_cpu_usage,
            "memory_usage": self.sp.get_memory_usage,
            "disk_usage": self.sp.get_disk_usage,
            "network_stats": self.sp.get_network_stats,
            "system_uptime": self.sp.get_system_uptime,
            "core_info":self.sp.get_system_info,
            "creds":self.sp.get_creds
        }

        manager = multiprocessing.Manager()
        _results = manager.dict()
        pool = multiprocessing.Pool(processes=4)
        async_results = [pool.apply_async(self._worker_function, args=((key, func),)) for key, func in _data.items()]

        for async_result in async_results:
            key, result = async_result.get()
            _results[key] = result
        
        pool.close()
        pool.join()

        for k,v in _results.items():
            if v==None:
                return None
            
        return _results
    
if __name__=="__main__":
    s=System()
    print(s.get_system_status)
    