#!/bin/bash

# 面试题库管理系统本地停止脚本（非Docker环境）

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# PID 文件路径
BACKEND_PID_FILE=".backend.pid"
FRONTEND_PID_FILE=".frontend.pid"

echo -e "${BLUE}🛑 停止面试题库管理系统（本地模式）...${NC}"
echo "================================"

# 停止后端服务
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat $BACKEND_PID_FILE)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}🔴 停止后端服务 (PID: $BACKEND_PID)...${NC}"
        kill $BACKEND_PID
        sleep 2
        # 如果进程还在运行，强制杀死
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill -9 $BACKEND_PID
        fi
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    else
        echo -e "${YELLOW}⚠️  后端进程不存在 (PID: $BACKEND_PID)${NC}"
    fi
    rm -f $BACKEND_PID_FILE
else
    echo -e "${YELLOW}⚠️  未找到后端 PID 文件${NC}"
    # 尝试通过端口杀死进程
    if lsof -ti:8000 >/dev/null 2>&1; then
        echo -e "${YELLOW}🔴 发现占用 8000 端口的进程，正在停止...${NC}"
        lsof -ti:8000 | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✅ 已停止占用 8000 端口的进程${NC}"
    fi
fi

# 停止前端服务
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat $FRONTEND_PID_FILE)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}🔴 停止前端服务 (PID: $FRONTEND_PID)...${NC}"
        kill $FRONTEND_PID
        sleep 2
        # 如果进程还在运行，强制杀死
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill -9 $FRONTEND_PID
        fi
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    else
        echo -e "${YELLOW}⚠️  前端进程不存在 (PID: $FRONTEND_PID)${NC}"
    fi
    rm -f $FRONTEND_PID_FILE
else
    echo -e "${YELLOW}⚠️  未找到前端 PID 文件${NC}"
    # 尝试通过端口杀死进程
    if lsof -ti:5173 >/dev/null 2>&1; then
        echo -e "${YELLOW}🔴 发现占用 5173 端口的进程，正在停止...${NC}"
        lsof -ti:5173 | xargs kill -9 2>/dev/null
        echo -e "${GREEN}✅ 已停止占用 5173 端口的进程${NC}"
    fi
fi

# 额外清理：确保所有相关进程都被停止
echo -e "${BLUE}🧹 清理相关进程...${NC}"

# 清理可能遗留的 Python 进程
pkill -f "python.*main.py" 2>/dev/null && echo -e "${GREEN}✅ 清理了遗留的 Python 进程${NC}" || true

# 清理可能遗留的 npm 进程
pkill -f "vite" 2>/dev/null && echo -e "${GREEN}✅ 清理了遗留的 Vite 进程${NC}" || true

echo ""
echo -e "${GREEN}✅ 所有服务已停止！${NC}"
echo ""
echo -e "${BLUE}📋 提示：${NC}"
echo -e "   重新启动服务: ${YELLOW}./start-local.sh${NC}"

