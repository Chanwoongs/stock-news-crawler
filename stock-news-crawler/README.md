# 📈 주식 호재 뉴스 자동 크롤러

무료 RSS 피드를 활용하여 주식 호재 뉴스를 자동으로 수집하고, 키워드 필터링을 통해 중요한 뉴스만 선별하여 HTML 리포트를 생성하는 프로그램입니다.

## 🎯 주요 기능

- ✅ **다중 RSS 소스 크롤링** (한국경제, 매일경제, 연합뉴스, SBS, 구글 뉴스)
- ✅ **비동기 처리**로 빠른 수집 (2~3초)
- ✅ **키워드 기반 필터링** (호재 뉴스만 선별)
- ✅ **중복 제거** (이미 수집한 뉴스 제외)
- ✅ **누적 저장** (필터링된 뉴스 계속 쌓임)
- ✅ **실행 이력 기록** (수집/필터링 통계)
- ✅ **최신순 자동 정렬** (가장 최신 뉴스가 위에)
- ✅ **상대 시간 표시** (5분 전, 1시간 전 등)
- ✅ **NEW 뱃지** (1시간 이내 뉴스 강조)
- ✅ **자동 HTML 리포트 생성** (반응형 디자인)
- ✅ **5분마다 자동 실행** (스케줄러)
- ✅ **완전 무료** (AI 사용 없음)

## 📁 프로젝트 구조

```
stock-news-crawler/
├── src/
│   ├── collectors/          # RSS 수집 모듈
│   ├── filters/             # 필터링 모듈
│   ├── generator/           # HTML 생성 모듈
│   └── main.py              # 메인 실행 파일
├── data/
│   ├── keywords.json        # 호재 키워드 데이터베이스
│   ├── cache.json           # 중복 제거 캐시 (자동 생성)
│   ├── filtered_news.json   # 필터링된 뉴스 누적 저장소
│   └── run_history.json     # 실행 이력 기록
├── output/                  # HTML 리포트 저장 폴더
│   └── index.html           # 최신 리포트 (자동 업데이트)
├── templates/
│   └── news_template.html   # HTML 템플릿
├── config.yaml              # 설정 파일
├── view_history.py          # 실행 이력 조회 스크립트
├── requirements.txt         # 필요한 패키지
└── README.md
```

## 🚀 설치 및 실행

### 사용 방법 선택

#### 🌐 방법 1: GitHub Actions (추천!)
**PC 없이 클라우드에서 자동 실행**
- ✅ 5분마다 자동 크롤링
- ✅ 휴대폰/PC 어디서든 접속
- ✅ 완전 무료
- ✅ 배터리/데이터 소모 없음

👉 **[GITHUB_SETUP.md](GITHUB_SETUP.md) 참고** (5분 설정)

---

#### 💻 방법 2: 로컬 실행 (PC에서 직접)

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 실행 방법

#### (1) 1회 실행 (테스트용)
```bash
python src/main.py --mode once
```

#### (2) 스케줄러 실행 (5분마다 자동)
```bash
python src/main.py --mode schedule
```

### 3. 결과 확인

브라우저로 `output/index.html` 파일을 열어 최신 호재 뉴스를 확인하세요!

```bash
# Windows
start output/index.html

# 또는 더블클릭
```

### 4. 실행 이력 조회

```bash
python view_history.py
```

**표시되는 정보:**
- 각 실행별 수집/신규/필터링 통계
- 누적된 총 뉴스 개수
- 실행 시간 및 평균 시간
- 총 실행 횟수

## 🔄 누적 저장 방식

이 크롤러는 **스마트 누적 시스템**을 사용합니다:

1. **중복 제거**: 같은 URL의 뉴스는 다시 수집하지 않음
2. **필터링된 뉴스만 누적**: 호재 키워드가 포함된 뉴스만 계속 쌓임
3. **자동 이력 기록**: 모든 실행 내역이 `data/run_history.json`에 저장됨
4. **최대 개수 제한**: `config.yaml`의 `max_accumulated`로 최대 누적 개수 설정 (기본 500건)

**예시:**
- 1차 실행: 20건 수집 → 5건 필터링 통과 → 누적 5건
- 2차 실행: 18건 수집 (2건 신규) → 1건 필터링 통과 → 누적 6건
- 3차 실행: 20건 수집 (0건 신규, 모두 중복) → 0건 필터링 통과 → 누적 6건 유지

