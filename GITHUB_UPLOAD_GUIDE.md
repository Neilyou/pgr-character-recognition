# GitHub上传完整指南

## 📋 准备工作

### 1. 确保已安装Git

检查Git是否已安装：
```bash
git --version
```

如果未安装，请从 https://git-scm.com/ 下载安装。

### 2. 配置Git用户信息（首次使用）

```bash
# 设置用户名
git config --global user.name "你的GitHub用户名"

# 设置邮箱
git config --global user.email "你的GitHub邮箱"

# 验证配置
git config --list
```

## 🚀 上传步骤

### 步骤1: 初始化本地仓库

在项目根目录打开命令行：

```bash
# 初始化Git仓库
git init

# 查看状态
git status
```

### 步骤2: 添加文件到暂存区

```bash
# 添加所有文件
git add .

# 查看将要提交的文件
git status
```

### 步骤3: 提交到本地仓库

```bash
git commit -m "Initial commit: PGR Character Recognition System"
```

### 步骤4: 在GitHub创建远程仓库

1. 登录 https://github.com
2. 点击右上角的 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `pgr-character-recognition`
   - **Description**: `战双帕弥什角色识别系统 - 基于深度学习的游戏角色识别Web应用`
   - **Public** 或 **Private**（根据需要选择）
   - **不要**勾选 "Initialize this repository with a README"
   - **不要**添加 .gitignore 和 license（我们已经有了）
4. 点击 "Create repository"

### 步骤5: 连接远程仓库

复制GitHub显示的仓库URL，然后执行：

```bash
# 添加远程仓库（替换为你的URL）
git remote add origin https://github.com/你的用户名/pgr-character-recognition.git

# 验证远程仓库
git remote -v
```

### 步骤6: 推送到GitHub

```bash
# 重命名分支为main（GitHub默认）
git branch -M main

# 推送到远程仓库
git push -u origin main
```

## 🔐 认证方式

### 方式1: HTTPS（推荐新手）

使用HTTPS URL时，需要输入GitHub用户名和密码（或Personal Access Token）。

**创建Personal Access Token**：
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. 勾选 `repo` 权限
4. 生成并保存token（只显示一次）
5. 推送时使用token作为密码

### 方式2: SSH

```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "你的邮箱"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 复制公钥到GitHub
# GitHub → Settings → SSH and GPG keys → New SSH key
```

使用SSH URL：
```bash
git remote set-url origin git@github.com:你的用户名/pgr-character-recognition.git
```

## 📝 完整命令序列

```bash
# 1. 配置Git（首次使用）
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"

# 2. 初始化并提交
git init
git add .
git commit -m "Initial commit: PGR Character Recognition System"

# 3. 连接远程仓库（替换URL）
git remote add origin https://github.com/你的用户名/pgr-character-recognition.git

# 4. 推送
git branch -M main
git push -u origin main
```

## ✅ 验证上传成功

1. 访问你的GitHub仓库页面
2. 应该能看到所有文件
3. README.md会自动显示在首页

## 🎨 美化GitHub仓库

### 添加Topics（标签）

在仓库页面点击 "Add topics"，添加：
- `deep-learning`
- `pytorch`
- `computer-vision`
- `flask`
- `character-recognition`
- `pgr`
- `punishing-gray-raven`

### 添加About

在仓库页面右侧 "About" 区域：
- Description: `战双帕弥什角色识别系统 - 基于深度学习的游戏角色识别Web应用`
- Website: 如果有部署的网站
- Topics: 添加相关标签

### 创建Release（可选）

1. 点击 "Releases" → "Create a new release"
2. Tag version: `v1.0.0`
3. Release title: `V1.0.0 - Initial Release`
4. Description: 描述主要功能
5. Publish release

## 📊 项目统计

上传后的仓库信息：
- **文件数**: 35个
- **代码行数**: ~3000行
- **仓库大小**: ~400KB
- **语言**: Python (90%), HTML (8%), Other (2%)

## 🔄 后续更新

当你修改代码后，更新到GitHub：

```bash
# 查看修改
git status

# 添加修改的文件
git add .

# 提交
git commit -m "描述你的修改"

# 推送
git push
```

## ❓ 常见问题

### Q: 推送时要求输入密码

A: 使用Personal Access Token代替密码

### Q: 提示"fatal: remote origin already exists"

A: 删除现有远程仓库：
```bash
git remote remove origin
git remote add origin 新的URL
```

### Q: 推送被拒绝

A: 可能是远程仓库有更新：
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Q: 文件太大无法上传

A: 检查.gitignore是否正确配置，确保大文件被排除

## 📞 获取帮助

- GitHub文档: https://docs.github.com
- Git文档: https://git-scm.com/doc
- 提交Issue寻求帮助

---

**准备好分享你的项目了！** 🚀
