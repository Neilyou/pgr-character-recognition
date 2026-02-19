"""
准备标注工作空间
将所有图片复制到统一目录，并创建类别文件
"""

import os
import shutil
from pathlib import Path

# 配置
SOURCE_DIR = "战双人物图像_调整尺寸"
WORKSPACE_DIR = "annotation_workspace"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
LABELS_DIR = os.path.join(WORKSPACE_DIR, "labels")

# 角色映射（文件夹名 -> 中文名）
CHARACTER_MAPPING = {
    "21hao": "21号",
    "aerfa": "阿尔法",
    "aila": "艾拉",
    "bianka": "比安卡",
    "dubian": "渡边",
    "kaleinina": "卡列尼娜",
    "kuluomu": "库洛姆",
    "lee": "里",
    "lifu": "丽芙",
    "luna": "露娜",
    "luosaita": "罗塞塔",
    "luxiya": "露西亚",
    "nuoan": "诺安",
    "qishi": "七实",
    "qu": "曲",
    "sailinna": "赛琳娜",
    "shenwei": "神威",
    "wanshi": "万事",
    "weila": "薇拉"
}

def create_workspace():
    """创建工作空间目录"""
    print("=" * 60)
    print("创建标注工作空间...")
    print("=" * 60)
    
    # 创建目录
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(LABELS_DIR, exist_ok=True)
    print(f"✓ 创建目录: {IMAGES_DIR}")
    print(f"✓ 创建目录: {LABELS_DIR}")

def copy_images():
    """复制所有图片到统一目录"""
    print("\n" + "=" * 60)
    print("复制图片文件...")
    print("=" * 60)
    
    total_images = 0
    character_stats = {}
    
    for character_folder in sorted(os.listdir(SOURCE_DIR)):
        source_path = os.path.join(SOURCE_DIR, character_folder)
        
        if not os.path.isdir(source_path):
            continue
        
        # 获取该角色的所有图片
        images = [f for f in os.listdir(source_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        character_stats[character_folder] = len(images)
        
        # 复制图片，使用 角色名_原文件名 的格式
        for img_file in images:
            source_file = os.path.join(source_path, img_file)
            # 新文件名格式: 角色文件夹_原文件名
            new_filename = f"{character_folder}_{img_file}"
            dest_file = os.path.join(IMAGES_DIR, new_filename)
            
            shutil.copy2(source_file, dest_file)
            total_images += 1
        
        print(f"✓ {character_folder:12s} - {len(images):3d} 张图片")
    
    print(f"\n总计: {total_images} 张图片")
    return character_stats

def create_classes_file():
    """创建类别文件"""
    print("\n" + "=" * 60)
    print("创建类别文件...")
    print("=" * 60)
    
    classes_file = os.path.join(WORKSPACE_DIR, "classes.txt")
    
    # 按字母顺序排序类别
    sorted_characters = sorted(CHARACTER_MAPPING.keys())
    
    with open(classes_file, 'w', encoding='utf-8') as f:
        for character in sorted_characters:
            f.write(f"{character}\n")
    
    print(f"✓ 创建文件: {classes_file}")
    print(f"✓ 类别数量: {len(sorted_characters)}")
    
    # 同时创建一个带中文名的映射文件
    mapping_file = os.path.join(WORKSPACE_DIR, "character_mapping.txt")
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write("# 角色映射表\n")
        f.write("# 格式: 类别ID | 文件夹名 | 中文名\n\n")
        for idx, character in enumerate(sorted_characters):
            chinese_name = CHARACTER_MAPPING[character]
            f.write(f"{idx:2d} | {character:12s} | {chinese_name}\n")
    
    print(f"✓ 创建文件: {mapping_file}")

def create_readme():
    """创建工作空间说明文件"""
    readme_file = os.path.join(WORKSPACE_DIR, "README.txt")
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write("战双角色标注工作空间\n")
        f.write("=" * 60 + "\n\n")
        f.write("目录结构:\n")
        f.write("  images/              - 待标注图片\n")
        f.write("  labels/              - 标注文件输出目录 (YOLO格式)\n")
        f.write("  classes.txt          - 类别列表\n")
        f.write("  character_mapping.txt - 角色映射表\n\n")
        f.write("使用 LabelImg 进行标注:\n")
        f.write("  1. 启动 LabelImg: labelImg\n")
        f.write("  2. Open Dir: 选择 images/ 目录\n")
        f.write("  3. Change Save Dir: 选择 labels/ 目录\n")
        f.write("  4. 确保使用 YOLO 格式\n")
        f.write("  5. 开始标注\n\n")
        f.write("标注格式 (YOLO):\n")
        f.write("  每个图片对应一个 .txt 文件\n")
        f.write("  格式: <class_id> <x_center> <y_center> <width> <height>\n")
        f.write("  坐标为归一化值 (0-1)\n\n")
        f.write("详细说明请参考: annotation_guide.md\n")
    
    print(f"✓ 创建文件: {readme_file}")

def print_summary(character_stats):
    """打印统计摘要"""
    print("\n" + "=" * 60)
    print("准备完成！")
    print("=" * 60)
    print(f"\n工作空间位置: {os.path.abspath(WORKSPACE_DIR)}")
    print(f"图片目录: {os.path.abspath(IMAGES_DIR)}")
    print(f"标注目录: {os.path.abspath(LABELS_DIR)}")
    
    print("\n下一步操作:")
    print("  1. 安装 LabelImg: pip install labelImg")
    print("  2. 启动标注工具: labelImg")
    print("  3. 参考 annotation_guide.md 进行标注")
    print("  4. 标注完成后运行: python validate_annotations.py")
    
    print("\n数据统计:")
    total = sum(character_stats.values())
    print(f"  总图片数: {total}")
    print(f"  角色数量: {len(character_stats)}")
    print(f"  平均每角色: {total / len(character_stats):.1f} 张")
    
    # 找出图片最多和最少的角色
    max_char = max(character_stats.items(), key=lambda x: x[1])
    min_char = min(character_stats.items(), key=lambda x: x[1])
    print(f"  最多: {max_char[0]} ({max_char[1]} 张)")
    print(f"  最少: {min_char[0]} ({min_char[1]} 张)")

def main():
    """主函数"""
    print("\n战双角色标注准备工具")
    print("=" * 60)
    
    # 检查源目录
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 错误: 找不到源目录 '{SOURCE_DIR}'")
        return
    
    # 创建工作空间
    create_workspace()
    
    # 复制图片
    character_stats = copy_images()
    
    # 创建类别文件
    create_classes_file()
    
    # 创建说明文件
    create_readme()
    
    # 打印摘要
    print_summary(character_stats)

if __name__ == "__main__":
    main()
