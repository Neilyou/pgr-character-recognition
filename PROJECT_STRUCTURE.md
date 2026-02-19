# 项目结构说明

## 📁 目录结构

```
pgr-character-recognition/
│
├── 📄 README.md                      # 项目说明
├── 📄 QUICKSTART.md                  # 快速开始指南
├── 📄 LICENSE                        # MIT许可证
├── 📄 requirements.txt               # Python依赖
├── 📄 .gitignore                     # Git忽略文件
│
├── 🚀 recognition_app_v2.py          # V2 Web应用（人脸检测+识别）
├── 🚀 recognition_app.py             # V1 Web应用（直接识别）
├── 🎓 train_classification_model.py  # 模型训练脚本
│
├── 🪟 start_app_v2.bat               # Windows启动脚本（V2）
├── 🪟 start_app.bat                  # Windows启动脚本（V1）
│
├── 📂 templates/                     # HTML模板
│   ├── character_recognition_v2.html # V2前端页面
│   └── character_recognition.html    # V1前端页面
│
├── 📂 models/                        # 模型文件（需训练生成）
│   ├── README.md                     # 模型说明
│   ├── best_model.pth               # 最佳模型权重
│   ├── class_names.json             # 类别映射
│   └── model_info.json              # 模型元数据
│
├── 📂 scripts/                       # 工具脚本
│   ├── README.md                     # 脚本说明
│   ├── process_and_augment.py       # 数据处理和增强
│   ├── prepare_classification_dataset.py # 准备训练数据
│   ├── image_size_adj.py            # 图片尺寸调整
│   ├── augment_dataset.py           # 数据增强
│   ├── prepare_annotation.py        # 准备标注数据
│   ├── validate_annotations.py      # 验证标注
│   ├── visualize_annotations.py     # 可视化标注
│   └── split_dataset.py             # 划分数据集
│
├── 📂 docs/                          # 文档
│   ├── WEB_APP_GUIDE.md             # Web应用使用指南
│   ├── V2_UPGRADE_GUIDE.md          # V2版本升级指南
│   ├── PROJECT_SUMMARY.md           # 项目总结
│   ├── DATASET_ANALYSIS.md          # 数据集分析
│   ├── IMAGE_COLLECTION_GUIDE.md    # 图片收集指南
│   ├── annotation_guide.md          # 标注指南
│   └── ANNOTATION_QUICKSTART.md     # 标注快速开始
│
├── 📂 战双人物图像_原始数据/         # 原始图片（不上传Git）
│   ├── 21hao/
│   ├── aerfa/
│   └── ...                          # 19个角色文件夹
│
├── 📂 战双人物图像_调整尺寸/         # 处理后图片（不上传Git）
│   ├── 21hao/
│   ├── aerfa/
│   └── ...                          # 19个角色文件夹
│
├── 📂 classification_dataset/        # 训练数据集（不上传Git）
│   ├── train/                       # 训练集
│   ├── val/                         # 验证集
│   └── class_mapping.txt            # 类别映射
│
└── 📂 annotation_workspace/          # 标注工作区（可选）
    ├── images/                      # 待标注图片
    └── labels/                      # 标注文件
```

## 📝 文件说明

### 核心文件

| 文件 | 说明 | 必需 |
|------|------|------|
| `recognition_app_v2.py` | V2应用主程序 | ✅ |
| `train_classification_model.py` | 模型训练脚本 | ✅ |
| `requirements.txt` | Python依赖列表 | ✅ |
| `models/best_model.pth` | 训练好的模型 | ✅ |
| `models/class_names.json` | 类别映射文件 | ✅ |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README.md` | 项目主文档 |
| `QUICKSTART.md` | 快速开始指南 |
| `docs/WEB_APP_GUIDE.md` | 详细使用指南 |
| `docs/V2_UPGRADE_GUIDE.md` | V2版本说明 |

### 工具脚本

| 脚本 | 用途 |
|------|------|
| `scripts/process_and_augment.py` | 数据预处理 |
| `scripts/prepare_classification_dataset.py` | 准备训练数据 |
| `scripts/augment_dataset.py` | 数据增强 |

## 🚫 不上传到Git的内容

以下内容已在 `.gitignore` 中配置：

- `战双人物图像_原始数据/` - 原始图片（太大）
- `战双人物图像_调整尺寸/` - 处理后图片（太大）
- `classification_dataset/` - 训练数据集（太大）
- `models/*.pth` - 模型文件（太大，>100MB）
- `annotation_workspace/` - 标注工作区（临时文件）
- `.kiro/` - IDE配置
- `__pycache__/` - Python缓存

## 📦 Git仓库大小

上传到Git的文件：
- Python代码：~50KB
- HTML/CSS：~100KB
- 文档：~200KB
- 配置文件：~10KB

**总计**: 约360KB（非常轻量）

## 🔄 工作流程

1. **克隆项目** → 获取代码
2. **准备数据** → 放入原始图片
3. **处理数据** → 运行scripts中的脚本
4. **训练模型** → 生成models文件
5. **启动应用** → 使用recognition_app_v2.py

## 💡 提示

- 模型文件需要单独下载或自己训练
- 数据集不包含在Git仓库中
- 首次使用需要准备数据和训练模型
- 所有大文件都已在.gitignore中排除
