# 故障排除指南

## 問題：應用崩潰 - Tcl/Tk 版本錯誤

### 錯誤信息
```
macOS 26 (2601) or later required, have instead 16 (1601) !
```

### 根本原因

macOS 系統自帶的 Tcl/Tk 8.5.9 版本太旧，並且有版本檢測問題。PyInstaller 打包的應用無法正確使用系統的 Tcl/Tk 框架。

### ✅ 解決方案

有兩種解決方案：

#### 方案 1：使用 Homebrew Python（推薦）

1. **安裝 Homebrew**（如果尚未安裝）：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **安裝 Homebrew Python 和 Tcl/Tk**：
   ```bash
   brew install python@3.11 python-tk@3.11
   ```

3. **使用 Homebrew Python 重新構建**：
   ```bash
   # 使用 Homebrew Python
   /opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
   /opt/homebrew/bin/python3.11 -m PyInstaller --clean --noconfirm UniqueCharEditor.spec
   ```

#### 方案 2：僅用於開發測試

如果只是想在本機運行測試，可以直接使用 Python 腳本：

```bash
# 直接運行 Python 腳本
python3 main.py
```

或

```bash
# 使用模塊方式運行
python3 -m unique_char_editor.editor
```

### 🔧 當前狀態

- ✅ 依賴已安裝
- ✅ 項目代碼正常
- ❌ **打包的 .app 無法運行**（Tcl/Tk 版本問題）
- ✅ 直接運行 Python 腳本可以正常工作

### 📝 技術細節

**為什麼會出現這個問題？**

1. **系統 Tcl/Tk 版本**: macOS 自帶的 Tk 8.5.9（2011 年發布）
2. **版本檢測失敗**: PyInstaller 打包後，Tk 無法正確檢測 macOS 版本
3. **框架依賴問題**: onedir 模式仍然依賴系統 Tcl/Tk 框架

**Homebrew Python 為什麼能解決？**

- Homebrew Python 包含獨立的 Tcl/Tk 8.6+ 版本
- 不依賴系統過時的 Tcl/Tk 框架
- PyInstaller 可以正確打包所有依賴

### 🚀 推薦工作流程

對於發布應用程序：

1. 使用 Homebrew Python 進行構建
2. 在多台 Mac 上測試（包括沒有 Homebrew 的機器）
3. 考慮使用代碼簽名（需要 Apple Developer 帳號）

對於個人使用：

- 直接使用 `python3 main.py` 運行
- 或使用 Homebrew Python 構建

### 📚 相關資源

- [PyInstaller macOS Issues](https://pyinstaller.org/en/stable/requirements.html#macos)
- [Python Tk/Tcl on macOS](https://www.python.org/download/mac/tcltk/)
- [Homebrew](https://brew.sh/)

### ⚠️ 注意事項

如果您的 Mac 是 Apple Silicon（M1/M2/M3/M4）：
- 確保安裝 ARM64 版本的 Homebrew
- 使用 `/opt/homebrew/bin/python3` 而不是 `/usr/local/bin/python3`

如果您的 Mac 是 Intel：
- Homebrew 路徑為 `/usr/local/bin/python3`
