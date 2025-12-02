#!/bin/bash
# 文件名分组提取脚本
# 遍历指定目录下的文件名，提取_with_{分组}_中的分组名，生成JSON文件

# 设置默认参数
# 优先使用./out目录，如果不存在则使用./img-output
if [ -d "./out" ]; then
    DEFAULT_DIR="./out"
elif [ -d "./img-output" ]; then
    DEFAULT_DIR="./img-output"
else
    DEFAULT_DIR="./img-output"
fi

TARGET_DIR="${1:-$DEFAULT_DIR}"
OUTPUT_FILE="${2:-./filename_groups.json}"

echo "=========================================="
echo "文件名分组提取工具"
echo "=========================================="
echo "目标目录: $TARGET_DIR"
echo "输出文件: $OUTPUT_FILE"
echo "------------------------------------------"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "错误: 目录 $TARGET_DIR 不存在"
    exit 1
fi

# 运行Python脚本
python3 extract_groups.py "$TARGET_DIR" "$OUTPUT_FILE"

echo "=========================================="
echo "处理完成！"
echo "分组信息已保存到: $OUTPUT_FILE"
echo "=========================================="