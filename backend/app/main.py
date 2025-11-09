from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import questions, ai_questions, random_questions, interview_session

# 创建数据库表
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的操作
    print("Starting Interview Question Bank API...")
    yield
    # 关闭时的操作
    print("Shutting down API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="面试题库管理系统API",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    questions.router,
    prefix=f"{settings.API_V1_STR}/questions",
    tags=["questions"]
)

app.include_router(
    ai_questions.router,
    prefix=f"{settings.API_V1_STR}/ai",
    tags=["ai"]
)

app.include_router(
    random_questions.router,
    prefix=f"{settings.API_V1_STR}/random",
    tags=["random"]
)

app.include_router(
    interview_session.router,
    prefix=f"{settings.API_V1_STR}/interview",
    tags=["interview"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Interview Question Bank API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)