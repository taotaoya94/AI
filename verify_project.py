#!/usr/bin/env python3
"""
项目完整性验证脚本
验证所有必需文件是否存在并且功能正常
"""

import os
import sys

def check_file(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✓ {description}: {filepath} ({size} bytes)")
        return True
    else:
        print(f"✗ {description}: {filepath} (不存在)")
        return False

def check_directory(dirpath, description):
    """检查目录是否存在"""
    if os.path.isdir(dirpath):
        count = len(os.listdir(dirpath))
        print(f"✓ {description}: {dirpath} ({count} 个文件)")
        return True
    else:
        print(f"✗ {description}: {dirpath} (不存在)")
        return False

def verify_project():
    """验证项目完整性"""
    print("="*60)
    print("项目完整性验证")
    print("="*60)
    print()
    
    checks = []
    
    print("【核心Python文件】")
    checks.append(check_file("config.py", "配置文件"))
    checks.append(check_file("main.py", "主程序"))
    checks.append(check_file("run_quick_demo.py", "快速演示"))
    checks.append(check_file("test_basic.py", "测试文件"))
    print()
    
    print("【源代码模块】")
    checks.append(check_file("src/__init__.py", "包初始化"))
    checks.append(check_file("src/models.py", "数据模型"))
    checks.append(check_file("src/crawler.py", "爬虫模块"))
    checks.append(check_file("src/parser.py", "解析器"))
    checks.append(check_file("src/database.py", "数据库"))
    checks.append(check_file("src/generator.py", "文档生成器"))
    print()
    
    print("【模板文件】")
    checks.append(check_file("templates/summary_template.html", "HTML模板"))
    checks.append(check_file("templates/summary_template.md", "Markdown模板"))
    print()
    
    print("【文档文件】")
    checks.append(check_file("README.md", "项目说明"))
    checks.append(check_file("USAGE.md", "使用说明"))
    checks.append(check_file("PROJECT_OVERVIEW.md", "项目概览"))
    checks.append(check_file("STATUS.md", "状态报告"))
    print()
    
    print("【配置文件】")
    checks.append(check_file("requirements.txt", "依赖列表"))
    checks.append(check_file(".gitignore", "Git忽略"))
    checks.append(check_file("setup.sh", "安装脚本"))
    print()
    
    print("【目录结构】")
    checks.append(check_directory("src", "源代码目录"))
    checks.append(check_directory("templates", "模板目录"))
    checks.append(check_directory("data", "数据目录"))
    checks.append(check_directory("data/output", "输出目录"))
    print()
    
    print("【功能测试】")
    try:
        import config
        print(f"✓ 配置加载成功: {len(config.INEQUALITY_NAMES)} 个不等式")
        checks.append(True)
    except Exception as e:
        print(f"✗ 配置加载失败: {str(e)}")
        checks.append(False)
    
    try:
        from src.models import Inequality, Example
        ineq = Inequality(name="测试")
        print(f"✓ 数据模型正常")
        checks.append(True)
    except Exception as e:
        print(f"✗ 数据模型错误: {str(e)}")
        checks.append(False)
    
    try:
        from src.parser import InequalityParser
        parser = InequalityParser()
        predefined = parser._get_predefined_data()
        print(f"✓ 解析器正常: {len(predefined)} 个预定义不等式")
        checks.append(True)
    except Exception as e:
        print(f"✗ 解析器错误: {str(e)}")
        checks.append(False)
    
    print()
    print("="*60)
    
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"验证结果: {passed}/{total} 项通过 ({percentage:.1f}%)")
    
    if passed == total:
        print("✓ 项目完整性验证通过！")
        print()
        print("下一步:")
        print("  1. 运行 'python run_quick_demo.py' 查看演示")
        print("  2. 运行 'python main.py' 爬取完整数据")
        print("  3. 查看 data/output/ 目录中的文档")
        return 0
    else:
        print("✗ 项目不完整，请检查缺失的文件")
        return 1

if __name__ == "__main__":
    sys.exit(verify_project())
