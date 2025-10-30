"""
데이터 초기화 스크립트 (Python)
"""
import os
import sys
import json

# Windows 콘솔 인코딩
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def reset_data():
    """모든 데이터 초기화"""
    
    print("=" * 60)
    print("\n  🔄 데이터 초기화 스크립트\n")
    print("=" * 60)
    print("\n⚠️  경고: 다음 데이터가 모두 삭제됩니다:\n")
    print("  - 캐시 (data/cache.json)")
    print("  - 누적 뉴스 (data/filtered_news.json)")
    print("  - 실행 이력 (data/run_history.json)")
    print("  - 생성된 HTML (output/*.html)")
    print("  - 실행 로그 (crawler.log)\n")
    
    confirm = input("정말 초기화하시겠습니까? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("\n초기화가 취소되었습니다.")
        return
    
    print("\n🔄 초기화 중...\n")
    
    deleted_count = 0
    
    # 1. cache.json 초기화
    cache_file = "data/cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({"urls": []}, f, ensure_ascii=False, indent=2)
        print("✅ cache.json 초기화")
        deleted_count += 1
    else:
        print("⚠️  cache.json 없음")
    
    # 2. filtered_news.json 삭제
    filtered_file = "data/filtered_news.json"
    if os.path.exists(filtered_file):
        os.remove(filtered_file)
        print("✅ filtered_news.json 삭제")
        deleted_count += 1
    else:
        print("⚠️  filtered_news.json 없음")
    
    # 3. run_history.json 삭제
    history_file = "data/run_history.json"
    if os.path.exists(history_file):
        os.remove(history_file)
        print("✅ run_history.json 삭제")
        deleted_count += 1
    else:
        print("⚠️  run_history.json 없음")
    
    # 4. crawler.log 삭제
    log_file = "crawler.log"
    if os.path.exists(log_file):
        os.remove(log_file)
        print("✅ crawler.log 삭제")
        deleted_count += 1
    else:
        print("⚠️  crawler.log 없음")
    
    # 5. output 폴더의 HTML 파일 삭제
    output_dir = "output"
    html_deleted = 0
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(output_dir, filename)
                os.remove(filepath)
                html_deleted += 1
        if html_deleted > 0:
            print(f"✅ output 폴더 HTML 파일 {html_deleted}개 삭제")
            deleted_count += html_deleted
        else:
            print("⚠️  output 폴더에 HTML 파일 없음")
    else:
        print("⚠️  output 폴더 없음")
    
    print("\n" + "=" * 60)
    print(f"\n✅ 초기화 완료! (총 {deleted_count}개 항목 삭제)\n")
    print("이제 처음부터 다시 시작할 수 있습니다.\n")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        reset_data()
    except KeyboardInterrupt:
        print("\n\n초기화가 취소되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

