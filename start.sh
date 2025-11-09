#!/bin/bash

# 面试题库管理系统启动脚本

echo "🚀 启动面试题库管理系统..."
echo "================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误：Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误：Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  未找到.env文件，创建默认配置..."
    cp .env.example .env
    echo "✅ 已创建.env文件，请根据需要修改配置"
fi

# 构建和启动服务
echo "📦 构建Docker镜像..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi

echo "🎉 构建成功！"
echo "🚀 启动服务..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 启动失败，请检查错误信息"
    exit 1
fi

echo "✅ 服务启动成功！"
echo ""
echo "🌐 应用地址："
echo "   前端应用: http://localhost"
echo "   后端API: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "📋 常用命令："
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo "   查看状态: docker-compose ps"
echo ""
echo "🔧 配置说明："
echo "   - 修改.env文件可配置OpenAI API密钥"
echo "   - 数据库文件保存在 ./backend/data/ 目录"
echo "   - 日志可通过 docker-compose logs 查看"
echo ""
echo "🎉 开始使用您的面试题库管理系统！"