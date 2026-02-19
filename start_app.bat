@echo off
echo ============================================================
echo 战双角色识别系统 - 启动脚本
echo ============================================================
echo.

REM 激活conda环境
call conda activate llava

REM 启动应用
python recognition_app.py

pause
