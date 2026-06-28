@echo off
chcp 65001 >nul
echo ==========================================
echo   Python大作业 - 上市公司数据可视化系统
echo ==========================================
echo.
echo 正在启动Flask服务器...
echo 浏览器访问: http://127.0.0.1:5000/login
echo 登录账号: lhl / 111
echo ==========================================
echo.

cd /d "C:\Users\liuha\WorkBuddy\2026-06-17-16-15-58\python期末汇报"
"C:\Users\liuha\.workbuddy\binaries\python\envs\default\Scripts\python.exe" app.py

pause
