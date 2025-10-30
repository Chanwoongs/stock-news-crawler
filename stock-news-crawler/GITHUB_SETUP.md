# GitHub Actions 설정 가이드

## 🚀 5분 안에 완료!

### 1단계: GitHub 저장소 생성

1. GitHub 로그인: https://github.com
2. 우측 상단 **[+]** → **[New repository]** 클릭
3. 저장소 설정:
   ```
   Repository name: stock-news-crawler
   Description: 주식 호재 뉴스 자동 크롤러
   Public (공개) 선택
   ✅ Add a README file 체크
   ```
4. **[Create repository]** 클릭

---

### 2단계: 코드 업로드

**방법 A: GitHub Desktop (쉬움)**

1. GitHub Desktop 다운로드: https://desktop.github.com
2. File → Add Local Repository
3. 현재 폴더 선택: `C:\Users\tkfkd\Desktop\stock-news-crawler`
4. **[Publish repository]** 클릭

**방법 B: Git 명령어 (빠름)**

```bash
cd C:\Users\tkfkd\Desktop\stock-news-crawler

# Git 초기화
git init
git add .
git commit -m "Initial commit: Stock News Crawler"

# 원격 저장소 연결 (저장소 URL 입력)
git remote add origin https://github.com/사용자명/stock-news-crawler.git
git branch -M main
git push -u origin main
```

**방법 C: 웹에서 업로드 (가장 쉬움)**

1. GitHub 저장소 페이지에서 **[Add file]** → **[Upload files]**
2. 모든 파일 드래그 앤 드롭
3. **[Commit changes]** 클릭

---

### 3단계: GitHub Actions 활성화

1. 저장소 페이지에서 **[Actions]** 탭 클릭
2. "I understand my workflows" 클릭
3. 자동으로 `.github/workflows/crawler.yml` 인식됨
4. 완료! ✅

---

### 4단계: GitHub Pages 활성화

1. 저장소 **[Settings]** 탭 클릭
2. 왼쪽 메뉴에서 **[Pages]** 클릭
3. Source 설정:
   ```
   Branch: gh-pages
   Folder: / (root)
   ```
4. **[Save]** 클릭
5. 2~3분 후 링크 생성:
   ```
   https://사용자명.github.io/stock-news-crawler/
   ```

---

### 5단계: 첫 실행 (수동)

1. **[Actions]** 탭으로 이동
2. 왼쪽에서 **"Stock News Crawler"** 클릭
3. 우측 **[Run workflow]** 버튼 클릭
4. **[Run workflow]** 확인
5. 진행 상황 실시간 확인 가능!

---

## ✅ 완료!

### 결과 확인

**웹사이트 접속:**
```
https://사용자명.github.io/stock-news-crawler/
```

**자동 실행:**
- 5분마다 자동으로 크롤링 실행
- 결과가 자동으로 웹사이트에 업데이트

**수동 실행:**
- Actions 탭에서 언제든 "Run workflow" 클릭

---

## 📱 휴대폰에서 보기

### 방법 1: 바로가기 저장
1. 휴대폰 브라우저에서 링크 접속
2. (iOS) 공유 → 홈 화면에 추가
3. (Android) 메뉴 → 홈 화면에 추가
4. 앱처럼 사용!

### 방법 2: QR 코드 생성
```
https://www.qr-code-generator.com/
→ 링크 입력
→ QR 생성
→ 휴대폰으로 스캔
```

---

## 🔧 설정 변경

### 실행 주기 변경

`.github/workflows/crawler.yml` 파일 수정:

```yaml
schedule:
  # 10분마다
  - cron: '*/10 * * * *'
  
  # 30분마다
  - cron: '*/30 * * * *'
  
  # 1시간마다
  - cron: '0 * * * *'
  
  # 매일 오전 9시
  - cron: '0 9 * * *'
```

### 한국 장 시간만 실행 (추천)

```yaml
schedule:
  # 평일 오전 9시~오후 4시, 5분마다
  - cron: '*/5 0-7 * * 1-5'  # UTC 기준 (한국 시간 -9시간)
```

---

## ⚠️ 주의사항

### GitHub Actions 무료 한도

**Public 저장소:**
- ✅ 무제한 무료!
- ✅ 제한 없음

**Private 저장소:**
- 월 2,000분 무료
- 85개 RSS 크롤링: 약 20초/회
- 5분마다: 월 약 8,640회
- 총 사용: 약 2,880분 (한도 초과)
- **→ Public 저장소 사용 추천**

### 문제 해결

**1. Actions가 실행 안 됨**
- Settings → Actions → General
- "Allow all actions" 선택

**2. GitHub Pages 404 에러**
- Settings → Pages에서 gh-pages 브랜치 확인
- 첫 실행 후 2~3분 대기

**3. 크롤링 실패**
- Actions 탭에서 로그 확인
- RSS 소스 문제일 수 있음

---

## 📊 실행 이력 확인

### GitHub Actions 로그
```
Actions 탭 → 특정 실행 클릭 → 상세 로그 확인
```

### 로그에서 확인 가능:
- 수집된 뉴스 개수
- 필터링 결과
- 실행 시간
- 오류 발생 여부

---

## 🎉 완성!

이제 PC 없이, 휴대폰 없이도:
- ✅ 5분마다 자동 크롤링
- ✅ 결과 자동 업데이트
- ✅ 어디서든 링크로 접속
- ✅ 완전 무료!

**링크를 북마크하고 언제든 확인하세요!** 🚀

