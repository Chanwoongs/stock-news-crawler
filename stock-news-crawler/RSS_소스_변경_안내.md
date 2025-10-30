# RSS 소스 변경 안내

## 📢 중요 변경사항 (2025-10-30)

### ❌ 중단된 RSS 소스
다음 RSS 피드들이 더 이상 작동하지 않습니다:
- **네이버 뉴스 RSS** (HTTP 302 리다이렉트)
- **다음 뉴스 RSS** (HTTP 404 Not Found)

### ✅ 새로운 RSS 소스

대신 다음의 **주요 언론사 RSS 피드**로 교체되었습니다:

| 언론사 | 수집량 | URL |
|--------|--------|-----|
| 한국경제 | ~50건 | https://www.hankyung.com/feed/economy |
| 매일경제 | ~50건 | https://www.mk.co.kr/rss/40300001/ |
| 연합뉴스 경제 | ~11건 | https://www.yonhapnewstv.co.kr/category/news/economy/feed/ |
| SBS 경제 | ~29건 | https://news.sbs.co.kr/news/SectionRssFeed.do?sectionId=01&plink=RSSREADER |
| 구글뉴스 주식 | ~16건 | https://news.google.com/rss/search?q=주식+when:1h&hl=ko&gl=KR&ceid=KR:ko |
| 구글뉴스 반도체 | ~1건 | https://news.google.com/rss/search?q=반도체+실적+when:1h&hl=ko&gl=KR&ceid=KR:ko |

**총 수집량: 약 157건 (이전 17건 → 9배 증가!)**

## 🎉 개선 효과

### 이전 (네이버/다음)
```
수집: 0~20건
신규: 0~20건  
필터링: 0~3건
```

### 현재 (주요 언론사)
```
수집: 140~160건 ✨
신규: 140건
필터링: 7~10건 ✨
```

**약 10배 더 많은 뉴스를 수집합니다!**

## 📝 추가 RSS 소스 추천

필요시 다음 RSS 소스를 `config.yaml`에 추가할 수 있습니다:

```yaml
rss_sources:
  # 추가 가능한 RSS
  - name: "조선일보_경제"
    url: "https://www.chosun.com/arc/outboundfeeds/rss/category/economy/"
    enabled: true
  
  - name: "중앙일보_경제"  
    url: "https://rss.joins.com/joins_economy_list.xml"
    enabled: true
```

## 🔧 문제 해결

### RSS 소스가 작동하지 않을 때

1. **RSS URL 테스트**:
   ```bash
   python -c "import feedparser; print(len(feedparser.parse('RSS_URL').entries))"
   ```

2. **대체 RSS 찾기**:
   - 언론사 공식 웹사이트에서 RSS 아이콘 찾기
   - 주로 URL: `https://사이트주소/rss` 또는 `/feed`

3. **직접 추가**:
   `config.yaml`의 `rss_sources`에 추가

## 📌 참고사항

- RSS 서비스는 언론사 정책에 따라 변경될 수 있습니다
- 정기적으로 RSS 작동 여부를 확인하세요
- 문제 발생 시 `crawler.log` 파일을 확인하세요

---

**업데이트 날짜**: 2025-10-30  
**버전**: v2.1.0

