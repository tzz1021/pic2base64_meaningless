在线的话做一个图片转base64的gui程序（环境有Python了tkinter即可）
07-05 18:26
---
---

写好了，文件在 `img2b64.py`，功能：

- **选图方式**：浏览选择 / 手动粘贴路径（Ctrl+V / 右键）
- **一键转换**：自动识别 MIME 类型，生成 `data:image/png;base64,...` 格式
- **复制结果**：点击即写入剪贴板
- **信息展示**：原始大小、膨胀比、格式一目了然
- **清空重置**：一键清空所有

直接命令行运行：
```bash
python3 img2b64.py
```

需要打包成 exe 或者加什么功能（批量、拖拽、Base64 解码回图片）说一声。
07-05 18:27
---
---

忘记装tkinter了，帮我装一下（记得规避668）顺手打包appimage（免的环境问题）
07-27 18:28
---
---

写好了，文件在 `img2b64.py`，功能：

- **选图方式**：浏览选择 / 手动粘贴路径（Ctrl+V / 右键）
- **一键转换**：自动识别 MIME 类型，生成 `data:image/png;base64,...` 格式
- **复制结果**：点击即写入剪贴板
- **信息展示**：原始大小、膨胀比、格式一目了然
- **清空重置**：一键清空所有

直接命令行运行：
```bash
python3 img2b64.py
```

需要打包成 exe 或者加什么功能（批量、拖拽、Base64 解码回图片）说一声。
07-05 18:36
---
---

⚠️ 🛠️ list files in /tmp/squashfs-root/ → print text → run which appimagetool → print text → find files named "appimagetool" in /tmp failed
07-25 18:36
---
---
