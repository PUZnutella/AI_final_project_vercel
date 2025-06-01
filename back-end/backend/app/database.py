from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 优先使用环境变量中的数据库URL，如果没有则使用SQLite
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    # 将 postgres:// 替换为 postgresql://
    database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    # 如果没有设置DATABASE_URL，使用本地SQLite
    database_url = "sqlite:///session.db"

# 创建数据库引擎
if database_url.startswith("sqlite"):
    engine = create_engine(database_url, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_engine(database_url, echo=False)

# 启动时建立 table
def init_db():
    SQLModel.metadata.create_all(engine)

# 获取 DB session
def get_session():
    with Session(engine) as session:
        yield session