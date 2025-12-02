# Cover Image Generator

This project is a command-line tool to generate cover images by overlaying text onto a background image.

The core logic is handled by a Python script (located outside this directory), which is orchestrated by the `run_cover.sh` shell script. The visual styling of the text (fonts, colors, layout) is defined in `guangshu_style.css`.

## Usage

To generate a cover image, execute the `run_cover.sh` script from your terminal. You need to provide three lines of text as a single JSON array string argument.

**Command:**
```bash
./run_cover.sh '["Line 1 Text", "Line 2 Text", "Line 3 Text"]'
```

**Example:**
```bash
./run_cover.sh '["Solo Company Tool", "Weclone", "Feed it chat logs to clone a digital version of yourself"]'
```
The script will generate an `output_cover.jpg` file in the `/Users/ryla/obsidian/GS/2.领域/1.广叔IP运营/` directory.

## File Descriptions

*   `run_cover.sh`: The main executable script that orchestrates the image generation.
*   `guangshu_style.css`: The CSS file that defines the visual appearance of the text. Modify this file to change text styles.
*   `debug_page.html`: A simple HTML file for previewing the text styles in a web browser.
*   `antuozongyi.ttf`: A font file used for styling the text.
*   `bg.jpg`: (Git-ignored) The background image for the cover.
*   `output_cover.jpg`: (Git-ignored) The generated final cover image.
*   `hisDoc/`: (Git-ignored) A directory for storing historical or generated files.

---

# 封面图片生成器

本项目是一个命令行工具，用于将文本叠加到背景图片上以生成封面图片。

核心逻辑由一个位于此目录之外的Python脚本处理，该脚本由 `run_cover.sh` shell脚本进行调用。文本的视觉样式（字体、颜色、布局）在 `guangshu_style.css` 文件中定义。

## 使用方法

要生成封面图片，请从终端执行 `run_cover.sh` 脚本。你需要提供一个包含三行文本的JSON数组字符串作为参数。

**命令:**
```bash
./run_cover.sh '["第一行文字", "第二行文字", "第三行文字"]'
```

**示例:**
```bash
./run_cover.sh '["一人公司神器", "Weclone", "喂给它聊天记录,克隆一个数字版的你自己"]'
```
脚本将在 `/Users/ryla/obsidian/GS/2.领域/1.广叔IP运营/` 目录下生成一个名为 `output_cover.jpg` 的文件。

## 文件说明

*   `run_cover.sh`: 用于调用图像生成功能的主要可执行脚本。
*   `guangshu_style.css`: 定义文本视觉样式的CSS文件。修改此文件可以更改文本样式。
*   `debug_page.html`: 一个简单的HTML文件，用于在Web浏览器中预览文本样式。
*   `antuozongyi.ttf`: 用于设置文本样式的字体文件。
*   `bg.jpg`: (Git忽略) 封面的背景图片。
*   `output_cover.jpg`: (Git忽略) 生成的最终封面图片。
*   `hisDoc/`: (Git忽略) 用于存放历史或生成文件的目录。
