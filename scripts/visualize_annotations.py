"""
可视化标注结果
在图片上绘制边界框，用于检查标注质量
"""

import os
import cv2
import random
from pathlib import Path

WORKSPACE_DIR = "annotation_workspace"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
LABELS_DIR = os.path.join(WORKSPACE_DIR, "labels")
CLASSES_FILE = os.path.join(WORKSPACE_DIR, "classes.txt")
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "visualizations")

# 为每个类别生成随机颜色
def generate_colors(num_classes):
    """为每个类别生成不同的颜色"""
    random.seed(42)  # 固定随机种子，保证颜色一致
    colors = []
    for i in range(num_classes):
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        colors.append(color)
    return colors

def load_classes():
    """加载类别列表"""
    if not os.path.exists(CLASSES_FILE):
        print(f"❌ 找不到类别文件: {CLASSES_FILE}")
        return []
    
    with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f if line.strip()]
    
    return classes

def draw_boxes(image_path, label_path, classes, colors, output_path):
    """在图片上绘制边界框"""
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 无法读取图片: {image_path}")
        return False
    
    height, width = img.shape[:2]
    
    # 读取标注
    if not os.path.exists(label_path):
        # 没有标注，保存原图
        cv2.imwrite(output_path, img)
        return True
    
    try:
        with open(label_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            box_width = float(parts[3])
            box_height = float(parts[4])
            
            # 转换为像素坐标
            x_center_px = int(x_center * width)
            y_center_px = int(y_center * height)
            box_width_px = int(box_width * width)
            box_height_px = int(box_height * height)
            
            # 计算边界框坐标
            x1 = int(x_center_px - box_width_px / 2)
            y1 = int(y_center_px - box_height_px / 2)
            x2 = int(x_center_px + box_width_px / 2)
            y2 = int(y_center_px + box_height_px / 2)
            
            # 获取颜色和类别名
            color = colors[class_id] if class_id < len(colors) else (255, 255, 255)
            class_name = classes[class_id] if class_id < len(classes) else f"Class_{class_id}"
            
            # 绘制边界框
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            
            # 绘制标签背景
            label_text = f"{class_name}"
            (text_width, text_height), baseline = cv2.getTextSize(
                label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            
            label_y = y1 - 10 if y1 - 10 > text_height else y1 + text_height + 10
            cv2.rectangle(
                img,
                (x1, label_y - text_height - 5),
                (x1 + text_width + 5, label_y + 5),
                color,
                -1
            )
            
            # 绘制标签文字
            cv2.putText(
                img,
                label_text,
                (x1 + 2, label_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )
        
        # 保存结果
        cv2.imwrite(output_path, img)
        return True
    
    except Exception as e:
        print(f"❌ 处理失败 {image_path}: {e}")
        return False

def main():
    """主函数"""
    print("\n战双角色标注可视化工具")
    print("=" * 60)
    
    # 加载类别
    classes = load_classes()
    if not classes:
        return
    
    print(f"✓ 加载类别: {len(classes)} 个")
    
    # 生成颜色
    colors = generate_colors(len(classes))
    
    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✓ 输出目录: {OUTPUT_DIR}")
    
    # 获取所有图片
    if not os.path.exists(IMAGES_DIR):
        print(f"❌ 找不到图片目录: {IMAGES_DIR}")
        return
    
    image_files = [f for f in os.listdir(IMAGES_DIR)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    if not image_files:
        print("❌ 没有找到图片文件")
        return
    
    print(f"✓ 找到图片: {len(image_files)} 张")
    
    # 处理图片
    print("\n" + "=" * 60)
    print("生成可视化...")
    print("=" * 60)
    
    success_count = 0
    
    for idx, img_file in enumerate(image_files, 1):
        image_path = os.path.join(IMAGES_DIR, img_file)
        label_path = os.path.join(LABELS_DIR, Path(img_file).stem + '.txt')
        output_path = os.path.join(OUTPUT_DIR, img_file)
        
        if draw_boxes(image_path, label_path, classes, colors, output_path):
            success_count += 1
            if idx % 10 == 0:
                print(f"  处理进度: {idx}/{len(image_files)}")
    
    print(f"\n✓ 完成: {success_count}/{len(image_files)} 张")
    print(f"\n可视化结果保存在: {os.path.abspath(OUTPUT_DIR)}")
    print("\n建议:")
    print("  1. 打开输出目录查看标注效果")
    print("  2. 检查边界框是否准确")
    print("  3. 检查类别标签是否正确")
    print("  4. 如有问题，返回 LabelImg 修正")

if __name__ == "__main__":
    main()
