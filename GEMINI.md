# GEMINI.md

## Project Overview

This project is a command-line tool designed to generate cover images. It takes three lines of text as input and overlays them onto a background image (`bg.jpg`) to create a final cover image (`output_cover.jpg`).

The core logic is handled by a Python script (located outside this directory), which is orchestrated by a shell script (`run_cover.sh`). The visual styling of the text (fonts, colors, layout) is defined in a CSS file (`guangshu_style.css`) and can be previewed using `debug_page.html`.

## Key Files

*   `run_cover.sh`: The main executable script. It takes the text content and passes all required parameters to the Python image generation script.
*   `guangshu_style.css`: Defines the visual appearance of the text on the cover. This is the primary file to modify for stylistic changes.
*   `debug_page.html`: A simple HTML file for previewing the styles defined in `guangshu_style.css` in a web browser.
*   `antuozongyi.ttf`: A font file used for styling the text.
*   `bg.jpg`: The background image for the cover. (Git-ignored)
*   `output_cover.jpg`: The generated final cover image. (Git-ignored)
*   `hisDoc/`: A directory for storing historical or generated files. (Git-ignored)

## Running the Tool

To generate a cover image, execute the `run_cover.sh` script from your terminal, providing the three lines of text as a JSON array string.

**Usage:**

```bash
./run_cover.sh '["第一行文字", "第二行文字", "第三行文字"]'
```

**Example:**

```bash
./run_cover.sh '["一人公司神器", "Weclone", "喂给它聊天记录,克隆一个数字版的你自己"]'
```

The script will then generate the `output_cover.jpg` file in the `/Users/ryla/obsidian/GS/2.领域/1.广叔IP运营/` directory.
