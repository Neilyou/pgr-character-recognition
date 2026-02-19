# 快速开始指南

## 🚀 5分钟快速部署

### 步骤1: 克隆项目

```bash
git clone https://github.com/your-username/pgr-character-recognition.git
cd pgr-character-recognition
```

### 步骤2: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤3: 下载或训练模型

**选项A: 使用预训练模型（推荐）**

如果有预训练模型，下载并放入 `models/` 目录：
- `best_model.pth`
- `class_names.json`

**选项B: 自己训练模型**

```bash
# 1. 准备数据（将图片放入 战双人物图像_原始数据/）
python scripts/process_and_augment.py

# 2. 准备训练数据集
python scripts/prepare_classification_dataset.py

# 3. 训练模型（需要20-30分钟）
python train_classification_model.py
```

### 步骤4: 启动应用

**Windows:**
```bash
start_app_v2.bat
```

**Linux/Mac:**
```bash
python recognition_app_v2.py
```

### 步骤5: 访问应用

在浏览器打开：http://127.0.0.1:5000

## 📱 使用方法

1. 点击或拖拽上传角色图片
2. 点击"开始识别"按钮
3. 查看识别结果

## ❓ 常见问题

### Q: 提示"模型文件不存在"

A: 需要先训练模型或下载预训练模型到 `models/` 目录

### Q: 识别速度很慢

A: 
- CPU模式下需要2-4秒
- 如果有GPU，安装CUDA版本的PyTorch可以加速

### Q: 识别准确率低

A: 
- 确保图片清晰，角色可见
- V2版本对复杂背景效果更好
- 可以尝试多次识别

### Q: 人脸检测失败

A: 
- 确保角色正面朝向
- 避免严重遮挡
- 如果检测失败，系统会自动使用整张图片

## 📚 更多文档

- [完整使用指南](docs/WEB_APP_GUIDE.md)
- [V2版本说明](docs/V2_UPGRADE_GUIDE.md)
- [项目总结](docs/PROJECT_SUMMARY.md)

## 🆘 获取帮助

如有问题，请查看 [Issues](https://github.com/your-username/pgr-character-recognition/issues)
