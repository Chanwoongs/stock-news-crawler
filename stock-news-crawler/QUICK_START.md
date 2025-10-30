# 🚀 빠른 시작 가이드

## 📍 프로젝트 위치
```
C:\Users\tkfkd\stock-news-crawler
```

## ⚡ 즉시 실행

### 방법 1: 배치 파일 실행 (추천!)
```
run.bat 더블클릭
```
1번 또는 2번 선택

### 방법 2: 명령어로 실행

#### 1회 테스트 실행
```bash
python src\main.py --mode once
```

#### 스케줄러 실행 (5분마다 자동)
```bash
python src\main.py --mode schedule
```

## 📊 결과 확인

### HTML 리포트 열기
```
output\index.html 더블클릭
```

브라우저에서 자동으로 열립니다!

## ⚙️ 설정 조정

### 더 많은 뉴스를 보고 싶다면

`config.yaml` 파일을 열어서:
```yaml
filtering:
  min_score: 3.0  # 5.0 → 3.0으로 낮춤
```

### 크롤링 주기 변경

`config.yaml` 파일에서:
```yaml
crawler:
  interval: 180  # 300 → 180 (3분으로 단축)
```

## 🔧 문제 해결

### 뉴스가 수집되지 않을 때
1. 인터넷 연결 확인
2. `crawler.log` 파일 확인

### 필터링된 뉴스가 0건일 때
- **정상입니다!** 호재 키워드가 포함된 뉴스가 없는 것
- `min_score`를 낮추면 더 많은 뉴스 표시됨 (예: 3.0)

### 신규 뉴스가 0건일 때
- 모두 이미 수집했던 뉴스들입니다
- 기존 누적된 뉴스는 계속 유지됩니다
- 시간이 지나면 새로운 뉴스가 수집됩니다

### 처음부터 다시 시작하고 싶을 때 (데이터 초기화)

**방법 1: 자동 초기화 스크립트 (추천)**
```bash
# Windows
reset.bat

# 또는 Python
python reset.py
```

**방법 2: 수동 삭제**
```bash
del data\cache.json
del data\filtered_news.json
del data\run_history.json
del output\*.html
del crawler.log
```

⚠️ **주의**: 모든 누적 데이터가 삭제됩니다!

## 📊 실행 이력 확인

누적된 실행 이력을 확인하려면:

```bash
python view_history.py
```

또는 더 많은 이력 보기:

```bash
python view_history.py --limit 50
```

**표시되는 정보:**
- 실행 시간
- 수집한 뉴스 개수
- 신규 뉴스 개수
- 필터링 통과한 뉴스 개수
- 누적된 총 뉴스 개수
- 실행 소요 시간

## 🔄 누적 방식 설명

1. **중복 제거**: 이미 수집한 URL은 다시 수집하지 않음
2. **필터링 누적**: 새로운 호재 뉴스가 발견되면 기존 뉴스에 계속 추가됨
3. **최대 개수**: `config.yaml`의 `max_accumulated` 설정으로 최대 누적 개수 조절 가능
4. **이력 기록**: 모든 실행 내역이 `data/run_history.json`에 저장됨

## 📁 주요 파일

| 파일 | 설명 |
|------|------|
| `run.bat` | 쉬운 실행 배치 파일 |
| `view_history.py` | 실행 이력 조회 스크립트 |
| `config.yaml` | 설정 파일 (크롤링 주기, 필터 점수) |
| `data/keywords.json` | 호재 키워드 데이터베이스 |
| `data/cache.json` | 중복 체크용 URL 캐시 |
| `data/filtered_news.json` | 필터링된 뉴스 누적 저장소 |
| `data/run_history.json` | 실행 이력 기록 |
| `output/index.html` | 최신 뉴스 리포트 |
| `crawler.log` | 실행 로그 |

## 💡 팁

1. **처음에는 `min_score: 3.0`으로 설정**
   - 더 많은 뉴스를 볼 수 있음
   
2. **스케줄러는 백그라운드로 실행**
   - 터미널 창을 최소화하고 계속 실행
   
3. **output 폴더를 즐겨찾기에 추가**
   - 빠르게 접근 가능

4. **키워드 커스터마이징**
   - `data/keywords.json`에 원하는 키워드 추가

## 🎯 추천 워크플로우

1. `run.bat` 실행 → **[2] 스케줄러 선택**
2. 터미널 최소화
3. 30분 후 `output\index.html` 확인
4. 마음에 드는 설정 찾으면 계속 실행!

---

**궁금한 점은 `README.md`를 참고하세요!**

