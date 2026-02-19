"""
为图像分类任务准备数据集
将战双人物图像_调整尺寸目录划分为训练集和验证集
"""

import os
import shutil
import random
from pathlib import Path

# 配置
SOURCE_DIR = "战双人物图像_调整尺寸"
OUTPUT_DIR = "classification_dataset"
TRAIN_DIR = os.path.join(OUTPUT_DIR, "train")
VAL_DIR = os.path.join(OUTPUT_DIR, "val")

# 划分比例
TRAIN_RATIO = 0.85  # 85% 训练，15% 验证
RANDOM_SEED = 42

def create_directories():
    """创建输出目录结构"""
    print("=" * 60)
    print("创建目录结构...")
    print("=" * 60)
    
    for split in ['train', 'val']:
        split_dir = os.path.join(OUTPUT_DIR, split)
        os.makedirs(split_dir, exist_ok=True)
    
    print(f"✓ 创建目录: {OUTPUT_DIR}")

def split_and_copy_images():
    """划分并复制图片"""
    print("\n" + "=" * 60)
    print("划分数据集...")
    print("=" * 60)
    
    random.seed(RANDOM_SEED)
    
    character_stats = {}
    total_train = 0
    total_val = 0
    
    # 遍历每个角色文件夹
    for character_folder in sorted(os.listdir(SOURCE_DIR)):
        source_path = os.path.join(SOURCE_DIR, character_folder)
        
        if not os.path.isdir(source_path):
            continue
        
        # 创建角色子目录
        train_char_dir = os.path.join(TRAIN_DIR, character_folder)
        val_char_dir = os.path.join(VAL_DIR, character_folder)
        os.makedirs(train_char_dir, exist_ok=True)
        os.makedirs(val_char_dir, exist_ok=True)
        
        # 获取所有图片
        images = [f for f in os.listdir(source_path)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        if not images:
            continue
        
        # 打乱顺序
        random.shuffle(images)
        
        # 划分数据
        split_idx = int(len(images) * TRAIN_RATIO)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # 确保验证集至少有1张图片（如果总数>=2）
        if len(images) >= 2 and len(val_images) == 0:
            val_images = [train_images.pop()]
        
        # 复制训练集图片
        for img in train_images:
            src = os.path.join(source_path, img)
            dst = os.path.join(train_char_dir, img)
            shutil.copy2(src, dst)
        
        # 复制验证集图片
        for img in val_images:
            src = os.path.join(source_path, img)
            dst = os.path.join(val_char_dir, img)
            shutil.copy2(src, dst)
        
        character_stats[character_folder] = {
            'train': len(train_images),
            'val': len(val_images),
            'total': len(images)
        }
        
        total_train += len(train_images)
        total_val += len(val_images)
        
        print(f"✓ {character_folder:12s} - 训练: {len(train_images):3d}, 验证: {len(val_images):3d}, 总计: {len(images):3d}")
    
    return character_stats, total_train, total_val

def create_class_mapping(character_stats):
    """创建类别映射文件"""
    mapping_file = os.path.join(OUTPUT_DIR, "class_mapping.txt")
    
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write("# 战双角色类别映射\n")
        f.write("# 格式: 类别ID | 文件夹名 | 训练集数量 | 验证集数量\n\n")
        
        for idx, (character, stats) in enumerate(sorted(character_stats.items())):
            f.write(f"{idx:2d} | {character:12s} | {stats['train']:3d} | {stats['val']:3d}\n")
    
    print(f"\n✓ 创建类别映射: {mapping_file}")

def print_summary(character_stats, total_train, total_val):
    """打印统计摘要"""
    print("\n" + "=" * 60)
    print("数据集划分完成！")
    print("=" * 60)
    
    print(f"\n总体统计:")
    print(f"  训练集: {total_train} 张 ({total_train/(total_train+total_val)*100:.1f}%)")
    print(f"  验证集: {total_val} 张 ({total_val/(total_train+total_val)*100:.1f}%)")
    print(f"  总计: {total_train + total_val} 张")
    print(f"  角色数量: {len(character_stats)} 个")
    
    print(f"\n数据集位置:")
    print(f"  {os.path.abspath(OUTPUT_DIR)}")
    
    print(f"\n目录结构:")
    print(f"  {OUTPUT_DIR}/")
    print(f"  ├── train/")
    for character in sorted(character_stats.keys())[:3]:
        print(f"  │   ├── {character}/")
    print(f"  │   └── ...")
    print(f"  ├── val/")
    for character in sorted(character_stats.keys())[:3]:
        print(f"  │   ├── {character}/")
    print(f"  │   └── ...")
    print(f"  └── class_mapping.txt")
    
    print(f"\n下一步:")
    print(f"  1. 检查数据集划分是否合理")
    print(f"  2. 运行训练脚本: python train_classification_model.py")

def main():
    """主函数"""
    print("\n战双角色分类数据集准备工具")
    print("=" * 60)
    
    # 检查源目录
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 错误: 找不到源目录 '{SOURCE_DIR}'")
        return
    
    # 创建目录
    create_directories()
    
    # 划分并复制图片
    character_stats, total_train, total_val = split_and_copy_images()
    
    # 创建类别映射
    create_class_mapping(character_stats)
    
    # 打印摘要
    print_summary(character_stats, total_train, total_val)

if __name__ == "__main__":
    main()
