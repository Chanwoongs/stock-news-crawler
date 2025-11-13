"""
HTML 리포트 생성 모듈
"""
import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from jinja2 import Template
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KST = timezone(timedelta(hours=9))


def get_relative_time(published_str: str) -> str:
    """
    상대 시간 계산 (예: 5분 전, 1시간 전) - 한국 시간 기준
    
    Args:
        published_str: 발행 시간 문자열 (YYYY-MM-DD HH:MM:SS, KST 기준)
        
    Returns:
        상대 시간 문자열
    """
    try:
        # 발행 시간 파싱
        if isinstance(published_str, str):
            # 다양한 형식 지원
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']:
                try:
                    published_dt = datetime.strptime(published_str, fmt)
                    published_dt = published_dt.replace(tzinfo=KST)
                    break
                except ValueError:
                    continue
            else:
                return published_str  # 파싱 실패시 원본 반환
        else:
            return str(published_str)
        
        # 현재 한국 시간과 비교
        now = datetime.now(tz=KST)
        diff = now - published_dt
        
        # 초 단위 차이
        seconds = int(diff.total_seconds())
        
        if seconds < 0:
            return "방금 전"
        elif seconds < 60:
            return f"{seconds}초 전"
        elif seconds < 3600:  # 1시간 미만
            minutes = seconds // 60
            return f"{minutes}분 전"
        elif seconds < 86400:  # 1일 미만
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes > 0:
                return f"{hours}시간 {minutes}분 전"
            else:
                return f"{hours}시간 전"
        elif seconds < 604800:  # 1주일 미만
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            if hours > 0:
                return f"{days}일 {hours}시간 전"
            else:
                return f"{days}일 전"
        else:
            # 1주일 이상이면 날짜 표시
            return published_dt.strftime('%Y-%m-%d %H:%M')
            
    except Exception as e:
        logger.warning(f"상대 시간 계산 오류: {e}")
        return str(published_str)


class HTMLGenerator:
    """HTML 뉴스 리포트 생성기"""
    
    def __init__(self, template_path: str, output_dir: str):
        """
        Args:
            template_path: HTML 템플릿 파일 경로
            output_dir: HTML 출력 디렉토리
        """
        self.template_path = template_path
        self.output_dir = output_dir
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 템플릿 로드
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = Template(f.read())
    
    def generate_report(self, news_list: List[Dict], output_filename: str = None) -> str:
        """
        HTML 리포트 생성
        
        Args:
            news_list: 뉴스 데이터 리스트
            output_filename: 출력 파일명 (없으면 날짜로 자동 생성)
            
        Returns:
            생성된 파일 경로
        """
        if output_filename is None:
            today = datetime.now(tz=KST).strftime('%Y-%m-%d')
            output_filename = f"{today}.html"
        
        # 1. 최신 순으로 정렬 (published 기준)
        sorted_news = self._sort_news_by_date(news_list)
        
        # 2. 각 뉴스에 상대 시간 추가 및 NEW 뱃지 판단
        for news in sorted_news:
            news['relative_time'] = get_relative_time(news.get('published', ''))
            news['is_new'] = self._is_recent_news(news.get('published', ''))  # 1시간 이내 뉴스
        
        # 3. 통계 계산
        high_score_count = len([n for n in sorted_news if n.get('score', 0) >= 7.0])
        
        # HTML 렌더링
        html_content = self.template.render(
            news_list=sorted_news,
            date=datetime.now(tz=KST).strftime('%Y년 %m월 %d일'),
            total_count=len(sorted_news),
            high_score_count=high_score_count,
            update_time=datetime.now(tz=KST).strftime('%H:%M')
        )
        
        # 파일 저장
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"📄 HTML 리포트 생성 완료: {output_path}")
        
        # index.html도 업데이트 (최신 파일로 복사)
        self._update_index(output_filename)
        
        return output_path
    
    def _sort_news_by_date(self, news_list: List[Dict]) -> List[Dict]:
        """
        뉴스를 발행 날짜 기준으로 최신 순 정렬
        
        Args:
            news_list: 뉴스 리스트
            
        Returns:
            정렬된 뉴스 리스트
        """
        def parse_date(news: Dict) -> datetime:
            """날짜 파싱 (정렬용)"""
            try:
                published = news.get('published', '')
                if isinstance(published, str):
                    # 다양한 형식 시도
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']:
                        try:
                            dt = datetime.strptime(published, fmt)
                            return dt.replace(tzinfo=KST)
                        except ValueError:
                            continue
                # 파싱 실패시 과거 날짜로 설정 (맨 뒤로 보냄)
                return datetime(1900, 1, 1, tzinfo=KST)
            except:
                return datetime(1900, 1, 1, tzinfo=KST)
        
        # 최신 순 정렬 (내림차순)
        return sorted(news_list, key=parse_date, reverse=True)
    
    def _is_recent_news(self, published_str: str) -> bool:
        """
        최근 뉴스 여부 판단 (1시간 이내) - 한국 시간 기준
        
        Args:
            published_str: 발행 시간 문자열 (KST 기준)
            
        Returns:
            True if 1시간 이내 뉴스
        """
        try:
            if isinstance(published_str, str):
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']:
                    try:
                        published_dt = datetime.strptime(published_str, fmt)
                        published_dt = published_dt.replace(tzinfo=KST)
                        break
                    except ValueError:
                        continue
                else:
                    return False
            else:
                return False
            
            # 현재 한국 시간과 비교
            now = datetime.now(tz=KST)
            diff = now - published_dt
            
            # 1시간(3600초) 이내면 True
            return diff.total_seconds() < 3600
        except:
            return False
    
    def _update_index(self, latest_filename: str):
        """index.html을 최신 리포트로 업데이트"""
        latest_path = os.path.join(self.output_dir, latest_filename)
        index_path = os.path.join(self.output_dir, 'index.html')
        
        try:
            with open(latest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"🔄 index.html 업데이트 완료")
        except Exception as e:
            logger.error(f"index.html 업데이트 실패: {e}")
    
    def generate_archive_index(self):
        """과거 리포트 목록 페이지 생성 (선택사항)"""
        # TODO: 나중에 구현
        pass


if __name__ == "__main__":
    # 테스트
    test_news = [
        {
            'title': '삼성전자, AI 반도체 특허 150건 신규 획득',
            'link': 'http://test.com/1',
            'summary': '삼성전자가 AI 관련 반도체 기술 특허 150건을 미국 특허청에 등록했다고 발표했다.',
            'source': '네이버금융',
            'published': '2025-10-30 14:30:00',
            'score': 9.2,
            'matched_keywords': ['특허', 'AI', '반도체', '신규']
        },
        {
            'title': 'SK하이닉스, HBM 수주 확대로 실적 호조',
            'link': 'http://test.com/2',
            'summary': 'SK하이닉스가 HBM3 제품 수주 확대로 분기 실적이 크게 개선될 전망이다.',
            'source': '다음증권',
            'published': '2025-10-30 13:15:00',
            'score': 8.5,
            'matched_keywords': ['수주', '실적호조', 'HBM']
        }
    ]
    
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    template_path = os.path.join(base_dir, 'templates', 'news_template.html')
    output_dir = os.path.join(base_dir, 'output')
    
    generator = HTMLGenerator(template_path, output_dir)
    output_file = generator.generate_report(test_news, 'test_report.html')
    
    print(f"\n✅ 테스트 리포트 생성: {output_file}")

