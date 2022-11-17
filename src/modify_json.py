import json
import datetime;

with open('sample.json', 'r+') as f:
    data = json.load(f)
    data['time'] = str(datetime.datetime.now())
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    f.truncate()     # remove remaining part