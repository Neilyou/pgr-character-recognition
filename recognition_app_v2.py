"""
战双角色识别Web应用 V2
使用人脸检测 + 角色识别的两阶段方案
"""
import os
import json
from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw
import torch
import torch.nn as nn
from torchvision import models, transforms
import io
import base64
import cv2
import numpy as np

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB限制

# 全局变量
model = None
class_names = None
device = None
transform = None
face_cascade = None

def load_face_detector():
    """加载人脸检测器"""
    global face_cascade
    
    # 使用OpenCV的Haar Cascade人脸检测器
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    # 也加载动漫人脸检测器（如果可用）
    anime_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'
    if os.path.exists(anime_cascade_path):
        print("加载动漫人脸检测器")
    
    print("人脸检测器加载成功！")
    return True

def detect_faces(image):
    """
    检测图片中的人脸
    返回: [(x, y, w, h, confidence), ...]
    """
    global face_cascade
    
    # 转换为OpenCV格式
    img_array = np.array(image)
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # 检测人脸 - 使用多个尺度参数以提高检测率
    faces = []
    
    # 尝试不同的参数组合
    params = [
        {'scaleFactor': 1.1, 'minNeighbors': 3, 'minSize': (30, 30)},
        {'scaleFactor': 1.05, 'minNeighbors': 3, 'minSize': (20, 20)},
        {'scaleFactor': 1.2, 'minNeighbors': 5, 'minSize': (40, 40)},
    ]
    
    for param in params:
        detected = face_cascade.detectMultiScale(
            gray,
            scaleFactor=param['scaleFactor'],
            minNeighbors=param['minNeighbors'],
            minSize=param['minSize']
        )
        
        for (x, y, w, h) in detected:
            # 计算置信度（基于检测框大小）
            confidence = min(1.0, (w * h) / (image.width * image.height * 0.5))
            faces.append((x, y, w, h, confidence))
    
    # 去重（合并重叠的检测框）
    faces = merge_overlapping_boxes(faces)
    
    # 如果没有检测到人脸，返回整张图片
    if len(faces) == 0:
        print("未检测到人脸，使用整张图片")
        return [(0, 0, image.width, image.height, 0.5)]
    
    print(f"检测到 {len(faces)} 个人脸区域")
    return faces

def merge_overlapping_boxes(boxes, iou_threshold=0.3):
    """合并重叠的检测框"""
    if len(boxes) == 0:
        return []
    
    # 按置信度排序
    boxes = sorted(boxes, key=lambda x: x[4], reverse=True)
    
    merged = []
    used = [False] * len(boxes)
    
    for i in range(len(boxes)):
        if used[i]:
            continue
        
        x1, y1, w1, h1, conf1 = boxes[i]
        merged.append(boxes[i])
        used[i] = True
        
        # 检查是否与其他框重叠
        for j in range(i + 1, len(boxes)):
            if used[j]:
                continue
            
            x2, y2, w2, h2, conf2 = boxes[j]
            
            # 计算IoU
            x_left = max(x1, x2)
            y_top = max(y1, y2)
            x_right = min(x1 + w1, x2 + w2)
            y_bottom = min(y1 + h1, y2 + h2)
            
            if x_right > x_left and y_bottom > y_top:
                intersection = (x_right - x_left) * (y_bottom - y_top)
                area1 = w1 * h1
                area2 = w2 * h2
                union = area1 + area2 - intersection
                iou = intersection / union if union > 0 else 0
                
                if iou > iou_threshold:
                    used[j] = True
    
    return merged

def expand_bbox(x, y, w, h, img_width, img_height, expand_ratio=0.3):
    """
    扩展边界框以包含更多上下文
    expand_ratio: 扩展比例（0.3表示每边扩展30%）
    """
    # 计算扩展量
    expand_w = int(w * expand_ratio)
    expand_h = int(h * expand_ratio)
    
    # 扩展边界框
    new_x = max(0, x - expand_w)
    new_y = max(0, y - expand_h)
    new_w = min(img_width - new_x, w + 2 * expand_w)
    new_h = min(img_height - new_y, h + 2 * expand_h)
    
    return new_x, new_y, new_w, new_h

def load_model():
    """加载训练好的模型"""
    global model, class_names, device, transform
    
    # 设置设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"使用设备: {device}")
    
    # 加载类别名称
    with open('models/class_names.json', 'r', encoding='utf-8') as f:
        class_names = json.load(f)
    print(f"加载了 {len(class_names)} 个类别")
    
    # 加载模型
    model = models.resnet18(pretrained=False)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(class_names))
    
    # 加载权重
    model.load_state_dict(torch.load('models/best_model.pth', map_location=device))
    model = model.to(device)
    model.eval()
    print("模型加载成功！")
    
    # 定义图像预处理
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    return True

