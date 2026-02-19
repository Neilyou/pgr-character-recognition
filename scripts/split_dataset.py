"""
划分数据集为训练集、验证集和测试集
确保每个类别在各集合中都有代表
"""

import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

WORKSPACE_DIR = "annotation_workspace"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
LABELS_DIR = os.path.join(WORKSPACE_DIR, "labels")
CLASSES_FILE = os.path.join(WORKSPACE_DIR, "classes.txt")

# 输出目录
DATASET_DIR = "dataset"
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")
TEST_DIR = os.path.join(DATASET_DIR, "test")

# 划分比例
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def load_classes():
    """加载类别列表"""
    with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f if line.strip()]
    return classes

def get_annotated_images():
    """获取所有已标注的图片"""
    annotated = []
    
    for img_file in os.listdir(IMAGES_DIR):
        if not img_file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        
        label_file = os.path.join(LABELS_DIR, Path(img_file).stem + '.txt')
        if os.path.exists(label_file):
            annotated.append(img_file)
    
    return annotated

def group_by_character(images):
    """按角色分组图片"""
    groups = defaultdict(list)
    
    for img_file in images:
        # 从文件名提取角色名（格式: 角色名_原文件名）
        character = img_file.split('_')[0]
        groups[character].append(img_file)
    
    return groups

def split_images(images, train_ratio, val_ratio, test_ratio):
    """划分图片列表"""
    random.shuffle(images)
    
    total = len(images)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_set = images[:train_end]
    val_set = images[train_end:val_end]
    test_set = images[val_end:]
    
    return train_set, val_set, test_set

def copy_files(image_list, dest_dir):
    """复制图片和标注文件到目标目录"""
    images_dest = os.path.join(dest_dir, "images")
    labels_dest = os.path.join(dest_dir, "labels")
    
    os.makedirs(images_dest, exist_ok=True)
    os.makedirs(labels_dest, exist_ok=True)
    
    for img_file in image_list:
        # 复制图片
        src_img = os.path.join(IMAGES_DIR, img_file)
        dst_img = os.path.join(images_dest, img_file)
        shutil.copy2(src_img, dst_img)
        
        # 复制标注
        label_file = Path(img_file).stem + '.txt'
        src_label = os.path.join(LABELS_DIR, label_file)
        dst_label = os.path.join(labels_dest, label_file)
        
        if os.path.exists(src_label):
            shutil.copy2(src_label, dst_label)

def create_data_yaml(classes, dataset_dir):
    """创建 YOLO 格式的数据配置文件"""
    yaml_file = os.path.join(dataset_dir, "data.yaml")
    
    with open(yaml_file, 'w', encoding='utf-8') as f:
        f.write(f"# 战双角色检测数据集配置\n\n")
        f.write(f"path: {os.path.abspath(dataset_dir)}\n")
        f.write(f"train: train/images\n")
        f.write(f"val: val/images\n")
        f.write(f"test: test/images\n\n")
        f.write(f"nc: {len(classes)}\n")
        f.write(f"names: {classes}\n")
    
    print(f"✓ 创建配置文件: {yaml_file}")

def print_statistics(train_set, val_set, test_set, character_groups):
    """打印统计信息"""
    print("\n" + "=" * 60)
    print("数据集划分统计")
    print("=" * 60)
    
    print(f"\n总体统计:")
    print(f"  训练集: {len(train_set)} 张 ({len(train_set)/(len(train_set)+len(val_set)+len(test_set))*100:.1f}%)")
    print(f"  验证集: {len(val_set)} 张 ({len(val_set)/(len(train_set)+len(val_set)+len(test_set))*100:.1f}%)")
    print(f"  测试集: {len(test_set)} 张 ({len(test_set)/(len(train_set)+len(val_set)+len(test_set))*100:.1f}%)")
    print(f"  总计: {len(train_set) + len(val_set) + len(test_set)} 张")
    
    print(f"\n各角色分布:")
    print(f"  {'角色':12s} | {'训练':>4s} | {'验证':>4s} | {'测试':>4s} | {'总计':>4s}")
    print(f"  {'-'*12}-+-{'-'*4}-+-{'-'*4}-+-{'-'*4}-+-{'-'*4}")
    
    for character in sorted(character_groups.keys()):
        train_count = sum(1 for img in train_set if img.startswith(character + '_'))
        val_count = sum(1 for img in val_set if img.startswith(character + '_'))
        test_count = sum(1 for img in test_set if img.startswith(character + '_'))
        total = train_count + val_count + test_count
        
        print(f"  {character:12s} | {train_count:4d} | {val_count:4d} | {test_count:4d} | {total:4d}")

