# 基于SQLAlchemy框架进行数据的持久化访问（aiomysql）：
# 进行数据库的持久化操作需要 session:AsyncSession 对象
# session对象可以通过 session_factory:async_sessionmaker 类的实例来产生（工厂设计模式）
# 创建工厂对象则需要 engine:AsyncEngine 来进行初始化
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from atguigu.conf.config import settings

engine:AsyncEngine|None = None
session_factory:async_sessionmaker[AsyncSession]|None = None

def init_db_engine_and_session_factory():
    global engine,session_factory
    engine = create_async_engine(
        url = settings.database_url,
        echo=False, # 是否开启SQL日志
        pool_pre_ping=False, # 是否开启连接预检查
    )
    session_factory = async_sessionmaker(
        engine,expire_on_commit=False
    )

async def close_db_engine():
    if engine is not None:
        await engine.dispose()
