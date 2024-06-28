import io
import json

with open("jemba_rules.json", "r") as f:
    data = json.load(f)

keys = list(data.keys())
keys.sort()
sorted_dict = {i: data[i] for i in keys}

output = io.StringIO()
output.write("|Name|Rule|\n|----|----|\n")
for k, v in sorted_dict.items():
    output.write(f"{k.title()}|{v}|\n")

with open("jemba_rules.md", "w") as f:
    f.write(output.getvalue())
