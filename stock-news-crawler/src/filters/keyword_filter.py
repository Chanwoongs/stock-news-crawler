"""
키워드 기반 호재 뉴스 필터링 모듈
"""
import json
import re
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KeywordFilter:
    """호재 키워드 기반 필터"""
    
    def __init__(self, keywords_file: str, exclude_keywords: List[str] = None):
        """
        Args:
            keywords_file: 키워드 JSON 파일 경로
            exclude_keywords: 제외할 키워드 리스트
        """
        with open(keywords_file, 'r', encoding='utf-8') as f:
            self.keywords_data = json.load(f)
        
        self.exclude_keywords = exclude_keywords or []
        
    def calculate_score(self, text: str) -> Tuple[float, List[str]]:
        """
        텍스트에서 키워드 점수 계산
        
        Returns:
            (점수, 매칭된 키워드 리스트)
        """
        text_lower = text.lower()
        total_score = 0.0
        matched_keywords = []
        
        # 각 우선순위별 키워드 검사
        for priority, data in self.keywords_data.items():
            keywords = data['keywords']
            score_weight = data['score']
            
            for keyword in keywords:
                # 대소문자 무시하고 검색
                if keyword.lower() in text_lower:
                    total_score += score_weight
                    matched_keywords.append(keyword)
        
        return total_score, matched_keywords
    
    def is_excluded(self, text: str) -> bool:
        """제외 키워드 포함 여부"""
        text_lower = text.lower()
        for exclude_kw in self.exclude_keywords:
            if exclude_kw.lower() in text_lower:
                return True
        return False
    
    def filter_news(self, news_list: List[Dict], min_score: float = 3.0) -> List[Dict]:
        """
        뉴스 리스트 필터링
        
        Args:
            news_list: 뉴스 항목 리스트
            min_score: 최소 점수 기준
            
        Returns:
            필터링된 뉴스 리스트 (점수 높은 순)
        """
        filtered_news = []
        
        for news in news_list:
            # 제외 키워드 체크
            combined_text = f"{news['title']} {news.get('summary', '')}"
            if self.is_excluded(combined_text):
                continue
            
            # 점수 계산
            score, keywords = self.calculate_score(combined_text)
            
            if score >= min_score:
                news['score'] = round(score, 1)
                news['matched_keywords'] = keywords
                filtered_news.append(news)
        
        # 점수 높은 순으로 정렬
        filtered_news.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"🔍 필터링 결과: {len(news_list)}건 → {len(filtered_news)}건 (기준: {min_score}점)")
        
        return filtered_news


class DeduplicateFilter:
    """중복 제거 필터"""
    
    def __init__(self, cache_file: str):
        """
        Args:
            cache_file: 캐시 파일 경로 (JSON)
        """
        self.cache_file = cache_file
        self.seen_urls = self._load_cache()
    
    def _load_cache(self) -> set:
        """캐시 파일 로드"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('urls', []))
        except FileNotFoundError:
            return set()
    
    def _save_cache(self):
        """캐시 파일 저장"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump({'urls': list(self.seen_urls)}, f, ensure_ascii=False, indent=2)
    
    def remove_duplicates(self, news_list: List[Dict]) -> List[Dict]:
        """중복 제거"""
        unique_news = []
        new_urls = []
        
        for news in news_list:
            url = news['link']
            if url not in self.seen_urls:
                unique_news.append(news)
                self.seen_urls.add(url)
                new_urls.append(url)
        
        # 캐시가 너무 커지면 최근 10000개만 유지
        if len(self.seen_urls) > 10000:
            self.seen_urls = set(list(self.seen_urls)[-10000:])
        
        self._save_cache()
        
        logger.info(f"🔄 중복 제거: {len(news_list)}건 → {len(unique_news)}건 (신규)")
        
        return unique_news


if __name__ == "__main__":
    # 테스트
    import os
    
    # 키워드 필터 테스트
    keywords_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'keywords.json')
    filter = KeywordFilter(keywords_file)
    
    test_news = [
        {
            'title': '삼성전자, 반도체 부문 실적 호조로 영업이익 급증',
            'summary': '3분기 영업이익 전년 대비 50% 증가',
            'link': 'http://test1.com'
        },
        {
            'title': 'LG전자 신제품 출시',
            'summary': '새로운 스마트폰 라인업 공개',
            'link': 'http://test2.com'
        },
        {
            'title': '일반 뉴스',
            'summary': '특별한 내용 없음',
            'link': 'http://test3.com'
        }
    ]
    
    filtered = filter.filter_news(test_news, min_score=3.0)
    
    print(f"\n필터링 결과: {len(filtered)}건")
    for news in filtered:
        print(f"\n제목: {news['title']}")
        print(f"점수: {news['score']}")
        print(f"키워드: {', '.join(news['matched_keywords'])}")

