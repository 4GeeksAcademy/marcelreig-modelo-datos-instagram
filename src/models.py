from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Boolean, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="user", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan")
    followers: Mapped[list["Follower"]] = relationship(
        "Follower", foreign_keys="[Follower.followed_id]", back_populates="followed")
    following: Mapped[list["Follower"]] = relationship(
        "Follower", foreign_keys="[Follower.follower_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email
        }


class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(250), nullable=True)
    like: Mapped[int] = mapped_column(default=0)
    url: Mapped[str] = mapped_column(String(250), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "like": self.like,
            "url": self.url
        }


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(250), nullable=False)
    like: Mapped[int] = mapped_column(default=0)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content,
            "like": self.like
        }


class Follower(db.Model):
    __tablename__ = "followers"
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    follow_date: Mapped[date] = mapped_column(nullable=True)

    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship(
        "User", foreign_keys=[followed_id], back_populates="followers")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "follow_date": self.follow_date.isoformat() if self.follow_date else None

        }
