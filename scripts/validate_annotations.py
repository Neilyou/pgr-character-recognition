"""
验证标注文件的正确性
检查格式、坐标范围、类别ID等
"""

import os
from pathlib import Path

WORKSPACE_DIR = "annotation_workspace"
IMAGES_DIR = os.path.join(WORKSPACE_DIR, "images")
LABELS_DIR = os.path.join(WORKSPACE_DIR, "labels")
CLASSES_FILE = os.path.join(WORKSPACE_DIR, "classes.txt")

def load_classes():
    """加载类别列表"""
    if not os.path.exists(CLASSES_FILE):
        print(f"❌ 找不到类别文件: {CLASSES_FILE}")
        return []
    
    with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f if line.strip()]
    
    return classes

def get_image_files():
    """获取所有图片文件"""
    if not os.path.exists(IMAGES_DIR):
        print(f"❌ 找不到图片目录: {IMAGES_DIR}")
        return []
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    images = []
    
    for file in os.listdir(IMAGES_DIR):
        if Path(file).suffix.lower() in image_extensions:
            images.append(file)
    
    return sorted(images)

def validate_annotation_file(label_file, num_classes):
    """验证单个标注文件"""
    errors = []
    warnings = []
    num_boxes = 0
    
    try:
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            warnings.append("标注文件为空")
            return errors, warnings, 0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            
            # 检查格式
            if len(parts) != 5:
                errors.append(f"行 {line_num}: 格式错误，应为5个值 (class_id x y w h)")
                continue
            
            try:
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
            except ValueError as e:
                errors.append(f"行 {line_num}: 数值格式错误 - {e}")
                continue
            
            # 检查类别ID
            if class_id < 0 or class_id >= num_classes:
                errors.append(f"行 {line_num}: 类别ID {class_id} 超出范围 [0, {num_classes-1}]")
            
            # 检查坐标范围
            if not (0 <= x_center <= 1):
                errors.append(f"行 {line_num}: x_center {x_center} 超出范围 [0, 1]")
            if not (0 <= y_center <= 1):
                errors.append(f"行 {line_num}: y_center {y_center} 超出范围 [0, 1]")
            if not (0 < width <= 1):
                errors.append(f"行 {line_num}: width {width} 超出范围 (0, 1]")
            if not (0 < height <= 1):
                errors.append(f"行 {line_num}: height {height} 超出范围 (0, 1]")
            
            # 检查边界框是否超出图片
            x_min = x_center - width / 2
            x_max = x_center + width / 2
            y_min = y_center - height / 2
            y_max = y_center + height / 2
            
            if x_min < 0 or x_max > 1 or y_min < 0 or y_max > 1:
                warnings.append(f"行 {line_num}: 边界框超出图片范围")
            
            # 检查边界框大小
            if width < 0.01 or height < 0.01:
                warnings.append(f"行 {line_num}: 边界框过小 (w={width:.3f}, h={height:.3f})")
            if width > 0.95 or height > 0.95:
                warnings.append(f"行 {line_num}: 边界框过大 (w={width:.3f}, h={height:.3f})")
            
            num_boxes += 1
    
    except Exception as e:
        errors.append(f"读取文件失败: {e}")
    
    return errors, warnings, num_boxes

def main():
    """主函数"""
    print("\n战双角色标注验证工具")
    print("=" * 60)
    
    # 加载类别
    classes = load_classes()
    if not classes:
        return
    
    print(f"✓ 加载类别: {len(classes)} 个")
    
    # 获取图片列表
    images = get_image_files()
    if not images:
        return
    
    print(f"✓ 找到图片: {len(images)} 张")
    
    # 验证标注
    print("\n" + "=" * 60)
    print("验证标注文件...")
    print("=" * 60)
    
    total_images = len(images)
    annotated_images = 0
    total_boxes = 0
    total_errors = 0
    total_warnings = 0
    
    missing_annotations = []
    files_with_errors = []
    files_with_warnings = []
    
    for img_file in images:
        # 获取对应的标注文件
        label_file = os.path.join(LABELS_DIR, Path(img_file).stem + '.txt')
        
        if not os.path.exists(label_file):
            missing_annotations.append(img_file)
            continue
        
        annotated_images += 1
        
        # 验证标注文件
        errors, warnings, num_boxes = validate_annotation_file(label_file, len(classes))
        
        total_boxes += num_boxes
        
        if errors:
            total_errors += len(errors)
            files_with_errors.append((img_file, errors))
            print(f"❌ {img_file}")
            for error in errors:
                print(f"   - {error}")
        elif warnings:
            total_warnings += len(warnings)
            files_with_warnings.append((img_file, warnings))
            print(f"⚠️  {img_file}")
            for warning in warnings:
                print(f"   - {warning}")
    
    # 打印统计
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    
    print(f"\n图片统计:")
    print(f"  总图片数: {total_images}")
    print(f"  已标注: {annotated_images} ({annotated_images/total_images*100:.1f}%)")
    print(f"  未标注: {len(missing_annotations)} ({len(missing_annotations)/total_images*100:.1f}%)")
    
    print(f"\n标注统计:")
    print(f"  总边界框数: {total_boxes}")
    if annotated_images > 0:
        print(f"  平均每张: {total_boxes/annotated_images:.2f} 个")
    
    print(f"\n质量检查:")
    print(f"  错误数: {total_errors}")
    print(f"  警告数: {total_warnings}")
    print(f"  有错误的文件: {len(files_with_errors)}")
    print(f"  有警告的文件: {len(files_with_warnings)}")
    
    # 显示未标注的图片
    if missing_annotations:
        print(f"\n未标注的图片 ({len(missing_annotations)}):")
        for img in missing_annotations[:10]:  # 只显示前10个
            print(f"  - {img}")
        if len(missing_annotations) > 10:
            print(f"  ... 还有 {len(missing_annotations) - 10} 张")
    
    # 类别分布统计
    print("\n" + "=" * 60)
    print("类别分布统计")
    print("=" * 60)
    
    class_counts = {i: 0 for i in range(len(classes))}
    
    for img_file in images:
        label_file = os.path.join(LABELS_DIR, Path(img_file).stem + '.txt')
        if os.path.exists(label_file):
            try:
                with open(label_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) == 5:
                            class_id = int(parts[0])
                            if 0 <= class_id < len(classes):
                                class_counts[class_id] += 1
            except:
                pass
    
    for class_id, count in sorted(class_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {classes[class_id]:12s}: {count:3d} 个边界框")
    
    # 总结
    print("\n" + "=" * 60)
    if total_errors == 0 and len(missing_annotations) == 0:
        print("✅ 验证通过！所有标注文件格式正确。")
    elif total_errors == 0:
        print("⚠️  标注格式正确，但有未标注的图片。")
    else:
        print("❌ 发现错误，请修正后重新验证。")
    print("=" * 60)

if __name__ == "__main__":
    main()
