# 图片叠加工具使用说明

## 功能介绍
这个工具可以遍历 `img-background` 目录中的所有图片，并在每个图片上叠加 `img-element` 目录中的PNG元素，输出到 `img-output` 目录。

## 文件结构
```
/Users/ryla/work/coverText/
├── img-background/          # 背景图片目录
├── img-element/           # PNG元素目录
├── img-output/           # 输出目录（自动生成）
├── overlay_images.py     # Python核心脚本
├── run_overlay.sh        # Shell调用脚本
└── OVERLAY_USAGE.md      # 本说明文档
```

## 使用方法

### 基本使用
```bash
./run_overlay.sh
```
这将使用默认设置处理所有图片。

### 高级选项
```bash
./run_overlay.sh --opacity 0.5 --position top-right
```

### 可用参数

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `--resize_factor` | 元素缩放比例 | 1.0 | 0.1-2.0（1.0为原比例） |
| `--opacity` | 元素透明度 | 1.0 | 0.0-1.0 |
| `--position` | 元素位置 | center | center, top-left, top-right, bottom-left, bottom-right, 或 x,y 坐标 |

#### 位置选项说明
- **center**: 居中放置
- **top-left**: 左上角
- **top-right**: 右上角  
- **bottom-left**: 左下角
- **bottom-right**: 右下角
- **x,y**: 自定义坐标，如 `100,200` 表示距离左边100像素，距离顶部200像素
| `--background_dir` | 背景图片目录 | img-background | 任意路径 |
| `--element_dir` | 元素图片目录 | img-element | 任意路径 |
| `--output_dir` | 输出目录 | img-output | 任意路径 |

### 位置选项说明
- `center`: 居中放置
- `top-left`: 左上角
- `top-right`: 右上角
- `bottom-left`: 左下角
- `bottom-right`: 右下角
- `x,y`: 自定义坐标，例如 `100,50`

### 透明度设置
透明度值范围从 0.0（完全透明）到 1.0（完全不透明）。

### 示例命令

1. **基本使用（默认参数）**
```bash
./run_overlay.sh
```

2. **设置元素缩放比例为0.5倍（缩小一半）**
```bash
./run_overlay.sh --resize_factor 0.5
```

3. **设置元素缩放比例为2倍（放大两倍）**
```bash
./run_overlay.sh --resize_factor 2.0
```

4. **半透明居中叠加**
```bash
./run_overlay.sh --opacity 0.5
```

5. **各角落位置示例**
```bash
./run_overlay.sh --position top-left --resize_factor 0.3
./run_overlay.sh --position top-right --resize_factor 0.4
./run_overlay.sh --position bottom-left --resize_factor 0.6
./run_overlay.sh --position bottom-right --resize_factor 0.5
```

6. **自定义坐标位置**
```bash
./run_overlay.sh --position 100,200 --resize_factor 0.8
```

7. **组合使用多个参数（缩放、透明度、位置）**
```bash
./run_overlay.sh --resize_factor 0.7 --opacity 0.8 --position bottom-right
```

8. **使用自定义目录**
```bash
./run_overlay.sh --background_dir /path/to/backgrounds --element_dir /path/to/elements --output_dir /path/to/output
```

## 输出文件命名规则
输出文件采用以下命名格式：
```
{背景图片名}_with_{元素图片名}.jpg
```
例如：`1_with_AI_ai技术.jpg`

## 注意事项

1. 只支持PNG格式的元素图片（支持透明度）
2. 背景图片支持多种格式：JPG、PNG、BMP、GIF
3. 如果元素图片比背景图片大，会自动缩放以适应背景
4. 输出图片格式为JPEG，质量设置为95%
5. 如果元素图片有透明通道，会正确保留透明度效果
6. 缩放比例范围：0.1-2.0，1.0为原比例，0.5为一半大小，2.0为两倍大小

## 故障排除

### 错误：找不到PIL模块
  - 确保已安装Pillow：`pip3 install Pillow`
  
### 错误：找不到图片文件
  - 检查图片是否存在于指定目录
  - 确认文件扩展名是否正确（.jpg, .png, .jpeg）
  
### 输出图片质量不佳
  - 检查原始图片的分辨率和质量
  - 确保元素图片有足够的分辨率
  
### 程序运行缓慢
  - 图片数量较多时处理时间会较长
  - 建议先在小批量图片上测试

### 缩放比例无效
  - 确保缩放比例在0.1-2.0范围内
  - 检查是否正确使用了`--resize_factor`参数

### 位置参数无效
  - 确保使用正确的位置名称：top-left, top-right, bottom-left, bottom-right, center
  - 自定义坐标格式：x,y（如 100,200）
  - 检查是否有拼写错误