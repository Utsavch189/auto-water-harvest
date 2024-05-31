from connection import conn,client

def createRaspberryTable():
    q="""
        CREATE TABLE IF NOT EXISTS Raspberry(
            id varchar(100) primary key,
            username varchar(100) unique,
            password varchar(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active Bool default true
        );
    """
    try:
        client.exec_query(q,conn)
    except Exception as e:
        print(e)
    finally:
        client.disconnect(conn)

def createRaspSensorTable():
    q="""
    create table if not exists RaspSensorData(
        id integer primary key autoincrement,
        raspberry_id varchar(100),
        temp_data varchar(10),
        humidity_data varchar(10),
        soil_moist_data varchar(10),
        uploaded_at timestamp default CURRENT_TIMESTAMP,
        foreign key(raspberry_id) references Raspberry(id)
    );
    """
    try:
        client.exec_query(q,conn)
    except Exception as e:
        print(e)
    finally:
        client.disconnect(conn)

def createRaspCoreSystemTable():
    q="""
        CREATE TABLE IF NOT EXISTS RaspberrySystem(
            id integer primary key autoincrement,
            raspberry_id varchar(100),
            cpu_temperature varchar(10),
            cpu_usage TEXT,
            memory_usage TEXT,
            disk_usage TEXT,
            network_stats TEXT,
            system_uptime varchar(50),
            core_info TEXT,
            uploaded_at timestamp default CURRENT_TIMESTAMP,
            foreign key(raspberry_id) references Raspberry(id)
        );
    """
    try:
        client.exec_query(q,conn)
    except Exception as e:
        print(e)
    finally:
        client.disconnect(conn)

def createRaspberryTaskControlTable():
    q="""
        CREATE TABLE IF NOT EXISTS RaspberryTaskControl(
            id integer primary key autoincrement,
            raspberry_id varchar(100),
            auto_harvest bool default true,
            pump_schedule_start timestamp default 0,
            pump_schedule_end timestamp default 0,
            system_cooling bool default true,
            uploaded_at timestamp default CURRENT_TIMESTAMP,
            foreign key(raspberry_id) references Raspberry(id)
        );
    """
    try:
        client.exec_query(q,conn)
    except Exception as e:
        print(e)
    finally:
        client.disconnect(conn)

def createErrorTable():

    q="""
        CREATE TABLE IF NOT EXISTS ErrorLog(
            id integer primary key autoincrement,
            error TEXT,
            raspberry_id varchar(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(raspberry_id) REFERENCES Raspberry(id)
        );
    """
    try:
        client.exec_query(q,conn)
    except Exception as e:
        print(e)
    finally:
        client.disconnect(conn)

if __name__=="__main__":
    # createRaspberryTable()
    # createRaspSensorTable()
    # createRaspCoreSystemTable()
    createRaspberryTaskControlTable()
    # createErrorTable()