## ⚙️ 설정 파일 (config.yaml)

```yaml
crawler:
  interval: 300  # 5분 (초 단위)
  
filtering:
  min_score: 5.0  # 최소 점수 (조정 가능)
  max_accumulated: 500  # 최대 누적 뉴스 개수
  
rss_sources:
  - name: "한국경제"
    url: "https://www.hankyung.com/feed/economy"
    enabled: true
  
  - name: "매일경제"
    url: "https://www.mk.co.kr/rss/40300001/"
    enabled: true
```

- `min_score`: 점수가 낮으면 더 많은 뉴스, 높으면 엄선된 뉴스만
- `interval`: 크롤링 주기 (초 단위)
- `rss_sources`: 원하는 RSS 소스 추가/제거 가능

## 📊 키워드 점수 시스템

| 우선순위 | 점수 | 키워드 예시 |
|---------|------|------------|
| 높음 | 3.0 | 실적호조, 신규계약, 특허, 수주, M&A |
| 중간 | 2.0 | 기술개발, 신제품, 수출증가, 제휴 |
| 낮음 | 1.0 | 성장, 확대, 투자, 증가 |

**예시**: "삼성전자 신규계약(3.0) + 수출증가(2.0) + 실적개선(1.5) = 6.5점"

## 🔧 커스터마이징

### 키워드 추가/수정

`data/keywords.json` 파일을 수정하여 원하는 키워드를 추가할 수 있습니다.

```json
{
  "high_priority": {
    "score": 3.0,
    "keywords": [
      "실적호조",
      "신규계약",
      "당신의_키워드"  // 여기에 추가
    ]
  }
}
```

### RSS 소스 추가

`config.yaml`에서 원하는 RSS 피드를 추가할 수 있습니다.

```yaml
rss_sources:
  - name: "새로운_소스"
    url: "https://..."
    enabled: true
```

## 📈 예상 성능

- **수집 속도**: 2~3초 (10개 RSS 소스, 비동기 처리)
- **수집량**: 5분마다 200~300건 (원본)
- **필터링 후**: 10~30건 (호재 뉴스)
- **하루 총량**: 100~300건 (실제 유의미한 호재)

## 🛠️ 문제 해결

### 뉴스가 수집되지 않을 때

1. 인터넷 연결 확인
2. RSS URL이 유효한지 확인
3. `crawler.log` 파일에서 오류 확인

### 필터링된 뉴스가 너무 적을 때

`config.yaml`에서 `min_score`를 낮추세요 (예: 5.0 → 3.0)

### 필터링된 뉴스가 너무 많을 때

`config.yaml`에서 `min_score`를 높이세요 (예: 5.0 → 7.0)

## 📝 로그 확인

실행 로그는 `crawler.log` 파일에 자동 저장됩니다.

```bash
# 최근 로그 확인
tail -f crawler.log  # Linux/Mac
Get-Content crawler.log -Tail 50  # Windows PowerShell
```

## 🎨 HTML 리포트 특징

- ✨ 모던한 디자인 (그라디언트 배경)
- 📱 반응형 (모바일 최적화)
- 🎯 점수별 색상 구분
- 🔍 키워드 하이라이팅
- 📊 통계 대시보드

## 🔄 자동 시작 설정 (선택사항)

### Windows 작업 스케줄러

1. 작업 스케줄러 열기
2. "기본 작업 만들기"
3. 프로그램: `python`
4. 인수: `C:\Users\...\stock-news-crawler\src\main.py --mode schedule`
5. 트리거: 시스템 시작 시

## 📜 라이선스

개인 사용 전용 (비상업적)

## 🙋 FAQ

**Q: AI 요약 기능을 추가하고 싶어요**  
A: `src/main.py`에서 필터링 후 OpenAI API 호출 코드를 추가하면 됩니다. (비용 발생)

**Q: 특정 종목만 모니터링하고 싶어요**  
A: `keywords.json`에 종목명을 추가하고 점수를 높게 설정하세요.

**Q: 텔레그램으로 알림 받고 싶어요**  
A: `src/main.py`에 텔레그램 봇 API 연동 코드를 추가하면 됩니다.

## 📞 지원

문제가 있으면 `crawler.log` 파일과 함께 문의하세요.

---

**⚠️ 주의사항**: 이 프로그램은 투자 참고용이며, 투자 판단은 본인 책임입니다.

