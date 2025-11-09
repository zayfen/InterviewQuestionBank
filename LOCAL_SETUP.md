# 本地启动脚本使用说明

本项目提供了两个便捷的脚本用于在本地环境（非 Docker）快速启动和停止应用。

## 📋 脚本列表

### 1. start-local.sh - 本地启动脚本
一键启动前后端服务的脚本。

**主要功能：**
- ✅ 自动检查 Python 3 和 Node.js 环境
- ✅ 自动创建 Python 虚拟环境（如果不存在）
- ✅ 自动安装前后端依赖
- ✅ 自动初始化数据库（如果不存在）
- ✅ 检查并释放被占用的端口
- ✅ 同时启动后端（端口 8000）和前端（端口 5173）服务
- ✅ 记录进程 PID 便于管理
- ✅ 彩色终端输出，清晰易读

**使用方法：**
```bash
./start-local.sh
```

**启动后访问：**
- 前端应用: http://localhost:5173
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 2. stop-local.sh - 本地停止脚本
优雅地停止所有运行中的服务。

**主要功能：**
- ✅ 根据 PID 文件停止后端和前端进程
- ✅ 如果 PID 文件不存在，通过端口查找并停止进程
- ✅ 清理所有相关的遗留进程
- ✅ 自动清理 PID 文件
- ✅ 友好的状态提示

**使用方法：**
```bash
./stop-local.sh
```

## 🚀 快速开始

### 首次启动

1. 确保安装了必要的环境：
   - Python 3.9+
   - Node.js 16+
   - npm

2. 配置后端环境变量：
```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，添加 OpenAI API 密钥（可选）
cd ..
```

3. 启动服务：
```bash
./start-local.sh
```

### 日常使用

**启动服务：**
```bash
./start-local.sh
```

**停止服务：**
```bash
./stop-local.sh
```

**重启服务：**
```bash
./stop-local.sh && ./start-local.sh
```

**查看日志：**
```bash
# 后端日志
tail -f backend/backend.log

# 前端日志
tail -f frontend/frontend.log
```

## 📂 生成的文件

启动脚本会生成以下文件和目录：

```
.
├── .backend.pid              # 后端进程 PID（被 .gitignore 忽略）
├── .frontend.pid             # 前端进程 PID（被 .gitignore 忽略）
├── backend/
│   ├── venv/                # Python 虚拟环境（被 .gitignore 忽略）
│   ├── backend.log          # 后端日志
│   └── interview_questions.db  # SQLite 数据库
└── frontend/
    ├── node_modules/        # 前端依赖（被 .gitignore 忽略）
    └── frontend.log         # 前端日志
```

## ⚠️ 常见问题

### 1. 端口被占用
如果启动时提示端口被占用，脚本会自动尝试停止占用端口的进程。如果仍有问题，可以手动执行：

```bash
# 释放 8000 端口（后端）
lsof -ti:8000 | xargs kill -9

# 释放 5173 端口（前端）
lsof -ti:5173 | xargs kill -9
```

### 2. Python 虚拟环境问题
如果虚拟环境出现问题，可以删除并重新创建：

```bash
rm -rf backend/venv
./start-local.sh
```

### 3. 依赖安装失败
确保有稳定的网络连接，并尝试：

```bash
# 清理后端依赖
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 清理前端依赖
rm -rf frontend/node_modules
cd frontend
npm install
cd ..
```

### 4. 数据库初始化失败
删除旧的数据库文件并重新初始化：

```bash
rm backend/interview_questions.db*
cd backend
source venv/bin/activate
python init_data.py
cd ..
```

## 🔧 高级配置

### 修改端口
如果需要修改服务端口，需要同时修改：

1. 后端端口：编辑 `backend/main.py` 中的端口配置
2. 前端端口：编辑 `frontend/vite.config.ts` 中的 server.port 配置
3. 启动脚本中的端口检查逻辑

### 使用其他 Python 版本
脚本默认使用 `python3` 命令。如果需要使用特定版本（如 python3.9），可以修改脚本中的 `python3` 为具体版本命令。

### 开启调试模式
查看更详细的启动日志：

```bash
# 前台启动后端（查看实时日志）
cd backend
source venv/bin/activate
python main.py

# 前台启动前端（新终端窗口）
cd frontend
npm run dev
```

## 🆚 与 Docker 方式对比

| 特性 | 本地启动 (start-local.sh) | Docker 启动 (start.sh) |
|------|---------------------------|------------------------|
| 启动速度 | ⚡ 快 | 🐢 慢（首次需构建） |
| 资源占用 | 💚 低 | 💛 中等 |
| 隔离性 | ❌ 无 | ✅ 完全隔离 |
| 调试便利性 | ✅ 容易 | ❌ 困难 |
| 生产环境 | ❌ 不推荐 | ✅ 推荐 |
| 开发环境 | ✅ 推荐 | 💛 可选 |
| 依赖管理 | 手动 | 自动 |

## 💡 最佳实践

1. **开发环境**：使用 `start-local.sh` 快速启动和调试
2. **生产环境**：使用 Docker (`start.sh`) 保证环境一致性
3. **每天开发前**：运行 `./start-local.sh` 启动服务
4. **每天开发后**：运行 `./stop-local.sh` 停止服务
5. **依赖更新后**：删除 `backend/venv` 和 `frontend/node_modules` 重新安装

## 🔗 相关文档

- [项目 README](./README.md)
- [后端文档](./backend/README.md)
- [前端文档](./frontend/README.md)
- [Docker 部署文档](./docs/docker-deployment.md)

---

如有问题，请提交 Issue 或查看项目文档。

