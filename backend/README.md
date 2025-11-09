# 面试题库管理系统

一个专业的技术面试题库管理平台，支持题目管理、AI生成、随机选题和面试模式。

## 技术栈

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

## 功能特性

### 核心功能
- ✅ 题目管理（CRUD）
- ✅ 智能搜索和筛选
- ✅ AI题目生成
- ✅ 随机选题
- ✅ 面试模式
- ✅ 响应式设计

### 题目管理
- 创建、编辑、删除题目
- 支持Markdown格式
- 分类和难度标记
- 标签系统

### AI增强
- 基于OpenAI API的题目生成
- 自动生成解析和标签
- 支持多种技术类别

### 面试模式
- 全屏面试界面
- 按难度梯度展示
- 解析显示切换
- 进度跟踪

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- SQLite 3.x

### 后端启动

1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 初始化数据库
```bash
python init_data.py
```

3. 启动服务
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API文档：http://localhost:8000/docs

### 前端启动

1. 安装依赖
```bash
cd frontend
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

应用地址：http://localhost:5173

## API接口

### 题目管理
- `GET /api/v1/questions` - 获取题目列表
- `POST /api/v1/questions` - 创建题目
- `GET /api/v1/questions/{id}` - 获取题目详情
- `PUT /api/v1/questions/{id}` - 更新题目
- `DELETE /api/v1/questions/{id}` - 删除题目

### 搜索筛选
- `GET /api/v1/questions/search` - 搜索题目

### AI功能
- `POST /api/v1/ai/generate` - AI生成题目
- `GET /api/v1/ai/categories` - 获取题目类别
- `GET /api/v1/ai/difficulties` - 获取难度等级

### 随机选题
- `GET /api/v1/random` - 随机获取题目
- `POST /api/v1/random/advanced` - 高级随机选题

### 面试模式
- `POST /api/v1/interview` - 创建面试会话
- `GET /api/v1/interview/preset/{type}` - 获取预设面试

## 项目结构

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
│   └── .env.example          # 环境变量示例
│
└── frontend/                 # Vue3前端
    ├── src/
    │   ├── components/       # Vue组件
    │   ├── views/           # 页面组件
    │   ├── stores/          # Pinia状态管理
    │   ├── api/             # API服务
    │   ├── types/           # TypeScript类型
    │   └── router/          # Vue路由
    ├── package.json         # Node.js依赖
    └── vite.config.ts       # Vite配置
```

## 配置说明

### 后端配置
创建 `.env` 文件：
```env
DATABASE_URL=sqlite:///./interview_questions.db
OPENAI_API_KEY=your_openai_api_key_here
API_V1_STR=/api/v1
PROJECT_NAME=Interview Question Bank API
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 前端配置
前端使用环境变量文件 `.env`：
```env
VITE_API_BASE_URL=/api
```

## 使用说明

### 题目管理
1. 访问 `/questions` 页面
2. 可以创建、编辑、删除题目
3. 支持按类别、难度、关键词筛选
4. 题目内容支持Markdown格式

### AI生成题目
1. 访问 `/generate` 页面
2. 选择题目类别、难度和数量
3. 点击生成按钮
4. 预览生成的题目并保存

### 随机选题
1. 访问 `/random` 页面
2. 设置选题参数（数量、类别、难度）
3. 生成随机题目集
4. 可以导出题目或开始面试

### 面试模式
1. 访问 `/interview` 页面
2. 选择预设面试模式或自定义配置
3. 开始全屏面试体验
4. 按顺序答题，可以查看解析

## 开发指南

### 添加新功能
1. 后端：更新模型和API
2. 前端：添加组件和页面
3. 测试前后端联调

### 代码规范
- 后端：遵循PEP 8规范
- 前端：使用ESLint和Prettier
- 提交前运行代码检查

## 部署

### 生产部署
1. 后端：使用Gunicorn + Uvicorn
2. 前端：构建静态文件
3. 使用Nginx反向代理

### Docker部署
```dockerfile
# 后端Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发流程
1. Fork项目
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请提交Issue或联系维护者。

---

**享受使用面试题库管理系统！** 🚀