#!/usr/bin/env python3
"""图片转 Base64 小工具 — 拖拽/选择文件，一键复制"""

import tkinter as tk
from tkinter import ttk, filedialog
import base64
import os

class Img2B64App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("图片转 Base64 🔧")
        self.root.geometry("720x520")
        self.root.resizable(True, True)
        self.root.minsize(480, 360)

        # 文件路径
        self.file_path = tk.StringVar()
        self.b64_result = tk.StringVar()
        self.file_size = tk.StringVar()
        self.img_ext = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # ---------- 顶部：文件选择 ----------
        frame_top = ttk.Frame(self.root, padding=(12, 8))
        frame_top.pack(fill=tk.X)

        ttk.Label(frame_top, text="图片文件：").pack(side=tk.LEFT)
        self.entry_path = ttk.Entry(frame_top, textvariable=self.file_path, width=50)
        self.entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
        ttk.Button(frame_top, text="浏览...", command=self._select_file).pack(side=tk.LEFT)
        ttk.Button(frame_top, text="清空", command=self._clear).pack(side=tk.LEFT, padx=(4, 0))

        # ---------- 信息行 ----------
        frame_info = ttk.Frame(self.root, padding=(12, 0))
        frame_info.pack(fill=tk.X)

        self.lbl_size = ttk.Label(frame_info, textvariable=self.file_size, foreground="gray")
        self.lbl_size.pack(side=tk.LEFT, padx=(0, 12))
        self.lbl_ext = ttk.Label(frame_info, textvariable=self.img_ext, foreground="gray")
        self.lbl_ext.pack(side=tk.LEFT)

        # ---------- 转换按钮 ----------
        frame_btn = ttk.Frame(self.root, padding=(12, 6))
        frame_btn.pack(fill=tk.X)

        self.btn_convert = ttk.Button(frame_btn, text="🔄 转换", command=self._convert)
        self.btn_convert.pack(side=tk.LEFT, padx=(0, 6))
        self.btn_copy = ttk.Button(frame_btn, text="📋 复制结果", command=self._copy_result, state=tk.DISABLED)
        self.btn_copy.pack(side=tk.LEFT)

        # ---------- 结果输出 ----------
        frame_result = ttk.Frame(self.root, padding=(12, 0))
        frame_result.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_result, text="Base64 结果：").pack(anchor=tk.W)

        txt_frame = ttk.Frame(frame_result)
        txt_frame.pack(fill=tk.BOTH, expand=True)

        self.txt_result = tk.Text(txt_frame, wrap=tk.WORD, font=("Consolas", 10), height=14)
        scroll_y = ttk.Scrollbar(txt_frame, orient=tk.VERTICAL, command=self.txt_result.yview)
        scroll_x = ttk.Scrollbar(txt_frame, orient=tk.HORIZONTAL, command=self.txt_result.xview)
        self.txt_result.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.txt_result.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # ---------- 状态栏 ----------
        self.status = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W, padding=(8, 2))
        self.status.pack(fill=tk.X, side=tk.BOTTOM)

        # ---------- 拖拽支持 ----------
        self._setup_drag_drop()

    def _setup_drag_drop(self):
        """绑定拖拽事件 (Linux / Windows 部分支持)"""
        self.root.drop_target_register = getattr(self.root, "drop_target_register", None)
        if self.root.drop_target_register:
            try:
                self.root.drop_target_register("*")
                self.root.dnd_bind("<<Drop>>", self._on_drop)
            except Exception:
                pass
        # 右键粘贴文件路径
        self.entry_path.bind("<Button-3>", lambda e: self._paste_path())
        self.entry_path.bind("<Control-v>", lambda e: self._paste_path())

    def _paste_path(self):
        try:
            self.entry_path.insert(0, self.root.clipboard_get())
            self._auto_update_info()
        except Exception:
            pass

    def _on_drop(self, event):
        path = event.data.strip().strip("{}") if event.data else ""
        if path and os.path.isfile(path):
            self.file_path.set(path)
            self._auto_update_info()

    def _auto_update_info(self):
        path = self.file_path.get().strip()
        if path and os.path.isfile(path):
            self._update_info(path)
            self.btn_convert.config(state=tk.NORMAL)
        else:
            self.file_size.set("")
            self.img_ext.set("")
            self.btn_convert.config(state=tk.DISABLED)

    def _select_file(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp *.ico *.tiff *.tif *.svg"),
                ("所有文件", "*.*"),
            ],
        )
        if path:
            self.file_path.set(path)
            self._update_info(path)

    def _update_info(self, path):
        size = os.path.getsize(path)
        self.file_size.set(f"大小: {self._fmt_size(size)}")
        _, ext = os.path.splitext(path)
        self.img_ext.set(f"格式: {ext.upper()}")
        self.btn_convert.config(state=tk.NORMAL)

    def _clear(self):
        self.file_path.set("")
        self.file_size.set("")
        self.img_ext.set("")
        self.b64_result.set("")
        self.txt_result.delete("1.0", tk.END)
        self.btn_convert.config(state=tk.DISABLED)
        self.btn_copy.config(state=tk.DISABLED)
        self.status.config(text="已清空")

    def _convert(self):
        path = self.file_path.get().strip()
        if not path or not os.path.isfile(path):
            self.status.config(text="❌ 文件不存在")
            return

        try:
            with open(path, "rb") as f:
                raw = f.read()

            ext = os.path.splitext(path)[1].lower()
            mime_map = {
                ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".bmp": "image/bmp", ".webp": "image/webp",
                ".ico": "image/x-icon", ".tiff": "image/tiff", ".tif": "image/tiff",
                ".svg": "image/svg+xml",
            }
            mime = mime_map.get(ext, "application/octet-stream")
            b64 = base64.b64encode(raw).decode("ascii")
            result = f"data:{mime};base64,{b64}"

            self.txt_result.delete("1.0", tk.END)
            self.txt_result.insert("1.0", result)
            self.b64_result.set(result)

            raw_kb = len(raw) / 1024
            b64_kb = len(result) / 1024
            self.status.config(
                text=f"✅ 转换完成！原始大小: {self._fmt_size(len(raw))}，Base64 长度: {len(result):,} 字符 ({b64_kb:.1f} KB)，膨胀比: {b64_kb/raw_kb:.1f}x"
            )
            self.btn_copy.config(state=tk.NORMAL)
        except Exception as e:
            self.status.config(text=f"❌ 转换失败: {e}")

    def _copy_result(self):
        text = self.b64_result.get()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        self.status.config(text="📋 已复制到剪贴板！")

    @staticmethod
    def _fmt_size(b):
        if b < 1024:
            return f"{b} B"
        elif b < 1024 ** 2:
            return f"{b/1024:.1f} KB"
        elif b < 1024 ** 3:
            return f"{b/1024**2:.1f} MB"
        return f"{b/1024**3:.2f} GB"

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Img2B64App().run()
