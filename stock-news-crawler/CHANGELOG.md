# 변경 이력

## v2.3.0 - 2025-10-30

### 🌍 영어 키워드 지원 추가

#### 문제점 해결
- **이전**: 영어 뉴스(구글 뉴스)는 거의 필터링되지 않음
- **원인**: 호재 키워드가 거의 한글만 (영어 5개뿐)
- **현재**: 60개+ 영어 호재 키워드 추가

#### 추가된 영어 호재 키워드

**고득점 (3.0점):**
- record profit, record revenue, record earnings
- surges, soars, jumps, skyrockets
- beats expectations, exceeds, outperforms
- patent, acquisition, buyback, breakthrough

**중득점 (2.0점):**
- partnership, collaboration, innovation
- expansion, technology, market share
- strategic, improved, turnaround

**기본 (1.0-1.5점):**
- growth, rises, increase, gains
- positive, upgrade, bullish, optimistic
- all-time high, robust, stellar, outstanding

#### 테스트 결과
- ✅ "Tesla Surges on Patent" → 13.0점 (통과)
- ✅ "Apple Record Profit" → 6.0점 (통과)
- ✅ "Amazon Rises on Growth" → 8.0점 (통과)
- ✅ "Microsoft Acquisition" → 5.0점 (통과)

**총 키워드 개수:** 50개 → 110개+ (2배 증가)

### 🛡️ 악재 필터링 시스템 대폭 강화

#### 문제점 해결
- **이전**: "Stock Tanks 19%" 같은 악재 뉴스가 호재로 분류됨
- **원인**: 단순 키워드 매칭 + 악재 키워드 부족 (4개뿐)
- **현재**: 42개 악재 키워드로 정확한 필터링

#### 추가된 악재 키워드 (38개 추가)

**주가 급락:**
- 폭락, 급락, 하락
- tanks, plunges, crashes, tumbles

**실적 악화:**
- 적자, 손실, 부진, 영업손실, 실적 악화
- sluggish, weak, disappointing, misses, lower forecast

**경영 문제:**
- 파산, 도산, 부도, 워크아웃, 구조조정, 정리해고, 감원

**법적 문제:**
- 배임, 사기, 기소, 구속, 압수수색, 고발

**기타 악재:**
- 리콜, 결함, 사고, 중단, 취소, 철회, 별세

#### 테스트 결과
- ✅ "Stock Tanks 19%" → 정상 차단
- ✅ "영업손실" → 정상 차단
- ✅ "구조조정" → 정상 차단
- ✅ "리콜 사태" → 정상 차단
- ✅ 호재 뉴스는 정상 통과

### 📝 수정된 파일
- `config.yaml` - exclude_keywords 대폭 확장 (4개 → 42개)
- `악재_필터링_설명.md` - 상세 가이드 추가

## v2.2.0 - 2025-10-30

### ✨ 새로운 기능

#### 1. 최신순 정렬
- **자동 정렬**: 모든 뉴스가 발행 시간 기준으로 자동 정렬됨
- **최신 뉴스 우선**: 가장 최근 뉴스가 맨 위에 표시
- **정렬 표시**: 헤더에 "⏱️ 최신순 정렬" 표시

#### 2. 상대 시간 표시
- **몇 분 전**: 현재 시간과 비교하여 상대 시간 표시
  - 1분 미만: "X초 전"
  - 1시간 미만: "X분 전"
  - 1일 미만: "X시간 전"
  - 1주일 미만: "X일 전"
  - 1주일 이상: 날짜 표시
- **강조 표시**: 상대 시간을 빨간색으로 강조
- **원본 시간**: 괄호 안에 정확한 발행 시간도 표시

#### 3. NEW 뱃지
- **1시간 이내 뉴스**: 🔥 NEW 뱃지 자동 표시
- **깜빡임 효과**: 주목도를 높이기 위한 애니메이션
- **모바일 지원**: 반응형 디자인 적용

### 📝 수정된 파일

#### `src/generator/html_generator.py`
- `get_relative_time()`: 상대 시간 계산 함수 추가
- `_sort_news_by_date()`: 최신순 정렬 함수 추가
- `_is_recent_news()`: 1시간 이내 뉴스 판단 함수 추가
- `generate_report()`: 정렬 및 상대 시간 처리 로직 적용

#### `templates/news_template.html`
- NEW 뱃지 스타일 추가 (깜빡임 애니메이션)
- 상대 시간 표시 영역 추가
- 헤더에 "최신순 정렬" 표시 추가
- 모바일 반응형 스타일 개선

### 🎨 UI 개선

