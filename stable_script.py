import argparse
import json
import re
from PIL import Image, ImageDraw, ImageFont
import textwrap

# =============================================================================
# 1. CSS 解析模块
# =============================================================================
def parse_css(css_path):
    """
    一个简易的CSS解析器，用于从 guangshu_style.css 文件中提取特定样式。
    它会查找 .text-block p, .line1, .line2, .line3 的规则。
    """
    styles = {
        'base': {},
        'line1': {},
        'line2': {},
        'line3': {}
    }
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            # 先用正则去掉所有CSS注释，这是修复bug的关键
            content = re.sub(r'/\*.*?\*/', '', f.read())
    except FileNotFoundError:
        print(f"错误：CSS文件未找到 at {css_path}")
        return None

    # 匹配规则块
    rule_pattern = re.compile(r'([^{]+)\{([^}]+)\}')
    rules = rule_pattern.findall(content)

    selector_map = {
        '.text-block p': 'base',
        '.text-block p.line1': 'line1',
        '.text-block p.line2': 'line2',
        '.text-block p.line3': 'line3'
    }

    for selector, properties_str in rules:
        selector = selector.strip()
        if selector in selector_map:
            key = selector_map[selector]
            properties = properties_str.strip().split(';')
            for prop in properties:
                if ':' in prop:
                    prop_name, prop_value = prop.split(':', 1)
                    prop_name = prop_name.strip()
                    prop_value = prop_value.strip()
                    if prop_name and prop_value:
                        styles[key][prop_name] = prop_value
    return styles

def get_line_style(styles, line_num):
    """合并基础样式和特定行的样式"""
    line_key = f'line{line_num}'
    # 先复制基础样式，然后用特定行的样式覆盖
    final_style = styles['base'].copy()
    final_style.update(styles.get(line_key, {}))
    return final_style

# =============================================================================
# 2. 渲染辅助函数
# =============================================================================
def parse_px(value):
    """从 '80px' 中提取数字 80"""
    if isinstance(value, str) and 'px' in value:
        return int(re.sub(r'px', '', value).strip())
    return int(value)

def parse_shadow(shadow_str):
    """从 ' -2px -2px 0 #000, ...' 中解析描边"""
    if not shadow_str or shadow_str == 'none':
        return []
    shadows = []
    # 正则表达式匹配每个shadow: x-offset y-offset blur-radius color
    shadow_pattern = re.compile(r'(-?\d+)px\s+(-?\d+)px\s+\d+\s+([^,]+)')
    for match in shadow_pattern.finditer(shadow_str):
        shadows.append({
            'x': int(match.group(1)),
            'y': int(match.group(2)),
            'color': match.group(3).strip()
        })
    return shadows

# =============================================================================
# 3. 主渲染函数
# =============================================================================
def create_cover(image_path, output_path, texts, style_css, font_paths):
    """
    主函数，用于创建封面
    """
    # --- 解析CSS ---
    styles = parse_css(style_css)
    if not styles:
        return

    # --- 加载图片和字体 ---
    try:
        image = Image.open(image_path).convert("RGBA")
    except FileNotFoundError:
        print(f"错误：输入图片未找到 at {image_path}")
        return
        
    draw = ImageDraw.Draw(image)
    img_width, img_height = image.size

    # --- 动态缩放逻辑 ---
    reference_width = 720.0
    scale_factor = img_width / reference_width
    print(f"--- INFO: Image width is {img_width}px. Scaling all pixel values by factor of {scale_factor:.2f} ---")
    
    # --- 逐行渲染文字 ---
    current_y = img_height / 2 - (150 * scale_factor)

    for i, text in enumerate(texts):
        line_num = i + 1
        style = get_line_style(styles, line_num)

        # --- 获取并缩放样式属性 ---
        font_size = int(parse_px(style.get('font-size', 80)) * scale_factor)
        font_color = style.get('color', 'white')
        line_height_multiplier = float(style.get('line-height', 1.3))
        
        font_family = style.get('font-family', '')
        if '综艺体' in font_family and font_paths.get('zongyi'):
            font_path = font_paths['zongyi']
        elif 'MyCoolEnglishFont' in font_family and font_paths.get('english'):
            font_path = font_paths['english']
        else:
            font_path = font_paths['main']

        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"错误：字体文件未找到 at {font_path}。请检查路径。")
            font = ImageFont.load_default()

        if style.get('font-style') == 'italic' and font_paths.get('italic'):
             try:
                font = ImageFont.truetype(font_paths['italic'], font_size)
             except IOError:
                print(f"警告：斜体字体 at {font_paths['italic']} 未找到。")

        # --- 处理换行 (新版，更精确) ---
        text_width_percent = style.get('width')
        wrapped_text = text
        if text_width_percent and '%' in text_width_percent:
            percent = int(text_width_percent.replace('%','').strip())
            max_width_pixels = img_width * (percent / 100.0)
            
            lines = []
            current_line = ""
            for char in text:
                if draw.textbbox((0,0), current_line + char, font=font)[2] <= max_width_pixels:
                    current_line += char
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = char
            if current_line:
                lines.append(current_line)
            wrapped_text = "\n".join(lines)

        # --- 精确计算位置和尺寸 ---
        bbox = draw.textbbox((0, 0), wrapped_text, font=font, align="center")
        text_left, text_top, text_right, text_bottom = bbox
        text_width = text_right - text_left
        text_height = text_bottom - text_top
        
        x_start = (img_width - text_width) / 2
        
        margin_top = int(parse_px(style.get('margin-top', 0)) * scale_factor)
        margin_str = style.get('margin', '0 auto')
        if margin_str != '0 auto':
             margin_parts = margin_str.split()
             if len(margin_parts) > 0:
                 margin_top += int(parse_px(margin_parts[0]) * scale_factor)

        if i == 0:
            current_y += margin_top
        else:
            prev_style = get_line_style(styles, i)
            prev_font_size = int(parse_px(prev_style.get('font-size', 80)) * scale_factor)
            current_y += prev_font_size * line_height_multiplier + margin_top

        y_start = current_y

        # --- 渲染背景块 (针对line3) ---
        bg_color = style.get('background-color')
        if bg_color:
            padding = int(20 * scale_factor)
            bg_box = [x_start - padding, y_start - padding, x_start + text_width + padding, y_start + text_height + padding]
            draw.rectangle(bg_box, fill=bg_color)

        # --- 渲染描边/阴影 ---
        draw_x = x_start - text_left
        draw_y = y_start - text_top

        shadows = parse_shadow(style.get('text-shadow'))
        for shadow in shadows:
            shadow_x = int(shadow['x'] * scale_factor)
            shadow_y = int(shadow['y'] * scale_factor)
            draw.text((draw_x + shadow_x, draw_y + shadow_y), wrapped_text, font=font, fill=shadow['color'], align="center")

        # --- 渲染主文字 ---
        draw.text((draw_x, draw_y), wrapped_text, font=font, fill=font_color, align="center")

    # --- 保存图片 ---
    try:
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            image = image.convert("RGB")
        image.save(output_path)
        print(f"封面已成功生成并保存到: {output_path}")
    except Exception as e:
        print(f"错误：保存图片失败。{e}")


