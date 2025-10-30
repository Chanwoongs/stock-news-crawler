"""
실행 이력 조회 스크립트
"""
import json
import os
import sys
from datetime import datetime

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def view_history(limit=20):
    """실행 이력 조회"""
    history_file = os.path.join('data', 'run_history.json')
    
    if not os.path.exists(history_file):
        print("❌ 실행 이력이 없습니다.")
        return
    
    with open(history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    if not history:
        print("❌ 실행 이력이 없습니다.")
        return
    
    print("=" * 80)
    print(f"📊 최근 실행 이력 (최근 {min(limit, len(history))}건)")
    print("=" * 80)
    print()
    
    # 최근 N개만 표시
    recent_history = history[-limit:]
    
    for i, record in enumerate(reversed(recent_history), 1):
        print(f"[{i}] {record['timestamp']}")
        print(f"    ├─ 수집: {record['collected']}건")
        print(f"    ├─ 신규: {record['new']}건")
        print(f"    ├─ 필터링 통과: {record['filtered_new']}건")
        print(f"    ├─ 누적 총계: {record['total_accumulated']}건")
        print(f"    └─ 실행 시간: {record['elapsed_seconds']}초")
        print()
    
    # 통계 요약
    print("=" * 80)
    print("📈 통계 요약")
    print("=" * 80)
    total_runs = len(history)
    total_collected = sum(r['collected'] for r in history)
    total_new = sum(r['new'] for r in history)
    total_filtered = sum(r['filtered_new'] for r in history)
    avg_time = sum(r['elapsed_seconds'] for r in history) / total_runs
    
    print(f"총 실행 횟수: {total_runs}회")
    print(f"총 수집 뉴스: {total_collected}건")
    print(f"총 신규 뉴스: {total_new}건")
    print(f"총 필터링 통과: {total_filtered}건")
    print(f"평균 실행 시간: {avg_time:.2f}초")
    
    if recent_history:
        current_accumulated = recent_history[-1]['total_accumulated']
        print(f"현재 누적 뉴스: {current_accumulated}건")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='실행 이력 조회')
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='표시할 최근 이력 개수 (기본: 20)'
    )
    
    args = parser.parse_args()
    view_history(args.limit)

