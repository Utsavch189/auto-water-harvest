from db.connection import conn,client
from utils import get_datetime

class Query:

    @staticmethod
    async def createRasp(id:str,username:str,password:str):
        exists_q="""
            SELECT * FROM Raspberry WHERE id='%s'
        """%(id,)

        insert_q="""
            INSERT INTO Raspberry(id,username,password,created_at) VALUES('%s','%s','%s','%s')
        """%(id,username,password,get_datetime())

        try:
            exists=client.exec_query(exists_q,conn)
            if not exists.get_result():
                client.exec_query(insert_q,conn)
            return
        except Exception as e:
            print(e)
    
    @staticmethod
    async def createDefaultTask(id:str,auto_harvest:bool,system_cooling:bool):
        exists_q="""
            SELECT * FROM RaspberryTaskControl WHERE raspberry_id='%s'
        """%(id,)

        insert_q="""
            INSERT INTO RaspberryTaskControl(raspberry_id,auto_harvest,system_cooling,uploaded_at) VALUES('%s',%d,%d,'%s')
        """%(id,auto_harvest,system_cooling,get_datetime())
        try:
            exists=client.exec_query(exists_q,conn)
            if not exists.get_result():
                client.exec_query(insert_q,conn)
            return
        except Exception as e:
            print(e)

    @staticmethod
    async def insert_error_log(rasp_id:str,error:str):
        q="""
            INSERT INTO ErrorLog(raspberry_id,error,created_at) VALUES('%s',"%s",'%s')
        """%(rasp_id,error,get_datetime())
        try:
            client.exec_query(q,conn)
        except Exception as e:
            print(e)
    
    @staticmethod
    async def insert_sensor_data(raspberry_id:str,temp_data:str,humidity_data:str,soil_moist_data:str):
        q="""
            INSERT INTO RaspSensorData(raspberry_id,temp_data,humidity_data,soil_moist_data,uploaded_at) VALUES('%s','%s','%s','%s','%s')
            """%(raspberry_id,str(temp_data),str(humidity_data),str(soil_moist_data),get_datetime())
        try:
            client.exec_query(q,conn)
        except Exception as e:
            print(e)

            
    @staticmethod
    async def insert_system_data(raspberry_id:str,cpu_temperature:str,cpu_usage:str,memory_usage:str,disk_usage:str,network_stats:str,system_uptime:str,core_info:str):
        q="""
            INSERT INTO RaspberrySystem(raspberry_id,cpu_temperature,cpu_usage,memory_usage,disk_usage,network_stats,system_uptime,core_info,uploaded_at)
            VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')
            """%(raspberry_id,cpu_temperature,cpu_usage,memory_usage,disk_usage,network_stats,system_uptime,core_info,get_datetime())
        # print(q)
        try:
            client.exec_query(q,conn)
        except Exception as e:
            print(e)
    
    @staticmethod
    async def get_updated_task(raspberry_id:str):
        q="""
            SELECT * FROM RaspberryTaskControl WHERE raspberry_id='%s'
        """%(raspberry_id,)
        try:
            res=client.exec_query(q,conn)
            data=[]
            for i in res:
                data.append(i)
            return data
        except Exception as e:
            print(e)