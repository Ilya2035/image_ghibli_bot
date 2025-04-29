from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, func, LargeBinary, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    balance = relationship("UserBalance", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserBalance(Base):
    __tablename__ = "user_balances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    balance: Mapped[int] = mapped_column(default=100)

    user = relationship("User", back_populates="balance")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="waiting")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="sessions")
    text_data = relationship("TextData", back_populates="session", uselist=False)
    image_data = relationship("ImageData", back_populates="session", uselist=False)
    audio_data = relationship("AudioData", back_populates="session", uselist=False)
    video_data = relationship("VideoData", back_populates="session", uselist=False)


class TextData(Base):
    __tablename__ = "text_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    input_text: Mapped[str] = mapped_column(Text, nullable=False)
    output_text: Mapped[str | None] = mapped_column(Text)

    session = relationship("Session", back_populates="text_data")


class ImageData(Base):
    __tablename__ = "image_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    input_image: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    output_image: Mapped[bytes | None] = mapped_column(LargeBinary)

    session = relationship("Session", back_populates="image_data")


class AudioData(Base):
    __tablename__ = "audio_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    input_audio: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    output_audio: Mapped[bytes | None] = mapped_column(LargeBinary)

    session = relationship("Session", back_populates="audio_data")


class VideoData(Base):
    __tablename__ = "video_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    input_video: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    output_video: Mapped[bytes | None] = mapped_column(LargeBinary)

    session = relationship("Session", back_populates="video_data")