def main():
    """主函数"""
    print("\n战双角色数据集划分工具")
    print("=" * 60)
    
    # 设置随机种子
    random.seed(42)
    
    # 加载类别
    classes = load_classes()
    print(f"✓ 加载类别: {len(classes)} 个")
    
    # 获取已标注的图片
    images = get_annotated_images()
    if not images:
        print("❌ 没有找到已标注的图片")
        return
    
    print(f"✓ 找到已标注图片: {len(images)} 张")
    
    # 按角色分组
    character_groups = group_by_character(images)
    print(f"✓ 角色数量: {len(character_groups)} 个")
    
    # 检查每个角色的图片数量
    print("\n各角色图片数量:")
    for character, imgs in sorted(character_groups.items()):
        print(f"  {character:12s}: {len(imgs):3d} 张")
    
    # 为每个角色分别划分数据集
    print("\n" + "=" * 60)
    print("划分数据集...")
    print("=" * 60)
    
    all_train = []
    all_val = []
    all_test = []
    
    for character, imgs in character_groups.items():
        if len(imgs) < 3:
            # 图片太少，全部放入训练集
            print(f"⚠️  {character}: 图片太少({len(imgs)}张)，全部放入训练集")
            all_train.extend(imgs)
        else:
            train, val, test = split_images(imgs, TRAIN_RATIO, VAL_RATIO, TEST_RATIO)
            all_train.extend(train)
            all_val.extend(val)
            all_test.extend(test)
    
    # 打乱顺序
    random.shuffle(all_train)
    random.shuffle(all_val)
    random.shuffle(all_test)
    
    # 创建目录结构
    print("\n创建目录结构...")
    for dir_path in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        os.makedirs(dir_path, exist_ok=True)
    
    # 复制文件
    print("复制文件...")
    copy_files(all_train, TRAIN_DIR)
    print(f"  ✓ 训练集: {len(all_train)} 张")
    
    copy_files(all_val, VAL_DIR)
    print(f"  ✓ 验证集: {len(all_val)} 张")
    
    copy_files(all_test, TEST_DIR)
    print(f"  ✓ 测试集: {len(all_test)} 张")
    
    # 创建配置文件
    create_data_yaml(classes, DATASET_DIR)
    
    # 打印统计
    print_statistics(all_train, all_val, all_test, character_groups)
    
    # 总结
    print("\n" + "=" * 60)
    print("✅ 数据集划分完成！")
    print("=" * 60)
    print(f"\n数据集位置: {os.path.abspath(DATASET_DIR)}")
    print(f"配置文件: {os.path.join(DATASET_DIR, 'data.yaml')}")
    
    print("\n目录结构:")
    print("  dataset/")
    print("  ├── data.yaml")
    print("  ├── train/")
    print("  │   ├── images/")
    print("  │   └── labels/")
    print("  ├── val/")
    print("  │   ├── images/")
    print("  │   └── labels/")
    print("  └── test/")
    print("      ├── images/")
    print("      └── labels/")
    
    print("\n下一步:")
    print("  1. 检查数据集划分是否合理")
    print("  2. 开始训练目标检测模型")
    print("  3. 使用命令: python train_detection_model.py")

if __name__ == "__main__":
    main()
