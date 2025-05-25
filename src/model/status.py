import uuid

from model.base import Base

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Status(Base):
    __tablename__ = "status"

    value: Mapped[str] = mapped_column(String(16), doc="Статус")
    doctor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("doctor.id"),
        nullable=False,
        doc="Врач",
    )
    initiator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        doc="Инициатор изменения статуса",
    )

    doctor = relationship("Doctor", uselist=False, back_populates="statuses")
