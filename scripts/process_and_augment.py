import os
from PIL import Image
import random

def pad_image(img, target_size=(224, 224), fill_color=(0, 0, 0)):
    """填充图片到目标尺寸"""
    # 计算缩放比例（保持长宽比）
    width, height = img.size
    target_width, target_height = target_size
    ratio = min(target_width / width, target_height / height)
    new_size = (int(width * ratio), int(height * ratio))
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # 创建画布并居中粘贴图片
    canvas = Image.new("RGB", target_size, fill_color)
    offset = (
        (target_width - new_size[0]) // 2,
        (target_height - new_size[1]) // 2
    )
    canvas.paste(img, offset)
    
    return canvas

def process_character_folder(input_dir, output_dir, character_name, min_images=30):
    """处理单个角色文件夹"""
    input_folder = os.path.join(input_dir, character_name)
    output_folder = os.path.join(output_dir, character_name)
    
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    
    # 获取所有图片文件
    image_files = []
    for file in os.listdir(input_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_files.append(file)
    
    original_count = len(image_files)
    print(f"\n处理 {character_name}: 原始图片 {original_count} 张")
    
    # 第一步：处理所有原始图片
    processed_images = []
    for idx, file in enumerate(image_files):
        try:
            input_path = os.path.join(input_folder, file)
            img = Image.open(input_path)
            
            # 转换为RGB（处理RGBA等格式）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整尺寸
            processed_img = pad_image(img)
            
            # 保存原始处理后的图片
            output_filename = f"{idx}.jpg"
            output_path = os.path.join(output_folder, output_filename)
            processed_img.save(output_path, quality=95)
            
            processed_images.append((processed_img, output_filename))
            
        except Exception as e:
            print(f"  错误处理 {file}: {str(e)}")
    
    # 第二步：如果图片少于30张，进行数据增强
    if len(processed_images) < min_images:
        needed = min_images - len(processed_images)
        print(f"  需要增强 {needed} 张图片（通过水平翻转）")
        
        # 随机选择图片进行翻转
        augment_count = 0
        while augment_count < needed and processed_images:
            # 随机选择一张图片
            original_img, original_name = random.choice(processed_images)
            
            # 水平翻转
            flipped_img = original_img.transpose(Image.FLIP_LEFT_RIGHT)
            
            # 保存翻转后的图片
            new_idx = len(processed_images) + augment_count
            output_filename = f"{new_idx}_flip.jpg"
            output_path = os.path.join(output_folder, output_filename)
            flipped_img.save(output_path, quality=95)
            
            augment_count += 1
        
        final_count = len(processed_images) + augment_count
        print(f"  完成！最终图片数: {final_count} 张 (原始: {len(processed_images)}, 增强: {augment_count})")
    else:
        print(f"  完成！最终图片数: {len(processed_images)} 张")
    
    return len(processed_images)

def main():
    """主函数"""
    input_dir = "战双人物图像_原始数据"
    output_dir = "战双人物图像_调整尺寸"
    min_images = 30
    
    print("=" * 60)
    print("战双角色图片处理与增强脚本")
    print("=" * 60)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"最小图片数: {min_images}")
    print("=" * 60)
    
    # 获取所有角色文件夹
    character_folders = []
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        if os.path.isdir(item_path):
            character_folders.append(item)
    
    character_folders.sort()
    print(f"\n找到 {len(character_folders)} 个角色文件夹")
    
    # 处理每个角色
    total_original = 0
    total_final = 0
    
    for character in character_folders:
        count = process_character_folder(input_dir, output_dir, character, min_images)
        total_original += count
        
        # 统计最终数量
        output_folder = os.path.join(output_dir, character)
        final_count = len([f for f in os.listdir(output_folder) if f.endswith('.jpg')])
        total_final += final_count
    
    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)
    print(f"总原始图片: {total_original} 张")
    print(f"总最终图片: {total_final} 张")
    print(f"增强图片: {total_final - total_original} 张")
    print("=" * 60)
    
    # 显示每个角色的最终统计
    print("\n各角色最终图片数量:")
    print("-" * 40)
    for character in sorted(character_folders):
        output_folder = os.path.join(output_dir, character)
        count = len([f for f in os.listdir(output_folder) if f.endswith('.jpg')])
        status = "✅" if count >= min_images else "⚠️"
        print(f"{status} {character:15s}: {count:3d} 张")

if __name__ == "__main__":
    main()
