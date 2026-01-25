import json
from datetime import datetime

COUNT_FILE = "visitor_count.json"
README_FILE = "README.md"

today = datetime.utcnow().strftime("%Y-%m-%d")

# load count
with open(COUNT_FILE, "r") as f:
    data = json.load(f)

# 날짜 바뀌면 today reset
if data["last_date"] != today:
    data["today"] = 0
    data["last_date"] = today

# GitHub Action 실행 = 방문 1회로 간주
data["today"] += 1
data["total"] += 1

# save json
with open(COUNT_FILE, "w") as f:
    json.dump(data, f, indent=2)

# update README
with open(README_FILE, "r") as f:
    readme = f.read()

start = "<!-- VISITOR-COUNT:START -->"
end = "<!-- VISITOR-COUNT:END -->"

new_block = f"""{start}
<p align="center">
  <b>Today:</b> {data['today']} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Total:</b> {data['total']}
</p>
{end}"""

old_block = readme.split(start)[1].split(end)[0]
readme = readme.replace(start + old_block + end, new_block)

with open(README_FILE, "w") as f:
    f.write(readme)