# =============================================================================
# 4. 命令行接口
# =============================================================================
# =============================================================================
# 4. 新增：系统字体查找模块
# =============================================================================
def find_system_font():
    """
    在macOS系统中查找可用的中文字体
    """
    import os
    font_preferences = [
        'PingFang.ttc',          # 平方
        'STHeiti Medium.ttc',    # 黑体-中
        'SimHei.ttf',            # 黑体
        'Hiragino Sans GB.ttc'   # 冬青黑体
    ]
    font_dirs = [
        '/System/Library/Fonts',
        '/System/Library/Fonts/Supplemental',
        '/Library/Fonts'
    ]

    for font_dir in font_dirs:
        for font_name in font_preferences:
            path = os.path.join(font_dir, font_name)
            if os.path.exists(path):
                return path
    return None

# =============================================================================
# 5. 命令行接口
# =============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='为图片添加风格化的文字封面')
    parser.add_argument('--image_path', required=True, help='输入图片的路径')
    parser.add_argument('--output_path', required=True, help='输出图片的路径')
    parser.add_argument('--texts', required=True, help="""包含三行文字的JSON字符串, e.g., '["line 1", "line 2", "line 3"]'""")
    parser.add_argument('--style_css', required=True, help='guangshu_style.css 文件的路径')
    parser.add_argument('--font_main', default=None, help='主字体路径。如果留空，脚本会尝试自动查找系统字体')
    parser.add_argument('--font_zongyi', default=None, help='综艺体字体的路径。如果留空，将使用主字体')
    parser.add_argument('--font_english', default=None, help='(可选) 英文专用字体的路径')
    parser.add_argument('--font_italic', default='', help='(可选) 斜体字体的路径')

    args = parser.parse_args()

    try:
        texts_list = json.loads(args.texts)
    except json.JSONDecodeError:
        print("错误: --texts 参数必须是有效的JSON格式字符串。")
        exit(1)

    # --- 自动查找或验证字体路径 ---
    main_font_path = args.font_main
    if not main_font_path:
        print("--- INFO: 未指定主字体, 尝试自动在系统中查找... ---")
        main_font_path = find_system_font()
        if main_font_path:
            print(f"--- INFO: 找到可用字体: {main_font_path} ---")
        else:
            print("错误: 自动查找字体失败。请使用 --font_main 手动指定一个中文字体路径。")
            exit(1)
    
    zongyi_font_path = args.font_zongyi if args.font_zongyi else main_font_path
    english_font_path = args.font_english if args.font_english else main_font_path

    font_paths = {
        'main': main_font_path,
        'zongyi': zongyi_font_path,
        'english': english_font_path,
        'italic': args.font_italic
    }
    
    create_cover(
        args.image_path,
        args.output_path,
        texts_list,
        args.style_css,
        font_paths
    )