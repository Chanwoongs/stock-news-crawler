"""
RSS 피드 수집 모듈 (비동기 처리)
"""
import asyncio
import aiohttp
import feedparser
from datetime import datetime, timezone, timedelta
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSCollector:
    """비동기 RSS 피드 수집기"""
    
    def __init__(self, rss_sources: List[Dict], timeout: int = 10):
        """
        Args:
            rss_sources: RSS 소스 목록 (config.yaml에서 로드)
            timeout: 요청 타임아웃 (초)
        """
        self.rss_sources = [source for source in rss_sources if source.get('enabled', True)]
        self.timeout = timeout
        
    async def fetch_feed(self, session: aiohttp.ClientSession, source: Dict) -> List[Dict]:
        """단일 RSS 피드 비동기 수집"""
        try:
            async with session.get(
                source['url'], 
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                content = await response.text()
                
                # feedparser는 동기 함수이므로 executor에서 실행
                loop = asyncio.get_event_loop()
                feed = await loop.run_in_executor(None, feedparser.parse, content)
                
                news_items = []
                for entry in feed.entries[:50]:  # 최대 50개만
                    try:
                        news_item = {
                            'title': entry.get('title', ''),
                            'link': entry.get('link', ''),
                            'summary': entry.get('summary', entry.get('description', ''))[:500],
                            'published': self._parse_date(entry),
                            'source': source['name'],
                            'raw_entry': entry
                        }
                        
                        # 필수 필드 검증
                        if news_item['title'] and news_item['link']:
                            news_items.append(news_item)
                            
                    except Exception as e:
                        logger.warning(f"항목 파싱 오류 ({source['name']}): {e}")
                        continue
                
                logger.info(f"✅ {source['name']}: {len(news_items)}건 수집")
                return news_items
                
        except asyncio.TimeoutError:
            logger.error(f"⏱️ 타임아웃: {source['name']}")
            return []
        except Exception as e:
            logger.error(f"❌ 수집 실패 ({source['name']}): {e}")
            return []
    
    async def collect_all(self) -> List[Dict]:
        """모든 RSS 피드 비동기 수집"""
        logger.info(f"📡 {len(self.rss_sources)}개 RSS 소스에서 뉴스 수집 시작...")
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_feed(session, source) for source in self.rss_sources]
            results = await asyncio.gather(*tasks)
        
        # 결과 병합
        all_news = []
        for news_list in results:
            all_news.extend(news_list)
        
        logger.info(f"🎉 총 {len(all_news)}건 수집 완료")
        return all_news
    
    def _parse_date(self, entry) -> str:
        """날짜 파싱 (UTC → KST 변환)"""
        try:
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                # UTC 시간으로 파싱
                dt_utc = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                # 한국 시간(KST, UTC+9)으로 변환
                dt_kst = dt_utc + timedelta(hours=9)
                return dt_kst.strftime('%Y-%m-%d %H:%M:%S')
            elif hasattr(entry, 'published'):
                return entry.published
        except:
            pass
        
        # 현재 한국 시간
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def run_collector(rss_sources: List[Dict], timeout: int = 10) -> List[Dict]:
    """동기 인터페이스 (메인에서 호출용)"""
    collector = RSSCollector(rss_sources, timeout)
    return asyncio.run(collector.collect_all())


if __name__ == "__main__":
    # 테스트
    test_sources = [
        {
            "name": "테스트_구글뉴스",
            "url": "https://news.google.com/rss/search?q=주식&hl=ko&gl=KR&ceid=KR:ko",
            "enabled": True
        }
    ]
    
    news = run_collector(test_sources)
    print(f"\n수집된 뉴스: {len(news)}건")
    if news:
        print("\n첫 번째 뉴스:")
        print(f"제목: {news[0]['title']}")
        print(f"출처: {news[0]['source']}")

