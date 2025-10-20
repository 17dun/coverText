#!/bin/bash

# 这是一个封装了所有固定参数的shell脚本，只接收一个参数：texts的JSON字符串

# 检查是否提供了texts参数
if [ -z "$1" ]; then
  echo "错误: 请提供一个包含三行文本的JSON字符串作为第一个参数。"
  echo "用法示例: ./run_cover.sh '["第一行", "第二行", "第三行"]'"
  exit 1
fi

# --- 固定参数配置 ---
# 请注意：为了让脚本在任何位置都能正确运行，这里使用了绝对路径
BASE_DIR="/Users/ryla/obsidian/GS/2.领域/1.广叔IP运营"

IMAGE_PATH="$BASE_DIR/bg.jpg"
OUTPUT_PATH="$BASE_DIR/output_cover.jpg"
STYLE_CSS="$BASE_DIR/guangshu_style.css"
FONT_ZONGYI="/Users/ryla/Desktop/antuozongyi.ttf"
FONT_ENGLISH="/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SCRIPT_PATH="$BASE_DIR/stable_script.py"

# 将第一个命令行参数赋值给TEXTS_JSON变量
TEXTS_JSON="$1"

# --- 执行Python脚本 ---
echo "正在使用以下文字生成封面:"
echo "$TEXTS_JSON"

python "$SCRIPT_PATH" \
  --image_path "$IMAGE_PATH" \
  --output_path "$OUTPUT_PATH" \
  --style_css "$STYLE_CSS" \
  --font_zongyi "$FONT_ZONGYI" \
  --font_english "$FONT_ENGLISH" \
  --texts "$TEXTS_JSON"

# 检查python脚本是否成功执行
if [ $? -eq 0 ]; then
  echo "封面生成成功: $OUTPUT_PATH"
else
  echo "封面生成失败，请检查错误信息。"
fi
