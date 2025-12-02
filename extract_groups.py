#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名分组提取脚本
遍历./out文件夹下的文件名，提取"_with_{分组}_"中的分组名，
生成分组JSON文件保存到根目录
"""

import os
import json
import re
from collections import defaultdict

def extract_groups_from_filenames(directory_path="./out"):
    """
    从文件名中提取分组信息
    
    Args:
        directory_path: 要遍历的目录路径
    
    Returns:
        dict: 分组字典，格式如{"工作流": ['2_with_工作流_1.jpg', '3_with_工作流_1.jpg']}
    """
    if not os.path.exists(directory_path):
        print(f"错误: 目录 {directory_path} 不存在")
        return {}
    
    # 用于存储分组结果
    groups = defaultdict(list)
    
    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        # 只处理文件，跳过子目录
        file_path = os.path.join(directory_path, filename)
        if not os.path.isfile(file_path):
            continue
            
        # 使用正则表达式提取分组名
        # 匹配模式1: _with_{分组名}_ (有结尾下划线)
        # 匹配模式2: _with_{分组名}. (没有结尾下划线，直接接文件扩展名)
        pattern1 = r'_with_(.+?)_'
        pattern2 = r'_with_(.+?)\.'
        
        match = re.search(pattern1, filename)  # 优先匹配有下划线的
        if not match:
            match = re.search(pattern2, filename)  # 如果没有，匹配没有下划线的
        
        if match:
            group_name = match.group(1)
            groups[group_name].append(filename)
            print(f"找到文件: {filename} -> 分组: {group_name}")
        else:
            print(f"跳过文件: {filename} (未匹配到分组模式)")
    
    # 转换为普通字典并排序
    result = {}
    for group_name in sorted(groups.keys()):
        result[group_name] = sorted(groups[group_name])
    
    return result

def save_to_json(data, output_path="./filename_groups.json"):
    """
    将分组数据保存为JSON文件
    
    Args:
        data: 分组字典
        output_path: 输出JSON文件路径
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n分组信息已保存到: {output_path}")
        return True
    except Exception as e:
        print(f"保存JSON文件失败: {str(e)}")
        return False

def main():
    """主函数"""
    import sys
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        # 检查是否存在out目录，如果不存在则使用img-output
        if os.path.exists("./out"):
            target_directory = "./out"
        elif os.path.exists("./img-output"):
            target_directory = "./img-output"
            print("注意: 使用img-output目录作为数据源")
        else:
            print("错误: 未找到out或img-output目录")
            return
    
    if len(sys.argv) > 2:
        output_json = sys.argv[2]
    else:
        output_json = "./filename_groups.json"
    
    print("=" * 50)
    print("文件名分组提取工具")
    print("=" * 50)
    
    print(f"目标目录: {target_directory}")
    print(f"输出文件: {output_json}")
    print("-" * 50)
    
    # 提取分组信息
    groups = extract_groups_from_filenames(target_directory)
    
    if not groups:
        print("未找到任何分组信息")
        return
    
    # 显示分组结果
    print(f"\n共找到 {len(groups)} 个分组:")
    for group_name, filenames in groups.items():
        print(f"\n分组 '{group_name}':")
        for filename in filenames:
            print(f"  - {filename}")
    
    # 保存为JSON文件
    if save_to_json(groups, output_json):
        print(f"\n✓ 成功生成JSON文件: {output_json}")
        
        # 显示JSON文件内容预览
        print("\nJSON文件内容预览:")
        with open(output_json, 'r', encoding='utf-8') as f:
            content = f.read()
            # 显示前500个字符
            preview = content[:500] + "..." if len(content) > 500 else content
            print(preview)
    else:
        print(f"\n✗ 生成JSON文件失败")

if __name__ == "__main__":
    main()