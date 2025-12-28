#!/bin/bash

echo "=================================================="
echo "  数学不等式自动汇总系统 - 安装脚本"
echo "=================================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "检测到 Python 版本: $python_version"

# 检查是否已存在虚拟环境
if [ -d "venv" ]; then
    echo ""
    echo "发现已存在的虚拟环境"
    read -p "是否删除并重新创建？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "删除旧的虚拟环境..."
        rm -rf venv
    else
        echo "保留现有虚拟环境"
    fi
fi

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "创建虚拟环境..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
    echo "✓ 虚拟环境创建成功"
fi

# 激活虚拟环境
echo ""
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo ""
echo "升级 pip..."
pip install --upgrade pip -q

# 安装依赖
echo ""
echo "安装依赖包..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo ""
echo "✓ 所有依赖安装成功"

# 创建必要的目录
echo ""
echo "创建必要的目录..."
mkdir -p data/output
echo "✓ 目录创建完成"

# 运行测试
echo ""
read -p "是否运行基本测试？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "运行测试..."
    python test_basic.py
    
    if [ $? -ne 0 ]; then
        echo "❌ 测试失败，请检查错误信息"
        exit 1
    fi
fi

echo ""
echo "=================================================="
echo "  ✓ 安装完成！"
echo "=================================================="
echo ""
echo "使用方法："
echo "  1. 激活虚拟环境："
echo "     source venv/bin/activate"
echo ""
echo "  2. 运行快速演示（推荐首次使用）："
echo "     python run_quick_demo.py"
echo ""
echo "  3. 运行完整版本（爬取所有36个不等式）："
echo "     python main.py"
echo ""
echo "  4. 查看使用文档："
echo "     cat USAGE.md"
echo ""
echo "生成的文档位于: data/output/"
echo ""
