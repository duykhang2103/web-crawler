import json

data = []
with open("./phongvu-data.json", "rb") as f:
    data = json.load(f)

for x in data:
    print(x['system'][0])
    if x['system'] == "" or x['system'][0] == "":
        x['system'] = ""

with open("./phongvu-data.json", "w", encoding = "utf8") as f:
    json.dump(data, f, ensure_ascii = False, indent = 4)