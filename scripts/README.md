# 工具脚本说明

本目录包含数据处理和模型训练的辅助脚本。

## 📝 脚本列表

### 数据处理

- **`process_and_augment.py`** - 数据处理和增强主脚本
  - 调整图片尺寸到224x224
  - 对少于30张的角色进行水平翻转增强
  - 确保所有角色至少有30张图片

- **`prepare_classification_dataset.py`** - 准备训练数据集
  - 将数据划分为训练集(85%)和验证集(15%)
  - 创建classification_dataset目录结构

- **`image_size_adj.py`** - 批量调整图片尺寸
  - 保持长宽比
  - 填充到目标尺寸

- **`augment_dataset.py`** - 数据增强脚本
  - 多种增强策略（旋转、翻转、亮度调整等）

### 标注工具

- **`prepare_annotation.py`** - 准备标注数据
  - 为目标检测任务准备图片
  - 创建annotation_workspace目录

- **`validate_annotations.py`** - 验证标注文件
  - 检查YOLO格式标注的正确性

- **`visualize_annotations.py`** - 可视化标注
  - 在图片上绘制标注框
  - 用于检查标注质量

- **`split_dataset.py`** - 划分数据集
  - 将标注数据划分为train/val/test

## 🚀 使用流程

### 1. 数据准备

```bash
# 将原始图片放入 战双人物图像_原始数据/ 文件夹
# 每个角色一个子文件夹

# 运行数据处理
python scripts/process_and_augment.py
```

### 2. 准备训练数据

```bash
python scripts/prepare_classification_dataset.py
```

### 3. 训练模型

```bash
# 返回项目根目录
python train_classification_model.py
```

## 📊 数据要求

- **最少图片数**: 每个角色至少20-30张
- **图片格式**: JPG, PNG, WEBP
- **图片质量**: 清晰、角色可见
- **命名规范**: 数字编号（0.jpg, 1.jpg, ...）

## ⚠️ 注意事项

1. 运行脚本前确保已安装所有依赖
2. 大型数据集处理可能需要较长时间
3. 建议在处理前备份原始数据
4. 某些脚本需要在项目根目录运行
