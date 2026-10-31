"""로봇 밸류체인 결과 대시보드 — 정답 스크립트 (Block 0~3).

사용: 작업 폴더(data/ 가 있는 곳)에서 실행한다.
  python -I -X utf8 build_dashboard.py
읽는 것: data/facts.csv · data/sources.md · data/textbook/ch3.md
만드는 것: outputs/index.html (대시보드 한 장) · expected.json (확인할 수치)
Python 표준 라이브러리만 쓴다. facts.csv·교재에 없는 숫자는 만들지 않는다.
"""
import csv
import html
import json
import re
from pathlib import Path

DATA = Path("data")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

# ---- 자료 읽기 -------------------------------------------------------------
facts = {r["번호"]: r for r in csv.DictReader(open(DATA / "facts.csv", encoding="utf-8-sig"))}


def cite(code):
    """facts.csv '출처' 열(S1;S6)을 [S1][S6] 으로"""
    return "".join(f"[{s.strip()}]" for s in code.split(";") if s.strip())


def eok(text):
    """'6조1,695억' → 61695 (억 원 단위)"""
    m = re.fullmatch(r"(?:(\d+)조)?([\d,]+)억", text.replace(" ", ""))
    jo = int(m.group(1) or 0)
    return jo * 10000 + int(m.group(2).replace(",", ""))


def num(text):
    return float(text.replace(",", ""))


def md_table(md, after):
    """마크다운에서 'after' 제목 뒤 첫 표를 [머리, 행들]로"""
    part = md.split(after, 1)[1]
    rows = []
    for line in part.splitlines():
        if line.startswith("|"):
            if re.match(r"^\|\s*:?-{2,}", line):
                continue
            rows.append([c.strip().replace("**", "") for c in line.strip().strip("|").split("|")])
        elif rows:
            break
    return rows[0], rows[1:]


ch3 = (DATA / "textbook" / "ch3.md").read_text(encoding="utf-8")
src_md = (DATA / "sources.md").read_text(encoding="utf-8")
sources = []
for line in src_md.splitlines():
    m = re.match(r"^\| (S\d+) \| (.+?) \| (.+?) \| (.+?) \| (\S+) \| (.+?) \|$", line)
    if m and m.group(1) not in [s[0] for s in sources]:
        sources.append(m.groups())

# ---- Block 0: 자료 점검 ----------------------------------------------------
rows_total = len(facts)
rows_confirmed = sum(1 for r in facts.values() if r["교차확인"] == "확인")
missing = [r for r in facts.values() if r["값"] == "미확보"]

# ---- Block 1: 밸류체인 지도 -------------------------------------------------
total = eok(facts["F07"]["값"])
parts = [eok(facts[k]["값"]) for k in ("F09", "F10", "F11")]
assert sum(parts) == total, "세 부문 합이 전체 매출과 다르다"
parts_sw_share = round(parts[2] / total * 100, 1)                       # 32.1
china_share = round(num(facts["F04"]["값"]) / num(facts["F01"]["값"]) * 100)  # 54

# ---- Block 2: 국산화율 -----------------------------------------------------
loc = [(facts[k]["항목"].split("— ")[-1], float(facts[k]["값"]), cite(facts[k]["출처"]))
       for k in ("F12", "F13", "F14", "F15")]
loc_min = min(loc, key=lambda x: x[1])
loc_max = max(loc, key=lambda x: x[1])
loc_over_half = sum(1 for x in loc if x[1] >= 50)

# ---- Block 3: 진입 기회 -----------------------------------------------------
hyundai_capacity = int(num(facts["F21"]["값"]))
hyundai_year = int(facts["F21"]["기준연도"].split()[0])
comp_head, comp_rows = md_table(ch3, "### 2-2. 먼저 들어간 회사들")
match_head, match_rows = md_table(ch3, "### 2-3. 역량 매칭표")

# ---- 대시보드 ---------------------------------------------------------------
e = html.escape


def card(big, cap):
    return f'<div class="card"><div class="big">{e(big)}</div><div class="cap">{e(cap)}</div></div>'


