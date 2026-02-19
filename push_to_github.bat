@echo off
echo ============================================================
echo 推送到GitHub
echo ============================================================
echo.

echo 正在推送到远程仓库...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo ✓ 推送成功！
    echo ============================================================
    echo.
    echo 访问你的GitHub仓库查看更新：
    echo https://github.com/Neilyou/pgr-character-recognition
    echo.
) else (
    echo.
    echo ============================================================
    echo ✗ 推送失败
    echo ============================================================
    echo.
    echo 可能的原因：
    echo 1. 网络连接问题
    echo 2. 需要身份验证
    echo 3. 远程仓库有更新
    echo.
    echo 解决方法：
    echo 1. 检查网络连接
    echo 2. 稍后重试
    echo 3. 查看 GITHUB_STATUS.md 了解更多解决方案
    echo.
)

pause
