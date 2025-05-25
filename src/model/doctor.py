import uuid

from model.base import Base

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Doctor(Base):
    __tablename__ = "doctor"

    modality: Mapped[dict[str, int]] = mapped_column(JSONB, doc="Модальность")
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), default=[], doc="Роли")
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), doc="Пользователь", nullable=False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organization.id"),
        nullable=False,
        doc="Организация",
    )
    division_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("division.id"),
        nullable=False,
        doc="Подразделение",
    )
    position_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("position.id"),
        nullable=False,
        doc="Должность",
    )

    organization = relationship("Organization", back_populates="doctors", uselist=False)
    division = relationship("Division", back_populates="doctors", uselist=False)
    position = relationship("Position", back_populates="doctors", uselist=False)
    statuses = relationship("Status", back_populates="doctor")
    sessions = relationship("Session", back_populates="doctor")
    directions = relationship("Direction", back_populates="doctor")
    conclusions = relationship("Conclusion", back_populates="doctor")
