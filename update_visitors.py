import json
from datetime import datetime, timezone, timedelta

COUNT_FILE = "visitor_count.json"
README_FILE = "README.md"

# -----------------------------
# Settings
# -----------------------------
# Korea Standard Time (KST) 기준으로 Today를 리셋
KST = timezone(timedelta(hours=9))
today_kst = datetime.now(KST).strftime("%Y-%m-%d")

start = "<!-- VISITOR-COUNT:START -->"
end = "<!-- VISITOR-COUNT:END -->"

# 배지 디자인 (세련된 초록/블랙 톤)
# - TODAY: 초록 (16a34a)
# - TOTAL: 블랙 (0b0f14)
# - style: for-the-badge
# - label: 아이콘 느낌 추가(emoji는 URL 인코딩 문제 없게 %로 처리)
TODAY_LABEL = "%F0%9F%91%81%20TODAY"   # 👁 TODAY
TOTAL_LABEL = "%E2%88%91%20TOTAL"     # ∑ TOTAL

TODAY_COLOR = "16a34a"
TOTAL_COLOR = "0b0f14"
STYLE = "for-the-badge"

# -----------------------------
# Load count
# -----------------------------
with open(COUNT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# 날짜 바뀌면 today reset (KST 기준)
if data.get("last_date") != today_kst:
    data["today"] = 0
    data["last_date"] = today_kst

# GitHub Action 실행 = 방문 1회로 간주
data["today"] = int(data.get("today", 0)) + 1
data["total"] = int(data.get("total", 0)) + 1

# save json
with open(COUNT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# -----------------------------
# Update README
# -----------------------------
with open(README_FILE, "r", encoding="utf-8") as f:
    readme = f.read()

if start not in readme or end not in readme:
    raise ValueError("README.md에 VISITOR-COUNT 마커가 없습니다. (START/END 주석을 확인하세요)")

# Shields 배지 URL (label / message / color / style)
today_badge = (
    f"https://img.shields.io/badge/{TODAY_LABEL}-{data['today']}-{TODAY_COLOR}"
    f"?style={STYLE}"
)
total_badge = (
    f"https://img.shields.io/badge/{TOTAL_LABEL}-{data['total']}-{TOTAL_COLOR}"
    f"?style={STYLE}"
)

# (선택) 아주 미세하게 고급스럽게: 배지 사이 간격 + 중앙정렬 유지
new_block = f"""{start}
<p align="center">
  <img src="{today_badge}" alt="today views" />
  <img src="{total_badge}" alt="total views" />
</p>
{end}"""

# 기존 블록 교체
old_inner = readme.split(start)[1].split(end)[0]
readme = readme.replace(start + old_inner + end, new_block)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(readme)
