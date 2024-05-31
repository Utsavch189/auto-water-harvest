from db.connection import conn,client

class Query:

    @staticmethod
    def createRasp(id:str,username:str,password:str):
        exists_q="""
            SELECT * FROM Raspberry WHERE id='%s'
        """%(id,)

        insert_q="""
            INSERT INTO Raspberry(id,username,password) VALUES('%s','%s','%s')
        """%(id,username,password)

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
            INSERT INTO ErrorLog(raspberry_id,error) VALUES('%s',"%s")
        """%(rasp_id,error)
        try:
            client.exec_query(q,conn)
        except Exception as e:
            print(e)