# 模型文件说明

## 📁 文件结构

训练完成后，此目录应包含以下文件：

```
models/
├── best_model.pth           # 最佳模型权重（必需）
├── full_model.pth           # 完整模型
├── class_names.json         # 类别映射（必需）
├── model_info.json          # 模型元数据
├── training_history.json    # 训练历史
├── training_curves.png      # 训练曲线图
└── checkpoint_epoch_*.pth   # 训练检查点
```

## 🚀 如何获取模型

### 方法1: 自己训练（推荐）

1. 准备数据集（至少30张/角色）
2. 运行训练脚本：
```bash
python train_classification_model.py
```

3. 训练完成后，模型文件会自动保存到此目录

### 方法2: 下载预训练模型

由于模型文件较大（>100MB），未包含在Git仓库中。

如果有预训练模型可用，请下载并放置在此目录。

## 📊 模型信息

- **架构**: ResNet18
- **输入尺寸**: 224x224
- **输出类别**: 19个角色
- **训练数据**: 709张图片
- **验证准确率**: 80.98%

## ⚠️ 注意事项

1. **必需文件**: `best_model.pth` 和 `class_names.json` 是运行应用的必需文件
2. **文件大小**: 模型文件约44MB，不建议上传到Git
3. **兼容性**: 模型使用PyTorch 2.0+训练，需要相同或更高版本加载

## 🔧 模型使用

模型会被以下文件自动加载：
- `recognition_app.py` (V1版本)
- `recognition_app_v2.py` (V2版本)

无需手动加载模型文件。
