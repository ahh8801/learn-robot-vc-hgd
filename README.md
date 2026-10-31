# 로봇 밸류체인 — learn-robot-vc-hgd

자동차 부품사 재직자가 교재 「로봇 밸류체인」 3장을 따라 공개 자료 숫자로 결과 대시보드 한 장을 만들며 "우리 회사는 밸류체인의 어느 고리에 설 것인가"를 판단해 보는 자율학습 강의다. 수업은 Claude Code 스킬 `/learn-robot-vc-hgd`가 진행한다 (Skills as Curriculum). 이 강의는 ahh8801이 course-forge로 직접 만들었다.

- **강의 웹앱 (브라우저에서 바로 수강)**: https://ahh8801.github.io/learn-robot-vc-hgd/app/ — 교재 3장 · 판단형 퀴즈 4문항 · 대시보드 · 우리 회사 워크시트(입력 내용은 내 브라우저에만 저장)
- **결과 대시보드**: https://ahh8801.github.io/learn-robot-vc-hgd/
- **교재 PDF**: [docs/Robot_Value_Chain_Textbook.pdf](docs/Robot_Value_Chain_Textbook.pdf) · **강의 덱 PDF**: [docs/Robot_Value_Chain_Deck.pdf](docs/Robot_Value_Chain_Deck.pdf)
- 처음이면 [GUIDE.md](GUIDE.md)부터. 기본 환경은 Claude 데스크톱 앱(Code 탭). VS Code는 GUIDE 부록 B

## 설치 — 한 줄

Claude Code 입력칸에 붙여 넣는다.

```
npx skills add ahh8801/learn-robot-vc-hgd --agent claude-code --global --yes 를 실행해 줘
```

새 세션에서 `/learn-robot-vc-hgd`를 입력하면 수업이 시작된다.

## 블록

| Block | 주제 | 끝나면 생기는 것 |
|---|---|---|
| 0 | 준비 — 작업 폴더 · 자료 읽는 법 | `~/robot-vc` 작업 폴더와 `env_check.txt` |
| 1 | 로봇 밸류체인 지도 | 대시보드 1장 칸 (세계 시장 · 국내 매출 구조) |
| 2 | 핵심 부품과 공급 구도 | 대시보드 2장 칸 (국산화율 차트 · 미확보 표시) |
| 3 | 자동차 부품사의 진입 기회 | 대시보드 3장 칸 (진출 사례 · 역량 매칭) + 내 PC의 우리 회사 워크시트 |

블록마다 교재의 '생각해 볼 질문'을 재료로 한 판단형 퀴즈 1문항이 있다.

## 수업 방식

| 구분 | 내용 |
|---|---|
| 목표 — AI Native | AI에게 맡기는 것이 기본인 방식으로 일한다 |
| 방법 — Skills as Curriculum | 스킬이 블록마다 설명 → 실습 → STOP → 확인·퀴즈를 진행한다 |
| 형식 — 자율학습 | 강사 없이 자기 속도로, 퀴즈로 스스로 점검한다 |

## 원본 강의와 데이터 출처

| 자료 | 출처 | 구분 |
|---|---|---|
| 교재 「로봇 밸류체인」 1~3장 | 만든 사람이 공개 자료로 직접 정리 (자료 기준일 2026-10-31) | 교재 |
| `facts.csv` (23행) | 교재에 쓴 숫자. 행마다 출처 번호 S1~S15 | 공개 자료에서 뽑은 실제 숫자 · 가상 데이터 없음 |
| `sources.md` | IFR, 한국로봇산업진흥원 실태조사 보도, 언론·증권사 보도, 회사 보도자료 등 15건 | 출처 목록 (주소 포함) |

미확보 항목(산업용 로봇 부품별 원가 비중 · 감속기 업체별 점유율 · 자사 역량 데이터)은 지어내지 않고 비워 두었다.

## 개정 이력

| 날짜 | 바뀐 점 |
|---|---|
| 2026-10-31 | 첫 판 — 블록 4개, 퀴즈 4문항 |
| 2026-11-01 | 강의 웹앱 `app/` 추가 — Claude Code 없이 브라우저에서 수강 |

## 만든 방법

- `/course-forge`로 만들었다. 제작 기록(원본 요약·커리큘럼·검수 결과)은 `forge/`에 있다.
- 원본: 같은 작업 폴더의 교재 `textbook/ch1~3.md`, `sources.md`, `facts.csv`, 강의 덱 PDF
