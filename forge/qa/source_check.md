# 원본 대조 — 정답 실행 값 vs 교재 · facts.csv

정답 스크립트 `assets/answers/build_dashboard.py`를 실행한 값(`expected.json`)을 원본(교재 `textbook/ch1~3.md`, `facts.csv`)과 대조했다. 2026-10-31.

| 키 | Block | 정답 실행 값 | 원본 값 | 원본 위치 | 일치 |
|---|---|---|---|---|---|
| rows_total | 0 | 23 | 23행 | facts.csv | 같음 |
| rows_confirmed | 0 | 18 | '확인' 18행 | facts.csv 교차확인 열 | 같음 |
| rows_missing | 0 | 2 | F17 · F18 | facts.csv | 같음 |
| domestic_sum | 1 | 6조1,695억 원 | 6조1,695억 원 | ch1 2-3 · F07 | 같음 (F09+F10+F11 합도 같음) |
| parts_sw_share | 1 | 32.1 | 32.1% | ch1 2-3 · F11 비고 | 같음 |
| china_share | 1 | 54 | 54% | ch1 2-2 · F04 비고 | 같음 (계산 54.4%, 정수 반올림) |
| loc_min_part · loc_min | 2 | 감속기 35.8 | 감속기 35.8% | ch2 2-3 · F12 | 같음 |
| loc_max_part · loc_max | 2 | 제어기 47.9 | 제어기 47.9% | ch2 2-3 · F15 | 같음 |
| loc_over_half | 2 | 0 | "네 부품 모두 절반에 못 미친다" | ch2 2-3 | 같음 |
| hyundai_capacity · hyundai_year | 3 | 30,000 · 2028 | 연 30,000대 · 2028년 가동 목표 | ch3 2-1 · F21 | 같음 |
| hl_target · hl_share | 3 | 2조3,000억 원 · 10 | 2035년 매출 2조3,000억 원 · 점유율 10% | ch3 2-2 · F19 · F20 | 같음 |
| schaeffler_share | 3 | 50% 초과 | 관절 액추에이터 수요의 50% 초과 | ch3 2-2 · F22 | 같음 |

## 바로잡은 것

- 앞선 대화에서 facts.csv의 교차 확인 행을 "19행"이라고 말한 적이 있다. 실제로 '확인'은 18행이고, 나머지는 부분 확인 1행 · 단일 출처 2행 · 미확보 2행이다. curriculum.md도 18로 고쳤다.
