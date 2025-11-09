# 面试题库管理系统

一个专业的技术面试题库管理平台，支持题目管理、AI生成、随机选题和面试模式。

## 🚀 功能特性

### 核心功能
- ✅ **题目管理** - 完整的CRUD操作
- ✅ **智能搜索** - 支持关键词、类别、难度筛选  
- ✅ **AI生成** - 基于OpenAI的题目自动生成
- ✅ **随机选题** - 灵活的随机选题功能
- ✅ **面试模式** - 专业的全屏面试体验
- ✅ **响应式设计** - 完美支持移动端

### 技术特色
- **现代技术栈** - Vue3 + FastAPI + TypeScript
- **高性能** - 虚拟DOM + 异步处理
- **可扩展** - 模块化架构设计
- **易部署** - Docker容器化支持

## 📸 界面预览

![首页预览](docs/images/home-preview.png)
![题目管理](docs/images/questions-preview.png)
![AI生成](docs/images/generate-preview.png)
![面试模式](docs/images/interview-preview.png)

## 🛠 技术栈

### 后端
- **FastAPI** - 现代、快速的Python Web框架
- **SQLAlchemy** - Python SQL工具包和ORM  
- **SQLite** - 轻量级数据库
- **OpenAI API** - AI题目生成功能

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - JavaScript的超集，添加了类型系统
- **TailwindCSS** - 实用优先的CSS框架
- **Pinia** - Vue状态管理
- **Vue Router** - Vue.js官方路由

## 🚦 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- SQLite 3.x

### 使用Docker（推荐）

1. 克隆项目
```bash
git clone https://github.com/yourusername/interview-question-bank.git
cd interview-question-bank
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，添加OpenAI API密钥（可选）
```

3. 启动服务
```bash
docker-compose up -d
```

4. 访问应用
- 前端：http://localhost
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

### 手动部署

#### 后端部署
```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据
python init_data.py

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端部署
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 或构建生产版本
npm run build
```

## 📁 项目结构

```
interview-question-bank/
├── backend/                    # FastAPI后端
│   ├── app/
│   │   ├── api/               # API路由
│   │   ├── models.py          # 数据库模型
│   │   ├── schemas.py         # Pydantic模型
│   │   ├── crud.py           # 数据库操作
│   │   ├── services/         # 业务服务
│   │   └── main.py           # FastAPI应用
│   ├── init_data.py          # 数据初始化脚本
│   ├── requirements.txt      # Python依赖
│   ├── Dockerfile            # 后端Docker配置
│   └── .env.example          # 环境变量示例
│
├── frontend/                 # Vue3前端
│   ├── src/
│   │   ├── components/       # Vue组件
│   │   ├── views/           # 页面组件
│   │   ├── stores/          # Pinia状态管理
│   │   ├── api/             # API服务
│   │   ├── types/           # TypeScript类型
│   │   └── router/          # Vue路由
│   ├── package.json         # Node.js依赖
│   ├── Dockerfile           # 前端Docker配置
│   ├── nginx.conf           # Nginx配置
│   └── vite.config.ts       # Vite配置
│
├── docker-compose.yml        # Docker Compose配置
├── .env.example             # 环境变量示例
└── README.md               # 项目说明
```

## 🔧 配置说明

### 环境变量
创建 `.env` 文件：
```env
# OpenAI API Key (可选，用于AI题目生成功能)
OPENAI_API_KEY=your_openai_api_key_here

# 数据库配置
DATABASE_URL=sqlite:///./interview_questions.db

# 其他配置
API_V1_STR=/api/v1
PROJECT_NAME=Interview Question Bank
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 功能配置
- **AI功能**：需要配置OpenAI API密钥
- **数据库**：默认使用SQLite，可配置其他数据库
- **跨域**：可配置允许的前端地址

## 📖 使用指南

### 题目管理
1. 访问首页点击"题目管理"
2. 创建新题目或编辑现有题目
3. 支持Markdown格式编辑
4. 可设置类别、难度和标签

### AI生成题目
1. 选择"AI生成"功能
2. 设置题目类别、难度和数量
3. 点击生成，等待AI创建题目
4. 预览并保存满意的题目

### 随机选题
1. 设置选题参数（数量、类别、难度）
2. 生成随机题目集
3. 可以导出题目或直接开始面试

### 面试模式
1. 选择预设面试或自定义配置
2. 进入全屏面试界面
3. 按顺序回答题目
4. 可随时查看解析和进度

## 🚀 部署指南

### 生产环境
```bash
# 构建生产镜像
docker-compose build

# 启动生产服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 监控和维护
- 查看容器状态：`docker-compose ps`
- 重启服务：`docker-compose restart`
- 更新服务：`docker-compose pull && docker-compose up -d`

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发流程
1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 代码规范
- 后端：遵循PEP 8规范
- 前端：使用ESLint和Prettier
- 提交前运行代码检查

## 📝 更新日志

### v1.0.0 (2024-11-09)
- ✅ 初始版本发布
- ✅ 完整的题目管理功能
- ✅ AI题目生成
- ✅ 随机选题和面试模式
- ✅ 响应式设计
- ✅ Docker部署支持

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 贡献者

感谢所有为这个项目做出贡献的开发者！

## 📞 联系方式

如有问题或建议：
- 提交 [Issue](https://github.com/yourusername/interview-question-bank/issues)
- 发送邮件：your.email@example.com

---

**享受使用面试题库管理系统！** 🎉

<div align="center">
  <p>⭐ 如果这个项目对你有帮助，请给个Star！</p>
  <img src="https://img.shields.io/badge/Vue%203-4FC08D?style=flat-square&logo=vue.js&logoColor=white" alt="Vue 3">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="TailwindCSS">
</div>