def get_character_display_name(class_name):
    """将类别名称转换为显示名称"""
    name_mapping = {
        '21hao': '21号',
        'aerfa': '阿尔法',
        'aila': '艾拉',
        'bianka': '比安卡',
        'dubian': '渡边',
        'kaleinina': '卡列尼娜',
        'kuluomu': '库洛姆',
        'lee': '里',
        'lifu': '丽芙',
        'luna': '露娜',
        'luosaita': '罗塞塔',
        'luxiya': '露西亚',
        'nuoan': '诺安',
        'qishi': '七实',
        'qu': '曲',
        'sailinna': '赛琳娜',
        'shenwei': '神威',
        'wanshi': '万事',
        'weila': '薇拉'
    }
    return name_mapping.get(class_name, class_name)

def predict_image(image):
    """预测图片中的角色"""
    global model, class_names, device, transform
    
    # 预处理图像
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    img_tensor = transform(image).unsqueeze(0).to(device)
    
    # 预测
    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        
    # 获取所有类别的概率
    probs = probabilities[0].cpu().numpy()
    
    # 创建结果列表（按概率排序）
    results = []
    for idx, prob in enumerate(probs):
        results.append({
            'class_name': class_names[idx],
            'display_name': get_character_display_name(class_names[idx]),
            'confidence': float(prob)
        })
    
    # 按置信度排序
    results.sort(key=lambda x: x['confidence'], reverse=True)
    
    return results

def predict_with_face_detection(image):
    """
    使用人脸检测 + 角色识别的两阶段方案
    """
    # 第一阶段：检测人脸
    faces = detect_faces(image)
    
    # 第二阶段：对每个人脸区域进行识别
    detections = []
    
    for idx, (x, y, w, h, face_conf) in enumerate(faces):
        # 扩展边界框以包含更多上下文
        exp_x, exp_y, exp_w, exp_h = expand_bbox(
            x, y, w, h, 
            image.width, image.height, 
            expand_ratio=0.5  # 扩展50%
        )
        
        # 裁剪人脸区域
        face_region = image.crop((exp_x, exp_y, exp_x + exp_w, exp_y + exp_h))
        
        # 识别角色
        results = predict_image(face_region)
        
        # 获取最佳结果
        best_result = results[0]
        
        # 组合人脸检测置信度和识别置信度
        combined_confidence = best_result['confidence'] * (0.7 + 0.3 * face_conf)
        
        detections.append({
            'id': idx + 1,
            'bbox': {
                'x': int(exp_x),
                'y': int(exp_y),
                'width': int(exp_w),
                'height': int(exp_h)
            },
            'bbox_percent': {
                'x': float((exp_x / image.width) * 100),
                'y': float((exp_y / image.height) * 100),
                'width': float((exp_w / image.width) * 100),
                'height': float((exp_h / image.height) * 100)
            },
            'character': best_result['display_name'],
            'class_name': best_result['class_name'],
            'confidence': float(combined_confidence),
            'face_confidence': float(face_conf),
            'recognition_confidence': float(best_result['confidence']),
            'top5_results': results[:5]
        })
    
    # 按置信度排序
    detections.sort(key=lambda x: x['confidence'], reverse=True)
    
    return detections

@app.route('/')
def index():
    """主页"""
    return render_template('character_recognition_v2.html')

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """识别接口 - 使用人脸检测"""
    try:
        # 检查是否有文件
        if 'image' not in request.files:
            return jsonify({'error': '没有上传图片'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 读取图片
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # 使用人脸检测 + 识别
        detections = predict_with_face_detection(image)
        
        return jsonify({
            'success': True,
            'detections': detections,
            'num_faces': len(detections),
            'total_classes': len(class_names)
        })
        
    except Exception as e:
        print(f"识别错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'识别失败: {str(e)}'}), 500

@app.route('/api/model_info')
def model_info():
    """获取模型信息"""
    try:
        with open('models/model_info.json', 'r', encoding='utf-8') as f:
            info = json.load(f)
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("战双角色识别系统 V2")
    print("人脸检测 + 角色识别")
    print("=" * 60)
    print("正在加载人脸检测器...")
    
    if not load_face_detector():
        print("✗ 人脸检测器加载失败！")
        exit(1)
    
    print("正在加载角色识别模型...")
    
    if load_model():
        print("=" * 60)
        print("✓ 系统启动成功！")
        print("访问地址: http://127.0.0.1:5000")
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        app.run(debug=True, port=5000)
    else:
        print("✗ 模型加载失败！")
