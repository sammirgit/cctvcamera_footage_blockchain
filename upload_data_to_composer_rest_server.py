import os
import time
import hashlib
import requests
from datetime import datetime

request_url = 'http://localhost:3000/api/org.example.biznet.HashInfo'
counter = 0 
while True:
    try:
        hasher = hashlib.md5()
        with open('camera_feed.mp4', 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
            os.rename('camera_feed.mp4','camera_feed'+str(counter)+'.mp4')
            counter += 1
        hash_data = hasher.hexdigest()
        print(hash_data)
        request_data = {
            "$class": "org.example.biznet.HashInfo",
            "owner": "Redwan",
            "hash_data": hash_data.upper(),
            "upload_date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        rr = requests.post(url=request_url, data=request_data)
        if(rr.status_code == 200):
            print("Data successfully updated")
        else:
            print("There was a problem uploading the data")

    except Exception as e:
        print("file not generated yet...")
    time.sleep(10)