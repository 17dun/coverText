#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片叠加脚本
遍历img-background目录中的所有图片，并在每个图片上叠加img-element目录中的PNG元素
"""

import os
import sys
from PIL import Image
import argparse

def overlay_images(background_path, element_path, output_path, position=(0, 0), opacity=1.0, scale_factor=1.0):
    """
    在背景图片上叠加元素图片
    
    Args:
        background_path: 背景图片路径
        element_path: 元素图片路径（PNG格式，支持透明度）
        output_path: 输出图片路径
        position: 元素图片在背景上的位置 (x, y) 或预设位置字符串
        opacity: 元素图片的透明度 (0.0-1.0)
        scale_factor: 元素缩放比例 (0.1-2.0，1.0为原比例)
    """
    try:
        # 打开背景图片
        background = Image.open(background_path).convert('RGBA')
        
        # 打开元素图片
        element = Image.open(element_path).convert('RGBA')
        
        # 应用用户指定的缩放比例
        if scale_factor != 1.0:
            new_size = (int(element.size[0] * scale_factor), 
                       int(element.size[1] * scale_factor))
            element = element.resize(new_size, Image.Resampling.LANCZOS)
        
        # 如果元素图片比背景图片大，调整元素图片大小
        if element.size[0] > background.size[0] or element.size[1] > background.size[1]:
            # 计算缩放比例，保持宽高比
            fit_scale_factor = min(background.size[0] / element.size[0], 
                             background.size[1] / element.size[1])
            new_size = (int(element.size[0] * fit_scale_factor * 0.8),  # 稍微缩小一点
                       int(element.size[1] * fit_scale_factor * 0.8))
            element = element.resize(new_size, Image.Resampling.LANCZOS)
        
        # 处理预设位置
        if isinstance(position, str):
            if position == 'center':
                position = ((background.size[0] - element.size[0]) // 2,
                           (background.size[1] - element.size[1]) // 2)
            elif position == 'top-left':
                position = (0, 0)
            elif position == 'top-right':
                position = (background.size[0] - element.size[0], 0)
            elif position == 'bottom-left':
                position = (0, background.size[1] - element.size[1])
            elif position == 'bottom-right':
                position = (background.size[0] - element.size[0], 
                           background.size[1] - element.size[1])
            else:
                position = ((background.size[0] - element.size[0]) // 2,
                           (background.size[1] - element.size[1]) // 2)
        elif position == (0, 0):
            # 如果位置是(0, 0)，则居中放置元素
            position = ((background.size[0] - element.size[0]) // 2,
                       (background.size[1] - element.size[1]) // 2)
        
        # 调整元素透明度
        if opacity < 1.0:
            # 创建一个新的alpha通道
            alpha = element.split()[-1]
            alpha = alpha.point(lambda p: int(p * opacity))
            element.putalpha(alpha)
        
        # 创建一个新的透明背景，大小与背景图片相同
        overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
        
        # 将元素图片粘贴到透明背景上
        overlay.paste(element, position, element)
        
        # 将元素叠加到背景图片上
        result = Image.alpha_composite(background, overlay)
        
        # 转换回RGB模式并保存
        final_result = result.convert('RGB')
        final_result.save(output_path, 'JPEG', quality=95)
        
        print(f"✓ 成功生成: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ 处理失败 {background_path}: {str(e)}")
        return False

def main():
    # 设置默认路径
    base_dir = "/Users/ryla/work/coverText"
    background_dir = os.path.join(base_dir, "img-background")
    element_dir = os.path.join(base_dir, "img-element")
    output_dir = os.path.join(base_dir, "img-output")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='图片叠加工具')
    parser.add_argument('--background_dir', type=str, default=background_dir,
                       help='背景图片目录路径')
    parser.add_argument('--element_dir', type=str, default=element_dir,
                       help='元素图片目录路径')
    parser.add_argument('--output_dir', type=str, default=output_dir,
                       help='输出图片目录路径')
    parser.add_argument('--position', type=str, default='center',
                       help='元素位置 (center, top-left, top-right, bottom-left, bottom-right, 或 x,y 坐标)')
    parser.add_argument('--opacity', type=float, default=1.0,
                       help='元素透明度 (0.0-1.0)')
    parser.add_argument('--resize_factor', type=float, default=1.0,
                       help='元素缩放因子 (0.1-2.0)')
    
    args = parser.parse_args()
    
    # 验证输入目录是否存在
    if not os.path.exists(args.background_dir):
        print(f"错误: 背景图片目录不存在: {args.background_dir}")
        sys.exit(1)
    
    if not os.path.exists(args.element_dir):
        print(f"错误: 元素图片目录不存在: {args.element_dir}")
        sys.exit(1)
    
    # 获取所有背景图片
    background_files = []
    for file in os.listdir(args.background_dir):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            background_files.append(file)
    
    if not background_files:
        print(f"警告: 在 {args.background_dir} 中没有找到图片文件")
        sys.exit(1)
    
    # 获取所有元素图片
    element_files = []
    for file in os.listdir(args.element_dir):
        if file.lower().endswith('.png'):
            element_files.append(file)
    
    if not element_files:
        print(f"警告: 在 {args.element_dir} 中没有找到PNG元素文件")
        sys.exit(1)
    
    print(f"找到 {len(background_files)} 张背景图片")
    print(f"找到 {len(element_files)} 个PNG元素")
    print(f"输出目录: {args.output_dir}")
    print("-" * 50)
    
    # 解析位置参数
    position_map = {
        'center': (0, 0),
        'top-left': None,
        'top-right': None,
        'bottom-left': None,
        'bottom-right': None
    }
    
    # 处理每个背景图片
    success_count = 0
    total_count = 0
    
    for bg_file in background_files:
        for element_file in element_files:
            total_count += 1
            
            bg_path = os.path.join(args.background_dir, bg_file)
            element_path = os.path.join(args.element_dir, element_file)
            
            # 生成输出文件名
            bg_name = os.path.splitext(bg_file)[0]
            element_name = os.path.splitext(element_file)[0]
            output_filename = f"{bg_name}_with_{element_name}.jpg"
            output_path = os.path.join(args.output_dir, output_filename)
            
            # 确定位置
            if args.position in position_map:
                if args.position == 'center':
                    position = (0, 0)
                else:
                    # 直接传递位置字符串给overlay_images函数处理
                    position = args.position
            elif ',' in args.position:
                # 自定义坐标
                try:
                    x, y = map(int, args.position.split(','))
                    position = (x, y)
                except ValueError:
                    print(f"警告: 无效的位置格式 '{args.position}'，使用居中")
                    position = (0, 0)
            else:
                print(f"警告: 未知的位置 '{args.position}'，使用居中")
                position = (0, 0)
            
            # 执行叠加
            if overlay_images(bg_path, element_path, output_path, position, args.opacity, args.resize_factor):
                success_count += 1
    
    print("-" * 50)
    print(f"处理完成! 成功生成 {success_count}/{total_count} 张图片")

if __name__ == "__main__":
    main()