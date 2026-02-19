# 效果图说明

## 📸 需要的截图

### 1. 主页上传界面 (upload_page.png)
- 访问 http://127.0.0.1:5000
- 截取完整的上传页面
- 建议尺寸: 1920x1080 或 1280x720

### 2. 识别结果页面 (detection_result.png)
- 上传一张角色图片
- 等待识别完成
- 截取显示检测框和识别结果的页面
- 确保能看到：
  - 图片上的检测框
  - 右侧的识别结果列表
  - 置信度信息

### 3. 训练曲线图 (training_curves.png)
- 位置: `models/training_curves.png`
- 直接复制到此文件夹
- 展示模型训练过程

### 4. 多角色识别 (multi_character.png) - 可选
- 上传包含多个角色的图片
- 展示同时识别多个角色的效果

## 🎨 截图技巧

### Windows截图方法

1. **全屏截图**: `Win + PrtScn`
2. **区域截图**: `Win + Shift + S`
3. **使用Snipping Tool**: 搜索"截图工具"

### 截图要求

- **格式**: PNG（推荐）或JPG
- **质量**: 高清，文字清晰可读
- **内容**: 完整展示功能，避免个人信息
- **大小**: 单张不超过2MB

## 📝 命名规范

建议的文件名：
- `upload_page.png` - 上传页面
- `detection_result.png` - 识别结果
- `training_curves.png` - 训练曲线
- `multi_character.png` - 多角色识别（可选）

## 🔄 更新截图

如果需要更新截图：
1. 替换对应的图片文件
2. 保持文件名不变
3. 提交到Git: `git add screenshots/ && git commit -m "Update screenshots"`
