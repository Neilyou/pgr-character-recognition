@echo off
echo ============================================================
echo GitHub上传助手
echo ============================================================
echo.

REM 检查Git是否已安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Git，请先安装Git
    echo 下载地址: https://git-scm.com/
    pause
    exit /b 1
)

echo [1/6] 检查Git配置...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo.
    echo 首次使用需要配置Git用户信息
    set /p username="请输入你的GitHub用户名: "
    set /p email="请输入你的GitHub邮箱: "
    git config --global user.name "%username%"
    git config --global user.email "%email%"
    echo 配置完成！
)

echo.
echo [2/6] 初始化Git仓库...
if not exist .git (
    git init
    echo Git仓库已初始化
) else (
    echo Git仓库已存在
)

echo.
echo [3/6] 添加文件到暂存区...
git add .
echo 文件已添加

echo.
echo [4/6] 提交到本地仓库...
git commit -m "Initial commit: PGR Character Recognition System"
if errorlevel 1 (
    echo 提交失败或没有新的更改
) else (
    echo 提交成功！
)

echo.
echo [5/6] 连接远程仓库...
echo.
echo 请先在GitHub创建仓库，然后复制仓库URL
echo 例如: https://github.com/your-username/pgr-character-recognition.git
echo.
set /p repo_url="请输入GitHub仓库URL: "

git remote remove origin 2>nul
git remote add origin %repo_url%
echo 远程仓库已连接

echo.
echo [6/6] 推送到GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo [失败] 推送失败，可能的原因：
    echo 1. 需要输入GitHub用户名和密码（或Personal Access Token）
    echo 2. 远程仓库已有内容
    echo 3. 网络连接问题
    echo.
    echo 请查看 GITHUB_UPLOAD_GUIDE.md 获取详细帮助
) else (
    echo.
    echo ============================================================
    echo [成功] 项目已成功上传到GitHub！
    echo ============================================================
    echo.
    echo 访问你的仓库: %repo_url%
    echo.
)

pause
