#!/usr/bin/env python3
"""
项目安装和配置测试脚本
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - 符合要求")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - 需要3.8+版本")
        return False

def check_node_version():
    """检查Node.js版本"""
    print("🔍 检查Node.js版本...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - 已安装")
            return True
        else:
            print("❌ Node.js 未安装或无法访问")
            return False
    except FileNotFoundError:
        print("❌ Node.js 未安装")
        return False

def check_docker():
    """检查Docker"""
    print("🔍 检查Docker...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ {version} - 已安装")
            return True
        else:
            print("❌ Docker 未安装或无法访问")
            return False
    except FileNotFoundError:
        print("❌ Docker 未安装")
        return False

def check_docker_compose():
    """检查Docker Compose"""
    print("🔍 检查Docker Compose...")
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ {version} - 已安装")
            return True
        else:
            print("❌ Docker Compose 未安装或无法访问")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose 未安装")
        return False

def check_project_structure():
    """检查项目结构"""
    print("🔍 检查项目结构...")
    
    required_files = [
        'backend/requirements.txt',
        'backend/app/main.py',
        'frontend/package.json',
        'frontend/src/main.ts',
        'docker-compose.yml',
        '.env.example'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if not missing_files:
        print("✅ 项目结构完整")
        return True
    else:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False

def check_environment_file():
    """检查环境变量文件"""
    print("🔍 检查环境变量文件...")
    
    if Path('.env').exists():
        print("✅ .env 文件已存在")
        return True
    elif Path('.env.example').exists():
        print("⚠️  .env 文件不存在，但有 .env.example 模板")
        print("   运行: cp .env.example .env")
        return False
    else:
        print("❌ 环境变量文件不存在")
        return False

def main():
    """主测试函数"""
    print("🚀 面试题库管理系统 - 环境检查")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_node_version(),
        check_docker(),
        check_docker_compose(),
        check_project_structure(),
        check_environment_file()
    ]
    
    print("\n" + "=" * 50)
    print("📊 检查结果汇总:")
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 环境检查通过！可以启动项目")
        print("\n下一步操作:")
        print("1. 如果使用Docker: ./start.sh")
        print("2. 如果手动部署: 分别启动前后端服务")
    else:
        print("\n❌ 环境检查未通过，请先解决上述问题")
        print("\n建议:")
        print("1. 安装缺失的依赖")
        print("2. 检查环境配置")
        print("3. 确保项目文件完整")

if __name__ == "__main__":
    main()