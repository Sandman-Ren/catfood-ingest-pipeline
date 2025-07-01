import os
from sqlalchemy import (
    create_engine, String, Integer, ForeignKey, DateTime,
    JSON, Text, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

DB_URL = os.getenv("DB_URL", "postgresql+psycopg://user:pass@localhost/catfood")

class Base(DeclarativeBase):
    pass

class Brand(Base):
    __tablename__ = "brand"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    barcode: Mapped[str] = mapped_column(String(32), unique=True, nullable=True)
    title: Mapped[str] = mapped_column(Text)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    raw_ingredients: Mapped[str] = mapped_column(Text)
    ingredients: Mapped[dict] = mapped_column(JSON)
    source: Mapped[str] = mapped_column(String(120))
    fetched_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    brand = relationship(Brand, lazy="joined")

def get_session(echo=False):
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(DB_URL, echo=echo, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
