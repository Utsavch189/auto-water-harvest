from datetime import datetime

def get_datetime():
    current_datetime = datetime.now()
    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

print(get_datetime())