def table(head, rows):
    th = "".join(f"<th>{e(h)}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


f = facts
sec1 = (
    '<div class="cards">'
    + card(f"{f['F01']['값']}대", f"2024년 세계 신규 설치 {cite(f['F01']['출처'])}")
    + card(f"{f['F02']['값']}대", f"2024년 세계 가동 대수 · 전년 대비 9% 증가 {cite(f['F02']['출처'])}")
    + card(f"{f['F03']['값']}대", f"2025년 신규 설치 (전망) {cite(f['F03']['출처'])}")
    + card(f"{china_share}%", f"2024년 설치 중 중국 비중 · {f['F04']['값']}대 {cite(f['F04']['출처'])}")
    + "</div>"
    + table(["부문 (2024)", "매출", "출처"], [
        ["제조업용 로봇", f"{f['F09']['값']} 원", cite(f["F09"]["출처"])],
        ["서비스용 로봇", f"{f['F10']['값']} 원", cite(f["F10"]["출처"])],
        ["로봇 부품·소프트웨어", f"{f['F11']['값']} 원 ({parts_sw_share}%)", cite(f["F11"]["출처"])],
        ["합계", f"{f['F07']['값']} 원 (전년 대비 3.2% 증가)", cite(f["F07"]["출처"])],
    ])
    + f'<p class="note">로봇 밀도 {f["F06"]["값"]}대(제조업 종사자 1만 명당, 2024, 세계 1위) {cite(f["F06"]["출처"])}</p>'
)

bars = "".join(
    f'<div class="row"><span class="lbl">{e(n)}</span><span class="track">'
    f'<span class="bar" style="width:{v}%"></span><span class="half"></span></span>'
    f'<span class="val">{v:.1f}</span></div>'
    for n, v, _ in loc
)
sec2 = (
    f'<div class="chart" role="img" aria-label="국산화율 감속기 35.8 모터 38.8 센서 42.5 제어기 47.9">{bars}'
    '<div class="axis"><span>0</span><span>50</span><span>100</span></div></div>'
    f'<p class="note">단위 %, {f["F12"]["기준연도"]}년 기준 {cite(f["F12"]["출처"])} · 점선 = 절반(50%)</p>'
    + table(["무엇을 보나", "값", "표기"], [
        ["휴머노이드 원가 중 액추에이터", f"{f['F16']['값']}%", f"보도 기준 추정 {cite(f['F16']['출처'])}"],
    ] + [[r["항목"], "미확보", "공개 원자료 없음 — 추정해서 채우지 않음"] for r in missing])
)

sec3 = (
    '<div class="cards two">'
    + card(f"연 {f['F21']['값']}대", f"현대차그룹 미국 로봇 공장 생산능력 {cite(f['F21']['출처'])}")
    + card(f"{hyundai_year}년", f"가동 목표 {cite(f['F21']['출처'])}")
    + "</div>"
    + "<h3>먼저 들어간 회사들</h3>" + table(comp_head, comp_rows)
    + '<p class="note">HL만도 숫자는 회사 목표, Schaeffler 숫자는 회사 발표 기준(다른 출처로 확인하지 못함).</p>'
    + "<h3>역량 매칭표</h3>" + table(match_head, match_rows)
)

src_rows = "".join(
    f'<li><b>{s[0]}</b> {e(s[1])} · {e(s[2])} · {e(s[3])} · <a href="{e(s[4])}">{e(s[4])}</a></li>' for s in sources
)

page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>로봇 밸류체인 대시보드</title>
<style>
:root{{--navy:#1B2C5E;--blue:#2E5BAA;--ink:#3B4252;--muted:#6B7280;--line:#D6D6DB;--gray:#F4F5F9;--bg:#FFFFFF}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif;color:var(--ink);background:var(--bg);line-height:1.55}}
main{{max-width:1080px;margin:0 auto;padding:24px 16px 48px}}
h1{{color:var(--navy);font-size:1.6rem;margin:0 0 6px}}
h2{{color:var(--navy);font-size:1.25rem;border-bottom:2px solid var(--navy);padding-bottom:6px;margin:36px 0 14px}}
h3{{color:var(--blue);font-size:1.05rem;margin:22px 0 8px}}
.lead{{background:var(--gray);border-left:5px solid var(--navy);padding:12px 14px;margin:14px 0}}
.meta,.note{{color:var(--muted);font-size:.9rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:14px}}
.card{{background:var(--gray);border-radius:8px;padding:16px;text-align:center}}
.big{{color:var(--navy);font-size:1.6rem;font-weight:700}}
.cap{{color:var(--muted);font-size:.88rem;margin-top:6px}}
.tw{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-size:.93rem}}
th{{background:var(--navy);color:#fff;text-align:left;padding:8px}}
td{{border-bottom:1px solid var(--line);padding:8px;vertical-align:top;word-break:keep-all}}
tbody tr:nth-child(even){{background:var(--gray)}}
.chart{{margin:6px 0}}
.row{{display:flex;align-items:center;gap:10px;margin:8px 0}}
.lbl{{width:4.2em;text-align:right;flex:none}}
.track{{position:relative;flex:1;height:30px;background:var(--gray);border-radius:4px}}
.bar{{position:absolute;left:0;top:0;bottom:0;background:var(--blue);border-radius:0 4px 4px 0}}
.half{{position:absolute;left:50%;top:-4px;bottom:-4px;border-left:2px dashed var(--muted)}}
.val{{width:3em;font-weight:700;color:var(--navy);flex:none}}
.axis{{display:flex;justify-content:space-between;margin:0 calc(3em + 10px) 0 calc(4.2em + 10px);color:var(--muted);font-size:.85rem}}
ul.src{{padding-left:18px;font-size:.88rem}} ul.src li{{margin:4px 0;word-break:break-all}}
a{{color:var(--blue)}}
</style></head>
<body><main>
<h1>로봇 밸류체인 — 자동차 부품사는 어느 고리에서 기회를 잡을 수 있는가</h1>
<p class="meta">공개 자료만 사용 · 자료 기준일 2026-10-31 · 숫자 옆 [S번호]는 맨 아래 출처 목록의 번호</p>
<p class="lead">부품 고리는 국내 로봇 매출의 {parts_sw_share}%다 {cite(f['F11']['출처'])}. 핵심 부품 국산화율은 모두 절반 미만이고 {cite(f['F12']['출처'])},
먼저 들어간 자동차 부품사는 액추에이터와 비전을 골랐다 [S9][S10][S14][S15].</p>

<h2>1장 로봇 밸류체인 지도</h2>
{sec1}

<h2>2장 핵심 부품과 공급 구도</h2>
{sec2}

<h2>3장 자동차 부품사의 진입 기회</h2>
{sec3}

<h2>출처</h2>
<ul class="src">{src_rows}</ul>
<p class="note">미확보 항목은 지어내지 않고 비워 두었다. 우리 회사 워크시트는 사내 자료라 이 페이지에 넣지 않는다.</p>
</main></body></html>
"""
(OUT / "index.html").write_text(page, encoding="utf-8")

# ---- expected.json ---------------------------------------------------------
V = lambda v, d, b: {"value": v, "decimals": d, "block": b}
expected = {"values": {
    "rows_total": V(rows_total, 0, 0),
    "rows_confirmed": V(rows_confirmed, 0, 0),
    "rows_missing": V(len(missing), 0, 0),
    "domestic_sum": V(f["F07"]["값"] + " 원", None, 1),
    "parts_sw_share": V(parts_sw_share, 1, 1),
    "china_share": V(china_share, 0, 1),
    "loc_min_part": V(loc_min[0], None, 2),
    "loc_min": V(loc_min[1], 1, 2),
    "loc_max_part": V(loc_max[0], None, 2),
    "loc_max": V(loc_max[1], 1, 2),
    "loc_over_half": V(loc_over_half, 0, 2),
    "hyundai_capacity": V(hyundai_capacity, 0, 3),
    "hyundai_year": V(hyundai_year, 0, 3),
    "hl_target": V(f["F19"]["값"] + " 원", None, 3),
    "hl_share": V(int(num(f["F20"]["값"])), 0, 3),
    "schaeffler_share": V(f["F22"]["값"].replace(" 초과", "% 초과"), None, 3),
}}
Path("expected.json").write_text(json.dumps(expected, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v["value"] for k, v in expected["values"].items()}, ensure_ascii=False))
