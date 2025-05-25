import uuid

from datetime import datetime

from model.base import Base

from sqlalchemy import DATE, UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Patient(Base):
    __tablename__ = "patient"

    first_name: Mapped[str] = mapped_column(String(16), default="", nullable=False)
    last_name: Mapped[str] = mapped_column(String(16), default="", nullable=False)
    patronymic: Mapped[str] = mapped_column(String(16), default="", nullable=False)
    phone_number: Mapped[str] = mapped_column(String(16), nullable=True)
    email: Mapped[str] = mapped_column(String(400), nullable=True)
    birth_date: Mapped[datetime] = mapped_column(DATE, nullable=True)
    snils: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id"), nullable=True
    )

    directions = relationship("Direction", back_populates="patient")
    conclusions = relationship("Conclusion", back_populates="patient")
