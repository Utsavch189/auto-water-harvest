from db.connection import conn,client
from utils import get_datetime

class Query:

    @staticmethod
    def createRasp(id:str,username:str,password:str):
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
    def createDefaultTask(id:str,auto_harvest:bool,system_cooling:bool):
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
    def insert_error_log(rasp_id:str,error:str):
        q="""
            INSERT INTO ErrorLog(raspberry_id,error,created_at) VALUES('%s',"%s",'%s')
        """%(rasp_id,error,get_datetime())
        try:
            client.exec_query(q,conn)
        except Exception as e:
            print(e)