#!/bin/bash

# UniqueCharEditor 構建腳本 for macOS

echo "🚀 開始構建 UniqueCharEditor..."
echo ""

# 檢查 Homebrew 是否存在
if ! command -v brew &> /dev/null; then
    echo "❌ 錯誤：未找到 Homebrew。請先安裝：https://brew.sh/"
    exit 1
fi

echo "✓ Homebrew 已安裝"

# 檢查 Homebrew Python 3.11 是否存在
PYTHON="/opt/homebrew/bin/python3.11"
if ! command -v "$PYTHON" &> /dev/null; then
    echo ""
    echo "❌ 未找到 Homebrew Python 3.11"
    echo "正在安裝 Python 3.11 和 python-tk..."
    brew install python@3.11 python-tk@3.11
fi

echo "✓ Python 3.11 已安裝"

# 安裝/更新依賴
echo ""
echo "📦 安裝/更新依賴..."
"$PYTHON" -m pip install -r requirements.txt

# 清理舊的構建文件
echo ""
echo "🧹 清理舊的構建文件..."
rm -rf build dist

# 執行構建
echo ""
echo "🔨 開始構建應用..."
"$PYTHON" -m PyInstaller --clean --noconfirm UniqueCharEditor.spec

# 檢查構建是否成功
if [ -d "dist/UniqueCharEditor.app" ]; then
    echo ""
    echo "✅ 構建成功！"
    echo ""
    echo "📍 應用位置: dist/UniqueCharEditor.app"
    echo ""
    echo "使用方法："
    echo "  1. 雙擊 dist/UniqueCharEditor.app 運行"
    echo "  2. 或執行: open dist/UniqueCharEditor.app"
    echo ""
    
    # 顯示應用大小
    APP_SIZE=$(du -sh dist/UniqueCharEditor.app | cut -f1)
    echo "📊 應用大小: $APP_SIZE"
    echo ""
    
    # 詢問是否立即運行
    read -p "是否立即運行應用？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 啟動應用..."
        open dist/UniqueCharEditor.app
    fi
else
    echo ""
    echo "❌ 構建失敗！請檢查錯誤訊息。"
    exit 1
fi
