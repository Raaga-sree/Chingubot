import os
import json
base_dir=os.path.dirname(__file__)
file_path=os.path.join(base_dir,"intents.json")
with open(file_path,"r") as f:
    data=json.load(f)
print("Loaded intents:")
print(data)