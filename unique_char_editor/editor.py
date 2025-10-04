import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import os

class UniqueCharEditor:
    def __init__(self, root):
        self.root = root

        # 設置視窗圖示
        try:
            ico_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
            if os.path.exists(ico_path):
                # 設置視窗標題列的圖示
                self.root.iconbitmap(ico_path)
                # 也設置任務欄圖示（Windows）
                self.root.wm_iconbitmap(ico_path)
            else:
                # 如果找不到圖示檔案，嘗試其他可能的路徑
                alternative_paths = [
                    os.path.join(os.getcwd(), "assets", "icon.ico"),
                    os.path.join(os.path.dirname(__file__), "icon.ico"),
                    "icon.ico"
                ]
                for alt_path in alternative_paths:
                    if os.path.exists(alt_path):
                        self.root.iconbitmap(alt_path)
                        self.root.wm_iconbitmap(alt_path)
                        break
        except (tk.TclError, OSError, Exception) as e:
            print(f"無法載入圖示檔案: {e}")
            pass

        self.root.title("UniqueCharEditor - 獨特字元編輯器")
        self.filename = None
        self.preview_font = tk.StringVar(value="JetBrains Mono")
        self.preview_size = tk.IntVar(value=14)

        # 現代化配色方案
        self.colors = {
            'bg_primary': '#1a1b26',      # 深藍灰背景
            'bg_secondary': '#24283b',    # 次要背景
            'bg_card': '#414868',         # 卡片背景
            'bg_input': '#f7f7f7',        # 輸入框背景
            'text_primary': '#c0caf5',    # 主要文字
            'text_secondary': '#9aa5ce',  # 次要文字
            'accent_blue': '#7aa2f7',     # 藍色強調
            'accent_green': '#9ece6a',    # 綠色強調
            'accent_purple': '#bb9af7',   # 紫色強調
            'accent_red': '#f7768e',      # 紅色強調
            'accent_orange': '#ff9e64',   # 橙色強調
            'hover_light': 'rgba(125, 207, 255, 0.1)'
        }

        self.root.configure(bg=self.colors['bg_primary'])
        self.root.geometry("1100x680")
        self.root.minsize(900, 600)

        # 配置 ttk 樣式
        self.setup_styles()

        # 創建主滾動容器
        main_canvas = tk.Canvas(root, bg=self.colors['bg_primary'], highlightthickness=0)
        main_scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = tk.Frame(main_canvas, bg=self.colors['bg_primary'])

        # 配置滾動
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)

        # 放置滾動容器
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")

        # 綁定鼠標滾輪事件
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_to_mousewheel(event):
            main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            main_canvas.unbind_all("<MouseWheel>")

        main_canvas.bind('<Enter>', _bind_to_mousewheel)
        main_canvas.bind('<Leave>', _unbind_from_mousewheel)

        # ========== 標題列 ==========
        title_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_primary'], height=60)
        title_frame.pack(fill="x", pady=(20,0))
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame, 
            text="🔤 UniqueCharEditor", 
            font=('Segoe UI', 20, 'bold'), 
            bg=self.colors['bg_primary'],
            fg=self.colors['accent_blue']
        )
        title_label.pack(pady=15)

        # ========== 檔案選擇區 ==========
        file_container = tk.Frame(self.scrollable_frame, bg=self.colors['bg_primary'])
        file_container.pack(fill="x", padx=50, pady=(10,20))

        file_card = tk.Frame(file_container, bg=self.colors['bg_card'], relief="flat", bd=0)
        file_card.pack(fill="x", pady=5)

        file_inner = tk.Frame(file_card, bg=self.colors['bg_card'])
        file_inner.pack(fill="x", padx=25, pady=20)

        tk.Label(
            file_inner, 
            text="📁 當前檔案", 
            font=('Segoe UI', 12, 'bold'), 
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side="left", padx=(0,15))

        self.file_path_var = tk.StringVar(value="請選擇要編輯的檔案...")
        self.file_entry = tk.Entry(
            file_inner, 
            textvariable=self.file_path_var, 
            font=('Segoe UI', 11),
            width=65, 
            state='readonly', 
            readonlybackground=self.colors['bg_input'],
            relief="flat",
            bd=8,
            fg='#555'
        )
        self.file_entry.pack(side="left", padx=(0,15))

        self.change_btn = tk.Button(
            file_inner, 
            text="📂 瀏覽", 
            command=self.change_file, 
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['accent_blue'],
            fg='white',
            activebackground='#5a7bc4',
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.change_btn.pack(side="left", padx=(0,20))

        self.count_label = tk.Label(
            file_inner, 
            text="📊 字元數: 0", 
            font=('Segoe UI', 11, 'bold'), 
            bg=self.colors['bg_card'],
            fg=self.colors['accent_green']
        )
        self.count_label.pack(side="left")

        # ========== 主內容區域 ==========
        # 創建居中的外層容器
        center_wrapper = tk.Frame(self.scrollable_frame, bg=self.colors['bg_primary'])
        center_wrapper.pack(expand=True, fill="both", pady=(0,30))

        # 主內容容器 - 使用固定寬度並居中
        main_container = tk.Frame(center_wrapper, bg=self.colors['bg_primary'])
        main_container.pack(expand=True, padx=50, pady=20)

        # 左側預覽區
        preview_container = tk.Frame(main_container, bg=self.colors['bg_primary'])
        preview_container.pack(side="left", fill="both", expand=True, padx=(0,25))

        preview_card = tk.Frame(preview_container, bg=self.colors['bg_card'], relief="flat", bd=0)
        preview_card.pack(fill="both", expand=True)

        # 預覽標題
        preview_header = tk.Frame(preview_card, bg=self.colors['bg_card'], height=50)
        preview_header.pack(fill="x", pady=(20,0))
        preview_header.pack_propagate(False)

        tk.Label(
            preview_header, 
            text="👁️ 內容預覽", 
            font=('Segoe UI', 14, 'bold'), 
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(side="left", padx=25)

        # 預覽文字框（帶滾動條）
        preview_content = tk.Frame(preview_card, bg=self.colors['bg_card'])
        preview_content.pack(fill="both", expand=True, padx=25, pady=(10,0))

        # 創建文字框和滾動條的容器
        text_container = tk.Frame(preview_content, bg=self.colors['bg_card'])
        text_container.pack(fill="both", expand=True)

        self.preview_box = tk.Text(
            text_container, 
            state='disabled',
            font=(self.preview_font.get(), self.preview_size.get()),
            wrap='char', 
            bg='#2a2e42', 
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            selectbackground=self.colors['accent_purple'],
            bd=0, 
            relief="flat",
            padx=15, 
            pady=15
        )

        # 添加垂直滾動條
        scrollbar = tk.Scrollbar(text_container, orient="vertical", command=self.preview_box.yview)
        self.preview_box.configure(yscrollcommand=scrollbar.set)

        # 將文字框和滾動條放置
        self.preview_box.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.preview_box.tag_configure("highlight", background=self.colors['accent_orange'], foreground="black")

        # 控制面板 - 使用更好的佈局
        control_panel = tk.Frame(preview_card, bg=self.colors['bg_card'], height=80)
        control_panel.pack(fill="x", padx=25, pady=(15,20))
        control_panel.pack_propagate(False)

        # 上排：字體設定
        font_row = tk.Frame(control_panel, bg=self.colors['bg_card'])
        font_row.pack(fill="x", pady=(5,8))

        tk.Label(font_row, text="🎨 字體設定:", font=('Segoe UI', 10, 'bold'), bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(side="left", padx=(0,15))

        tk.Label(font_row, text="字體:", font=('Segoe UI', 9), bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side="left", padx=(0,5))

        # 獲取系統字體並創建字體選項
        available_fonts = sorted(font.families())
        common_fonts = ['Arial', 'Times New Roman', 'Consolas', 'JetBrains Mono', 'Courier New', 'Microsoft JhengHei', 'SimHei', 'SimSun']

        # 合併常用字體和系統字體，去除重複
        font_options = []
        for f in common_fonts:
            if f in available_fonts:
                font_options.append(f)

        # 添加其他系統字體
        for f in available_fonts:
            if f not in font_options:
                font_options.append(f)

        font_combobox = ttk.Combobox(
            font_row, 
            textvariable=self.preview_font, 
            values=font_options,
            width=16, 
            state="readonly",
            font=('Segoe UI', 9)
        )
        font_combobox.pack(side="left", padx=(0,15))

        # 綁定字體變更事件
        font_combobox.bind('<<ComboboxSelected>>', lambda e: self.update_preview())

        tk.Label(font_row, text="大小:", font=('Segoe UI', 9), bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side="left", padx=(0,5))
        font_size = tk.Spinbox(font_row, from_=8, to=48, textvariable=self.preview_size, width=5, command=self.update_preview, relief="flat", bd=3)
        font_size.pack(side="left", padx=(0,15))

        apply_btn = tk.Button(
            font_row, 
            text="✨ 套用", 
            command=self.update_preview,
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['accent_purple'],
            fg='white',
            activebackground='#9b85d4',
            relief="flat",
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2"
        )
        apply_btn.pack(side="left")

        # 下排：搜尋功能
        search_row = tk.Frame(control_panel, bg=self.colors['bg_card'])
        search_row.pack(fill="x", pady=(0,5))

        tk.Label(search_row, text="🔍 字元搜尋:", font=('Segoe UI', 10, 'bold'), bg=self.colors['bg_card'], fg=self.colors['text_primary']).pack(side="left", padx=(0,15))

        tk.Label(search_row, text="查找:", font=('Segoe UI', 9), bg=self.colors['bg_card'], fg=self.colors['text_secondary']).pack(side="left", padx=(0,5))
        self.search_entry = tk.Entry(search_row, width=12, font=('Segoe UI', 9), relief="flat", bd=3)
        self.search_entry.pack(side="left", padx=(0,15))

        self.search_btn = tk.Button(
            search_row, 
            text="🔆 高亮顯示", 
            command=self.highlight_char,
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['accent_orange'],
            fg='white',
            activebackground='#e6865a',
            relief="flat",
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2"
        )
        self.search_btn.pack(side="left")

        # ========== 右側操作區 ==========
        op_container = tk.Frame(main_container, bg=self.colors['bg_primary'], width=240)
        op_container.pack(side="right", fill="y")
        op_container.pack_propagate(False)

        op_card = tk.Frame(op_container, bg=self.colors['bg_card'], relief="flat", bd=0)
        op_card.pack(fill="both", expand=True)

        # 操作標題
        op_header = tk.Frame(op_card, bg=self.colors['bg_card'], height=50)
        op_header.pack(fill="x", pady=(20,10))
        op_header.pack_propagate(False)

        tk.Label(
            op_header, 
            text="⚡ 操作面板", 
            font=('Segoe UI', 13, 'bold'), 
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        ).pack(padx=20)

        # 按鈕區域
        btn_container = tk.Frame(op_card, bg=self.colors['bg_card'])
        btn_container.pack(fill="both", expand=True, padx=20, pady=10)

        # 按鈕樣式配置
        buttons_config = [
            ("➕ 新增字元", self.add_chars_dialog, self.colors['accent_green'], '#7db46c'),
            ("➖ 刪除字元", self.del_chars_dialog, self.colors['accent_blue'], '#5a7bc4'),
            ("📥 批量導入", self.import_chars_file, self.colors['accent_purple'], '#9b85d4'),
            ("🔍 缺字比對", self.compare_chars_dialog, self.colors['accent_orange'], '#e6865a'),
            ("🔄 移除重複", self.remove_duplicates, self.colors['accent_orange'], '#e6865a'),
            ("🗑️ 清空全部", self.clear_all, self.colors['accent_red'], '#d85d7a')
        ]

        self.operation_buttons = []
        for i, (text, command, bg_color, hover_color) in enumerate(buttons_config):
            btn = tk.Button(
                btn_container,
                text=text,
                command=command,
                font=('Segoe UI', 11, 'bold'),
                bg=bg_color,
                fg='white',
                activebackground=hover_color,
                relief="flat",
                bd=0,
                width=16,
                pady=12,
                cursor="hand2"
            )

            # 特殊間距處理
            pady_top = 25 if i == len(buttons_config)-1 else 8
            btn.pack(pady=(pady_top, 8), fill="x")
            self.operation_buttons.append(btn)

        # 初始狀態
        self.set_buttons_state("disabled")
        self.update_preview()

    def setup_styles(self):
        """設定 ttk 樣式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置各種樣式
        style.configure('Custom.TButton',
                       background=self.colors['accent_blue'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))

        style.map('Custom.TButton',
                 background=[('active', '#5a7bc4')])

    def set_buttons_state(self, state):
        for btn in self.operation_buttons:
            btn.config(state=state)
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
        self.count_label.config(text=f"📊 字元數: {len(content)}" if self.filename else "📊 字元數: 0")
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
        # 過濾掉換行符號和空白字符
        filtered_str = ''.join(c for c in new_str if not c.isspace())
        existing = set(self.get_content())
        to_add = [c for c in filtered_str if c not in existing]
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
            
            # 過濾掉換行符號和空白字符，並去除重複字元
            filtered_str = ''.join(c for c in import_content if not c.isspace())
            unique_chars = ''.join(dict.fromkeys(filtered_str))  # 保持順序並去除重複
            
            existing = set(self.get_content())
            to_add = [c for c in unique_chars if c not in existing]
            
            if to_add:
                with open(self.filename, "a", encoding="utf-8") as f:
                    f.write("".join(to_add))
                messagebox.showinfo("批量導入成功", f"已新增 {len(to_add)} 個不重複字元：\n{''.join(to_add)}")
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

    def remove_duplicates(self):
        """移除檔案中的重複字元"""
        content = self.get_content()
        if not content:
            messagebox.showinfo("提示", "檔案內容為空，無需移除重複字元。")
            return
        
        # 計算重複字元數量
        original_count = len(content)
        unique_chars = ''.join(dict.fromkeys(content))  # 保持順序並去除重複
        unique_count = len(unique_chars)
        duplicates_count = original_count - unique_count
        
        if duplicates_count == 0:
            messagebox.showinfo("無重複", "檔案中沒有重複字元。")
            return
        
        # 二次確認對話框
        confirm_msg = f"發現 {duplicates_count} 個重複字元\n\n" \
                     f"原始字元數: {original_count}\n" \
                     f"去重後字元數: {unique_count}\n\n" \
                     f"確定要移除重複字元嗎？\n此操作無法還原！"
        
        if messagebox.askyesno("移除重複字元", confirm_msg):
            self.write_content(unique_chars)
            self.update_preview()
            messagebox.showinfo("完成", f"已成功移除 {duplicates_count} 個重複字元！\n\n" \
                                        f"原始: {original_count} 個字元\n" \
                                        f"現在: {unique_count} 個字元")

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