from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    
    # Primary key with type hints
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Required fields
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True,
        nullable=False
    )
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # Optional fields with proper typing
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Timestamps with server defaults
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relationships - note the typing
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        lazy="selectin"  # Eager loading strategy
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
    
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(default=False)
    
    # Foreign key with proper indexing
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Relationship back to User
    author: Mapped["User"] = relationship(back_populates="posts")
    
    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title})>"