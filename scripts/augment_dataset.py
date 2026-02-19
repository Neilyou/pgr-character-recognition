"""
数据增强脚本
为样本不足的角色生成增强图片
"""

import os
import cv2
import numpy as np
from pathlib import Path
import random

SOURCE_DIR = "战双人物图像_调整尺寸"
OUTPUT_DIR = "战双人物图像_增强"

# 需要增强的角色及目标数量
AUGMENT_TARGETS = {
    'qu': 20,          # 从2张增强到20张
    'shenwei': 20,     # 从5张增强到20张
    'wanshi': 20,      # 从5张增强到20张
    'dubian': 20,      # 从7张增强到20张
    'qishi': 20,       # 从7张增强到20张
    'kaleinina': 20,   # 从11张增强到20张
    'nuoan': 20,       # 从11张增强到20张
    'sailinna': 20,    # 从11张增强到20张
    '21hao': 20,       # 从12张增强到20张
    'aila': 20,        # 从14张增强到20张
}

def augment_image(image):
    """对单张图片进行随机增强"""
    augmented_images = []
    
    # 1. 水平翻转
    flipped = cv2.flip(image, 1)
    augmented_images.append(('flip', flipped))
    
    # 2. 旋转 (-15° 到 15°)
    for angle in [-15, -10, -5, 5, 10, 15]:
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, matrix, (w, h), 
                                 borderMode=cv2.BORDER_REFLECT)
        augmented_images.append((f'rot{angle}', rotated))
    
    # 3. 亮度调整
    for factor in [0.7, 0.85, 1.15, 1.3]:
        adjusted = cv2.convertScaleAbs(image, alpha=factor, beta=0)
        augmented_images.append((f'bright{factor}', adjusted))
    
    # 4. 对比度调整
    for factor in [0.8, 1.2]:
        adjusted = cv2.convertScaleAbs(image, alpha=factor, beta=0)
        augmented_images.append((f'contrast{factor}', adjusted))
    
    # 5. 高斯模糊
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    augmented_images.append(('blur', blurred))
    
    # 6. 锐化
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    augmented_images.append(('sharp', sharpened))
    
    # 7. 色调调整
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    for shift in [-10, 10]:
        hsv_shifted = hsv.copy()
        hsv_shifted[:,:,0] = (hsv_shifted[:,:,0] + shift) % 180
        hue_shifted = cv2.cvtColor(hsv_shifted, cv2.COLOR_HSV2BGR)
        augmented_images.append((f'hue{shift}', hue_shifted))
    
    # 8. 饱和度调整
    for factor in [0.7, 1.3]:
        hsv_sat = hsv.copy()
        hsv_sat[:,:,1] = np.clip(hsv_sat[:,:,1] * factor, 0, 255)
        sat_adjusted = cv2.cvtColor(hsv_sat, cv2.COLOR_HSV2BGR)
        augmented_images.append((f'sat{factor}', sat_adjusted))
    
    return augmented_images

def augment_character(character, target_count):
    """为单个角色生成增强图片"""
    source_path = os.path.join(SOURCE_DIR, character)
    output_path = os.path.join(OUTPUT_DIR, character)
    
    if not os.path.exists(source_path):
        print(f"❌ 找不到角色目录: {character}")
        return
    
    os.makedirs(output_path, exist_ok=True)
    
    # 获取原始图片
    original_images = [f for f in os.listdir(source_path)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    current_count = len(original_images)
    needed = target_count - current_count
    
    print(f"\n{character}:")
    print(f"  原始图片: {current_count} 张")
    print(f"  目标数量: {target_count} 张")
    print(f"  需要生成: {needed} 张")
    
    # 复制原始图片
    for img_file in original_images:
        src = os.path.join(source_path, img_file)
        dst = os.path.join(output_path, img_file)
        image = cv2.imread(src)
        cv2.imwrite(dst, image)
    
    if needed <= 0:
        print(f"  ✓ 无需增强")
        return
    
    # 生成增强图片
    generated = 0
    random.seed(42)
    
    while generated < needed:
        # 随机选择一张原始图片
        img_file = random.choice(original_images)
        img_path = os.path.join(source_path, img_file)
        image = cv2.imread(img_path)
        
        if image is None:
            continue
        
        # 生成增强图片
        augmented = augment_image(image)
        
        # 随机选择一种增强方式
        aug_type, aug_image = random.choice(augmented)
        
        # 保存
        base_name = Path(img_file).stem
        ext = Path(img_file).suffix
        output_name = f"{base_name}_aug{generated}_{aug_type}{ext}"
        output_file = os.path.join(output_path, output_name)
        
        cv2.imwrite(output_file, aug_image)
        generated += 1
        
        if generated % 5 == 0:
            print(f"  进度: {generated}/{needed}")
    
    print(f"  ✓ 完成！总计: {current_count + generated} 张")

def main():
    """主函数"""
    print("=" * 60)
    print("战双角色数据增强工具")
    print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    total_original = 0
    total_augmented = 0
    
    for character, target in AUGMENT_TARGETS.items():
        augment_character(character, target)
        
        source_path = os.path.join(SOURCE_DIR, character)
        if os.path.exists(source_path):
            original = len([f for f in os.listdir(source_path)
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
            total_original += original
            total_augmented += target
    
    # 复制不需要增强的角色
    print("\n" + "=" * 60)
    print("复制其他角色...")
    print("=" * 60)
    
    for character in os.listdir(SOURCE_DIR):
        if character in AUGMENT_TARGETS:
            continue
        
        source_path = os.path.join(SOURCE_DIR, character)
        if not os.path.isdir(source_path):
            continue
        
        output_path = os.path.join(OUTPUT_DIR, character)
        os.makedirs(output_path, exist_ok=True)
        
        images = [f for f in os.listdir(source_path)
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        for img_file in images:
            src = os.path.join(source_path, img_file)
            dst = os.path.join(output_path, img_file)
            image = cv2.imread(src)
            if image is not None:
                cv2.imwrite(dst, image)
        
        print(f"✓ {character}: {len(images)} 张")
        total_original += len(images)
        total_augmented += len(images)
    
    print("\n" + "=" * 60)
    print("数据增强完成！")
    print("=" * 60)
    print(f"\n原始数据集: {total_original} 张")
    print(f"增强后数据集: {total_augmented} 张")
    print(f"增加: {total_augmented - total_original} 张 (+{(total_augmented/total_original-1)*100:.1f}%)")
    print(f"\n输出目录: {os.path.abspath(OUTPUT_DIR)}")
    print("\n下一步:")
    print("  1. 检查增强后的图片质量")
    print("  2. 使用增强后的数据集重新训练")
    print("  3. 修改 prepare_classification_dataset.py 中的 SOURCE_DIR")

if __name__ == "__main__":
    main()
