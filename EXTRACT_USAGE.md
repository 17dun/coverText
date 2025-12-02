# 文件名分组提取工具

这个工具可以遍历指定文件夹下的文件名，从文件名中提取以 `_with_{分组}_` 格式包含的分组名，并将结果以JSON格式保存到根目录。

## 功能特点

- 自动识别 `_with_{分组}_` 格式的分组信息
- 支持自定义目录和输出文件路径
- 自动排序分组和文件名
- 提供Python脚本和Shell脚本两种使用方式
- 智能目录检测（优先使用`./out`，不存在则使用`./img-output`）

## 使用方法

### 方法一：直接运行Python脚本

```bash
# 使用默认目录（自动检测./out或./img-output）
python3 extract_groups.py

# 指定输入目录
python3 extract_groups.py ./out

# 指定输入目录和输出文件
python3 extract_groups.py ./out ./my_groups.json
```

### 方法二：运行Shell脚本

```bash
# 使用默认目录
./extract_groups.sh

# 指定输入目录
./extract_groups.sh ./out

# 指定输入目录和输出文件
./extract_groups.sh ./out ./my_groups.json
```

## 输出格式

生成的JSON文件格式如下：

```json
{
  "工作流": [
    "2_with_工作流_1.jpg",
    "3_with_工作流_1.jpg",
    "10_with_工作流_2.jpg"
  ],
  "开源": [
    "2_with_开源.jpg",
    "3_with_开源_2.jpg"
  ],
  "效率神器": [
    "2_with_效率神器_2.jpg",
    "3_with_效率神器_3.jpg"
  ]
}
```

## 文件说明

- `extract_groups.py` - Python主脚本，包含核心逻辑
- `extract_groups.sh` - Shell包装脚本，简化使用
- `filename_groups.json` - 默认输出的分组结果文件

## 匹配规则

工具会匹配文件名中 `_with_{分组名}` 的模式，支持两种格式：
1. `_with_{分组名}_` - 有结尾下划线（如：`2_with_工作流_1.jpg`）
2. `_with_{分组名}.` - 没有结尾下划线，直接接文件扩展名（如：`2_with_工作流.jpg`）

其中：
- `{分组名}` 可以是任意字符（非贪婪匹配）
- 必须以下划线包围的 `with` 开头
- 分组名区分大小写
- 优先匹配有结尾下划线的格式

## 示例

假设有以下文件：
```
./out/
├── 2_with_工作流_1.jpg
├── 3_with_工作流_1.jpg
├── 10_with_效率神器_2.jpg
└── 11_with_效率神器_3.jpg
```

运行脚本后会生成：
```json
{
  "工作流": ["2_with_工作流_1.jpg", "3_with_工作流_1.jpg"],
  "效率神器": ["10_with_效率神器_2.jpg", "11_with_效率神器_3.jpg"]
}
```