import os
from PIL import Image, ImageOps

def pad_image(input_path, output_path, target_size=(224, 224), fill_color=(0, 0, 0)):
    """填充图片到目标尺寸并保存"""
    try:
        img = Image.open(input_path)
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
      
        # 保存图片
        canvas.save(output_path)
        print(f"Processed: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def batch_process(root_input_dir, root_output_dir, target_size=(224, 224), fill_color=(0, 0, 0)):
    """批量处理所有子文件夹中的图片"""
    # 遍历所有子文件夹
    for subdir, _, files in os.walk(root_input_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # 输入路径
                input_path = os.path.join(subdir, file)
              
                # 输出路径（保持相同目录结构）
                relative_path = os.path.relpath(subdir, root_input_dir)
                output_subdir = os.path.join(root_output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                output_path = os.path.join(output_subdir, file)
              
                # 处理图片
                pad_image(input_path, output_path, target_size, fill_color)

# 参数设置
root_input_dir = "E:\AI学习\战双人物识别\战双人物图像_原始数据"   # 替换为你的输入目录
root_output_dir = "E:\AI学习\战双人物识别\战双人物图像_调整尺寸"  # 替换为你的输出目录
target_size = (224, 224)  # 目标尺寸
fill_color = (0, 0, 0)     # 填充颜色（黑色）

# 执行批量处理
batch_process(root_input_dir, root_output_dir, target_size, fill_color)