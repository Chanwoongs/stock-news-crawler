@echo off
chcp 65001 > nul
echo ======================================
echo    주식 호재 뉴스 크롤러
echo ======================================
echo.

cd /d %~dp0

echo [1] 1회 실행 (테스트)
echo [2] 스케줄러 실행 (5분마다)
echo.
choice /c 12 /n /m "선택하세요: "

if errorlevel 2 goto schedule
if errorlevel 1 goto once

:once
echo.
echo 1회 실행 중...
python src\main.py --mode once
pause
goto end

:schedule
echo.
echo 스케줄러 시작... (Ctrl+C로 종료)
python src\main.py --mode schedule
goto end

:end

