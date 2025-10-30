"""
장 시간대만 실행하는 스케줄러
- 평일 오전 8:30 ~ 오후 4:00만 실행
- 1분마다 크롤링
- 장 마감 후에는 대기
"""
import schedule
import time
import sys
from datetime import datetime
from src.main import StockNewsCrawler

# Windows 콘솔 인코딩
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def is_trading_hours():
    """한국 장 시간인가? (평일 8:30~16:00)"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    # 주말 체크
    if now.weekday() >= 5:  # 토요일(5), 일요일(6)
        return False
    
    # 오전 8:30 ~ 오후 4:00 (16:00)
    if hour == 8 and minute >= 30:
        return True
    elif 9 <= hour < 16:
        return True
    
    return False


def run_if_trading_hours():
    """장 시간에만 크롤링 실행"""
    now = datetime.now()
    
    if is_trading_hours():
        print("\n" + "=" * 60)
        print(f"🔥 [{now.strftime('%H:%M:%S')}] 장 시간 - 크롤링 실행!")
        print("=" * 60)
        
        try:
            crawler = StockNewsCrawler()
            crawler.run_once()
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    else:
        # 장 마감 후에는 30분마다 한 번만 출력
        if now.minute % 30 == 0:
            weekday_name = ["월", "화", "수", "목", "금", "토", "일"][now.weekday()]
            if now.weekday() >= 5:
                print(f"😴 [{now.strftime('%H:%M')}] 주말 - 대기 중...")
            else:
                print(f"😴 [{now.strftime('%H:%M')}] 장 마감 - 대기 중... (다음 실행: 내일 오전 8:30)")


def main():
    """메인 실행"""
    print("=" * 60)
    print("🚀 장 시간대 실시간 뉴스 크롤러 시작!")
    print("=" * 60)
    print("⏰ 실행 시간: 평일 오전 8:30 ~ 오후 4:00")
    print("🔄 크롤링 주기: 1분마다")
    print("💤 장 마감 시간: 대기 (절전 모드)")
    print("=" * 60)
    
    now = datetime.now()
    if is_trading_hours():
        print(f"✅ 현재 장 시간입니다! 크롤링을 시작합니다.")
    else:
        weekday = now.weekday()
        if weekday >= 5:
            print(f"⚠️ 현재 주말입니다. 월요일 오전 8:30까지 대기합니다.")
        else:
            print(f"⚠️ 현재 장 마감 시간입니다. 내일 오전 8:30까지 대기합니다.")
    
    print("=" * 60)
    print("⚡ Ctrl+C를 눌러 종료할 수 있습니다.\n")
    
    # 시작하자마자 한 번 실행
    run_if_trading_hours()
    
    # 1분마다 체크
    schedule.every(1).minutes.do(run_if_trading_hours)
    
    # 무한 루프
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # 30초마다 스케줄 체크
    except KeyboardInterrupt:
        print("\n\n👋 크롤러를 종료합니다.")
        print("=" * 60)


if __name__ == "__main__":
    main()

