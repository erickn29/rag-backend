import uuid

from datetime import datetime

from model.base import Base

from sqlalchemy import TIMESTAMP, UUID, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DoctorSession(Base):
    __tablename__ = "doctor_session"

    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("doctor.id"),
        nullable=False,
        doc="Врач",
    )
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        doc="Время начала",
    )
    end_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        doc="Время окончания",
    )
    created_at = None  # type: ignore
    updated_at = None  # type: ignore

    doctor = relationship("Doctor", uselist=False, back_populates="sessions")
