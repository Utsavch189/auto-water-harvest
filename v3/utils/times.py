from datetime import datetime

def get_current_time()->str:
    return datetime.now().strftime("%H:%M:%S")

if __name__=="__main__":
    print(get_current_time()<"16:34:00")