import time
from datetime import datetime

def get_timestamp():
    return int(time.time())

def timestamp_to_time(ts):
    return datetime.fromtimestamp(ts).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


print(get_timestamp())
print(timestamp_to_time(1784709694))