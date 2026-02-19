"""
训练战双角色分类模型
使用 ResNet18 架构进行迁移学习
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, datasets, models
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import os
import time
import copy
import json

# 参数配置
config = {
    "data_dir": "classification_dataset",
    "model_name": "resnet18",
    "batch_size": 16,
    "num_epochs": 30,
    "learning_rate": 0.001,
    "input_size": 224,
    "device": torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
    "save_dir": "models",
    "checkpoint_interval": 5  # 每5个epoch保存一次
}

# 数据增强与预处理
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(config['input_size']),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(config['input_size']),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

def load_datasets():
    """加载数据集"""
    print("=" * 60)
    print("加载数据集...")
    print("=" * 60)
    
    image_datasets = {x: datasets.ImageFolder(
        os.path.join(config['data_dir'], x),
        data_transforms[x]
    ) for x in ['train', 'val']}
    
    dataloaders = {x: DataLoader(
        image_datasets[x],
        batch_size=config['batch_size'],
        shuffle=True if x == 'train' else False,
        num_workers=0,  # Windows 上设置为 0
        pin_memory=True if torch.cuda.is_available() else False
    ) for x in ['train', 'val']}
    
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes
    
    print(f"✓ 训练集: {dataset_sizes['train']} 张图片")
    print(f"✓ 验证集: {dataset_sizes['val']} 张图片")
    print(f"✓ 类别数量: {len(class_names)} 个")
    print(f"✓ 类别列表: {class_names}")
    
    return image_datasets, dataloaders, dataset_sizes, class_names

def initialize_model(num_classes):
    """初始化模型"""
    print("\n" + "=" * 60)
    print("初始化模型...")
    print("=" * 60)
    
    # 加载预训练的 ResNet18
    model = models.resnet18(pretrained=True)
    
    # 冻结前面的层（可选）
    # for param in model.parameters():
    #     param.requires_grad = False
    
    # 修改最后一层
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    model = model.to(config['device'])
    
    print(f"✓ 模型: {config['model_name']}")
    print(f"✓ 输出类别: {num_classes}")
    print(f"✓ 设备: {config['device']}")
    
    return model

def train_model(model, criterion, optimizer, scheduler, dataloaders, dataset_sizes, num_epochs):
    """训练模型"""
    print("\n" + "=" * 60)
    print("开始训练...")
    print("=" * 60)
    
    since = time.time()
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0
    
    # 记录训练过程
    history = {
        'train_loss': [],
        'val_loss': [],
        'train_acc': [],
        'val_acc': [],
        'learning_rates': []
    }
    
    # 创建保存目录
    os.makedirs(config['save_dir'], exist_ok=True)
    
    for epoch in range(num_epochs):
        print(f'\nEpoch {epoch+1}/{num_epochs}')
        print('-' * 40)
        
        # 每个epoch都有训练和验证阶段
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()
            
            running_loss = 0.0
            running_corrects = 0
            
            # 迭代数据
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(config['device'])
                labels = labels.to(config['device'])
                
                # 梯度清零
                optimizer.zero_grad()
                
                # 前向传播
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    
                    # 反向传播 + 优化
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                
                # 统计
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            
            if phase == 'train':
                scheduler.step()
            
            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]
            
            # 记录历史
            if phase == 'train':
                history['train_loss'].append(epoch_loss)
                history['train_acc'].append(epoch_acc.item())
                history['learning_rates'].append(optimizer.param_groups[0]['lr'])
            else:
                history['val_loss'].append(epoch_loss)
                history['val_acc'].append(epoch_acc.item())
            
            print(f'{phase:5s} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')
            
            # 保存最佳模型
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model_wts = copy.deepcopy(model.state_dict())
                print(f'  ✓ 新的最佳模型！准确率: {best_acc:.4f}')
        
        # 定期保存检查点
        if (epoch + 1) % config['checkpoint_interval'] == 0:
            checkpoint_path = os.path.join(config['save_dir'], f'checkpoint_epoch_{epoch+1}.pth')
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_acc': best_acc,
                'history': history
            }, checkpoint_path)
            print(f'  ✓ 保存检查点: {checkpoint_path}')
    
    time_elapsed = time.time() - since
    print('\n' + '=' * 60)
    print(f'训练完成！用时 {time_elapsed//60:.0f}分 {time_elapsed%60:.0f}秒')
    print(f'最佳验证准确率: {best_acc:.4f}')
    print('=' * 60)
    
    # 加载最佳模型权重
    model.load_state_dict(best_model_wts)
    return model, history, best_acc

def save_model(model, class_names, history, best_acc):
    """保存模型和相关信息"""
    print("\n" + "=" * 60)
    print("保存模型...")
    print("=" * 60)
    
    # 保存模型权重
    model_path = os.path.join(config['save_dir'], 'best_model.pth')
    torch.save(model.state_dict(), model_path)
    print(f"✓ 模型权重: {model_path}")
    
    # 保存完整模型（包括结构）
    full_model_path = os.path.join(config['save_dir'], 'full_model.pth')
    torch.save(model, full_model_path)
    print(f"✓ 完整模型: {full_model_path}")
    
    # 保存类别名称
    class_names_path = os.path.join(config['save_dir'], 'class_names.json')
    with open(class_names_path, 'w', encoding='utf-8') as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)
    print(f"✓ 类别名称: {class_names_path}")
    
    # 保存训练历史
    history_path = os.path.join(config['save_dir'], 'training_history.json')
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)
    print(f"✓ 训练历史: {history_path}")
    
    # 保存模型信息
    model_info = {
        'model_name': config['model_name'],
        'num_classes': len(class_names),
        'class_names': class_names,
        'input_size': config['input_size'],
        'best_accuracy': float(best_acc),
        'num_epochs': config['num_epochs'],
        'batch_size': config['batch_size'],
        'learning_rate': config['learning_rate']
    }
    
    info_path = os.path.join(config['save_dir'], 'model_info.json')
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(model_info, f, ensure_ascii=False, indent=2)
    print(f"✓ 模型信息: {info_path}")

def visualize_training(history):
    """可视化训练过程"""
    print("\n" + "=" * 60)
    print("生成训练曲线...")
    print("=" * 60)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Loss 曲线
    axes[0, 0].plot(history['train_loss'], label='Train Loss', linewidth=2)
    axes[0, 0].plot(history['val_loss'], label='Val Loss', linewidth=2)
    axes[0, 0].set_title('Loss Curve', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Accuracy 曲线
    axes[0, 1].plot(history['train_acc'], label='Train Acc', linewidth=2)
    axes[0, 1].plot(history['val_acc'], label='Val Acc', linewidth=2)
    axes[0, 1].set_title('Accuracy Curve', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Learning Rate 曲线
    axes[1, 0].plot(history['learning_rates'], linewidth=2, color='green')
    axes[1, 0].set_title('Learning Rate', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Learning Rate')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 训练 vs 验证准确率对比
    epochs = range(1, len(history['train_acc']) + 1)
    axes[1, 1].plot(epochs, history['train_acc'], 'b-', label='Train Acc', linewidth=2)
    axes[1, 1].plot(epochs, history['val_acc'], 'r-', label='Val Acc', linewidth=2)
    axes[1, 1].fill_between(epochs, history['train_acc'], history['val_acc'], alpha=0.2)
    axes[1, 1].set_title('Train vs Val Accuracy', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Accuracy')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存图表
    plot_path = os.path.join(config['save_dir'], 'training_curves.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"✓ 训练曲线: {plot_path}")
    
    plt.show()

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("战双角色分类模型训练")
    print("=" * 60)
    print(f"设备: {config['device']}")
    print(f"批次大小: {config['batch_size']}")
    print(f"训练轮数: {config['num_epochs']}")
    print(f"学习率: {config['learning_rate']}")
    
    # 加载数据
    image_datasets, dataloaders, dataset_sizes, class_names = load_datasets()
    
    # 初始化模型
    model = initialize_model(len(class_names))
    
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config['learning_rate'])
    
    # 学习率调度器
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)
    
    # 训练模型
    model, history, best_acc = train_model(
        model, criterion, optimizer, scheduler,
        dataloaders, dataset_sizes, config['num_epochs']
    )
    
    # 保存模型
    save_model(model, class_names, history, best_acc)
    
    # 可视化训练过程
    visualize_training(history)
    
    print("\n" + "=" * 60)
    print("✅ 训练完成！")
    print("=" * 60)
    print(f"\n模型文件位置: {os.path.abspath(config['save_dir'])}")
    print("\n下一步:")
    print("  1. 查看训练曲线: models/training_curves.png")
    print("  2. 测试模型: python test_model.py")
    print("  3. 集成到Web应用: 更新 app.py")

if __name__ == '__main__':
    main()
