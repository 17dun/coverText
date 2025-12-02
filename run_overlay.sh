#!/bin/bash

# 图片叠加脚本
# 遍历img-background目录中的所有图片，并在每个图片上叠加img-element目录中的PNG元素

# 设置基础目录
BASE_DIR="/Users/ryla/work/coverText"
BACKGROUND_DIR="$BASE_DIR/img-background"
ELEMENT_DIR="$BASE_DIR/img-element"
OUTPUT_DIR="$BASE_DIR/img-output"

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "图片叠加工具"
echo "=========================================="
echo "背景图片目录: $BACKGROUND_DIR"
echo "元素图片目录: $ELEMENT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "=========================================="

# 检查必要的目录是否存在
if [ ! -d "$BACKGROUND_DIR" ]; then
    echo "错误: 背景图片目录不存在: $BACKGROUND_DIR"
    exit 1
fi

if [ ! -d "$ELEMENT_DIR" ]; then
    echo "错误: 元素图片目录不存在: $ELEMENT_DIR"
    exit 1
fi

# 运行Python脚本
/usr/bin/python3 "$BASE_DIR/overlay_images.py" \
    --background_dir "$BACKGROUND_DIR" \
    --element_dir "$ELEMENT_DIR" \
    --output_dir "$OUTPUT_DIR" \
    "$@"

echo "=========================================="
echo "处理完成！"
echo "输出文件保存在: $OUTPUT_DIR"
echo "=========================================="