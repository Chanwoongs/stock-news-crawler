"""
주식 호재 뉴스 크롤러 메인 실행 파일
"""
import os
import sys
import yaml
import json
import logging
import time
from datetime import datetime
import schedule

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import run_collector
from src.filters import KeywordFilter, DeduplicateFilter
from src.generator import HTMLGenerator

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('crawler.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class StockNewsCrawler:
    """주식 호재 뉴스 크롤러"""
    
    def __init__(self, config_path: str):
        """
        Args:
            config_path: 설정 파일 경로 (config.yaml)
        """
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 프로젝트 루트 디렉토리
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 경로 설정
        keywords_file = os.path.join(self.base_dir, 'data', 'keywords.json')
        cache_file = os.path.join(self.base_dir, self.config['cache']['file'])
        self.filtered_news_file = os.path.join(self.base_dir, 'data', 'filtered_news.json')
        self.run_history_file = os.path.join(self.base_dir, 'data', 'run_history.json')
        template_path = os.path.join(self.base_dir, 'templates', 'news_template.html')
        output_dir = os.path.join(self.base_dir, self.config['output']['directory'])
        
        # 모듈 초기화
        self.keyword_filter = KeywordFilter(
            keywords_file,
            self.config['filtering']['exclude_keywords']
        )
        self.dedupe_filter = DeduplicateFilter(cache_file)
        self.html_generator = HTMLGenerator(template_path, output_dir)
    
    def _load_filtered_news(self):
        """저장된 필터링 뉴스 불러오기"""
        try:
            with open(self.filtered_news_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_filtered_news(self, news_list):
        """필터링된 뉴스 저장 (누적)"""
        with open(self.filtered_news_file, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
    
    def _log_run_history(self, collected_count, new_count, filtered_count, total_count, elapsed_time):
        """실행 이력 기록"""
        try:
            with open(self.run_history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []
        
        history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'collected': collected_count,
            'new': new_count,
            'filtered_new': filtered_count,
            'total_accumulated': total_count,
            'elapsed_seconds': round(elapsed_time, 2)
        })
        
        # 최근 1000개만 유지
        if len(history) > 1000:
            history = history[-1000:]
        
        with open(self.run_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def run_once(self):
        """1회 실행"""
        try:
            start_time = time.time()
            logger.info("=" * 60)
            logger.info("🚀 뉴스 크롤링 시작")
            logger.info("=" * 60)
            
            # 1. RSS 수집
            collected_news = run_collector(
                self.config['rss_sources'],
                self.config['crawler']['timeout']
            )
            collected_count = len(collected_news)
            
            if not collected_news:
                logger.warning("⚠️ 수집된 뉴스가 없습니다.")
                elapsed = time.time() - start_time
                self._log_run_history(0, 0, 0, len(self._load_filtered_news()), elapsed)
                return
            
            # 2. 중복 제거 (신규 뉴스만 추출)
            new_news = self.dedupe_filter.remove_duplicates(collected_news)
            new_count = len(new_news)
            
            # 3. 신규 뉴스가 있으면 키워드 필터링
            filtered_new_count = 0
            filtered_new = []
            
            if new_news:
                filtered_new = self.keyword_filter.filter_news(
                    new_news,
                    self.config['filtering']['min_score']
                )
                filtered_new_count = len(filtered_new)
            else:
                logger.info("ℹ️ 신규 뉴스가 없습니다. (모두 중복)")
            
            # 4. 기존 뉴스 불러와서 누적
            existing_news = self._load_filtered_news()
            
            if filtered_new:
                # 신규 필터링된 뉴스를 맨 앞에 추가 (최신순)
                all_news = filtered_new + existing_news
                
                # 최대 개수 제한 (설정 가능)
                max_news = self.config.get('filtering', {}).get('max_accumulated', 500)
                all_news = all_news[:max_news]
                
                # 저장
                self._save_filtered_news(all_news)
                
                logger.info(f"📊 신규 호재 뉴스: {filtered_new_count}건 추가")
                logger.info(f"📚 누적 호재 뉴스: {len(all_news)}건")
            else:
                if new_news:
                    logger.info("ℹ️ 신규 뉴스 중 필터링 기준을 통과한 뉴스가 없습니다.")
                all_news = existing_news
                logger.info(f"📚 현재 누적 호재 뉴스: {len(existing_news)}건")
            
            # 5. HTML 생성 (누적 뉴스가 있으면 항상 생성)
            if all_news:
                output_path = self.html_generator.generate_report(all_news)
                logger.info(f"✅ 리포트 생성 완료: {output_path}")
            else:
                logger.info("ℹ️ 아직 필터링된 호재 뉴스가 없습니다.")
            
            # 실행 시간
            elapsed = time.time() - start_time
            logger.info(f"⏱️ 실행 시간: {elapsed:.2f}초")
            
            # 실행 이력 기록
            self._log_run_history(collected_count, new_count, filtered_new_count, len(all_news), elapsed)
            
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ 오류 발생: {e}", exc_info=True)
    
    def run_scheduler(self):
        """스케줄러 실행 (5분마다)"""
        interval_seconds = self.config['crawler']['interval']
        interval_minutes = interval_seconds / 60
        
        logger.info("=" * 60)
        logger.info(f"🤖 스케줄러 시작: {interval_minutes}분마다 실행")
        logger.info("=" * 60)
        
        # 즉시 1회 실행
        self.run_once()
        
        # 스케줄 등록
        schedule.every(interval_seconds).seconds.do(self.run_once)
        
        # 무한 루프
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n👋 프로그램 종료")


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='주식 호재 뉴스 크롤러')
    parser.add_argument(
        '--mode',
        choices=['once', 'schedule'],
        default='schedule',
        help='실행 모드: once (1회 실행) 또는 schedule (스케줄러)'
    )
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='설정 파일 경로'
    )
    
    args = parser.parse_args()
    
    # 설정 파일 경로
    if not os.path.isabs(args.config):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_dir, args.config)
    else:
        config_path = args.config
    
    # 크롤러 초기화
    crawler = StockNewsCrawler(config_path)
    
    # 실행 모드에 따라 실행
    if args.mode == 'once':
        crawler.run_once()
    else:
        crawler.run_scheduler()


if __name__ == "__main__":
    main()

