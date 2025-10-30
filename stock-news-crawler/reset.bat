@echo off
chcp 65001 > nul
echo ======================================
echo.
echo   데이터 초기화 스크립트
echo.
echo ======================================
echo.
echo ⚠️  경고: 다음 데이터가 모두 삭제됩니다:
echo.
echo   - 캐시 (data/cache.json)
echo   - 누적 뉴스 (data/filtered_news.json)
echo   - 실행 이력 (data/run_history.json)
echo   - 생성된 HTML (output/*.html)
echo   - 실행 로그 (crawler.log)
echo.
set /p confirm="정말 초기화하시겠습니까? (y/N): "

if /i "%confirm%" neq "y" (
    echo.
    echo 초기화가 취소되었습니다.
    pause
    exit /b
)

echo.
echo 🔄 초기화 중...
echo.

:: 캐시 초기화
if exist "data\cache.json" (
    echo {"urls": []} > data\cache.json
    echo ✅ cache.json 초기화
) else (
    echo ⚠️  cache.json 없음
)

:: 누적 뉴스 삭제
if exist "data\filtered_news.json" (
    del /f /q "data\filtered_news.json"
    echo ✅ filtered_news.json 삭제
) else (
    echo ⚠️  filtered_news.json 없음
)

:: 실행 이력 삭제
if exist "data\run_history.json" (
    del /f /q "data\run_history.json"
    echo ✅ run_history.json 삭제
) else (
    echo ⚠️  run_history.json 없음
)

:: 로그 파일 삭제
if exist "crawler.log" (
    del /f /q "crawler.log"
    echo ✅ crawler.log 삭제
) else (
    echo ⚠️  crawler.log 없음
)

:: output 폴더의 HTML 파일 삭제
if exist "output\*.html" (
    del /f /q "output\*.html"
    echo ✅ output 폴더 HTML 파일 삭제
) else (
    echo ⚠️  output 폴더에 HTML 파일 없음
)

echo.
echo ======================================
echo.
echo ✅ 초기화 완료!
echo.
echo 이제 처음부터 다시 시작할 수 있습니다.
echo.
echo ======================================
echo.
pause

