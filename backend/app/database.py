from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLite 连接配置，启用 WAL 模式和更好的并发支持
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # 增加超时时间，避免锁定问题
    },
    pool_pre_ping=True,  # 检查连接有效性
    echo=False
)

# 为 SQLite 启用 WAL 模式，提高并发性能
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=30000")  # 30秒的忙等待超时
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()