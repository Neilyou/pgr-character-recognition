"""
战双角色识别Web应用
使用训练好的ResNet18模型进行角色识别
"""
import os
import json
from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
import io
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB限制

# 全局变量
model = None
class_names = None
device = None
transform = None

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

@app.route('/')
def index():
    """主页"""
    return render_template('character_recognition.html')

@app.route('/api/recognize', methods=['POST'])
def recognize():
    """识别接口"""
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
        
        # 预测
        results = predict_image(image)
        
        # 返回前5个结果
        top_results = results[:5]
        
        return jsonify({
            'success': True,
            'results': top_results,
            'total_classes': len(class_names)
        })
        
    except Exception as e:
        print(f"识别错误: {str(e)}")
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
    print("战双角色识别系统")
    print("=" * 60)
    print("正在加载模型...")
    
    if load_model():
        print("=" * 60)
        print("✓ 系统启动成功！")
        print("访问地址: http://127.0.0.1:5000")
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        app.run(debug=True, port=5000)
    else:
        print("✗ 模型加载失败！")
