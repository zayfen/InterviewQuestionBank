#!/bin/bash

# 面试题库管理系统本地启动脚本（非Docker环境）

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# PID 文件路径
BACKEND_PID_FILE=".backend.pid"
FRONTEND_PID_FILE=".frontend.pid"

echo -e "${BLUE}🚀 启动面试题库管理系统（本地模式）...${NC}"
echo "================================"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：Python3 未安装，请先安装 Python 3.9+${NC}"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 错误：Node.js 未安装，请先安装 Node.js${NC}"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ 错误：npm 未安装，请先安装 npm${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 版本：$(python3 --version)${NC}"
echo -e "${GREEN}✅ Node.js 版本：$(node --version)${NC}"
echo -e "${GREEN}✅ npm 版本：$(npm --version)${NC}"
echo ""

# 检查后端 .env 文件
if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}⚠️  未找到后端 .env 文件，创建默认配置...${NC}"
    if [ -f backend/.env.example ]; then
        cp backend/.env.example backend/.env
        echo -e "${GREEN}✅ 已创建 backend/.env 文件，请根据需要修改配置${NC}"
    else
        echo -e "${RED}❌ 错误：找不到 backend/.env.example 文件${NC}"
        exit 1
    fi
fi

# 1. 安装后端依赖
echo -e "${BLUE}📦 检查后端依赖...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  未找到虚拟环境，创建新的虚拟环境...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo -e "${BLUE}📦 安装 Python 依赖...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✅ Python 依赖安装完成${NC}"

# 初始化数据库（如果需要）
if [ ! -f "interview_questions.db" ]; then
    echo -e "${BLUE}🗄️  初始化数据库...${NC}"
    python init_data.py
    echo -e "${GREEN}✅ 数据库初始化完成${NC}"
fi

cd ..

# 2. 安装前端依赖
echo -e "${BLUE}📦 检查前端依赖...${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  未找到 node_modules，安装前端依赖...${NC}"
    npm install
    echo -e "${GREEN}✅ 前端依赖安装完成${NC}"
else
    echo -e "${GREEN}✅ 前端依赖已存在${NC}"
fi

cd ..

# 3. 检查端口占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

if check_port 8000; then
    echo -e "${YELLOW}⚠️  警告：端口 8000 已被占用${NC}"
    echo -e "${YELLOW}   正在尝试停止占用端口的进程...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

if check_port 5173; then
    echo -e "${YELLOW}⚠️  警告：端口 5173 已被占用${NC}"
    echo -e "${YELLOW}   正在尝试停止占用端口的进程...${NC}"
    lsof -ti:5173 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# 4. 启动后端服务
echo ""
echo -e "${BLUE}🚀 启动后端服务...${NC}"
cd backend
source venv/bin/activate

# 后台启动后端
nohup python3 main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../$BACKEND_PID_FILE

cd ..

# 等待后端启动
sleep 3

# 检查后端是否启动成功
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ 后端服务启动成功 (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}❌ 后端服务启动失败，请查看 backend/backend.log${NC}"
    exit 1
fi

# 5. 启动前端服务
echo -e "${BLUE}🚀 启动前端服务...${NC}"
cd frontend

# 后台启动前端
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../$FRONTEND_PID_FILE

cd ..

# 等待前端启动
sleep 3

# 检查前端是否启动成功
if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ 前端服务启动成功 (PID: $FRONTEND_PID)${NC}"
else
    echo -e "${RED}❌ 前端服务启动失败，请查看 frontend/frontend.log${NC}"
    # 停止后端
    kill $BACKEND_PID 2>/dev/null || true
    rm -f $BACKEND_PID_FILE
    exit 1
fi

# 6. 显示启动信息
echo ""
echo -e "${GREEN}✅ 所有服务启动成功！${NC}"
echo ""
echo -e "${BLUE}🌐 应用地址：${NC}"
echo -e "   前端应用: ${GREEN}http://localhost:5173${NC}"
echo -e "   后端API:  ${GREEN}http://localhost:8000${NC}"
echo -e "   API文档:  ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}📋 常用命令：${NC}"
echo -e "   查看后端日志: ${YELLOW}tail -f backend/backend.log${NC}"
echo -e "   查看前端日志: ${YELLOW}tail -f frontend/frontend.log${NC}"
echo -e "   停止服务:     ${YELLOW}./stop-local.sh${NC}"
echo -e "   重启服务:     ${YELLOW}./stop-local.sh && ./start-local.sh${NC}"
echo ""
echo -e "${BLUE}🔧 配置说明：${NC}"
echo -e "   - 修改 backend/.env 文件可配置 OpenAI API 密钥"
echo -e "   - 数据库文件保存在 backend/ 目录"
echo -e "   - 后端进程 PID: $BACKEND_PID"
echo -e "   - 前端进程 PID: $FRONTEND_PID"
echo ""
echo -e "${GREEN}🎉 开始使用您的面试题库管理系统！${NC}"

