import tkinter as tk
from tkinter import filedialog, messagebox
import os

class UniqueCharEditor:
    def __init__(self, root):
        self.root = root

        try:
            ico_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if os.path.exists(ico_path):
                self.root.iconbitmap(ico_path)
        except tk.TclError:
            pass
        except OSError:
            pass


        self.root.title("UniqueCharEditor")
        self.filename = None
        self.preview_font = tk.StringVar(value="Consolas")
        self.preview_size = tk.IntVar(value=18)

        self.root.configure(bg="#f5f6fa")
        self.root.geometry("900x480")
        self.root.minsize(760, 360)

        # ========== 上方檔案列 ==========
        file_frame = tk.Frame(root, bg="#f5f6fa")
        file_frame.pack(fill="x", pady=12)

        tk.Label(file_frame, text="當前檔案：", font=('Segoe UI', 12, 'bold'), bg="#f5f6fa").pack(side="left", padx=(18,2))
        self.file_path_var = tk.StringVar(value="請選擇檔案")
        self.file_entry = tk.Entry(
            file_frame, textvariable=self.file_path_var, font=('Segoe UI', 12),
            width=60, state='readonly', readonlybackground="#fff", relief="flat"
        )
        self.file_entry.pack(side="left", padx=3)
        self.change_btn = tk.Button(file_frame, text="選擇檔案", command=self.change_file, width=9)
        self.change_btn.pack(side="left", padx=7)
        self.count_label = tk.Label(file_frame, text="字元數: 0", font=('Segoe UI', 11), bg="#f5f6fa")
        self.count_label.pack(side="left", padx=16)

        # ========== 主內容區域 ==========
        main_frame = tk.Frame(root, bg="#f5f6fa")
        main_frame.pack(expand=True, fill="both", padx=18, pady=6)

        # 預覽區卡片
        preview_card = tk.Frame(main_frame, bd=2, relief="groove", bg="#fafcff")
        preview_card.pack(side="left", padx=6, pady=10, fill="both", expand=True)

        # 內容預覽
        tk.Label(preview_card, text="內容預覽", font=('Segoe UI', 12, 'bold'), bg="#fafcff").pack(anchor='w', padx=12, pady=(9,3))
        self.preview_box = tk.Text(
            preview_card, height=11, width=44, state='disabled',
            font=(self.preview_font.get(), self.preview_size.get()),
            wrap='char', bg="#fff", bd=0, padx=8, pady=8
        )
        self.preview_box.pack(fill="both", expand=True, padx=12, pady=(0,4))
        self.preview_box.tag_configure("highlight", background="#ffd94a", foreground="black")

        # 下方設定/查找區塊
        util_frame = tk.Frame(preview_card, bg="#fafcff")
        util_frame.pack(fill="x", padx=12, pady=(0,8))

        # 字體設定
        tk.Label(util_frame, text="字體:", font=('Segoe UI', 10), bg="#fafcff").pack(side="left", padx=(0,2))
        font_entry = tk.Entry(util_frame, textvariable=self.preview_font, width=11)
        font_entry.pack(side="left", padx=(0,6))
        tk.Label(util_frame, text="大小:", font=('Segoe UI', 10), bg="#fafcff").pack(side="left")
        font_size = tk.Spinbox(util_frame, from_=8, to=48, textvariable=self.preview_size, width=3, command=self.update_preview)
        font_size.pack(side="left", padx=(2, 8))
        tk.Button(util_frame, text="套用", command=self.update_preview, width=5).pack(side="left", padx=(0, 16))

        # 查找區塊
        tk.Label(util_frame, text="查找字元:", font=('Segoe UI', 10), bg="#fafcff").pack(side="left")
        self.search_entry = tk.Entry(util_frame, width=7)
        self.search_entry.pack(side="left", padx=(2,0))
        self.search_btn = tk.Button(util_frame, text="高亮", command=self.highlight_char, width=6)
        self.search_btn.pack(side="left", padx=(5, 0))

        # ========== 右側操作區卡片 ==========
        op_card = tk.Frame(main_frame, bd=2, relief="groove", bg="#fcfcfc")
        op_card.pack(side="left", padx=(24,6), pady=14, fill="y")

        btn_opts = dict(width=18, height=2, font=('Segoe UI', 11, 'bold'), bg="#f6f7fb", activebackground="#ebeffa", relief=tk.RAISED)
        self.add_btn = tk.Button(op_card, text="新增", command=self.add_chars_dialog, **btn_opts)
        self.add_btn.pack(pady=(15,8))
        self.del_btn = tk.Button(op_card, text="刪除", command=self.del_chars_dialog, **btn_opts)
        self.del_btn.pack(pady=8)
        self.import_btn = tk.Button(op_card, text="批量導入", command=self.import_chars_file, **btn_opts)
        self.import_btn.pack(pady=8)
        self.compare_btn = tk.Button(op_card, text="批量缺字比對", command=self.compare_chars_dialog, **btn_opts)
        self.compare_btn.pack(pady=8)
        self.clear_btn = tk.Button(op_card, text="清空全部", command=self.clear_all, **dict(btn_opts, bg="#fff2f2", fg="#b42a2a", activebackground="#ffdada"))
        self.clear_btn.pack(pady=(36,12))

        # 初始全部 disable
        self.set_buttons_state("disabled")
        self.update_preview()

    def set_buttons_state(self, state):
        self.add_btn.config(state=state)
        self.del_btn.config(state=state)
        self.import_btn.config(state=state)
        self.compare_btn.config(state=state)
        self.clear_btn.config(state=state)
        self.search_btn.config(state=state)

    def get_content(self):
        if not self.filename or not os.path.exists(self.filename):
            return ""
        with open(self.filename, "r", encoding="utf-8") as f:
            return f.read()

    def write_content(self, content):
        if not self.filename:
            return
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(content)

    def update_preview(self):
        content = self.get_content()
        self.preview_box.config(state='normal')
        self.preview_box.delete(1.0, tk.END)
        for i in range(0, len(content), 20):
            self.preview_box.insert(tk.END, content[i:i+20] + '\n')
        self.preview_box.config(font=(self.preview_font.get(), self.preview_size.get()))
        self.preview_box.config(state='disabled')
        self.count_label.config(text=f"字元數: {len(content)}" if self.filename else "字元數: 0")
        self.preview_box.tag_remove("highlight", "1.0", tk.END)

    def change_file(self):
        path = filedialog.askopenfilename(
            title="選擇要編輯的文字檔",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            self.filename = path
            self.file_path_var.set(self.filename)
            self.set_buttons_state("normal")
            self.update_preview()

    def add_chars_dialog(self):
        self.open_input_dialog("新增字元", "請輸入要新增的字元（可多個）:", self.add_chars)

    def del_chars_dialog(self):
        self.open_input_dialog("刪除字元", "請輸入要刪除的字元（可多個）:", self.del_chars)

    def open_input_dialog(self, title, prompt, handler):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.grab_set()
        tk.Label(dialog, text=prompt, font=('Segoe UI', 11)).pack(padx=14, pady=8)
        entry = tk.Entry(dialog, width=24, font=('Consolas', 13))
        entry.pack(padx=14, pady=8)
        entry.focus_set()
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=8)
        def ok():
            value = entry.get()
            if value:
                result = handler(value)
                if result:
                    messagebox.showinfo("成功", result)
                else:
                    messagebox.showinfo("無變更", "沒有任何字元被異動。")
                dialog.destroy()
                self.update_preview()
            else:
                messagebox.showinfo("提示", "未輸入內容")
        def cancel():
            dialog.destroy()
        tk.Button(btn_frame, text="確認", width=8, command=ok).pack(side="left", padx=6)
        tk.Button(btn_frame, text="取消", width=8, command=cancel).pack(side="left", padx=6)
        dialog.bind('<Return>', lambda e: ok())
        dialog.bind('<Escape>', lambda e: cancel())

    def add_chars(self, new_str):
        existing = set(self.get_content())
        to_add = [c for c in new_str if c not in existing]
        if to_add:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write("".join(to_add))
            return f"已新增：{''.join(to_add)}"
        return ""

    def del_chars(self, del_str):
        content = self.get_content()
        remove_set = set(del_str)
        new_content = ''.join(c for c in content if c not in remove_set)
        removed = [c for c in set(content) if c in remove_set]
        if new_content != content:
            self.write_content(new_content)
            return f"已刪除：{''.join(removed)}"
        return ""

    def import_chars_file(self):
        path = filedialog.askopenfilename(
            title="批量導入字元檔案",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                import_content = f.read()
            added = self.add_chars(import_content)
            if added:
                messagebox.showinfo("批量導入成功", added)
            else:
                messagebox.showinfo("無新增", "沒有任何新字元被新增。")
            self.update_preview()

    def compare_chars_dialog(self):
        path = filedialog.askopenfilename(
            title="選擇要比對的 txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                compare_content = f.read()
            current = set(self.get_content())
            to_find = set(compare_content)
            missing = sorted(list(to_find - current))
            if missing:
                msg = f"缺少 {len(missing)} 個字：\n" + "".join(missing)
                messagebox.showinfo("缺字報表", msg)
            else:
                messagebox.showinfo("缺字報表", "全部字元皆已包含！")

    def clear_all(self):
        if messagebox.askyesno("清空全部", "確定要清空所有字元內容？\n此操作無法還原！"):
            self.write_content("")
            self.update_preview()
            messagebox.showinfo("完成", "已清空全部內容。")

    def highlight_char(self):
        char = self.search_entry.get()
        if not char:
            messagebox.showinfo("提示", "請輸入要查找的字元")
            return
        self.preview_box.config(state='normal')
        self.preview_box.tag_remove("highlight", "1.0", tk.END)
        found = False
        idx = 1.0
        while True:
            idx = self.preview_box.search(char, idx, stopindex=tk.END)
            if not idx:
                break
            self.preview_box.tag_add("highlight", idx, f"{idx}+1c")
            found = True
            idx = f"{idx}+1c"
        self.preview_box.config(state='disabled')
        if not found:
            messagebox.showinfo("查找", f"沒有找到「{char}」這個字元。")