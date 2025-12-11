# 構建說明

## 系統要求

⚠️ **重要**: 由於 macOS 系統自帶的 Tcl/Tk 8.5.9 版本過舊，必須使用 Homebrew Python 3.11 進行構建。

### 前置條件

1. **Homebrew** (macOS 套件管理器)
2. **Homebrew Python 3.11** (包含更新的 Tcl/Tk 8.6+)
3. **python-tk@3.11** (Homebrew Python 的 tkinter 支援)

### 快速安裝

```bash
# 安裝 Homebrew（如果尚未安裝）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安裝 Python 3.11 和 python-tk
brew install python@3.11 python-tk@3.11

# 安裝 Python 依賴
/opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
```

## 已完成的構建

✅ Mac 應用程式已成功構建！

### 輸出位置

構建完成的文件位於 `dist` 目錄：
- **UniqueCharEditor.app** - 完整的 Mac 應用程式包（推薦使用）
- **UniqueCharEditor** - 獨立可執行文件

### 如何使用

#### 方法 1：使用 .app 應用包（推薦）

1. 打開 Finder
2. 導航到項目的 `dist` 文件夾
3. 雙擊 `UniqueCharEditor.app` 即可運行
4. （可選）將 `UniqueCharEditor.app` 拖到「應用程式」文件夾以便於訪問

#### 方法 2：使用命令行

```bash
# 進入 dist 目錄
cd dist

# 運行應用
open UniqueCharEditor.app
```

### 常見問題

**Q: 無法打開應用，提示「來自身份不明開發者」怎麼辦？**

A: 首次運行時，macOS 可能會阻止未簽名的應用。解決方法：
1. 右鍵點擊 `UniqueCharEditor.app`
2. 選擇「打開」
3. 在彈出的對話框中點擊「打開」

或使用終端命令：
```bash
xattr -cr dist/UniqueCharEditor.app
```

**Q: 如何重新構建？**

A: 運行以下命令：
```bash
# 使用自動化腳本（推薦）
./build.sh

# 或手動構建
/opt/homebrew/bin/python3.11 -m PyInstaller --clean --noconfirm UniqueCharEditor.spec
```

### 發布應用

如果要分發給其他用戶：

1. **壓縮應用**：
   ```bash
   cd dist
   zip -r UniqueCharEditor-mac.zip UniqueCharEditor.app
   ```

2. **（可選）代碼簽名**：
   如果你有 Apple 開發者帳號，可以對應用進行簽名：
   ```bash
   codesign --deep --force --sign "Developer ID Application: Your Name" UniqueCharEditor.app
   ```

3. **測試**：在另一台 Mac 上解壓並測試應用是否正常運行

### 技術細節

- **架構**：ARM64 (Apple Silicon)
- **Python 版本**：3.11.14 (Homebrew)
- **Tcl/Tk 版本**：8.6.17 (Homebrew)
- **PyInstaller 版本**：6.17.0
- **包含的資源**：應用圖標（自動從 .ico 轉換為 .icns）
- **模式**：Windowed + onedir（無終端窗口）

### 依賴項

項目依賴已記錄在 `requirements.txt`：
- `pyinstaller>=6.0.0` - 用於構建應用程式
- `pillow>=10.0.0` - 用於圖標格式轉換

### 構建環境

確保你的系統已安裝：
- **Homebrew** (macOS 套件管理器)
- **Homebrew Python 3.11+** (包含 Tcl/Tk 8.6+)
- **python-tk@3.11** (tkinter 支援)
- 所有 requirements.txt 中列出的依賴

**為什麼必須使用 Homebrew Python？**

macOS 系統自帶的 Python 使用過時的 Tcl/Tk 8.5.9 框架，PyInstaller 打包的應用無法正確使用這個版本。Homebrew Python 3.11 包含更新的 Tcl/Tk 8.6.17，可以正常工作。

### 開發者備註

- 應用使用 onefile 模式構建，所有資源都打包在單個 .app 包中
- 圖標會自動從 .ico 格式轉換為 macOS 所需的 .icns 格式
- 應用不顯示終端窗口（console=False）