- ⏱️ 상대 시간을 빨간색(#e74c3c)으로 강조
- 🔥 NEW 뱃지 애니메이션 효과 (2초 주기)
- 원본 시간은 회색으로 작게 표시
- 모바일에서도 NEW 뱃지 정상 표시

## v2.1.0 - 2025-10-30

### 📡 RSS 소스 대체

네이버/다음 RSS 중단에 따른 대체 RSS 적용:
- 한국경제, 매일경제, 연합뉴스, SBS 추가
- 수집량 약 9배 증가 (17건 → 157건)

## v2.0.0 - 2025-10-30

### 🎉 주요 개선사항

#### 1. 누적 저장 시스템 구현
- **이전**: 중복 제거 후 신규 뉴스만 필터링하여 표시 (이전 뉴스 사라짐)
- **현재**: 필터링된 뉴스를 계속 누적하여 저장 (이전 뉴스 유지)
- **파일**: `data/filtered_news.json` 에 누적 저장
- **설정**: `config.yaml`의 `max_accumulated`로 최대 누적 개수 조절 가능 (기본 500건)

#### 2. 실행 이력 기록 기능
- **자동 기록**: 모든 실행 내역을 JSON 파일에 저장
- **기록 항목**:
  - 실행 시간 (timestamp)
  - 수집한 뉴스 개수 (collected)
  - 신규 뉴스 개수 (new)
  - 필터링 통과한 뉴스 개수 (filtered_new)
  - 누적된 총 뉴스 개수 (total_accumulated)
  - 실행 소요 시간 (elapsed_seconds)
- **파일**: `data/run_history.json`

#### 3. 실행 이력 조회 스크립트
- **새 파일**: `view_history.py`
- **기능**:
  - 최근 실행 이력 표시 (기본 20건)
  - 통계 요약 (총 실행 횟수, 총 수집/신규/필터링 개수, 평균 실행 시간)
  - Windows 콘솔 인코딩 문제 해결
- **사용법**: `python view_history.py [--limit N]`

#### 4. 개선된 로그 메시지
- 수집/신규/필터링/누적 개수를 명확히 구분하여 표시
- 신규 뉴스가 없을 때 현재 누적 개수 표시
- 실행 시간 자동 기록

### 📝 수정된 파일

#### `src/main.py`
- `_load_filtered_news()`: 저장된 필터링 뉴스 불러오기
- `_save_filtered_news()`: 필터링된 뉴스 누적 저장
- `_log_run_history()`: 실행 이력 자동 기록
- `run_once()`: 누적 저장 로직 적용, 로그 개선

#### `config.yaml`
- `filtering.max_accumulated` 옵션 추가 (최대 누적 뉴스 개수)

#### `QUICK_START.md`
- 실행 이력 조회 섹션 추가
- 누적 방식 설명 추가
- 신규 뉴스가 0건일 때 해결 방법 추가
- 초기화 방법 추가
- 주요 파일 목록 업데이트

#### `README.md`
- 주요 기능에 "누적 저장", "실행 이력 기록" 추가
- 프로젝트 구조에 새 파일들 추가
- 누적 저장 방식 섹션 추가
- 실행 이력 조회 섹션 추가

### 🐛 버그 수정

- **중복 제거 오해 해결**: 중복된 뉴스를 "제거"하는 것이 아니라 "추가하지 않는" 것으로 로직 개선
- **Windows 콘솔 인코딩**: 이모지 출력 시 인코딩 에러 해결

### 💡 사용 예시

```bash
# 크롤러 1회 실행
python src/main.py --mode once

# 실행 이력 확인
python view_history.py

# 더 많은 이력 보기
python view_history.py --limit 50

# 처음부터 다시 시작 (초기화)
del data\cache.json
del data\filtered_news.json
del data\run_history.json
```

### 📊 동작 방식

1. RSS 피드에서 뉴스 수집
2. 중복 제거 (cache.json 기반)
3. 신규 뉴스만 키워드 필터링
4. 필터링 통과한 뉴스를 기존 뉴스에 추가 (누적)
5. 전체 누적 뉴스로 HTML 생성
6. 실행 이력 자동 기록

### 🎯 기대 효과

- ✅ 이전에 수집했던 호재 뉴스를 계속 볼 수 있음
- ✅ 새로운 호재 뉴스가 추가되면 자동으로 누적됨
- ✅ 실행 통계를 통해 크롤러 성능 모니터링 가능
- ✅ 중복 제거가 정확히 동작함을 확인 가능

---

## v1.0.0 - 2025-10-29

- 초기 버전 출시
- RSS 크롤링 기능
- 키워드 필터링
- HTML 리포트 생성
- 스케줄러 기능

